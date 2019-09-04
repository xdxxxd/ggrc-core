# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
add_missing_acp_revisions

Create Date: 2019-09-04 20:09:31.848954
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name

import datetime
import json

from alembic import op
import sqlalchemy as sa

from ggrc.migrations import utils


# revision identifiers, used by Alembic.
revision = '007ee00ff963'
down_revision = '8937c6e26f00'


def parse_datetime_obj(o):
  """Prepare datetime object for json dumping"""
  if isinstance(o, (datetime.date, datetime.datetime)):
    return o.isoformat()
  return o


def get_acr_without_revision(connection):
  """Get all acps without revisions."""
  sql = """
      SELECT * FROM access_control_people
       WHERE id NOT IN (
        SELECT resource_id FROM revisions
         WHERE resource_type = "AccessControlPerson")
       AND id != 1
  """
  acps = list(connection.execute(sa.text(sql)))
  return acps


def get_system_user_id(connection):
  """Get system user id."""
  system_user_email = 'ggrc-system@google.com'
  sql = """
      SELECT * FROM people
       WHERE email = :system_user_email
  """
  people_id = list(connection.execute(sa.text(sql),
                                      system_user_email=system_user_email))
  people_id = people_id[0].id if people_id else 1
  return people_id


def create_revision(connection, acp, system_user_id, event_id):
  """Create revision."""
  content = {
      'display_name': '',
      'created_at': acp.created_at,
      'updated_at': acp.updated_at,
      'ac_list_id': acp.ac_list_id,
      'modified_by_id': system_user_id,
      'person_id': acp.person_id,
      'modified_by': None,
      'type': 'AccessControlPerson',
      'id': acp.id
  }
  content = json.dumps(content, default=parse_datetime_obj)
  sql = """
      INSERT INTO revisions (
        resource_id,
        resource_type,
        event_id,
        modified_by_id,
        action,
        content,
        created_at,
        updated_at
      )
      VALUES (
        :resource_id,
        :resource_type,
        :event_id,
        :modified_by_id,
        :action,
        :content,
        NOW(),
        NOW()
      )
  """
  connection.execute(
      sa.text(sql),
      resource_id=acp.id,
      resource_type='AccessControlPerson',
      event_id=event_id,
      modified_by_id=system_user_id,
      action='created',
      content=content
  )


def upgrade():
  """Upgrade database schema and/or data, creating a new revision."""
  connection = op.get_bind()
  acps = get_acr_without_revision(connection)
  system_user_id = get_system_user_id(connection)
  event_id = utils.create_event(connection, system_user_id, 'Person')
  for acp in acps:
    create_revision(connection, acp, system_user_id, event_id)


def downgrade():
  """Downgrade database schema and/or data back to the previous revision."""
  raise NotImplementedError("Downgrade is not supported")
