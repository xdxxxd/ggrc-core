/*
 Copyright (C) 2020 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import canMap from 'can-map';
import {isProposableExternally} from '../../plugins/utils/ggrcq-utils';

export default canMap.extend({
  define: {
    isReadonly: {
      get() {
        let instance = this.attr('instance');
        if (!instance) {
          return false;
        }

        let readonly = this.attr('readOnly');
        return instance.constructor.isProposable
            || readonly
            || instance.attr('readonly');
      },
    },
    redirectionEnabled: {
      get() {
        return isProposableExternally(this.attr('instance'));
      },
    },
  },
  instance: null,
  updatableGroupId: null,
  includeRoles: [],
  excludeRoles: [],
  conflictRoles: [],
  orderOfRoles: [],
  readOnly: false,
  // When we delete some role this action can delete another acl role on the backend.
  // In this case we get in response less objects then was in request.
  // But canJs is merging array-attributes not replacing.
  // As result it doesn't remove redundant element.
  filterACL() {
    let filteredACL = this.attr('instance.access_control_list')
      .filter((role) => role.id);

    this.attr('instance.access_control_list').replace(filteredACL);
  },
  save(args) {
    this.attr('updatableGroupId', args.groupId);

    return this.attr('instance').save()
      .then(() => {
        this.filterACL();
      }).always(() => {
        this.attr('updatableGroupId', null);
      });
  },
});
