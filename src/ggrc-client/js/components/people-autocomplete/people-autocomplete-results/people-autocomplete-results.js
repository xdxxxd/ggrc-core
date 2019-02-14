/*
    Copyright (C) 2019 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import baseAutocompleteResults from '../../custom-autocomplete/autocomplete-results';
import template from './people-autocomplete-results.stache';

export default can.Component.extend({
  tag: 'people-autocomplete-results',
  template,
  leakScope: false,
  viewModel: baseAutocompleteResults.extend({
    currentValue: null,
    showResults: false,
    showNewValue: false,
  }),
  events: {
    removeActive() {
      const activeItems = 
        $(this.element).find('.autocomplete-item.active');
      activeItems.removeClass('active');
    },
    '.autocomplete-item mouseenter'(element, event) {
      this.removeActive();
      $(element).addClass('active');
    }
  },
});
