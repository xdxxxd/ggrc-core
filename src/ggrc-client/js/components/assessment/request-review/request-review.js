/*
  Copyright (C) 2019 Google Inc., authors, and contributors
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import './request-review-roles';
import template from './request-review.stache';

export default can.Component.extend({
  tag: 'request-review',
  template,
  leakScope: true,
  viewModel: {
    review: null,
    loading: false,
  },
});
