import React, { Component } from 'react';
import classNames from 'classnames';

import {connect} from 'react-redux';

import {isEmpty} from '../../helpers';
import {savedObjectsActions} from '../../actions/savedObjects.actions';
import Wrapper from '../../components/Wrapper';
import { SearchBar } from '../../components/SearchBar';
import { NestedFilters} from '../../components/NestedFilters';
import { ObjectContainer } from '../../components/ObjectContainer';
import { Map } from '../../components/Map';
import { ObjectDetail } from '../../components/ObjectDetail';
import ActiveFacets from '../../components/ActiveFacets';
import { MultipleSimilarImages } from '../../components/MultipleSimilarImages';
import ImageSearchResult from '../../components/ImageSearchResult';
import UserRequestInfo from '../../components/UserRequestInfo';


import * as S from './result.module.css';

import dataSvc from '../../api';

class Result extends Component {

  constructor(props) {
    super(props);
    this.state = {
      query: '',
      toggleLeftSidebar: false,
      toggleRightSidebar: false,
      facets: [],
      results: [],
      count: '',
      filterFacets: {},
      paging: {},
      page: '',
      object: {},
      viewOption: 2,
      mobileFiltersOpen: false,
      similarImages: [],
      lang: 'en',
      savedObjects: {},
      objectListForAI: [],
      classified: [],
      instance: {},
      imageSearch: false,
      searchImgId: '',
      userInfo: {},
      cleanFacets: {}
    }
  }

  componentDidMount = () => {
    const {match, location, dispatch} = this.props;
    dataSvc.apiUsage()
      .then(res=> {
        this.setState({
          userInfo: res.data
        })
      })
    dataSvc.getFacets()
        .then(res => {
          let facets = res.data.facets;

          Object.entries(facets)
            .forEach(item => {
            let fName = item[0].replace(/_filter_/, '');
                if(item[1][fName]) {
                  item[1][fName].buckets.map(bucket => {
                    return bucket.doc_count = 0;
                  })
                }
          })
        this.setState({
          facets:  res.data.facets,
          cleanFacets: facets
        })
      })
    let storedSession = sessionStorage.getItem('searchType');
    let storedFacetSession = sessionStorage.getItem('facets');
    let storedSearchQuery = sessionStorage.getItem('searchQuery');
    let storedmultipleImageSearch = sessionStorage.getItem('multipleImageSearch');
    if(storedmultipleImageSearch) {
      this.setState({objectListForAI: JSON.parse(storedmultipleImageSearch)})
    }
    if(storedSession === 'image' && !location.data && !match.params.id) {
        this.setState({
          searchImgId: sessionStorage.getItem('imageId')
        }, () => this.handleImageSearch())
    } else if (storedSearchQuery && !storedFacetSession && !match.params.id) {
      this.setState({
        query: storedSearchQuery
      }, () => this.handleSearch());
    } else if (storedSearchQuery && storedFacetSession && !match.params.id) {
        this.setState({
          query: storedSearchQuery,
          filterFacets: JSON.parse(storedFacetSession)
        }, () => this.handleSearch());
    } else if(location.data && !match.params.id ) {
      if(location.data.imageId) {
        this.setState({
          imageSearch: true,
          searchImgId: location.data.imageId
        }, () => this.handleImageSearch(location.data.imageId));
      } else if (location.data.query) {
        this.setState({
          query: location.data.query,
          filterFacets: location.data.facets
        }, () => this.handleSearch()) ;
      } else {
        this.setState({
          filterFacets: location.data.facets 
        }, () => this.handleSearch()) ;
      }
     
    } else if (match.params.params) {
      this.setState({
        query: match.params.params
      }, () => this.handleSearch());
    }else if (match.params.id) {
      this.props.history.push('/search/object/'+match.params.id);
      
      dataSvc.getObject(match.params.id)
        .then(obj => {
          this.setState({
            object: obj.data,
          });
        })
      if(!isEmpty(storedFacetSession)) {
        this.setState({
          filterFacets: JSON.parse(storedFacetSession)
        }, () => this.handleSearch())
      }
      
    } else {
      if(!isEmpty(storedFacetSession)) {
        this.setState({
          filterFacets: JSON.parse(storedFacetSession)
        }, () => this.handleSearch())
      } else {
        this.handleSearch();
      }
    }
    const {user} = this.props;
    if(user.account_settings) {
      this.setState({lang: user.account_settings.language})
    }

    dataSvc.getUserCollectionList()
      .then(res=> {
        this.setState({
          savedObjects: res.data.results
        })
      })
      dispatch(savedObjectsActions.getAll());

  }

  componentWillReceiveProps(nextProps) {
    if(nextProps.match.params.id && this.state.object.id) {
      if(nextProps.match.params.id !== this.state.object.id) {
        dataSvc.getObject(nextProps.match.params.id)
          .then(obj => {
            this.setState({
              object: obj.data,
            });
          })
      }
    }
    if(!nextProps.match.params.id && this.state.object.id ) {
      this.setState({objectId: '', object: {}});
      this.props.history.push('/search/result/');
    }
  }

