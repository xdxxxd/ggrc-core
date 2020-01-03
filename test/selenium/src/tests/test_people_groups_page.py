# Copyright (C) 2020 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""People/Groups page smoke tests."""
# pylint: disable=no-self-use
# pylint: disable=invalid-name

import pytest

from lib import base, users
from lib.entities import entities_factory
from lib.service import webui_service, rest_facade


class TestOrgGroupPage(base.Test):
  """Tests org group page, part of smoke tests, section 7."""
  # pylint: disable=too-few-public-methods

  @pytest.mark.smoke_tests
  def test_create_org_group(self, selenium):
    """Tests Org Group creation via UI."""
    org_group = entities_factory.OrgGroupsFactory().create()
    actual_org_group = webui_service.OrgGroupsService(
        selenium).create_obj_and_get_obj(org_group)
    rest_org_group = rest_facade.get_obj(actual_org_group)
    org_group.update_attrs(
        created_at=rest_org_group.created_at,
        updated_at=rest_org_group.updated_at,
        modified_by=users.current_user(),
        slug=rest_org_group.slug,
        url=rest_org_group.url).repr_ui()
    self.general_equal_assert(org_group, actual_org_group, "custom_attributes")
