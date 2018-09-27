import React, { Component } from 'react'
import {connect} from 'react-redux';
import classNames from 'classnames';

import translations from '../../shared/translations';

import * as S from './nestedfilters.module.css';

import NestedFilter from '../NestedFilter';

import { Filter } from '../Filter';

class NestedFilters extends Component {

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
    const orderingNL = {};
    const orderingEN = {};
    const sortOrderNL = [
      '_filter_importer_uid',
      '_filter_country_nl',
      '_filter_city_nl',
      '_filter_material_nl',
      'period_1_nls',
      '_filter_object_type_nl'
    ];
  
    const sortOrderEN = [
      '_filter_importer_uid',
      '_filter_material_en',
      '_filter_object_type_en',
      'period_1_ens',
      '_filter_city_en',
      '_filter_country_en',
    ];

    for (var i=0; i<sortOrderNL.length; i++)
    orderingNL[sortOrderNL[i]] = i;
    for (var i=0; i<sortOrderEN.length; i++)
    orderingEN[sortOrderEN[i]] = i;
    const filterNames = [
      '_filter_object_date_begin',
      '_filter_object_date_end',
      '_filter_language_code_orig',
      '_filter_classified_as',
      '_filter_period_nl',
      '_filter_period_en',
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
        .sort(((a, b) => (lang === 'en' ? (orderingEN[a[0]] - orderingEN[b[0]]) || a[0].localeCompare(b[0]) : (orderingNL[a[0]] - orderingNL[b[0]]) || a[0].localeCompare(b[0]))))
        .map((facet, index) => {
          let fName = facet[0].replace(/_filter_/, '');
          if(facet[0] === 'period_1_ens' || facet[0] === 'period_1_nls') { 
            return(
              <NestedFilter
                lang={lang}
                key={fName}
                count={facet[1].doc_count}
                title={fName}
                raw_title={fName}
                filterHandler={filterHandler}
                filterFacets={filterFacets}
                showCount={true}
                options={facet[1][(facet[0] === 'period_1_ens' ? 'period_1_en' : 'period_1_nl_name')]}
                />
            )
           
          } else {
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
          }
         
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

const connectedNestedFilters = connect(mapStateToProps)(NestedFilters);
export {connectedNestedFilters as NestedFilters};