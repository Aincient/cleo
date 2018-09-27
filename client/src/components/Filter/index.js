import React, { Component, Fragment } from 'react'
import classNames from 'classnames';
import {connect} from 'react-redux';

import {isEmpty} from '../../helpers';

import translations from '../../shared/translations';

import { FacetOption } from '../../components/FacetOption';
import FacetOverlay from '../../components/FacetOverlay';

import * as S from './filter.module.css';

class Filter extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isOpen: false,
      overlayIsOpen: false,
      lang: 'en'
    }
  }

  componentDidMount = () => {
    const {user} = this.props;
    if(user.account_settings) {
      this.setState({lang: user.account_settings.language})
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
      count, 
      options, 
      raw_title, 
      filterHandler,
      theme,
      showCount,
      openModal
    } = this.props;
    let itemsToShow = openModal ? 0 : 10;
    const {
      isOpen,
      overlayIsOpen,
      lang
    } = this.state;
    let moreHandle;
    if(options.length > itemsToShow) {
      moreHandle = <div className={S.handleOverlay} onClick={this.handleOverlay}>{translations(lang)['more']}</div>;
    }
    
    return (
      <Fragment>
        <div className={classNames(S.root, {[S.dashboard]: theme === 'dashboard', 'col-12 col-md-6': theme === 'dashboard'})}>
          <div className={classNames(S.title)} onClick={openModal ? this.handleOverlay : this.handleToggle}>
            <span className={S.filterTitle}>{title}</span>
            <span className={S.count}> ({count})</span>
            {this.countChosenFacets(raw_title) && theme === 'dashboard' ? <span className={S.selected}>{this.countChosenFacets(raw_title)} selected</span> : '' }
            <span 
              onClick={this.toggle}
              className={S.handle}>{isOpen ? '-' : '+'}</span>
          </div>
          <div className={classNames(S.options, {[S.open]: isOpen})}>
            {options.slice(0,itemsToShow).map((bucket, index)=> {
              return(
                <FacetOption 
                  key={bucket.key} 
                  filterHandler={filterHandler} 
                  raw={raw_title} 
                  name={bucket.key}
                  count={showCount ? bucket.doc_count : ''}
                  checked={this.isChecked(raw_title, bucket.key)} />
              )
            })}
            {moreHandle}
          </div>
        </div>
        {overlayIsOpen && <FacetOverlay
                  options={options} 
                  title={title}
                  raw_title={raw_title}
                  handleOverlay={this.handleOverlay}
                  filterHandler={this.handleFilterSelectCloseOverlay}  
                  showCount={showCount}
                  isChecked={this.isChecked}
                  lang={lang}  />}
      </Fragment>
    )
  }
}

const mapStateToProps = (state, ownProps) => {
  const { authentication: {user} } = state;
  return {
      user
  };
}

const connectedFilter = connect(mapStateToProps)(Filter);
export {connectedFilter as Filter};