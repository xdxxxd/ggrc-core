/*
    Copyright (C) 2019 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import canStache from 'can-stache';
import canMap from 'can-map';
import canComponent from 'can-component';
import template from './assessment-tree-actions.stache';

export default canComponent.extend({
  tag: 'assessment-tree-actions',
  view: canStache(template),
  viewModel: canMap.extend({
    define: {
      showBulkComplete: {
        value: false,
      },
    },
    instance: null,
    parentInstance: null,
    model: null,
  }),
});
