import React, { Component } from 'react'
import classNames from 'classnames';

import translations from '../../shared/translations';

import reactStringReplace from 'react-string-replace';

import * as S from '../FacetOverlay/facetoverlay.module.css';

import * as N from './nestedfacetoverlay.module.css';

class NestedFacetOverlay extends Component {
  constructor(props) {
    super(props);
    this.state = {
      openFacets: []
    }
  }

  handleToggle = (facet) => {
    const {openFacets} = this.state;
    if(facet) {
      if(openFacets.includes(facet)) {
        let filteredArray = this.state.openFacets.filter(item => item !== facet)
        this.setState({openFacets: filteredArray});
      } else {
        this.setState({
          openFacets: [...this.state.openFacets, facet]
        })
      }
    }
  }

  isOpenFacet = (facet) => {
    const {openFacets} = this.state;
    if(openFacets.includes(facet)) {
      return true;
    }
  }


  render () {
    const {
      options,
      title,
      handleOverlay,
      lang,
      filterHandler,
      isChecked
    } = this.props;
    const mappingPeriod = {
      nl: {
        period1: 'period_1_nls',
        period1Sub: 'period_1_nl_name',
        period1Filter: 'period_1_nl',
        period2: 'period_2_nls',
        period2Sub: 'period_2_nl_name',
        period2Filter: 'period_2_nl',
        period3: 'period_3_nls',
        period3Sub: 'period_3_nl_name',
        period3Filter: 'period_3_nl',
        period4: 'period_4_nls',
        period4Sub: 'period_4_nl_name',
        period4Filter: 'period_4_nl'
      },
      en: {
        period1: 'period_1_ens',
        period1Sub: 'period_1_en',
        period1Filter: 'period_1_en',
        period2: 'period_2_ens',
        period2Sub: 'period_2_en',
        period2Filter: 'period_2_en',
        period3: 'period_3_ens',
        period3Sub: 'period_3_en',
        period3Filter: 'period_3_en',
        period4: 'period_4_ens',
        period4Sub: 'period_4_en',
        period4Filter: 'period_4_en'
      }
    }
    return(
      <div className={S.overlayWrapper}>
        <div className={S.overlay}>
          <div className={S.overlayHeader}>
            {title} <span className={S.close} onClick={handleOverlay}>{translations(lang)['confirm']}</span>
          </div>
          <div className="row">
            <div className={classNames(N.options, S.open)}>
              {options.buckets.filter(opt => opt.key !== '_').map((option, i)=> {
                  return(
                    <div key={i}>
                      <div className={N.nestedFacetOverlayTitle}>
                        <input 
                            id={option.key + i}
                            className={S.filterOptionCheckbox}
                            type="checkbox"
                            checked={isChecked([mappingPeriod[lang]['period1Filter']] , option.key ) || ''}
                            name={option.key + i}
                            onChange={()=> {return}}
                          />
                        <label 
                          htmlFor={option.key + i}
                          onClick={(e) => filterHandler(option.key, [mappingPeriod[lang]['period1Filter']] , e)}>
                          {reactStringReplace(option.key, /\d\d\d\d\_/ , (match) =>  <span className={S.filterOptionName}>{match}</span>)}
                        </label>
                        <span className={N.count}>({option.doc_count})</span>
                        {
                          option[mappingPeriod[lang]['period2']][mappingPeriod[lang]['period2Sub']].buckets.filter(opt => opt.key !== '_').length > 0 ? (
                            <span className={N.toggleHandle} onClick={(e) => this.handleToggle(option.key)}>{this.isOpenFacet(option.key) ? '-' : '+'}</span>
                          ): null
                        }
                       
                      </div>
                      <div className={classNames(N.nestedFacet, {[N.facetOpen]: this.isOpenFacet(option.key)} )}>
                        {option[mappingPeriod[lang]['period2']][mappingPeriod[lang]['period2Sub']].buckets.filter(opt => opt.key !== '_').map((period2, i)=> {
                          return(
                            <div key={i}>
                              <div className={classNames(N.nestedFacetOverlayTitle)}>
                                <input 
                                    id={period2.key + i + [mappingPeriod[lang]['period2']]}
                                    className={S.filterOptionCheckbox}
                                    type="checkbox"
                                    checked={isChecked( [mappingPeriod[lang]['period2Filter']] , period2.key) || ''}
                                    name={period2.key + i + [mappingPeriod[lang]['period2']]}
                                    onChange={()=> {return}}
                                  />
                                  <label 
                                    htmlFor={period2.key + i + [mappingPeriod[lang]['period2']]} 
                                    onClick={(e) => filterHandler(period2.key, [mappingPeriod[lang]['period2Filter']] , e)}>
                                    {reactStringReplace(period2.key, /\d\d\d\d\_/ , (match) =>  <span className={S.filterOptionName}>{match}</span>)}
                                  </label>
                                  <span className={N.count}>({period2.doc_count})</span>
                                  {
                                    option[mappingPeriod[lang]['period2']][mappingPeriod[lang]['period2Sub']].buckets.filter(opt => opt.key !== '_').length > 0 ? (
                                      <span className={N.toggleHandle} onClick={(e) => this.handleToggle(period2.key)}>{this.isOpenFacet(period2.key) ? '-' : '+'}</span>
                                    ): null
                                  }
                              </div>
                              <div className={classNames(N.nestedFacet, {[N.facetOpen]: this.isOpenFacet(period2.key)} )}>
                                {period2[mappingPeriod[lang]['period3']][mappingPeriod[lang]['period3Sub']].buckets.filter(opt => opt.key !== '_').map((period3, i)=> {
                                    return(
                                      <div key={i}>
                                        <div className={classNames(N.nestedFacetOverlayTitle)}>
                                          <input 
                                              id={period3.key + i + [mappingPeriod[lang]['period3']]}
                                              className={S.filterOptionCheckbox}
                                              type="checkbox"
                                              checked={isChecked( [mappingPeriod[lang]['period3Filter']] , period3.key ) || ''}
                                              name={period3.key + i + [mappingPeriod[lang]['period3']]}
                                              onChange={()=> {return}}
                                            />
                                            <label 
                                              htmlFor={period3.key + i + [mappingPeriod[lang]['period3']]}
                                              onClick={(e) => filterHandler(period3.key, [mappingPeriod[lang]['period3Filter']] , e)}>
                                              {reactStringReplace(period3.key, /\d\d\d\d\_/ , (match) =>  <span className={S.filterOptionName}>{match}</span>)}
                                            </label>
                                            <span className={N.count}>({period3.doc_count})</span>
                                            {
                                              period3[mappingPeriod[lang]['period4']][mappingPeriod[lang]['period4Sub']].buckets.filter(opt => opt.key !== '_').length > 0 ? (
                                                <span className={N.toggleHandle} onClick={(e) => this.handleToggle(period3.key)}>{this.isOpenFacet(period3.key) ? '-' : '+'}</span>
                                               ): null
                                            }
                                        </div>
                                        <div className={classNames(N.nestedFacet, {[N.facetOpen]: this.isOpenFacet(period3.key)} )}>
                                          {period3[mappingPeriod[lang]['period4']][mappingPeriod[lang]['period4Sub']].buckets.filter(opt => opt.key !== '_').map((period4, i)=> {
                                            if(period4.key !== "_") {
                                              return(
                                                <div key={i}>
                                                  <div className={classNames(N.nestedFacetOverlayTitle, N.open)}>
                                                    <input 
                                                        id={period4.key + [mappingPeriod[lang]['period4']]}
                                                        className={S.filterOptionCheckbox}
                                                        type="checkbox"
                                                        checked={isChecked([mappingPeriod[lang]['period4Filter']] , period4.key ) || ''}
                                                        name={period4.key + [mappingPeriod[lang]['period4']]}
                                                        onChange={()=> {return}}
                                                      />
                                                      <label 
                                                        htmlFor={period4.key + [mappingPeriod[lang]['period4']]} 
                                                        onClick={(e) => filterHandler(period4.key, [mappingPeriod[lang]['period4Filter']] , e)}>
                                                        {reactStringReplace(period4.key, /\d\d\d\d\_/ , (match) =>  <span className={S.filterOptionName}>{match}</span>)}
                                                      </label>
                                                      <span className={N.count}>({period4.doc_count})</span>
                                                  </div>
                                                </div>
                                              )
                                            }
                                          })}
                                        </div>
                                      </div>
                                    )
                                  
                                  
                                })}
                              </div>
                            </div>  
                          ) 
                        })}
                      </div>
                    </div>
                  )
                }
              )}
            </div>
          </div>
        </div>
      </div>
    )
  }
}

export default NestedFacetOverlay