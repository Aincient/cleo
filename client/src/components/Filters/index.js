import React, { Component } from 'react'
import {connect} from 'react-redux';
import classNames from 'classnames';

import translations from '../../shared/translations';

import {isEmpty} from '../../helpers';

import * as S from './filters.module.css';

import { Filter } from '../Filter';

class Filters extends Component {

  constructor (props) {
    super(props)
    this.state = {
      lang: ''
    }
  }

  componentDidMount = () => {
    const {user} = this.props;
    if(user.account_settings) {
      this.setState({lang: user.account_settings.language})
    }   
  }  

  renderFacets = () => {
    const {facets, filterHandler, filterFacets} = this.props;
    const {lang} = this.state;
    const ordering = {};
    const sortOrder = ['_filter_importer_uid', '_filter_period_nl', '_filter_country_nl', '_filter_city_nl'];
    for (var i=0; i<sortOrder.length; i++)
    ordering[sortOrder[i]] = i;

    const filterNames = [
        '_filter_object_date_begin', 
        '_filter_object_date_end', 
        '_filter_language_code_orig',
        '_filter_classified_as',
        '_filter_classified_as_1',
        '_filter_classified_as_2',
        '_filter_classified_as_3',
        '_filter_primary_object_type_nl',
        '_filter_primary_object_type_en'
      ]
    const facetOptions = Object
        .entries(facets)
        .filter(name => !filterNames.includes(name[0]))
        .sort(((a, b) => (ordering[a.type] - ordering[b.type]) || a.name.localeCompare(b.name)))
        .map((facet, index) => {
          let fName = facet[0].replace(/_filter_/, '');
            return (
              <Filter
                key={fName}
                title={translations(lang).facets[fName]}
                raw_title={fName}
                filterHandler={filterHandler}
                count={facet[1][fName].buckets.length}
                options={facet[1][fName].buckets}
                filterFacets={filterFacets}
                closeOverlay={true}
                showCount={true}
              />
          );
        })
    return facetOptions;
  }

  render () {
    const {mobileFiltersOpen, handleMobileFilters} = this.props;
    return (
      <div className={classNames(S.root, {[S.open]: mobileFiltersOpen})}>
        <span className={S.closeMobileFilters} onClick={() => handleMobileFilters()}></span>
        <div className={S.wrapper}>
          {this.renderFacets()}
        </div>
      </div>
    )
  }
}

const mapStateToProps = (state, ownProps) => {
  const { authentication: {user} } = state;
  return {
      user
  };
}

const connectedFilters = connect(mapStateToProps)(Filters);
export {connectedFilters as Filters};