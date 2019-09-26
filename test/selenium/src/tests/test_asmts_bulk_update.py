# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Tests for bulk update functionality."""
# pylint: disable=no-self-use
# pylint: disable=unused-argument
# pylint: disable=redefined-outer-name
# pylint: disable=invalid-name
# pylint: disable=too-many-arguments
import pytest

from lib import base, users
from lib.constants import object_states, roles
from lib.rest_facades import roles_rest_facade
from lib.service import rest_facade, webui_facade, webui_service


@pytest.fixture()
def asmts_w_verifier(second_creator, audit_w_auditor):
  """Creates 7 assessments, set global creator as a verifier.

  Returns:
    List of created assessments.
  """
  return [rest_facade.create_asmt(
      audit_w_auditor, verifiers=second_creator) for _ in xrange(7)]


def audit_page(audit):
  """Opens generic widget class of mapped objects according to source obj."""
  return webui_service.AssessmentsService().open_widget_of_mapped_objs(audit)


def my_assessments_page(*args):
  """Opens 'My Assessment' page."""
  return webui_service.AssessmentsService().open_my_assessments_page()


class TestBulkComplete(base.Test):
  """Tests for Bulk Complete functionality."""
  # pylint: disable=no-self-use
  # pylint: disable=invalid-name
  # pylint: disable=too-many-arguments

  @pytest.fixture()
  def deprecated_asmts(self, audit):
    """Returns 5 assessments in 'Deprecated' status."""
    return [rest_facade.create_asmt(audit, status=object_states.DEPRECATED)
            for _ in xrange(5)]

  @pytest.mark.skip(
      reason="Bulk Complete flow is currently disabled and will be reworked.")
  @pytest.mark.parametrize("page", [audit_page, my_assessments_page])
  def test_bulk_complete_state_for_author(
      self, login_as_creator, audit, deprecated_asmts, soft_assert, page,
      selenium
  ):
    """Confirms that 'Bulk complete' option/button is displayed correctly
    for author of objects."""
    page = page(audit)
    webui_facade.soft_assert_bulk_complete_for_completed_asmts(
        soft_assert, deprecated_asmts, page)
    webui_facade.soft_assert_bulk_complete_for_opened_asmts(
        soft_assert, deprecated_asmts, page)
    soft_assert.assert_expectations()

  @pytest.mark.skip(
      reason="Bulk Complete flow is currently disabled and will be reworked.")
  @pytest.mark.parametrize("page", [audit_page, my_assessments_page])
  @pytest.mark.parametrize(
      "audit_role, asmt_role, bulk_complete_btn_visibility",
      [(roles_rest_facade.custom_audit_read_role(),
        roles_rest_facade.custom_asmt_read_role(), False),
       (roles.AUDITORS, roles.VERIFIERS, True)],
      ids=["reader", "editor"])
  def test_bulk_complete_state_for_reader_and_editor(
      self, audit_role, asmt_role, creator, second_creator,
      login_as_creator, audit, deprecated_asmts, bulk_complete_btn_visibility,
      soft_assert, page, selenium
  ):
    """Confirms that 'Bulk complete' option/button is displayed correctly
    for user with Read/Edit rights."""
    rest_facade.update_acl(
        [audit], second_creator,
        **roles_rest_facade.get_role_name_and_id(audit.type, audit_role))
    rest_facade.update_acl(
        deprecated_asmts, second_creator,
        **roles_rest_facade.get_role_name_and_id(deprecated_asmts[0].type,
                                                 asmt_role))
    users.set_current_user(second_creator)
    page = page(audit)
    users.set_current_user(creator)
    webui_facade.soft_assert_bulk_complete_for_completed_asmts(
        soft_assert, deprecated_asmts, page)
    webui_facade.soft_assert_bulk_complete_for_opened_asmts(
        soft_assert, deprecated_asmts, page,
        is_displayed=bulk_complete_btn_visibility)
    soft_assert.assert_expectations()


class TestBulkVerify(base.Test):
  """Tests for Bulk Verify functionality."""

  @pytest.mark.smoke_tests
  @pytest.mark.parametrize('page', [audit_page, my_assessments_page])
  def test_bulk_verify_option_for_verifier(
      self, second_creator, login_as_creator, audit_w_auditor,
      asmts_w_verifier, login_as_second_creator, page, soft_assert, selenium
  ):
    """Check bulk verify option for user with verifier role."""
    page = page(audit_w_auditor)
    webui_facade.soft_assert_bulk_verify_for_not_in_review_state(
        page, asmts_w_verifier, soft_assert)
    webui_facade.soft_assert_bulk_verify_for_in_review_state(
        page, asmts_w_verifier[-1], soft_assert, is_available=True)
    soft_assert.assert_expectations()

  @pytest.mark.smoke_tests
  @pytest.mark.parametrize('page', [audit_page, my_assessments_page])
  def test_bulk_verify_option_for_non_verifier(
      self, second_creator, login_as_creator, audit_w_auditor,
      asmts_w_verifier, page, soft_assert, selenium
  ):
    """Check bulk verify option for user without verifier role."""
    page = page(audit_w_auditor)
    webui_facade.soft_assert_bulk_verify_for_not_in_review_state(
        page, asmts_w_verifier, soft_assert)
    webui_facade.soft_assert_bulk_verify_for_in_review_state(
        page, asmts_w_verifier[-1], soft_assert, is_available=False)
    soft_assert.assert_expectations()

  @pytest.mark.smoke_tests
  @pytest.mark.parametrize('page', [audit_page, my_assessments_page])
  def test_bulk_verification(
      self, second_creator, login_as_creator, audit_w_auditor,
      asmts_w_verifier, login_as_second_creator, page, soft_assert, selenium
  ):
    """Check that assessments statuses actually have been updated after
    bulk verify has been completed."""
    for asmt in asmts_w_verifier:
      rest_facade.update_object(asmt, status=object_states.READY_FOR_REVIEW)
    page = page(audit_w_auditor)
    modal = page.open_bulk_verify_modal()
    soft_assert.expect(
        not modal.is_verify_button_active,
        "'Bulk Verify' button should be disabled if no selected assessments.")
    soft_assert.expect(not modal.filter_section.is_expanded,
                       "'Filter' section should be collapsed.")
    webui_facade.soft_assert_verified_state_after_bulk_verify(
        page, audit_w_auditor, soft_assert)
    soft_assert.assert_expectations()
