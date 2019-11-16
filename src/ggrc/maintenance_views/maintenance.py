# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""View functions for maintenance"""

# pylint: disable=invalid-name
# pylint: disable=no-else-return

import re

from logging import getLogger
from ggrc.maintenance import maintenance_app
from ggrc import db
from ggrc import migrate
from ggrc import settings
from ggrc.models.maintenance import Maintenance
from ggrc.models.maintenance import MigrationLog
from ggrc.models.background_task import BackgroundTask

from google.appengine.api import users
from google.appengine.ext import deferred

from flask import json
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
import sqlalchemy

logger = getLogger(__name__)


@maintenance_app.route('/maintenance/index')
def index():
  """Renders admin maintenance dashboard."""
  gae_user = users.get_current_user()
  if not (gae_user and gae_user.email() in settings.BOOTSTRAP_ADMIN_USERS):
    return "Unauthorized", 403
  context = {'migration_status': 'Not started',
             'reindex_status': 'Not started'}
  if session.get('migration_started'):
    try:
      row = db.session.query(MigrationLog).order_by(
          MigrationLog.id.desc()).first()
      if not row:
        return render_template("maintenance/trigger.html", **context)

      if row.log:
        context['migration_status'] = 'Error'

      elif row.is_migration_complete:
        context['migration_status'] = 'Complete'

      else:
        context['migration_status'] = 'In progress'
    except sqlalchemy.exc.ProgrammingError as e:
      if not re.search(r"""\(1146, "Table '.+' doesn't exist"\)$""",
                       e.message):
        raise

  context['reindex_status'] = set_latest_task_status('reindex')

  return render_template("maintenance/trigger.html", **context)


def get_latest_task(bg_name):
  """Returns the latest background task by given name"""
  return BackgroundTask.query \
                       .filter(BackgroundTask.name.contains(bg_name)) \
                       .order_by('-id') \
                       .first()


def get_latest_task_status(bg_name):
  """Returns status of the latest background task by given name"""
  latest_task = get_latest_task(bg_name)

  if latest_task:
    return latest_task.status

  return None


def set_latest_task_status(bg_name):
  """Returns status of the latest background task by given name to render"""
  status = get_latest_task_status(bg_name)

  if status == BackgroundTask.RUNNING_STATUS:
    return 'In progress'
  elif status == BackgroundTask.SUCCESS_STATUS:
    return 'Finished'

  # when there is no bg task with given name or status is
  # BackgroundTask.PENDING_STATUS return 'Not started'
  return 'Not started'


def trigger_migration():
  """Triggers a deferred task for migration."""
  try:
    maint_row = db.session.query(Maintenance).get(1)
    if maint_row and maint_row.under_maintenance:
      logger.info(
          'System is under maintenance. Try running migration later.')
      return None
    mig_row = MigrationLog(is_migration_complete=False)
    db.session.add(mig_row)

    # Set the db flag before running migrations
    if maint_row:
      maint_row.under_maintenance = True
    else:
      maint_row = Maintenance(under_maintenance=True)
      db.session.add(maint_row)
    db.session.plain_commit()
  except sqlalchemy.exc.ProgrammingError as e:
    if re.search(r"""\(1146, "Table '.+' doesn't exist"\)$""", e.message):
      mig_row = None
    else:
      raise

  mig_row_id = mig_row.id if mig_row else 0
  deferred.defer(migrate.migrate, row_id=mig_row_id, _queue='ggrc')
  session['migration_started'] = True
  return mig_row_id


@maintenance_app.route('/maintenance/reindex', methods=['POST'])
def run_reindex():
  """Triggers a background task to run reindexing"""

  if not get_latest_task_status('reindex') in (BackgroundTask.PENDING_STATUS,
                                               BackgroundTask.RUNNING_STATUS):
    from ggrc.models import background_task
    background_task.create_task(
        name="reindex",
        url="/admin/reindex",
        method="POST",
    )
    db.session.commit()

  return redirect(url_for('index'))


@maintenance_app.route('/maintenance/migrate', methods=['POST'])
def run_migration():
  """Allow authenticated user or with valid access token to run migration."""
  if "access_token" not in request.form:
    gae_user = users.get_current_user()
    if not (gae_user and gae_user.email() in settings.BOOTSTRAP_ADMIN_USERS):
      return json.dumps({"message": "Unauthorized"}), 403

    trigger_migration()
    return redirect(url_for('index'))

  if not (hasattr(settings, 'ACCESS_TOKEN') and
          request.form.get("access_token") == settings.ACCESS_TOKEN):
    logger.error("Invalid access token: %s", request.form.get("access_token"))
    return json.dumps({"message": "Unauthorized"}), 403

  mig_row_id = trigger_migration()
  data = {'migration_task_id': mig_row_id,
          'message': 'Migration is running in background'}
  return json.dumps(data), 202


def _turn_off_maintenance_mode():
  """Turn off maintenance mode."""
  db_row = db.session.query(Maintenance).get(1)
  if db_row:
    db_row.under_maintenance = False
    db.session.add(db_row)
    db.session.commit()
    return "Maintenance mode turned off successfully"
  return "Maintenance mode has was not turned on."


@maintenance_app.route('/maintenance/turnoff_maintenance_mode',
                       methods=['POST'])
def turn_off_maintenance_mode():
  """Allow authenticated user to turn off maintenance mode."""
  if "access_token" not in request.form:
    gae_user = users.get_current_user()
    if not (gae_user and
            gae_user.email() in settings.BOOTSTRAP_ADMIN_USERS):
      return "Unauthorized", 403

    return _turn_off_maintenance_mode() or ""

  if not (hasattr(settings, 'ACCESS_TOKEN') and
          request.form.get("access_token") == settings.ACCESS_TOKEN):
    logger.error("Invalid access token: %s", request.form.get("access_token"))
    return "Unauthorized", 403

  return _turn_off_maintenance_mode(), 202


@maintenance_app.route('/maintenance/check_migration_status/<row_id>',
                       methods=['GET'])
def check_migration_status(row_id):
  """Checks and returns the status of migration."""
  try:
    maint_row = db.session.query(Maintenance).get(1)
    mig_row = db.session.query(MigrationLog).get(row_id)
    if not (mig_row and maint_row):
      data = {"status": "Fail",
              "message": "No migration entry in db."}
      return json.dumps(data), 202

    if mig_row.log:
      data = {"status": "Fail",
              "message": "Migration failed : {}".format(mig_row.log)}
      return json.dumps(data), 202

    if not mig_row.is_migration_complete:
      return json.dumps({"status": "In progress"}), 202

    return json.dumps({"status": "Complete"}), 202

  except sqlalchemy.exc.ProgrammingError as e:
    logger.error(e.message)
    if not re.search(r"""\(1146, "Table '.+' doesn't exist"\)$""", e.message):
      raise
