# coding=utf-8
# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Classes to represent Change Log elements of object's page/panel."""
# pylint: disable=too-few-public-methods
from lib import base
from lib.entities import entity


class ChangeLog(base.WithBrowser):
  """Represents Change Log element."""

  def __init__(self):
    super(ChangeLog, self).__init__()
    self._root = self._browser.element(class_name="tab-container")

  def get_changelog_items(self):
    """Returns a list of changelog entries."""
    return [ChangeLogEntry(entry_el).change_log_item
            for entry_el in self._root.elements(class_name="w-status")]

  def get_object_creation_entry(self):
    """Return changelog entry that is related to object creation."""
    return self.get_changelog_items()[-1]


class ReadonlyChangeLog(ChangeLog):
  """Represents Change Log element for disabled objects."""

  @property
  def open_change_log_in_new_fe_btn(self):
    """Returns button in Change Log tab for opening Change Log in new
    frontend."""
    return self._root.element(text="Open Change Log in new frontend")

  @property
  def is_log_message_displayed(self):
    """Returns whether log message for disabled objects exists."""
    return self._root.element(class_name="revision-log__logs-message").exists

  def open_change_log_in_new_fe(self):
    """Click "Open Change Log in new frontend" button if it exists."""
    if self.open_change_log_in_new_fe_btn.exists:
      self.open_change_log_in_new_fe_btn.click()


class ChangeLogEntry(object):
  """Represents a single changelog entry."""

  def __init__(self, entry_el):
    self._root = entry_el

  def _get_changes(self):
    """Collects attributes changes data.
    Stores this data in list of dicts. List is sorted to provide correct
    comparison with expected values. Each dict represents single attribute
    change entry.
    Returns:
      list of dicts."""
    def parse_value(value):
      """Return None if value is 'Em dash' else returns value."""
      return value if not value == u'—' else None

    def parse_attr_name(value):
      """Returns attribute name transformed from UI representation into
      corresponded attribute name of object entity."""
      attrs_to_remap = entity.Representation.remap_collection()
      return (attrs_to_remap[value.upper()]
              if value.upper() in attrs_to_remap else value)

    changes_list = []
    for change_item_element in self._root.elements(class_name="clearfix"):
      change_item_texts = [
          e.text for e in change_item_element.elements(class_name="third-col")]
      change_item = {
          "attribute_name": parse_attr_name(change_item_texts[0]),
          "original_value": parse_value(change_item_texts[1]),
          "new_value": parse_value(change_item_texts[2])}
      changes_list.append(change_item)
    return sorted(changes_list)

  @property
  def change_log_item(self):
    """Returns Change log item as ChangeLogItemEntity instance."""
    return entity.ChangeLogItemEntity(
        author=self._root.element(tag_name="person-data").text,
        changes=self._get_changes())
