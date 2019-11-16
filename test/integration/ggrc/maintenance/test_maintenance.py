# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>


"""Test for indexing of snapshotted objects"""

import mock

from ggrc import settings
import ggrc.maintenance_views as maintenance_views
from ggrc.maintenance import maintenance_app

from integration.ggrc import TestCase


class TestMaintenanceIntegration(TestCase):
  """Test set for Maintenance app."""

  def setUp(self):
    self.client = maintenance_app.test_client()
    super(TestMaintenanceIntegration, self).setUp()
    self.init_taskqueue()

  @mock.patch.object(settings, "APP_ENGINE", True, create=True)
  def test_run_reindex(self):
    """Reindex from Maintenance app"""
    with maintenance_app.test_client() as client:
      self.assertEqual(
          maintenance_views.maintenance.get_latest_task_status("reindex"),
          None)

      response = client.post("/maintenance/reindex")
      self.assertEqual(
          response.status_code,
          302)
      latest_reindex = maintenance_views.maintenance \
                                        .get_latest_task("reindex")
      self.assertEqual(
          maintenance_views.maintenance.get_latest_task_status("reindex"),
          "Pending")

      # Check if is it possible to trigger reindex once
      # another one is running
      client.post("/maintenance/reindex")
      latest_reindex_to_check = maintenance_views.maintenance \
                                                 .get_latest_task("reindex")
      self.assertEqual(
          latest_reindex.id,
          latest_reindex_to_check.id)