  handleNewSearch = (query) => {
    this.setState({
      query: query,
      filterFacets: '', 
      objectId: '', 
      object: {},
      imageSearch: false,
      searchImgId: '',
      objectListForAI: []
    }, () => this.handleSearch(true));
  }

  handleObjectDetail = (object) => {
    this.setState({object});
    this.props.history.push('/search/object/'+object.id);
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
    sessionStorage.setItem('facets', JSON.stringify(filterFacets));
    this.setState({
        filterFacets: filterFacets, 
        page: 1, 
        objectId: '',
        object: {},
        mobileFiltersOpen: false}, ()=> {
          if(sessionStorage.getItem('searchType') === 'image') {
            this.handleImageSearch();
          } else {
            this.handleSearch();
          }
        })
        this.resetObjectListAI()
  }

  handlePaging = (page) => {
    const {imageSearch} = this.state;
    if(imageSearch) {
      this.setState({page}, () => this.handleImageSearch());
    } else {
      this.setState({page}, () => this.handleSearch());
    }
  }

  handleImageSearch = () => {
    const {searchImgId, page, filterFacets} = this.state;
    sessionStorage.setItem('searchType', 'image');
    sessionStorage.setItem('imageId', searchImgId);
    dataSvc.getImageResultCollectionWithFacets(searchImgId, filterFacets, page)
    .then(res => {
      this.setState({
        results: res.data.results,
        count: res.data.count,
        facets: res.data.facets,
        classified: res.data.classified,
        instance: res.data.instance,
        paging: {
          next: res.data.next,
          previous: res.data.previous,
          count: res.data.count,
          current: res.data.current_page,
          pageSize: res.data.page_size,
        }
      })
    })
  }

  handleFacets = (newFacets) => {
    const {cleanFacets} = this.state;
    const facetArr = JSON.parse(JSON.stringify(cleanFacets))

    if(!isEmpty(newFacets) && !isEmpty(facetArr)) {
      Object.entries(newFacets)
        .forEach(item => {
          let fName = item[0].replace(/_filter_/, '');
            if(item[1][fName]) {
              item[1][fName].buckets.map(bucket => {
                if(facetArr[item[0]][fName]) {
                  let findIn = facetArr[item[0]][fName].buckets.findIndex(x => x.key === bucket.key);
                  facetArr[item[0]][fName].buckets[findIn].doc_count = bucket.doc_count ;
                }
              })
              }
        })
        this.setState({
          facets: facetArr
        });
    }
  }

  


  handleSearch = (fresh) => {
    const {query, filterFacets, page} = this.state;
    sessionStorage.setItem('searchType', 'text');
    sessionStorage.setItem('searchQuery', query);
    sessionStorage.setItem('facets', JSON.stringify(filterFacets));
    let pageNumber;
    if(fresh) {
      pageNumber = 1;
      sessionStorage.removeItem('hasMultipleAIImageSearchedClicked');
      sessionStorage.removeItem('multipleImageSearch');
      this.setState({
        filterFacets: '', 
        objectId: '', 
        object: {},
        imageSearch: false,
        searchImgId: '',
        objectListForAI: []
        
      }, () => {
        dataSvc.getCollection(query, filterFacets, pageNumber)
        .then(res => {
          
          this.setState({
            query: query,
            results: res.data.results,
            count: res.data.count,
            paging: {
              next: res.data.next,
              previous: res.data.previous,
              count: res.data.count,
              current: res.data.current_page,
              pageSize: res.data.page_size,
            }
          })
           this.handleFacets(res.data.facets)
          window.scrollTo(0, 0);
        })
      });
      
    } else {    
      pageNumber = page;
      dataSvc.getCollection(query, filterFacets, pageNumber)
        .then(res => {
          this.setState({
            query: query,
            results: res.data.results,
            count: res.data.count,
            paging: {
              next: res.data.next,
              previous: res.data.previous,
              count: res.data.count,
              current: res.data.current_page,
              pageSize: res.data.page_size,
            }
          })
          this.handleFacets(res.data.facets)
          window.scrollTo(0, 0);
        })
    }
  }


  handleViewOption = (option) => {
    this.setState({viewOption: option});
  }


  renderObjectDetail = () => {
    const {results, object} = this.state;
    let objectChoice;
    if(results.legnth > 0 && !isEmpty(object)) {
      objectChoice = results.filter(res=> res.id === object.id)[0];
    } else {
      objectChoice = object
    }
   if(objectChoice) {
      return ;
    }
  }
  
  handleToggle = (option) => {
    switch(option) {
      case 'left':
        this.setState({toggleLeftSidebar: !this.state.toggleLeftSidebar})
      break;
      case 'right':
        this.setState({toggleRightSidebar: !this.state.toggleRightSidebar})
      break;
      default:
      break;
    }
  }

  removeFacet = (name, raw) => {
    this.filterHandler(name, raw);
  }

