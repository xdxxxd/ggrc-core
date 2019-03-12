/*
    Copyright (C) 2019 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import template from './editable-people-group-header.stache';

export default can.Component.extend({
  tag: 'editable-people-group-header',
  template,
  leakScope: true,
  viewModel: {
    define: {
      peopleCount: {
        get: function () {
          if (this.attr('currentVerifiers')) {
            return this.attr('currentVerifiers.length');
          }

          return this.attr('people.length');
        },
      },
    },
    currentVerifiers: [],
    singleUserRole: false,
    editableMode: false,
    isLoading: false,
    canEdit: true,
    required: false,
    people: [],
    instance: null,
    openEditMode: function () {
      this.dispatch('editPeopleGroup');
    },
  },
});
