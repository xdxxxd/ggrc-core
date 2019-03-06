# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
Add control assertions for demo

Create Date: 2019-03-06 05:38:03.179442
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name

from alembic import op

# revision identifiers, used by Alembic.
revision = '22624692e663'
down_revision = '57b14cb4a7b4'


def upgrade():
  """Upgrade database schema and/or data, creating a new revision."""
  op.execute(
      """
          INSERT INTO categories(
              `name`,
              `type`,
              `created_at`,
              `updated_at`
          ) VALUES
          ("E/O - Existence or Occurrence", "ControlAssertion", NOW(), NOW()),
          ("C - Completeness", "ControlAssertion", NOW(), NOW()),
          ("V/A - Valuation or Allocation", "ControlAssertion", NOW(), NOW()),
          ("R&O - Rights and Obligations", "ControlAssertion", NOW(), NOW()),
          ("A - Authorization", "ControlAssertion", NOW(), NOW()),
          ("P&D - Presentation and Disclosure",
           "ControlAssertion",
           NOW(),
           NOW()),
          ("N/A - Indirect F/S Assertion (ITGC Only)",
           "ControlAssertion",
           NOW(),
           NOW());
      """
  )


def downgrade():
  """Downgrade database schema and/or data back to the previous revision."""
  pass
