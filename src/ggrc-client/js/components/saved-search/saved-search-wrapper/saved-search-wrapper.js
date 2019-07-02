/*
  Copyright (C) 2019 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import canComponent from 'can-component';
import canMap from 'can-map';
import SavedSearch from '../../../models/service-models/saved-search';
import Pagination from '../../base-objects/pagination';
import {isMyWork} from '../../../plugins/utils/current-page-utils';
import {
  parseFilterJson,
  selectSavedSearchFilter,
} from '../../../plugins/utils/advanced-search-utils';
import * as BusinessModels from '../../../models/business-models';

export default canComponent.extend({
  tag: 'saved-search-wrapper',
  leakScope: true,
  viewModel: canMap.extend({
    define: {
      isGlobalSearch: {
        get() {
          return this.attr('searchType') === 'GlobalSearch';
        },
      },
      isShowSavedSearch: {
        get() {
          if (this.attr('isGlobalSearch')) {
            return true;
          }

          // do NOT show Advanced saved seacrhes on Dashboard tab
          if (isMyWork()) {
            return false;
          }

          return true;
        },
      },
      searchesPaging: {
        value() {
          return new Pagination({
            pageSize: 10, pageSizeSelect: [10],
          });
        },
      },
      isPagingShown: {
        get() {
          const total = this.attr('searchesPaging.total');
          const pageSize = this.attr('searchesPaging.pageSize');

          return total > pageSize;
        },
      },
    },
    objectType: '',
    searches: [],
    searchType: '',
    savedFiltersToApply: null,
    advancedSearch: null,
    isLoading: false,
    applySearch({search}) {
      const advancedSearch = this.attr('advancedSearch');
      if (advancedSearch) {
        selectSavedSearchFilter(advancedSearch, search);
      } else {
        const filter = parseFilterJson(search.filters);
        const model = BusinessModels[search.object_type];
        const savedFiltersToApply = {
          filterItems: filter.filterItems,
          mappingItems: filter.mappingItems,
          statusItem: filter.statusItem,
          savedSearchId: search.id,
        };

        if (model) {
          savedFiltersToApply.modelName = model.model_singular;
          savedFiltersToApply.modelDisplayName = model.title_plural;
        }

        this.attr('savedFiltersToApply', savedFiltersToApply);
      }
    },
    loadSavedSearches() {
      // do NOT set type for global search
      const type = this.attr('isGlobalSearch') ?
        null :
        this.attr('objectType');

      const paging = this.attr('searchesPaging');
      const searchType = this.attr('searchType');

      const needToGoToPrevPage = (
        paging.attr('current') > 1 &&
        this.attr('searches.length') === 1
      );

      if (needToGoToPrevPage) {
        paging.attr('current', paging.attr('current') - 1);
      }

      this.attr('isLoading', true);
      return SavedSearch.findBy(searchType, paging, type)
        .then(({total, values}) => {
          this.attr('searchesPaging.total', total);

          const searches = values.map((value) => new SavedSearch(value));
          this.attr('searches', searches);
        }).always(() => {
          this.attr('isLoading', false);
        });
    },
    savedSearchCreated(ev) {
      this.loadSavedSearches().then(() => {
        this.applySearch(ev);
      });
    },
  }),
  events: {
    '{viewModel.searchesPaging} current'() {
      this.viewModel.loadSavedSearches();
    },
    inserted() {
      if (this.viewModel.attr('isShowSavedSearch')) {
        this.viewModel.loadSavedSearches();
      }
    },
  },
});
