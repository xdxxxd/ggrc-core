# Copyright (C) 2020 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Tests for task group task specific export."""
import collections

import ddt
import mock

from ggrc.models import all_models
from ggrc.converters import errors
from integration.ggrc import TestCase
from integration.ggrc.models import factories


@ddt.ddt
class TestMetricsImport(TestCase):
  """Test for metrics import."""

  def setUp(self):
    super(TestMetricsImport, self).setUp()
    self.client.get("/login")

  def test_metrics_import(self):
    """Test metrics import"""
    regulation = factories.RegulationFactory()
    standard = factories.StandardFactory()
    metric_data = [
        collections.OrderedDict([
            ("object_type", "Metric"),
            ("Code*", ""),
            ("Title*", "Metric-1"),
            ("Admin*", "user@example.com"),
            ("Assignee", "user@example.com"),
            ("Verifier", "user@example.com"),
            ("map:regulation", ""),
            ("map:standard", ""),
        ]),
        collections.OrderedDict([
            ("object_type", "Metric"),
            ("Code*", ""),
            ("Title*", "Metric-2"),
            ("Admin*", "user@example.com"),
            ("Assignee", "user@example.com"),
            ("Verifier", "user@example.com"),
            ("map:regulation", regulation.slug),
            ("map:standard", ""),
        ]),
        collections.OrderedDict([
            ("object_type", "Metric"),
            ("Code*", ""),
            ("Title*", "Metric-3"),
            ("Admin*", "user@example.com"),
            ("Assignee", "user@example.com"),
            ("Verifier", "user@example.com"),
            ("map:regulation", ""),
            ("map:standard", standard.slug),
        ]),
    ]

    response = self.import_data(*metric_data)

    metric_response = response[0]
    self.assertEqual(metric_response["created"], 3)
    self._check_csv_response(response, {
        "Metric": {
            "row_warnings": {
                errors.MAP_UNMAP_SCOPE_ERROR.format(
                    line=4,
                    object_type="Regulation",
                    action="map",
                ),
                errors.MAP_UNMAP_SCOPE_ERROR.format(
                    line=5,
                    object_type="Standard",
                    action="map",
                ),
            },
        }
    })

  @ddt.data(
      (True, "test_ggrcq"),
      (False, ""),
  )
  @ddt.unpack
  def test_metrics_deprecated_import(self, is_integration, test_url):
    """Test metrics import with Deprecated status message"""
    with mock.patch("ggrc.settings.GGRC_Q_INTEGRATION_URL",
                    test_url) as ggrc_q_link:
      metric = factories.MetricFactory()
      response = self.import_data(collections.OrderedDict([
          ("object_type", "Metric"),
          ("Code*", metric.slug),
          ("Launch Status", "Deprecated"),
      ]))
      expected_response = {} if not is_integration else {
          "Metric": {
              "row_warnings": {
                  errors.DEPRECATED_DELETED_METRIC_STATUS.format(
                      line=3,
                      object_type="Metric",
                      object_title=metric.title,
                      ggrc_q_link=ggrc_q_link,
                      action_status="deprecation",
                  ),
              },
          }
      }
      self._check_csv_response(response, expected_response)
      metric = all_models.Metric.query.first()
      self.assertEqual(metric.status, "Deprecated")
