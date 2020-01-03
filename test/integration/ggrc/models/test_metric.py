# Copyright (C) 2020 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Integration tests for Metric"""

from ggrc.models import all_models

from integration.ggrc import TestCase
from integration.ggrc.models import factories
from integration.ggrc import generator


class TestMetric(TestCase):
  """Tests for metric model."""

  def setUp(self):
    super(TestMetric, self).setUp()
    self.gen = generator.ObjectGenerator()

  def test_create_metric_by_api(self):
    """Test create metric via API"""
    data = (
        ({"title": "Title 1", "slug": "Slug 1"}, True),
        ({"title": "Title 2", "slug": "Slug 1"}, False),
        ({"title": "Title 2", "slug": "Slug 2"}, True),
        ({"title": "Title 2"}, False)
    )
    creator = self.gen.generate_object

    for metric_data, is_created in data:
      response, metric = creator(
          all_models.Metric,
          metric_data
      )
      if is_created:
        self.assertEqual(metric.title, metric_data["title"])
      else:
        self.assertEqual(response.status_code, 400)

  def test_auto_slug_generation(self):
    """Test auto slug generation"""
    factories.MetricFactory(title="title")
    metric = all_models.Metric.query.first()
    self.assertEqual("METRIC-{}".format(metric.id), metric.slug)
