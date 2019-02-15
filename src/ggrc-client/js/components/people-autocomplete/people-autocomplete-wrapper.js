/*
    Copyright (C) 2019 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import './people-autocomplete-results/people-autocomplete-results';

import baseAutocompleteWrapper from './../custom-autocomplete/autocomplete-wrapper';
import PersonModel from '../../models/business-models/person';

let viewModel = baseAutocompleteWrapper.extend({
  currentValue: null,
  modelName: 'Person',
  modelConstructor: PersonModel,
  queryField: 'email',
  result: [],
  objectsToExclude: [],
  showResults: false,
  showNewValue: false,
  actionKey: null,
  define: {
    currentValue: {
      set(newValue) {
        if (newValue !== null) {
          this.getResult(newValue);
        } else {
          this.attr('showResults', false);
        }

        return newValue;
      },
    },
  },
  getResult(value) {
    this.requestItems(value)
      .then((data) => {
        const modelName = this.attr('modelName');
        const result = _.map(data[modelName].values,
          (object) => new PersonModel(object));
        this.attr('result', result);
        this.attr('showResults', this.attr('currentValue') !== null);
      });
  },
});

export default can.Component.extend({
  tag: 'people-autocomplete-wrapper',
  template: '<content></content>',
  leakScope: true,
  viewModel: viewModel,
});
