import React, { Component, Fragment } from 'react';
import classNames from 'classnames';
import {withRouter} from 'react-router-dom';

import { alertActions } from '../../actions/alert.actions';

import {connect} from 'react-redux';

import NestedFilter from '../NestedFilter';

import translations from '../../shared/translations';

import { Filter } from '../Filter';

import * as S from './search.module.css';

import dataSvc from '../../api';

class Search extends Component {

  constructor(props) {
    super(props);
    this.state = {
      query: '',
      option: "1",
      advancedIsOpen: false,
      isLoading: false,
      facets: [],
      filterFacets: {},
      lang: 'en',
      file: null,
      imageIsUploading: false
    }
  }

  componentDidMount = () => {
    const {user} = this.props;
    dataSvc.getFacets().then(res => {
      this.setState({facets: res.data.facets});
    })
    if(user.account_settings) {
      this.setState({lang: user.account_settings.language})
    }
  }

  handleChange = (e) => {
    let {value} = e.target;
    this.setState({query: value})
  }

  handleSearchSubmit = (e) => {
    e.preventDefault();
    const {query} = this.state;
    this.props.history.push({
      pathname: `/search/result/`,
      data: { 
        query: query,
        facets: this.state.filterFacets 
      }
    })
  }

  handleImageSearch = (e) => {
    const {dispatch} = this.props;
    e.preventDefault();
    const {file} = this.state;
    if(file) {
      this.setState({imageIsUploading: true})
      let reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => {
        dataSvc.imageUpload(reader.result)
         .then(
          res=> {
            this.props.history.push({
              pathname: `/search/result/`,
              data: { imageId: res.data.id }
            })
          },
          error => {
            dispatch(alertActions.error(error.response.data));
            this.setState({imageIsUploading: false})
          });
      }
    }
  }

  handleSearchOption = (e) => {
    this.setState({option: e.target.value});
  }

  handleAdvancedToggle = (e) => {
    this.setState(prevState => ({advancedIsOpen: !prevState.advancedIsOpen }))
  }

  handleFile = (e) => {
    this.setState({file:e.target.files[0]})
  }
 
  renderSearchOption = () => {
    const {option, lang, imageIsUploading} = this.state;
    let el;
    switch(option) {
      case "1":
        el = <InputOption 
                ref={this.inputref}
                type="text" 
                className={S.input}
                placeHolder={translations(lang).searchOptions['placeholder']}
                name="textsearch"
                onChange={this.handleChange} />
      break;
      case "2":
        el = <span className={S.fileUpload}>
              <input 
                disabled={imageIsUploading}
                type="file" 
                accept='image/*'
                onChange={this.handleFile} />
            </span>
      break;
      default:
        el = <InputOption 
                type="text" 
                className={S.input}
                placeHolder={translations(lang).searchOptions['placeholder']}
                name="textsearch"
                onChange={this.handleChange} />
      break;
    }
    return (
      el
    )
  }

  filterHandler = (name, raw, element) => {

    let filterFacets = Object.assign({}, this.state.filterFacets);

    if(filterFacets.hasOwnProperty(raw)) {
      if(filterFacets[raw].includes(name)) {
        let i = filterFacets[raw].indexOf(name);
        if(i !== -1) {
          filterFacets[raw].splice(i, 1);
        }
        if(filterFacets[raw].length === 0) {
          delete filterFacets[raw];
        }
      } else {
        filterFacets[raw].push(name);
      }
      
    } else {
      filterFacets[raw] = [name];
    }
    this.setState({filterFacets: filterFacets});

  }

  renderFacets = () => {
    const {facets, filterFacets, lang} = this.state;
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
      '_filter_period_en',
      '_filter_period_nl',
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
                filterHandler={this.filterHandler}
                filterFacets={filterFacets}
                raw_title={fName}
                theme='dashboard'
                options={facet[1][(facet[0] === 'period_1_ens' ? 'period_1_en' : 'period_1_nl_name')]}
                />
            )
          } else {
            return (
              <Filter
                key={fName}
                title={translations(lang).facets[fName]}
                raw_title={fName}
                filterFacets={filterFacets}
                filterHandler={this.filterHandler}
                count={facet[1][fName].buckets.length}
                options={facet[1][fName].buckets}
                theme='dashboard'
                closeOverlay={false}
                openModal={true}
              />
            );
          }
        })
    return facetOptions;
  }

  render() {
    const {
      advancedIsOpen, 
      facets, 
      lang, 
      option, 
      imageIsUploading, 
      file
    } = this.state;
    const {userInfo} = this.props;
    return (
      <Fragment>
        <div className={S.root}> 
          <div className={classNames(S.wrapper, {[S.disabled]: userInfo.num_requests_left === 0 && userInfo.scope === 'authenticated_user'})}>
          {
            imageIsUploading && 
              <div className={S.uploadNotice}>{translations(lang)['uploadNotice']}</div>
          }
          <form name="search" onSubmit={option === "1" ? this.handleSearchSubmit : this.handleImageSearch}>
            <div className={classNames(S.inputWrapper, {[S.hasAdvanced]: advancedIsOpen} )}>
              <div className={classNames( 'input-group', S.group)}>
                <select className={S.dropdown} onChange={this.handleSearchOption} disabled={imageIsUploading}>
                  <option value="1">{translations(lang).searchOptions['text']}</option>
                  <option value="2">{translations(lang).searchOptions['image']} (beta)</option>
                </select>
              {facets && this.renderSearchOption()}
              {option === "1" ? (
                <button type="submit" className={S.submit}></button>
              ): (
                <button 
                  type="submit" 
                  disabled={imageIsUploading || !file} 
                  className={classNames(S.submit, S.uploadSubmit, {['button-loader']: imageIsUploading})}>
                </button>
              )}
              </div>
            </div>
            {option === "1" && (
              <Fragment>
                <span 
                className={classNames(S.advancedHandle, {[S.open]: advancedIsOpen} )} 
                onClick={this.handleAdvancedToggle}>
                  {translations(lang)['advancedSearch']}
                </span>
              
                <div className={classNames(S.advanced, {[S.show]: advancedIsOpen})}>
                  <div className="row">
                    {this.renderFacets()}
                  </div>
                </div>
              </Fragment>
              )}  
            </form>
          </div>
        </div>
        <div className={S.searchInfoContainer}>
            <div className={S.searchInfoWrapper}>
              {translations(lang)['homeInfoText']}
            </div>
        </div>
      </Fragment>
    );
  }
}

const mapStateToProps = (state, ownProps) => {
  const { authentication: {user} } = state;
  return {
      user
  };
}

const connectedSearch = withRouter(connect(mapStateToProps)(Search));
export {connectedSearch as Search};


const InputOption = (props) => {
  return (
    <input 
      autoComplete="off"
      type={props.type} 
      name={props.name} 
      className={props.classname}
      placeholder={props.placeHolder}
      onChange={props.onChange}/>
  )
}