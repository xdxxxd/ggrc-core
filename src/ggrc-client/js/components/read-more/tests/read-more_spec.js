/*
  Copyright (C) 2019 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import {getComponentVM} from '../../../../js_specs/spec-helpers';
import Component from '../read-more';

describe('read-more component', () => {
  let vm;

  beforeEach(() => {
    vm = getComponentVM(Component);
  });

  describe('toggle() method', () => {
    let eventMock;

    beforeEach(() => {
      eventMock = {
        stopPropagation: jasmine.createSpy(),
      };
    });

    it('calls stopPropagation()', () => {
      vm.toggle(eventMock);

      expect(eventMock.stopPropagation).toHaveBeenCalled();
    });

    it('switchs expanded attribute', () => {
      vm.attr('expanded', true);
      vm.toggle(eventMock);

      expect(vm.attr('expanded')).toBe(false);
      vm.toggle(eventMock);

      expect(vm.attr('expanded')).toBe(true);
    });
  });
  describe('set() of cssClass attribute', () => {
    it('returns empty string if viewModel.expanded is true', () => {
      vm.attr('expanded', true);
      expect(vm.attr('cssClass')).toEqual('');
    });
    it('returns specific css string ' +
    'if viewModel.expanded is false', () => {
      for (let i; i <= 10; i++) {
        vm.attr('maxLinesNumber', i);
        expect(vm.attr('cssClass')).toEqual('ellipsis-truncation-' + i);
      }
    });
  });
});
