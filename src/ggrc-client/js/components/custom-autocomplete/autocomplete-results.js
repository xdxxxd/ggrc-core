/*
    Copyright (C) 2019 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

// Base viewModel for 'autocomplete-result' component which is part of 'custom-autocomplete'.
// It displays available items and handles selected items.

export default can.Map.extend({
  define: {
    _items: {
      get: function () {
        return this.attr('items').map((item, index) => {
          return {
            _index: index,
            name: item.name,
          };
        });
      },
    },
  },
  items: [],
  currentValue: null,
  showResults: false,
  showNewValue: false,
  // event must be provided by parent component
  addNewItem: function () {
    this.dispatch({
      type: 'addNewItem',
      newValue: this.attr('currentValue'),
    });
    this.hide();
  },
  // event must be provided by parent component
  selectItem: function (index) {
    this.dispatch({
      type: 'selectItem',
      item: this.attr('items')[index],
    });
    this.hide();
  },
  hide: function () {
    this.attr('currentValue', null);
    this.attr('showResults', false);
  },
});
