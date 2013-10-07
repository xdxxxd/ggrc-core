# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: silas@reciprocitylabs.com
# Maintained By: silas@reciprocitylabs.com

from datetime import datetime
from os.path import abspath, dirname, join

from mock import patch

from ggrc import db
from ggrc.converters.import_helper import handle_csv_import
from ggrc.converters.common import ImportException
from ggrc.converters.controls import ControlsConverter
from ggrc.fulltext.mysql import MysqlRecordProperty
from ggrc.models import Control, Category, Policy, System
from tests.ggrc import TestCase

THIS_ABS_PATH = abspath(dirname(__file__))
CSV_DIR = join(THIS_ABS_PATH, 'comparison_csvs/')


class TestImport(TestCase):
  def setUp(self):
    self.patcher = patch('ggrc.converters.base.log_event')
    self.mock_log = self.patcher.start()
    self.date1 = datetime(2013, 9, 25)
    self.date2 = datetime(2013, 9, 26)
    super(TestImport, self).setUp()

  def tearDown(self):
    self.patcher.stop()
    super(TestImport, self).tearDown()

  def test_simple(self):
    #csv_filename = join(CSV_DIR, "minimal_import.csv")
    csv_filename = join(CSV_DIR, "minimal_export2.csv")
    expected_titles = set([
      "Minimal Control 1",
      "Minimal Control 2",
    ])
    expected_start_dates = set([None, self.date1])
    expected_end_dates = set([None, self.date2])
    expected_slugs = set(["CTRL-1", "CTRL-2"])
    pol1 = Policy(
      kind="Company Policy",
      title="Example Policy",
      slug="POL-123",
    )
    db.session.add(pol1)
    db.session.commit()
    options = {'directive_id': pol1.id, 'dry_run': False}
    handle_csv_import(
        ControlsConverter,
        csv_filename,
        **options
    )
    actual_titles = set()
    actual_slugs = set()
    actual_start_dates = set()
    actual_end_dates = set()
    print pol1.controls
    for control in pol1.controls:
      actual_titles.add(control.title)
      actual_slugs.add(control.slug)
      actual_start_dates.add(control.start_date)
      actual_end_dates.add(control.end_date)
    self.assertEqual(
        expected_titles,
        actual_titles,
        "Control titles not imported correctly"
    )
    #self.assertEqual(
    #    expected_slugs,
    #    actual_slugs,
    #    "Control slugs not imported correctly"
    #)
    #self.assertEqual(
    #    expected_end_dates,
    #    actual_end_dates,
    #    "Control end dates not imported correctly"
    #)
    #self.assertEqual(
    #    expected_start_dates,
    #    actual_start_dates,
    #    "Control start dates not imported correctly"
    #)
    self.mock_log.assert_called_once_with(db.session)
    # check that imported items appear in index
    results = MysqlRecordProperty.query.filter(
        MysqlRecordProperty.type == 'Control',
        MysqlRecordProperty.content.match('Minimal Control')
    ).all()
    index_results = set([x.content for x in results])
    for title in expected_titles:
      self.assertIn(
          title,
          index_results,
          "{0} not indexed".format(title)
      )

  def test_mappings(self):
    sys1 = System(slug="ACLS", title="System1")
    sys2 = System(slug="SLCA", title="System2")
    db.session.add(sys1)
    db.session.add(sys2)
    expected_titles = set([
      "Complex Control 2",
    ])
    expected_slugs = set([
      "CTRL-2345",
    ])
    csv_filename = join(CSV_DIR, "mappings_import.csv")
    pol1 = Policy(
      kind="Company Policy",
      title="Example Policy",
      slug="POL-123",
    )
    db.session.add(pol1)
    db.session.commit()
    options = {'directive_id': pol1.id, 'dry_run': False}
    handle_csv_import(
        ControlsConverter,
        csv_filename,
        **options
    )
    actual_titles = set()
    actual_slugs = set()
    for control in pol1.controls:
      actual_titles.add(control.title)
      actual_slugs.add(control.slug)
    self.assertEqual(
        expected_titles,
        actual_titles,
        "Control titles not imported correctly"
    )
    self.assertEqual(
        expected_slugs,
        actual_slugs,
        "Control slugs not imported correctly"
    )
    systems = System.query.all()
    for system in systems:
      self.assertEqual(
          system.controls,
          pol1.controls,
          "System {0} not connected to controls on import".format(
              system.slug
          ),
      )
    self.mock_log.assert_called_once_with(db.session)
    # check that imported items appear in index
    results = MysqlRecordProperty.query.filter(
        MysqlRecordProperty.type == 'Control',
        MysqlRecordProperty.content.match('Complex Control 2')
    ).all()
    index_results = set([x.content for x in results])
    for title in expected_titles:
      self.assertIn(
          title,
          index_results,
          "{0} not indexed".format(title)
      )

  def test_directive_slug_mismatch(self):
    sys1 = System(slug="ACLS", title="System1")
    db.session.add(sys1)
    expected_titles = set([
      "Complex Control 2",
    ])
    expected_slugs = set([
      "CTRL-2345",
    ])
    csv_filename = join(CSV_DIR, "mappings_import_mismatch.csv")
    pol1 = Policy(
      kind="Company Policy",
      title="Example Policy",
      slug="POL-123",
    )
    db.session.add(pol1)
    db.session.commit()
    options = {'directive_id': pol1.id, 'dry_run': False}
    actual_titles = set()
    actual_slugs = set()
    self.assertRaises(ImportException, handle_csv_import, ControlsConverter, csv_filename, **options)

  def test_invalid_dates(self):
    #csv_filename = join(CSV_DIR, "minimal_import_dashes.csv")
    csv_filename = join(CSV_DIR, "minimal_import_dashes.csv")
    expected_titles = set([
      "Minimal Control 1",
      "Minimal Control 2",
    ])
    expected_start_dates = set([None, self.date1])
    expected_end_dates = set([None, self.date2])
    expected_slugs = set(["CTRL-1", "CTRL-2"])
    pol1 = Policy(
      kind="Company Policy",
      title="Example Policy",
      slug="POL-123",
    )
    db.session.add(pol1)
    db.session.commit()
    options = {'directive_id': pol1.id, 'dry_run': False}
    handle_csv_import(
        ControlsConverter,
        csv_filename,
        **options
    )
    actual_titles = set()
    actual_slugs = set()
    actual_start_dates = set()
    actual_end_dates = set()
    for control in pol1.controls:
      actual_titles.add(control.title)
      actual_slugs.add(control.slug)
      actual_start_dates.add(control.start_date)
      actual_end_dates.add(control.end_date)
    self.assertEqual(
        expected_titles,
        actual_titles,
        "Control titles not imported correctly"
    )
    self.assertEqual(
        expected_slugs,
        actual_slugs,
        "Control slugs not imported correctly"
    )
    #self.assertEqual(
    #    expected_end_dates,
    #    actual_end_dates,
    #    "Control end dates not imported correctly"
    #)
    #self.assertEqual(
    #    expected_start_dates,
    #    actual_start_dates,
    #    "Control start dates not imported correctly"
    #)
    self.mock_log.assert_called_once_with(db.session)
    # check that imported items appear in index
    results = MysqlRecordProperty.query.filter(
        MysqlRecordProperty.type == 'Control',
        MysqlRecordProperty.content.match('Minimal Control')
    ).all()
    index_results = set([x.content for x in results])
    for title in expected_titles:
      self.assertIn(
          title,
          index_results,
          "{0} not indexed".format(title)
      )

  #def test_system_mismatch(self):
  #  sys1 = System(slug="ACLS", title="System1")
  #  db.session.add(sys1)
  #  expected_titles = set([
  #    "Complex Control 2",
  #  ])
  #  expected_slugs = set([
  #    "CTRL-2345",
  #  ])
  #  csv_filename = join(CSV_DIR, "mappings_import.csv")
  #  pol1 = Policy(
  #    kind="Company Policy",
  #    title="Example Policy",
  #    slug="POL-123",
  #  )
  #  db.session.add(pol1)
  #  db.session.commit()
  #  options = {'directive_id': pol1.id, 'dry_run': False}
  #  actual_titles = set()
  #  actual_slugs = set()
  #  self.assertRaises(ImportException, handle_csv_import, ControlsConverter, csv_filename, **options)
