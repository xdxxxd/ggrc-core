# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Mentioning person smoke tests."""
# pylint: disable=no-self-use
# pylint: disable=too-many-arguments
# pylint: disable=unused-argument
# pylint: disable=invalid-name

import pytest

from lib.rest_facades import person_rest_facade
from lib.ui import comments_ui_facade
from lib.utils import string_utils


class TestMentioningPerson(object):
  """Tests of mentioning person."""

  @pytest.fixture(scope="function")
  def people(self):
    """Creates 10 people."""
    for _ in xrange(10):
      person_rest_facade.create_person()

  @pytest.mark.parametrize('first_symbol', [string_utils.Symbols.PLUS,
                                            string_utils.Symbols.AT_SIGN])
  def test_mentioning_on_asmt_comment_panel(
      self, people, audit, assessment, selenium, first_symbol, soft_assert
  ):
    """Checks mentioning on assessment comment panel on info panel.

    Preconditions:
        - Program created via REST API.
        - Audit created under Program via REST API.
        - Assessment created under Audit via REST API.
        - 10 People created via REST API.
    """
    comments_ui_facade.check_mentioning_on_asmt_comment_panel(
        selenium, soft_assert, audit, assessment, first_symbol)
