/*
    Copyright (C) 2019 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import template from './autocomplete-dropdown.stache';
import {getMappedAttrName} from '../../plugins/ggrc_utils';

export default can.Component.extend({
  tag: 'autocomplete-dropdown',
  template,
  leakScope: true,
  viewModel: {
    options: [],
    filteredOptions: [],
    isOpen: false,
    canOpen: false,
    title: '',
    modelName: '',
    define: {
      isEmpty: {
        type: 'boolean',
        get() {
          return !this.attr('filteredOptions').length;
        },
      },
      value: {
        set(value) {
          this.attr('title', getMappedAttrName(this.attr('modelName'), value));
          return value;
        },
      },
    },
    initOptions() {
      this.attr('filteredOptions', this.attr('options'));
    },
    filterOptions(el) {
      let value = el.val().toLowerCase();
      let filteredOptions = this.attr('options').filter((item) => {
        return item.value.toLowerCase().includes(value);
      }).map((item) => ({...item, title: item.title || item.value}));

      this.attr('filteredOptions', filteredOptions);
    },
    openDropdown() {
      this.attr('canOpen', true);
    },
    closeDropdown() {
      this.attr('isOpen', false);
      this.attr('canOpen', false);
    },
    changeOpenCloseState() {
      if (!this.attr('isOpen')) {
        if (this.attr('canOpen')) {
          this.initOptions();
          this.attr('canOpen', false);
          this.attr('isOpen', true);
        }
      } else {
        this.closeDropdown();
      }
    },
    onBodyClick(ev) {
      ev.stopPropagation();
    },
    onChange(item) {
      this.attr('value', item.value);
      this.closeDropdown();
    },
  },
  events: {
    '{window} click'() {
      this.viewModel.changeOpenCloseState();
    },
  },
});
