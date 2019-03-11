/*
 Copyright (C) 2019 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import './request-review/request-review';
import {ROLES_CONFLICT} from '../../events/eventTypes';
import '../custom-roles/custom-roles';
import '../custom-roles/custom-roles-modal';
import template from './templates/assessment-people.stache';
import * as localStorage from '../../plugins/utils/local-storage-utils';

const tag = 'assessment-people';

export default can.Component.extend({
  tag,
  template,
  leakScope: true,
  viewModel: {
    define: {
      emptyMessage: {
        type: 'string',
        value: '',
      },
    },
    reviewGroups: [],
    rolesConflict: false,
    infoPaneMode: true,
    instance: {},
    conflictRoles: ['Assignees', 'Verifiers'],
    orderOfRoles: ['Creators', 'Assignees', 'Verifiers'],
    modalState: {
      open: false,
    },
    requestReview(ev) {
      this.attr('modalState.open', ev.modalState.open);
    },
    save(ev) {
      let groups = ev.reviewGroups;
      this.attr('reviewGroups', groups);
      if (this.attr('instance.id')) {
        localStorage.setReviewStateByAssessmentId(
          this.attr('instance.id'), groups.attr()
        );
      }
      this.dispatch('updated');
    },
  },
  events: {
    [`{instance} ${ROLES_CONFLICT.type}`]: function (ev, args) {
      this.viewModel.attr('rolesConflict', args.rolesConflict);
    },
  },
});
