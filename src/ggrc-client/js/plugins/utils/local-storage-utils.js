/*
 Copyright (C) 2019 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

/**
 * Returns all saved records by key
 * @param {String} key - local storage key
 * @return {Array} - list of saved objects by key
 */
function get(key) {
  let ids = window.localStorage.getItem(`${key}:ids`);
  ids = JSON.parse(ids) || [];

  let result = [];

  ids.forEach((id) => {
    let data = window.localStorage.getItem(`${key}:${id}`);

    if (data) {
      result.push(JSON.parse(data));
    }
  });

  return result;
}

/**
 * Creates record in local storage by key
 * @param {String} key - local storage key
 * @param {Object} data - object for saving
 * @return {Object} - saved object with assigned local storage id
 */
function create(key, data) {
  let id = 1;
  // add new id to id's list
  let ids = window.localStorage.getItem(`${key}:ids`);
  if (ids) {
    ids = JSON.parse(ids);
    id = Math.max(0, ...ids) + 1;
    ids.push(id);
  } else {
    ids = [id];
  }
  window.localStorage.setItem(`${key}:ids`, JSON.stringify(ids));

  // create new
  let item = Object.assign({id}, data);
  window.localStorage.setItem(`${key}:${id}`, JSON.stringify(item));

  return item;
}

/**
 * Updates existing object in local storage by key
 * @param {String} key - local storage key
 * @param {Object} data object for saving. Should contain local storage id.
 */
function update(key, data) {
  window.localStorage.setItem(`${key}:${data.id}`, JSON.stringify(data));
}

/**
 * Removes object from local storage by key
 * @param {String} key local storage key
 * @param {String/Integer} id object id in local storage
 */
function remove(key, id) {
  if (window.localStorage.getItem(`${key}:${id}`)) {
    window.localStorage.removeItem(`${key}:${id}`);

    // remove from list
    let ids = window.localStorage.getItem(`${key}:ids`);

    if (ids) {
      ids = JSON.parse(ids);
      const index = ids.indexOf(id);

      if (index !== -1) {
        ids.splice(index, 1);
        window.localStorage.setItem(`${key}:ids`, JSON.stringify(ids));
      }
    }
  }
}

/**
 * Removes all data from local storage by key
 * If key is not passed whole local storage is cleared.
 * @param {String} key local storage key
 */
function clear(key) {
  if (!key) {
    window.localStorage.clear();
  }

  let ids = window.localStorage.getItem(`${key}:ids`);
  ids = JSON.parse(ids) || [];
  ids.forEach((id) => {
    window.localStorage.removeItem(`${key}:${id}`);
  });
  window.localStorage.removeItem(`${key}:ids`);
}

const verifier = GGRC.access_control_roles.find((role) => {
  return role.name === 'Verifiers';
});

const defaultReviewState = [
  {
    title: 'Internal 1st Rewiever',
    groupId: verifier.id,
    people: [],
    reviewed: false,
    disabled: false,
  },
  {
    title: 'Internal 2nd Rewiever',
    groupId: verifier.id,
    people: [],
    reviewed: false,
    disabled: false,
  },
  {
    title: 'Internal 3rd Rewiever',
    groupId: verifier.id,
    people: [],
    reviewed: false,
    disabled: false,
  },
  {
    title: 'EY Reviewer #1',
    groupId: verifier.id,
    people: [],
    reviewed: false,
    disabled: true,
  },
  {
    title: 'EY Reviewer #2',
    groupId: verifier.id,
    people: [],
    reviewed: false,
    disabled: true,
  },
];

const REVIEW_KEY = 'demo';
function setReviewStateByAssessmentId(assessmentId, data) { // eslint-disable-line
  window.localStorage.setItem(`${REVIEW_KEY}:${assessmentId}`,
    JSON.stringify(data));
}

function getReviewStateByAssessmentId(assessmentId) { // eslint-disable-line
  return JSON.parse(
    window.localStorage.getItem(`${REVIEW_KEY}:${assessmentId}`)
  );
}

export {
  get,
  create,
  update,
  remove,
  clear,
  setReviewStateByAssessmentId,
  getReviewStateByAssessmentId,
  defaultReviewState,
};
