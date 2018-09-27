import React, { Component, Fragment } from 'react'

import classNames from 'classnames';
import {isEmpty} from '../../helpers';
import translations from '../../shared/translations';

import NestedFacetOverlay from '../NestedFacetOverlay';

import * as S from './nestedfilter.module.css';

class NestedFilter extends Component {
  
  constructor(props) {
    super(props);
    this.state = {
      isOpen: false,
      overlayIsOpen: false,
      lang: 'en'
    }
  }

  handleToggle = () => {
    this.setState((prevState)=>({isOpen: !prevState.isOpen}));
  }

  handleOverlay = () => {
    this.setState((prevState)=>({overlayIsOpen: !prevState.overlayIsOpen}));
  }

  isChecked = (raw, name) => {
    const {filterFacets} = this.props;
    if(!isEmpty(filterFacets)) {
      if(filterFacets.hasOwnProperty(raw)) {
        if(filterFacets[raw].includes(name)){
          return true;
        }
      }
      return false;
    }
  }
  countChosenFacets = (raw) => {
    const {filterFacets} = this.props;
    if(!isEmpty(filterFacets)) {
      if(filterFacets.hasOwnProperty(raw)) {
        return filterFacets[raw].length;
      }
      return false;
    }
  }

  handleFilterSelectCloseOverlay = (name, raw) => {
    const {filterHandler, closeOverlay} = this.props;
    if(closeOverlay) {
      this.setState({overlayIsOpen: false});
    }
    filterHandler(name, raw);    
  }

  render () {
    const {
      title, 
      raw_title,
      count, 
      options, 
      lang,
      filterHandler,
      theme
    } = this.props;
    const {
      isOpen,
      overlayIsOpen
    } = this.state;

    return (
      <Fragment>
        <div className={classNames(S.root, {[S.dashboard]: theme === 'dashboard', 'col-12 col-md-6': theme === 'dashboard'})}>
          <div className={classNames(S.title)} onClick={this.handleOverlay}>
            <span className={S.filterTitle}>{translations(lang).facets[title]}</span>
            <span className={S.count}> ({count})</span>
            <span 
              className={S.handle}>{isOpen ? '-' : '+'}</span>
          </div>
        
        </div>
        {overlayIsOpen && <NestedFacetOverlay
                  options={options} 
                  title={translations(lang).facets[title]}
                  raw_title={raw_title}
                  handleOverlay={this.handleOverlay}
                  filterHandler={filterHandler}  
                  showCount={count}
                  isChecked={this.isChecked}
                  lang={lang}  />}
      </Fragment>
    )
  }
}

export default NestedFilter