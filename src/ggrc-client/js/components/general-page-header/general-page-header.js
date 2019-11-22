/*
    Copyright (C) 2019 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import canStache from 'can-stache';
import canMap from 'can-map';
import canComponent from 'can-component';
import template from './templates/general-page-header.stache';
import {
  isProposableExternally,
  isChangeableExternally,
} from '../../plugins/utils/ggrcq-utils';
import {isSnapshot} from '../../plugins/utils/snapshot-utils';

const viewModel = canMap.extend({
  define: {
    redirectionEnabled: {
      get() {
        return isProposableExternally(this.attr('instance'));
      },
    },
    showProposalButton: {
      get() {
        const instance = this.attr('instance');
        return (
          instance.constructor.isProposable &&
          !isChangeableExternally(instance) &&
          !isSnapshot(instance)
        );
      },
    },
  },
  instance: null,
  isSaving: false,
});

export default canComponent.extend({
  tag: 'general-page-header',
  view: canStache(template),
  leakScope: true,
  viewModel,
});
