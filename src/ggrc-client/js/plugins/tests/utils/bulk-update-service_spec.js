/*
  Copyright (C) 2019 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import * as AjaxExtensions from '../../ajax-extensions';
import service from '../../utils/bulk-update-service';

describe('GGRC BulkUpdateService', function () {
  describe('update() method', function () {
    let method;
    let ajaxRes;

    beforeEach(function () {
      method = service.update;
      ajaxRes = {
      };
      ajaxRes.done = jasmine.createSpy().and.returnValue(ajaxRes);
      ajaxRes.fail = jasmine.createSpy().and.returnValue(ajaxRes);

      spyOn(AjaxExtensions, 'ggrcAjax')
        .and.returnValue(ajaxRes);
    });

    it('makes ajax call with transformed data', function () {
      let model = {
        table_plural: 'some_model',
      };
      let data = [{
        id: 1,
      }];

      method(model, data, {state: 'In Progress'});

      expect(AjaxExtensions.ggrcAjax)
        .toHaveBeenCalledWith({
          url: '/api/some_model',
          method: 'PATCH',
          contentType: 'application/json',
          data: '[{"id":1,"state":"In Progress"}]',
        });
    });
  });
});
