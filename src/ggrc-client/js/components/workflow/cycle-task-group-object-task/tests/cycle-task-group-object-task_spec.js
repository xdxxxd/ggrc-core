/*
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import Component from '../cycle-task-group-object-task';
import RefreshQueue from '../../../../models/refresh_queue';

describe('GGRC.Components.cycleTaskGroupObjectTask', function () {
  let viewModel;

  beforeEach(function () {
    viewModel = new Component.prototype.viewModel({
      instance: {
        cycle: {},
      },
    });
    viewModel.attr('instance', {
      cycle: {},
    });
  });

  describe('viewModel scope', function () {
    describe('init() method', function () {
      let cycleDfd;

      beforeEach(function () {
        cycleDfd = new can.Deferred();
        spyOn(viewModel, 'loadCycle').and.returnValue(cycleDfd);
      });

      it('calls loadCycle method', function () {
        viewModel.init();
        expect(viewModel.loadCycle).toHaveBeenCalled();
      });

      it('loads workflow after cycle is loaded', function () {
        spyOn(viewModel, 'loadWorkflow');
        cycleDfd.resolve();

        viewModel.init();
        expect(viewModel.loadWorkflow).toHaveBeenCalled();
      });
    });

    describe('loadCycle() method', function () {
      describe('when reified cycle is not empty', function () {
        let trigger;
        let triggerDfd;
        let reifiedCycle;

        beforeEach(function () {
          reifiedCycle = new can.Map({data: 'Data'});
          viewModel.attr('instance.cycle').reify =
            jasmine.createSpy('reify').and.returnValue(reifiedCycle);

          triggerDfd = can.Deferred();
          trigger = spyOn(RefreshQueue.prototype, 'trigger')
            .and.returnValue(triggerDfd);
        });

        it('adds reified cycle to the refresh queue', function () {
          let enqueue = spyOn(RefreshQueue.prototype, 'enqueue')
            .and.returnValue({trigger: trigger});
          viewModel.loadCycle();
          expect(enqueue).toHaveBeenCalledWith(reifiedCycle);
        });

        it('triggers the refresh queue', function () {
          viewModel.loadCycle();
          expect(trigger).toHaveBeenCalled();
        });

        it('returns deferred result', function () {
          let result = viewModel.loadCycle();
          expect(can.isDeferred(result)).toBe(true);
        });

        describe('when the refresh queue was resolved', function () {
          it('returns first result of response', function (done) {
            let data = {data: 'Data'};
            triggerDfd.resolve([data]);
            viewModel.loadCycle().then(function (response) {
              expect(response).toBe(data);
              done();
            });
          });

          it('sets cycle to viewModel', function (done) {
            let data = 'cycle';
            triggerDfd.resolve([data]);
            viewModel.loadCycle().then(function () {
              expect(viewModel.attr('cycle')).toEqual(data);
              done();
            });
          });
        });
      });

      it('returns rejected deferred object', function (done) {
        viewModel.loadCycle().fail(done);
      });
    });

    describe('loadWorkflow() method', function () {
      describe('when cycle was loaded successfully', function () {
        let trigger;
        let triggerDfd;
        let reifiedObject;
        let cycle;

        beforeEach(function () {
          cycle = new can.Map({
            workflow: {},
          });
          reifiedObject = {};
          cycle.attr('workflow').reify = jasmine.createSpy('reify')
            .and.returnValue(reifiedObject);

          triggerDfd = can.Deferred();
          trigger = spyOn(RefreshQueue.prototype, 'trigger')
            .and.returnValue(triggerDfd);
        });

        describe('before workflow loading', function () {
          let enqueue;

          beforeEach(function () {
            enqueue = spyOn(RefreshQueue.prototype, 'enqueue')
              .and.returnValue({trigger: trigger});
            triggerDfd.resolve();
          });

          it('pushes a workflow to refresh queue', function (done) {
            viewModel.loadWorkflow(cycle)
              .then(function () {
                expect(enqueue).toHaveBeenCalledWith(reifiedObject);
                done();
              });
          });

          it('triggers refresh queue', function (done) {
            viewModel.loadWorkflow(cycle)
              .then(function () {
                expect(trigger).toHaveBeenCalled();
                done();
              });
          });
        });

        describe('after workflow loading', function () {
          it('sets first value of loaded data to workflow field',
          function (done) {
            let data = {data: 'Data'};
            triggerDfd.resolve([data]);
            viewModel.loadWorkflow(cycle)
              .then(function () {
                expect(viewModel.attr('workflow').serialize()).toEqual(data);
                done();
              });
          });
        });
      });
    });

    describe('onStateChange() method', function () {
      let refreshDfd;
      let event;

      beforeEach(function () {
        event = {};
        refreshDfd = can.Deferred();
        viewModel.attr('instance', {
          refresh: jasmine.createSpy('refresh').and.returnValue(refreshDfd),
        });
      });

      it('refreshes instance', function () {
        viewModel.onStateChange(event);
        expect(viewModel.attr('instance').refresh).toHaveBeenCalled();
      });

      describe('when refresh operation was resolved', function () {
        let refreshed;

        beforeEach(function () {
          refreshed = new can.Map({
            save: jasmine.createSpy('save'),
          });
          refreshDfd.resolve(refreshed);
        });

        it('sets status for refreshed instance', function (done) {
          event.state = 'state';
          viewModel.onStateChange(event);
          refreshDfd.then(function () {
            expect(refreshed.attr('status')).toBe(event.state);
            done();
          });
        });

        it('saves refreshed instance', function (done) {
          viewModel.onStateChange(event);
          refreshDfd.then(function () {
            expect(refreshed.save).toHaveBeenCalled();
            done();
          });
        });
      });
    });

    describe('showLink() method', function () {
      let pageInstance;

      beforeEach(function () {
        pageInstance = spyOn(GGRC, 'page_instance');
      });

      describe('returns true', function () {
        it('if the workflow is not a page instance', function () {
          let pageInstanceObj = {
            type: 'Type',
          };
          pageInstance.and.returnValue(pageInstanceObj);
          expect(viewModel.showLink()).toBe(true);
        });
      });

      describe('returns false', function () {
        it('if the workflow is a page instance', function () {
          let pageInstanceObj = {
            type: 'Workflow',
          };
          pageInstance.and.returnValue(pageInstanceObj);
          expect(viewModel.showLink()).toBe(false);
        });
      });
    });
  });
});