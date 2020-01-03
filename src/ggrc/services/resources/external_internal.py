# Copyright (C) 2020 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""API resource for models that can be as external as internal."""

from ggrc import login
from ggrc.services import common


class ExternalInternalResource(common.Resource):
  """Resource handler for models that can work as external and as internal."""
  # pylint: disable=abstract-method

  def validate_headers_for_put_or_delete(self, obj):
    """Check ETAG for internal request and skip for external."""
    if login.is_external_app_user():
      return None
    return super(
        ExternalInternalResource, self
    ).validate_headers_for_put_or_delete(obj)
