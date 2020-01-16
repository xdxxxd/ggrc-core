# Copyright (C) 2020 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
Remove duplicated comment relations for external comments

Create Date: 2020-01-10 10:58:02.220915
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name

import sqlalchemy as sa
from sqlalchemy.sql import func
from sqlalchemy.sql import select

from alembic import op

from ggrc.models import all_models


# revision identifiers, used by Alembic.
revision = 'c7620a843c18'
down_revision = '3141784ef298'


def upgrade():
  """Upgrade database schema and/or data, creating a new revision."""
  conn = op.get_bind()
  # select duplicated relations
  duplicated_relations = conn.execute("""
    SELECT r1.id, r1.source_id, r1.source_type, r1.destination_id,
        r1.destination_type
    FROM relationships r1
    JOIN relationships r2 ON r1.source_id = r2.destination_id
        AND r1.destination_id = r2.source_id
        AND r2.source_type = 'ExternalComment'
        AND r1.destination_type = 'ExternalComment';
    """).fetchall()

  if not duplicated_relations:
    print "Duplicated revisions were not found"
    return

  relations_ids = [rel[0] for rel in duplicated_relations]
  relation_items = [rel[1:] for rel in duplicated_relations]

  rev = all_models.Revision
  revisions = rev.query.filter(
      sa.tuple_(
          rev.source_id, rev.source_type,
          rev.destination_id, rev.destination_type
      ).in_(relation_items)
  ).all()

  if revisions:
    # find events
    revision_ids = [rev_.id for rev_ in revisions]
    event_ids = [rev_.event_id for rev_ in revisions]

    # find unique events
    table = rev.__table__
    stmt = select([table.c.event_id]).where(table.c.event_id.in_(event_ids))\
        .group_by(table.c.event_id).having(func.count(table.c.event_id) == 1)
    events = conn.execute(stmt).fetchall()

    # delete revisions
    print "Delete duplicated revisions related to mirrored relations"
    delete_stmt = rev.__table__.delete(rev.id.in_(revision_ids))
    conn.execute(delete_stmt)

    if events:
      unique_event_ids = [event[0] for event in events]
      # delete unique events
      print "Delete duplicated unique events related to mirrored relations"
      delete_stmt = all_models.Event.__table__.delete(
          all_models.Event.id.in_(unique_event_ids))
      conn.execute(delete_stmt)

  # delete relations
  print "Delete duplicated mirrored relations"
  delete_stmt = all_models.Relationship.__table__.delete(
      all_models.Relationship.id.in_(relations_ids))
  conn.execute(delete_stmt)


def downgrade():
  """Downgrade database schema and/or data back to the previous revision."""
  raise NotImplementedError("Downgrade is not supported")
