/*
  Copyright (C) 2019 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import * as pickerUtils from '../../../plugins/utils/gdrive-picker-utils';
import * as NotifiersUtils from '../../../plugins/utils/notifiers-utils';
import tracker from '../../../tracker';
import {getComponentVM} from '../../../../js_specs/spec-helpers';
import Component from '../ggrc-gdrive-picker-launcher';

describe('ggrc-gdrive-picker-launcher', function () {
  'use strict';

  let viewModel;
  let eventStub = {
    preventDefault: function () {},
  };

  beforeEach(function () {
    viewModel = getComponentVM(Component);
    spyOn(tracker, 'start').and.returnValue(() => {});
  });

  describe('onClickHandler() method', function () {
    it('call confirmationCallback() if it is provided', function () {
      spyOn(viewModel, 'confirmationCallback');

      viewModel.onClickHandler(null, null, eventStub);

      expect(viewModel.confirmationCallback).toHaveBeenCalled();
    });

    it('pass callbackResult to $.when()', function () {
      let dfd = $.Deferred();
      let thenSpy = jasmine.createSpy('then');
      spyOn(viewModel, 'confirmationCallback').and.returnValue(dfd);
      spyOn($, 'when').and.returnValue({
        then: thenSpy,
      });

      viewModel.onClickHandler(null, null, eventStub);

      expect($.when).toHaveBeenCalledWith(dfd);
      expect(thenSpy).toHaveBeenCalled();
    });

    it('pass null to $.when() when callback is not provided', function () {
      let thenSpy = jasmine.createSpy('then');
      spyOn($, 'when').and.returnValue({
        then: thenSpy,
      });

      viewModel.onClickHandler(null, null, eventStub);

      expect($.when).toHaveBeenCalledWith(null);
      expect(thenSpy).toHaveBeenCalled();
    });
  });

  describe('onKeyup() method', function () {
    describe('if escape key was clicked', function () {
      let event;
      let element;

      beforeEach(function () {
        const ESCAPE_KEY_CODE = 27;
        event = {
          keyCode: ESCAPE_KEY_CODE,
          stopPropagation: jasmine.createSpy('stopPropagation'),
        };
        element = $('<div></div>');
      });

      it('calls stopPropagation for passed event', function () {
        viewModel.onKeyup(element, event);
        expect(event.stopPropagation).toHaveBeenCalled();
      });

      it('unsets focus for element', function (done) {
        const blur = function () {
          done();
          element.off('blur', blur);
        };
        element.on('blur', blur);
        viewModel.onKeyup(element, event);
      });
    });
  });

  describe('trigger_upload() method', function () {
    let uploadFilesDfd;
    let createModelDfd;
    let el;

    beforeEach(function () {
      el = jasmine.createSpyObj(['data', 'trigger']);
      uploadFilesDfd = $.Deferred();
      spyOn(pickerUtils, 'uploadFiles').and.returnValue(uploadFilesDfd);
    });

    it('sets "isUploading" flag to true', function () {
      viewModel.attr('isUploading', false);

      viewModel.trigger_upload(viewModel, el);

      expect(viewModel.attr('isUploading')).toBe(true);
    });

    describe('sets "isUploading" flag to false', function () {
      beforeEach(function () {
        createModelDfd = $.Deferred();
        viewModel.attr('isUploading', true);
        spyOn(viewModel, 'createDocumentModel').and.returnValue(createModelDfd);
      });

      it('when uploadFiles() was failed', function (done) {
        uploadFilesDfd.reject();

        viewModel.trigger_upload(viewModel, el).fail(() => {
          expect(viewModel.attr('isUploading')).toBe(false);
          done();
        });
      });

      it('after createDocumentModel() success', function (done) {
        uploadFilesDfd.resolve();
        createModelDfd.resolve([]);

        viewModel.trigger_upload(viewModel, el).then(() => {
          expect(viewModel.attr('isUploading')).toBe(false);
          done();
        });
      });

      it('when createDocumentModel() was failed', function (done) {
        uploadFilesDfd.resolve();
        createModelDfd.reject();

        viewModel.trigger_upload(viewModel, el).fail(() => {
          expect(viewModel.attr('isUploading')).toBe(false);
          done();
        });
      });
    });
  });

  describe('trigger_upload_parent() method', () => {
    let uploadDfd;
    let parentFolderDfd;
    let parentFolderStub;
    let errorMessage;

    beforeEach(() => {
      parentFolderStub = {id: 'id'};
      parentFolderDfd = $.Deferred();
      uploadDfd = $.Deferred();

      spyOn(pickerUtils, 'findGDriveItemById').and.returnValue(parentFolderDfd);
      spyOn(viewModel, 'uploadParentHelper').and.returnValue(uploadDfd);
      spyOn($.fn, 'trigger').and.callThrough();
    });

    it('uses transient folder as parent folder if it exists', () => {
      viewModel.instance.attr('_transient.folder', 'folder');

      viewModel.trigger_upload_parent(viewModel);
      expect(pickerUtils.findGDriveItemById).not.toHaveBeenCalled();
    });

    it('calls findGDriveItemById() if transient folder doesn\'t exist', () => {
      let folderId = 123;
      viewModel.instance.attr('_transient.folder', undefined);
      viewModel.instance.attr('folder', folderId);

      viewModel.trigger_upload_parent(viewModel);
      expect(pickerUtils.findGDriveItemById).toHaveBeenCalledWith(folderId);
    });


    it('calls uploadParentHelper() method', (done) => {
      parentFolderDfd.resolve(parentFolderStub);

      viewModel.trigger_upload_parent(viewModel).then(() => {
        expect(viewModel.uploadParentHelper).toHaveBeenCalled();
        done();
      });
    });

    it('displays error message if gdrive hasn\'t found', (done) => {
      parentFolderDfd.reject();
      errorMessage = 'Can\'t upload: No GDrive folder found';

      viewModel.trigger_upload_parent(viewModel).fail(() => {
        expect($.fn.trigger).toHaveBeenCalledWith('ajax:flash', {
          warning: errorMessage,
        });
        done();
      });
    });
  });

  describe('uploadParentHelper() method', () => {
    let uploadParentHelper;
    let uploadFilesDfd;
    let parentFolderDfd;
    let files;
    let parentFolderStub;
    let scope;
    let error;

    beforeEach(() => {
      parentFolderStub = {id: 'id'};
      parentFolderDfd = $.Deferred();
      uploadFilesDfd = $.Deferred();
      files = ['file', 'file'];

      scope = {
        instance: {
          type: 'type',
        },
      };

      spyOn(viewModel, 'createDocumentModel')
        .and.returnValue(uploadFilesDfd.resolve());

      spyOn(pickerUtils, 'uploadFiles')
        .and.returnValue(parentFolderDfd);

      spyOn(NotifiersUtils, 'notifier');

      uploadParentHelper = viewModel.uploadParentHelper.bind(viewModel);
    });

    it('sets "isUploading" flag to true', () => {
      viewModel.attr('isUploading', false);

      uploadParentHelper(parentFolderStub);
      expect(viewModel.attr('isUploading')).toBe(true);
    });

    it('sets "isUploading" flag to false after uploadFiles() success',
      (done) => {
        parentFolderDfd.resolve(files);

        viewModel.attr('isUploading', true);

        uploadParentHelper(parentFolderStub, scope).then(() => {
          expect(viewModel.attr('isUploading')).toBe(false);
          done();
        });
      });

    it('sets "isUploading" flag to false when uploadFiles() was failed',
      (done) => {
        parentFolderDfd.reject();

        viewModel.attr('isUploading', true);

        uploadParentHelper(parentFolderStub, scope).fail(() => {
          expect(viewModel.attr('isUploading')).toBe(false);
          done();
        });
      });

    it('calls createDocumentModel() method after uploadFiles() success',
      (done) => {
        parentFolderDfd.resolve(files);

        viewModel.attr('isUploading', true);

        uploadParentHelper(parentFolderStub, scope).then(() => {
          expect(viewModel.createDocumentModel).toHaveBeenCalledWith(files);
          done();
        });
      });

    it('calls notifier() if error code equal 403',
      (done) => {
        error = {
          code: 403,
          type: 'GDRIVE_PICKER_ERR_CANCEL',
        };

        parentFolderDfd.reject(error);

        uploadParentHelper(parentFolderStub, scope).fail(() => {
          expect(NotifiersUtils.notifier)
            .toHaveBeenCalledWith('error', NotifiersUtils.messages[403]);
          done();
        });
      });

    it('calls notifier() if error type not equal GDRIVE_PICKER_ERR_CANCEL',
      (done) => {
        error = {
          code: 404,
          type: 'SOME_ANOTHER_ERROR',
          message: 'not found',
        };

        parentFolderDfd.reject(error);

        uploadParentHelper(parentFolderStub, scope).fail(() => {
          expect(NotifiersUtils.notifier)
            .toHaveBeenCalledWith('error', error.message);
          done();
        });
      });
  });
});
