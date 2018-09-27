  import React, { Component, Fragment } from 'react';

import {connect} from 'react-redux';

import constants from  '../../shared/constants';
import translations from '../../shared/translations';

import Pagination from 'react-js-pagination';

import classNames from 'classnames';

import noImage from '../../images/noimage.png';

import * as S from './objectcontainer.module.css';

class ObjectContainer extends Component {

  constructor(props) {
    super(props);
    this.state = {
      customPageNr: '',
      lang: 'en'
    }
  }

  componentDidMount = () => {
    const {user} = this.props;
    if(user.account_settings) {
      this.setState({lang: user.account_settings.language})
    }
  }

  handleCustomPageNumber = (e) => {
    this.setState({customPageNr: e.target.value});
  }

  isChecked = (id) => {
    const {similarImages} = this.props;
    if(similarImages) {
      if(similarImages.includes(id)){
        return true;
      }
      return false;
    }
  }

  render () {
    const {
      objects,
      paging,
      handlePaging,
      handleViewOption,
      viewOption,
      handleObjectDetail,
      handleCustomPage,
      handleObjectListAI,
      count,
      query
    } = this.props;

    const {lang} = this.state;
    return (
      <div className={S.root}>
        {count} {translations(lang)['results']} {query ? ` ${translations(lang)['for']} ${query}`: ''}

        <ResultOptions 
          paging={paging}
          handlePaging={handlePaging}
          handleViewOption={handleViewOption}
          viewOption={viewOption}
          handleCustomPage={handleCustomPage}
          handleCustomPageNumber={this.handleCustomPageNumber}
          customPageNr={this.state.customPageNr} />

        <div className={classNames(S.wrapper, 'row')}>
          {objects.map(object=> 
            <div 
              key={object.id} 
              className={classNames({ 'col-12 col-md-6 col-lg-4 col-xl-3': viewOption === 2, 'col-12': viewOption === 3, 'col-6 col-md-2': viewOption === 1})}>
                <div className={classNames("input-field", S.selectImageForAI)}>
                  <input 
                    id={object.id} 
                    type="checkbox"  
                    autoComplete="off" 
                    name="image1"
                    checked={this.isChecked(object.id) || ''}
                    onChange={() => handleObjectListAI(object.id)} />
                  <label  htmlFor={object.id}></label>
                </div>
                <div 
                  onClick={()=> handleObjectDetail(object)}
                  className={classNames(S.objectWrapper,S.imageViewer)}>
                  {viewOption === 1 ? (
                    <Fragment>
                      <div className={S.image}>
                        {object.images.length > 0 ? (
                          <img src={constants.api.url + object.images_urls[0].lr} alt=""/>
                        ) : (
                          <img src={noImage} alt="Not available"/>
                        )}
                      </div>
                    </Fragment>
                  ) : viewOption === 2 ? (
                    <Fragment>
                      <div className={S.image}>
                      {object.images.length > 0 ? (
                          <img src={constants.api.url + object.images_urls[0].lr} alt=""/>
                        ) : (
                          <img src={noImage} alt="Not available"/>
                        )}
                      </div>
                      <div className={S.title}>
                        {lang === 'en' ? object.title_en && object.title_en.map(title=> `${title}; `) : object.title_nl && object.title_nl.map(title=> `${title}; `)}
                      </div>
                      <div className={S.type}>
                        {lang === 'en' ? object.primary_object_type_en && object.primary_object_type_en : object.primary_object_type_nl && object.primary_object_type_nl}
                      </div>
                      <div className={S.provenance}>
                        {lang === 'en' ? object.country_en && object.country_en : object.country_nl && object.country_nl}
                      </div>
                      </Fragment>
                  ) : viewOption === 3 ?  (
                    <div className="row">
                      <div className="col-3">
                        <div className={S.image}>
                          {object.images.length > 0 ? (
                            <img src={constants.api.url + object.images_urls[0].lr} alt=""/>
                          ) : (
                            <img src={noImage} alt="Not available"/>
                          )}
                        </div>
                      </div>
                      <div className="col-9">
                        <div className={S.title}>
                          {lang === 'en' ? object.title_en && object.title_en.map(title=> `${title}; `) : object.title_nl && object.title_nl.map(title=> `${title}; `)}
                        </div>
                        <div className={S.type}>
                          {lang === 'en' ? object.primary_object_type_en && object.primary_object_type_en : object.primary_object_type_nl && object.primary_object_type_nl}
                        </div>
                        <div className={S.collection}>
                          {object.importer_uid && translations(lang).collections[object.importer_uid]}
                        </div>
                        <div className={S.provenance}>
                          {lang === 'en' ? (object.period_en.length ===  1 ? object.period_en : object.period_en.map((period, i)=> <div key={i}>{period}</div>)) :  (object.period_nl.length ===  1 ? object.period_nl : object.period_nl.map((period, i)=> <div key={i}>{period}</div>))}
                        </div>
                        <div className={S.provenance}>
                          {lang === 'en' ? object.country_en && object.country_en : object.country_nl && object.country_nl}
                        </div>
                      </div>
                    </div>
                  ) : null}
                </div>
            </div>)
          }
        </div>

        <ResultOptions 
          paging={paging}
          handlePaging={handlePaging}
          handleViewOption={handleViewOption}
          viewOption={viewOption}
          handleCustomPage={handleCustomPage}
          handleCustomPageNumber={this.handleCustomPageNumber}
          customPageNr={this.state.customPageNr} />
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

const connectedObjectContainer = connect(mapStateToProps)(ObjectContainer);
export {connectedObjectContainer as ObjectContainer};


const ResultOptions = (props) => {
  return (
    <div className="row">
      <div className={classNames(S.pagingWrapper, "col-12 col-lg-7")}>
        <Pagination 
          onChange={props.handlePaging}
          activePage={props.paging.current}
          itemsCountPerPage={props.paging.pageSize}
          totalItemsCount={props.paging.count}
          prevPageText='<'
          nextPageText='>'
          pageRangeDisplayed={4}
          innerClass={S.paging}
          activeClass={S.active} />
      </div>
      <div className="col-6 col-lg-2">
        <div className={classNames(S.goto, "input-group")} >
          <input 
            type="number"
            min="1"
            placeholder={props.paging.current} 
            onChange={(e) => props.handleCustomPageNumber(e)}/>
          <button 
            onClick={() => props.handleCustomPage(props.customPageNr)}
            type="button"
            className="button">
            Go
          </button>
        </div>
      </div>
      <div className={classNames(S.viewOption, "col-6 col-lg-3")}>
        <div className="input-group">
        <span 
            onClick={()=>props.handleViewOption(1)}
            className={classNames(S.viewOptionVisual, 'button', {'active': props.viewOption === 1})}></span>
          <span 
            onClick={()=>props.handleViewOption(2)}
            className={classNames(S.viewOptionGrid, 'button', {'active': props.viewOption === 2})}></span>
          <span
            onClick={()=>props.handleViewOption(3)}
            className={classNames(S.viewOptionList, 'button ', {'active': props.viewOption === 3})}></span>
        </div>
      </div>
    </div>
  )
}
