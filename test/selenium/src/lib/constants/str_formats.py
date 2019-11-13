# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""String formats."""
from lib.utils import string_utils

MENTIONED_EMAIL = string_utils.Symbols.PLUS + "{email} "
MAILTO = "mailto:{email}"
