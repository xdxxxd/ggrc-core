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
    '.autocomplete-item mouseenter'(element) {
      this.removeActive();
      $(element).addClass('active');
    },
    '{viewModel} selectActive'() {
      const items = $(this.element).find('.autocomplete-item');
      const activeIndex = _.findIndex(items,
        (item) => $(item).hasClass('active'));
      this.viewModel.selectItem(activeIndex);
    },
    '{viewModel} highlightNext'() {
      const nextItem = $(this.element)
        .find('.autocomplete-item.active + .autocomplete-item')[0];

      if (nextItem) {
        this.removeActive();
        $(nextItem).addClass('active');
      } else {
        const firstItem = $(this.element).find('.autocomplete-item')[0];

        if (firstItem) {
          this.removeActive();
          $(firstItem).addClass('active');
        }
      }
    },
    '{viewModel} highlightPrevious'() {
      const items = $(this.element).find('.autocomplete-item');

      const activeIndex = _.findIndex(items,
        (item) => $(item).hasClass('active'));

      if (activeIndex && activeIndex > 0) {
        this.removeActive();
        $(items[activeIndex - 1]).addClass('active');
      } else {
        if (activeIndex === 0 && items.length > 1) {
          this.removeActive();
          $(items[items.length - 1]).addClass('active');
        }
      }
    },
  },
});
