/*
 Copyright (C) 2019 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import '../../related-objects/related-people-access-control';
import '../../related-objects/related-people-access-control-group';
import '../../people/deletable-people-group';
import '../../autocomplete/autocomplete';
import '../../external-data-autocomplete/external-data-autocomplete';
import template from './request-review-roles.stache';

export default can.Component.extend({
  tag: 'request-review-roles',
  template,
  leakScope: true,
  viewModel: {
    review: null,
  },
});
