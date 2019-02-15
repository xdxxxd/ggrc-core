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
    const type = this.attr('modelName');
    const externalServiceUrl = GGRC.config.external_services[type];

    if (externalServiceUrl) {
      $.get({
        url: externalServiceUrl,
        data: {
          prefix: value,
          limit: 10,
        },
      }).then(this.processItems.bind(this));
    } else {
      return this.requestItems(value)
        .then(this.processItems.bind(this));
    }
  },
  processItems(data) {
    const modelName = this.attr('modelName');
    const result = GGRC.config.external_services[modelName] ?
      data : data[modelName].values;
    this.attr('result', result);
    this.attr('showResults', this.attr('currentValue') !== null);
  },
});

export default can.Component.extend({
  tag: 'people-autocomplete-wrapper',
  template: '<content></content>',
  leakScope: true,
  viewModel: viewModel,
});
