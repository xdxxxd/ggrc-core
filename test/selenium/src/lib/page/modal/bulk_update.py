# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Models for bulk update modals."""
import re
from lib import base


class BaseBulkUpdateModal(base.Modal):
  """Common class for Bulk Complete and Bulk Verify modals."""
  # pylint: disable=too-few-public-methods

  def __init__(self):
    super(BaseBulkUpdateModal, self).__init__()
    self._root = self._browser.div(class_name="modal")
    self.filter_section = FilterSection(self._root)

  @property
  def is_displayed(self):
    """Returns whether modal is opened or not."""
    return self._root.exists


class BulkVerifyModal(BaseBulkUpdateModal):
  """Represents bulk verify modal."""

  def __init__(self):
    super(BulkVerifyModal, self).__init__()
    self._root = self._root.element(tag_name="assessments-bulk-verify")
    self.select_assessments_section = SelectAssessmentsToVerifySection(
        self._root)

  @property
  def verify_button(self):
    """Returns whether 'Verify' button."""
    return self._root.button(text='Verify')

  @property
  def is_verify_button_active(self):
    """Returns whether 'Verify' button is enabled and can be clicked."""
    return self.verify_button.wait_until(lambda x: x.exists).enabled

  def click_verify(self):
    """Clicks 'Verify' button."""
    self.verify_button.click()


class FilterSection(object):
  """Represents collapsible filter section."""
  # pylint: disable=too-few-public-methods

  def __init__(self, parent_element):
    self._root = parent_element.element(
        tag_name="collapsible-panel", text=re.compile("FILTER"))

  @property
  def is_expanded(self):
    """Returns whether section is expanded or not."""
    return "is-expanded" in self._root.div(class_name="body-inner").classes


class SelectAssessmentsToVerifySection(object):
  """Represents 'Select assessments' section."""
  # pylint: disable=too-few-public-methods

  def __init__(self, parent_element):
    self._root = parent_element.element(
        tag_name="collapsible-panel", text=re.compile("SELECT ASSESSMENTS"))

  def click_select_all(self):
    """Clicks 'Select All' link to select all assessments."""
    self._root.button(text="All").click()
