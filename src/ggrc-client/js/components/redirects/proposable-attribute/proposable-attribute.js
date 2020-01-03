/*
 Copyright (C) 2020 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import canStache from 'can-stache';
import canMap from 'can-map';
import canComponent from 'can-component';
import template from './templates/proposable-attribute.stache';
import {isProposableExternally} from '../../../plugins/utils/ggrcq-utils';

const viewModel = canMap.extend({
  define: {
    showToolbarControls: {
      get() {
        return isProposableExternally(this.attr('instance'));
      },
    },
  },
  instance: null,
  attrName: '',
  title: '',
  mandatory: false,
});

export default canComponent.extend({
  tag: 'proposable-attribute',
  leakScope: false,
  view: canStache(template),
  viewModel,
});