  clearFacets = () => {
    const {imageSearch} = this.state;
    sessionStorage.removeItem('facets');
    this.resetObjectListAI()    
    if(imageSearch) {
      this.setState({filterFacets: {}}, () => this.handleImageSearch());
    } else {
      this.setState({filterFacets: {}}, () => this.handleSearch());
    }
  }

  handleCustomPage = (e) => {
    const {page} = this.state;
    const nr = e;
    if(!isNaN(nr)) {
      if(page !== nr) {
        this.setState({page: nr}, () => this.handleSearch())
      }
    }
  }

  handleMobileFilters = () => {
    this.setState((prevState)=>({mobileFiltersOpen: !prevState.mobileFiltersOpen}));
  }

  handleObjectListAI = (id) => {
    const {objectListForAI} = this.state;
    if(id) {
      if(objectListForAI.includes(id)) {
        let filteredArray = this.state.objectListForAI.filter(item => item !== id)
        this.setState({objectListForAI: filteredArray}, ()=> sessionStorage.setItem('multipleImageSearch', JSON.stringify(this.state.objectListForAI)));
      } else {
        this.setState({
          objectListForAI: [...this.state.objectListForAI, id]
        }, ()=> sessionStorage.setItem('multipleImageSearch', JSON.stringify(this.state.objectListForAI)))
      }
    }
    sessionStorage.removeItem('hasMultipleAIImageSearchedClicked');
  }

  resetObjectListAI = () => {
    sessionStorage.removeItem('hasMultipleAIImageSearchedClicked');
    sessionStorage.removeItem('multipleImageSearch');
    this.setState({objectListForAI: []})
  }

  goBack = () => {
    this.setState({object: ''}, () => this.props.history.push('/search/result'));
  }


  render () {
    const {
      query,
      toggleLeftSidebar,
      toggleRightSidebar,
      facets,
      results,
      count,
      paging,
      objectId,
      viewOption,
      filterFacets,
      mobileFiltersOpen,
      object,
      lang,
      savedObjects,
      objectListForAI,
      searchImgId,
      classified,
      instance,
      userInfo
    } = this.state;
     return (
      <Wrapper lang={lang}>
        <div className="row">
          <div className="col-12">
            <SearchBar 
              handleNewSearch={this.handleNewSearch} 
              query={query} />
          </div>
        </div>
        <span className={classNames(S.mobileFilterTrigger, 'hide-sm-up')} onClick={this.handleMobileFilters}>Open Filters</span>
        <div className="row">
          <UserRequestInfo 
            userInfo={userInfo} 
            lang={lang} />

          <div className={classNames({'col-0 col-md-3 col-xl-2': !toggleLeftSidebar })}>
            {searchImgId &&
              <ImageSearchResult 
                instance={instance} 
                classified={classified} />}
            
              <NestedFilters 
                toggleSidebar={this.handleToggle}
                facets={facets}
                filterFacets={filterFacets}
                clearFacets={this.clearFacets}
                filterHandler={this.filterHandler}
                mobileFiltersOpen={mobileFiltersOpen}
                handleMobileFilters={this.handleMobileFilters}
                />
          </div>
          <div className="col-12 col-md">
            {!isEmpty(filterFacets) && <ActiveFacets 
                                              lang={lang}
                                              removeFacet={this.removeFacet}
                                              facets={filterFacets}
                                              clearFacets={this.clearFacets} />}
            {!isEmpty(object) ? (
              <ObjectDetail 
                key={object.id}
                objectId={objectId}
                goBack={this.goBack} 
                object={object} 
                objects={results}
                handleObjectDetail={this.handleObjectDetail}
                savedObjects={savedObjects}
                handleObjectSave={this.handleObjectSave}
                handleObjectRemove={this.handleObjectRemove} />
            ) : (
              <ObjectContainer
                objects={results}
                paging={paging}
                query={query} 
                count={count}
                handlePaging={this.handlePaging}
                handleObjectDetail={this.handleObjectDetail}
                handleViewOption={this.handleViewOption}
                viewOption={viewOption}
                handleCustomPage={this.handleCustomPage}
                handleObjectListAI={this.handleObjectListAI}
                similarImages={objectListForAI}
              />
            )}
          </div>
          {
            isEmpty(object) ? (
              <div className={classNames({'col-12 col-xl-3 col-md-9 offset-md-3 offset-xl-0': !toggleRightSidebar })}>
              <Map
                objects={results}
                handleObjectDetail={this.handleObjectDetail}
                />
                <MultipleSimilarImages 
                  handleObjectDetail={this.handleObjectDetail}
                  similarImages={objectListForAI}
                  resetObjectListAI={this.resetObjectListAI}
                  lang={lang} />
            </div>
            ): null
          }
        </div>
      </Wrapper>
    )
  }
}

const mapStateToProps = (state, ownProps) => {
  const { authentication: {user} } = state;
  return {
      user
  };
}

const connectedResult = connect(mapStateToProps)(Result);
export {connectedResult as Result};
