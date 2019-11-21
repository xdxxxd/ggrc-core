# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""This module contains notification utils."""

import functools
import logging

from ggrc import settings


logger = logging.getLogger(__name__)


def exec_if_notifications_enabled(func):
  """Execute function only if `NOTIFICATIONS_ENABLED` setting is `True`."""
  @functools.wraps(func)
  def wrapper(*args, **kwargs):
    """Check `NOTIFICATIONS_ENABLED` setting and call `func` if `True`."""
    if settings.NOTIFICATIONS_ENABLED:
      return func(*args, **kwargs)

    logger.info(
        "%s could not be executed since notification mechanism is disabled",
        func.__name__)

    return None

  return wrapper
