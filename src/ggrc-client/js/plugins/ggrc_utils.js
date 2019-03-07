/*
 Copyright (C) 2019 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import {getRolesForType} from '../plugins/utils/acl-utils';

/**
 * A module containing various utility functions.
 */

/**
 * Performs filtering on provided array like instances
 * @param {Array} items - array like instance
 * @param {Function} filter - filtering function
 * @param {Function} selectFn - function to select proper attributes
 * @return {Array} - filtered array
 */
function _applyFilter(items, filter, selectFn) {
  selectFn = selectFn ||
    function (x) {
      return x;
    };
  return Array.prototype.filter.call(items, function (item) {
    return filter(selectFn(item));
  });
}

/**
 * Helper function to create a filtering function
 * @param {Object|null} filterObj - filtering params
 * @return {Function} - filtering function
 */
function _makeTypeFilter(filterObj) {
  function checkIsNotEmptyArray(arr) {
    return arr && Array.isArray(arr) && arr.length;
  }
  return function (type) {
    type = type.toString().toLowerCase();
    if (!filterObj) {
      return true;
    }
    if (checkIsNotEmptyArray(filterObj.only)) {
      // Do sanity transformation
      filterObj.only = filterObj.only.map(function (item) {
        return item.toString().toLowerCase();
      });
      return filterObj.only.indexOf(type) > -1;
    }
    if (checkIsNotEmptyArray(filterObj.exclude)) {
      // Do sanity transformation
      filterObj.exclude = filterObj.exclude.map(function (item) {
        return item.toString().toLowerCase();
      });
      return filterObj.exclude.indexOf(type) === -1;
    }
    return true;
  };
}

function applyTypeFilter(items, filterObj, getTypeSelectFn) {
  let filter = _makeTypeFilter(filterObj);
  return _applyFilter(items, filter, getTypeSelectFn);
}

function isInnerClick(el, target) {
  el = el instanceof $ ? el : $(el);
  return el.has(target).length || el.is(target);
}

function inViewport(el) {
  let bounds;
  let isVisible;

  el = el instanceof $ ? el[0] : el;
  bounds = el.getBoundingClientRect();

  isVisible = window.innerHeight > bounds.bottom &&
  window.innerWidth > bounds.right;

  return isVisible;
}

function getPickerElement(picker) {
  return _.find(_.values(picker), function (val) {
    if (val instanceof Node) {
      return /picker-dialog/.test(val.className);
    }
    return false;
  });
}

function loadScript(url, callback) {
  let script = document.createElement('script');
  script.type = 'text/javascript';
  if (script.readyState) {
    script.onreadystatechange = function () {
      if (script.readyState === 'loaded' ||
        script.readyState === 'complete') {
        script.onreadystatechange = null;
        callback();
      }
    };
  } else {
    script.onload = function () {
      callback();
    };
  }
  script.src = url;
  document.getElementsByTagName('head')[0].appendChild(script);
}

function hasPending(parentInstance) {
  let list = parentInstance._pendingJoins;

  return !!(list && list.length);
}

/**
 * Remove all HTML tags from the string
 * @param {String} originalText - original string for parsing
 * @return {string} - plain text without tags
 */
function getPlainText(originalText) {
  originalText = originalText || '';
  return originalText.replace(/<[^>]*>?/g, '').trim();
}

/**
 * Build string of assignees types separated by commas.
 * @param {Object} instance - Object instance
 * @return {String} assignees types separated by commas
 */
function getAssigneeType(instance) {
  let currentUser = GGRC.current_user;
  let roles = getRolesForType(instance.type);
  let userType = null;

  if (!instance || !currentUser) {
    return;
  }

  _.forEach(roles, function (role) {
    let aclPerson = instance
      .access_control_list
      .filter((item) => item.ac_role_id === role.id &&
        item.person.id == currentUser.id); // eslint-disable-line

    if (!aclPerson.length) {
      return;
    }

    userType = userType ? userType + ',' + role.name : role.name;
  });

  return userType;
}

function getTruncatedList(items) {
  const itemsLimit = 5;
  const mainContent = items
    .slice(0, itemsLimit)
    .join('\n');
  const lastLine = items.length > itemsLimit
    ? `\n and ${items.length - itemsLimit} more`
    : '';

  return mainContent + lastLine;
}

const ATTR_MAPPER = {
  Program: {
    'Program Managers': 'Alphabet / Google SOX PMO',
    'Program Editors': 'RCS',
  },
  Process: {
    Admin: 'RCS',
    Assignee: 'Secondary RCS',
    'System Owners': 'Process Owners',
    Verifier: 'Alphabet / Google SOX PMO',
    'Reference URL': 'Flowchart Link',
  },
  Control: {
    Admin: 'Control Owners',
  },
  System: {
    Admin: 'Eng Compliance',
    Verifier: 'Alphabet / Google SOX PMO',
  },
  Assessment: {
    Creators: 'Alphabet / Google SOX PMO',
    Assignees: 'Assessment Submitters',
  },
  KeyReport: {
    Admin: 'Alphabet / Google SOX PMO',
    'System Owners': 'Key Report Owners',
    Assignee: 'Secondary RCS',
  },
  Risk: {
    Admin: 'Alphabet / Google SOX PMO',
  },
  Audit: {
    'Audit Captains': 'Alphabet / Google SOX PMO',
  },
  Issue: {
    Admin: 'Alphabet / Google SOX PMO',
  },
  // Account Balance
  Project: {
    Admin: 'RCS',
    Assignee: 'Secondary RCS',
    'System Owners': 'Process Owners',
    Verifier: 'Alphabet / Google SOX PMO',
  },
};

function getMappedAttrName(type, attrName) {
  const mapper = ATTR_MAPPER[type];

  if (!mapper) {
    return attrName;
  }

  return mapper[attrName] || attrName;
}

export {
  applyTypeFilter,
  isInnerClick,
  inViewport,
  getPickerElement,
  loadScript,
  hasPending,
  getPlainText,
  getAssigneeType,
  getTruncatedList,
  getMappedAttrName,
};
