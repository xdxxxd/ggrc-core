# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""UI facade for comment actions."""
# pylint: disable=invalid-name
from lib.constants import counters, str_formats
from lib.service import webui_service
from lib.utils import string_utils


def soft_assert_max_emails_num(comments_panel, soft_assert):
  """Soft assert max number of emails in dropdown is valid."""
  soft_assert.expect(
      comments_panel.emails_dropdown.number_of_items ==
      counters.MAX_EMAILS_IN_DROPDOWN,
      "There should be max {} items in dropdown".format(
          counters.MAX_EMAILS_IN_DROPDOWN))


def soft_assert_mentioning_format_in_input_field(
    soft_assert, email, comments_panel
):
  """Soft assert selected email appears in input field with '+' sign before
  it.
  """
  soft_assert.expect(comments_panel.input_field.text ==
                     str_formats.MENTIONED_EMAIL.format(email=email),
                     "Selected email should appear in comment field with '{}'"
                     " sign before it".format(string_utils.Symbols.PLUS))


def soft_assert_mentioning_format_in_comment(
    comments_panel, soft_assert, email
):
  """Soft assert mentioned email appears in comment with '+' sign before it
  and it is a link."""
  soft_assert.expect(comments_panel.scopes[0].get('description') ==
                     str_formats.MENTIONED_EMAIL.format(email=email).rstrip(),
                     "Comment should be displayed under 'Comments' box")
  soft_assert.expect(str_formats.MAILTO.format(email=email) in
                     comments_panel.scopes[0].get('links'),
                     "Added comment should be a link")


def check_mentioning_on_asmt_comment_panel(
    selenium, soft_assert, audit, assessment, first_symbol
):
  """Checks mentioning on assessment comment panel on info panel."""
  comments_panel = (webui_service.AssessmentsService(selenium).
                    open_info_panel_of_mapped_obj(
                        src_obj=audit, obj=assessment).comments_panel)
  comments_panel.call_email_dropdown(first_symbol)
  soft_assert_max_emails_num(comments_panel, soft_assert)
  mentioned_email = comments_panel.emails_dropdown.select_first_email()
  soft_assert_mentioning_format_in_input_field(
      soft_assert, mentioned_email, comments_panel)
  comments_panel.click_add_button()
  soft_assert_mentioning_format_in_comment(
      comments_panel, soft_assert, mentioned_email)
  soft_assert.assert_expectations()
