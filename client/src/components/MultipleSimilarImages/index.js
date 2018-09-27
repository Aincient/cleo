import React, { Component } from 'react'
import {connect} from 'react-redux';

import translations from '../../shared/translations';
import constants from '../../shared/constants';

import dataSvc from '../../api';

import * as S from './multiplesimilarimages.module.css';

class MultipleSimilarImages extends Component {
  constructor (props) {
    super(props)
    this.state = {
      searched: false,
      results: {},
      isLoading: false
    }
  }

  componentDidMount = () => {
    if(sessionStorage.getItem('hasMultipleAIImageSearchedClicked')) {
      this.handleMultipleImageSearch()
    }
  }


  componentWillReceiveProps(nextProps) {
    if (nextProps.similarImages !== this.state.similarImages) {
      this.setState({
        searched: false,
        results: {},
        isLoading: false
      })
    }
  }

  handleMultipleImageSearch = () => {
    const {similarImages} = this.props;
    this.setState({isLoading: true})
    sessionStorage.setItem('multipleImageSearch', JSON.stringify(similarImages));
    dataSvc.searchCollectionAI(similarImages)
      .then(res=> {
        sessionStorage.setItem('hasMultipleAIImageSearchedClicked',  true);
        this.setState({
          searched: true,
          isLoading: false,
          results: res.data.results
        })
      })
  }

  handleReset = () => {
    const {resetObjectListAI} = this.props;
    sessionStorage.removeItem('multipleImageSearch');
    sessionStorage.removeItem('hasMultipleAIImageSearchedClicked');
    resetObjectListAI();
    this.setState({
      searched: false,
      results: {},
      isLoading: false
    })
  }

  gotoObject = (object) => {
    this.props.handleObjectDetail(object);
  }
  
  render () {
    const {similarImages, lang} = this.props;
    const {searched, results, isLoading} = this.state;
    return (
      <div className={S.root}>
        <div className={S.wrapper}>
          {searched ? (
            <div className={S.imageWrapper}>
              <div className={S.startImageSearch}>
                <h4>AI search</h4>
                <button
                  className="button" 
                  onClick={()=> this.handleReset()}>
                    Reset
                </button>
              </div>
               
                {results && results.map((object, i)=> {
                  return(
                    <div 
                      key={i}
                      onClick={() => this.gotoObject(object)}
                      className={S.image}
                      style={{backgroundImage: "url(" + constants.api.url + object.images_urls[0].lr + ")"}}>
                    </div>
                  )
                })}
            </div>
          ) : (
            <div> 
            {
              similarImages.length > 1 ? (
                isLoading ? (
                  <span className="loader loader-dark"></span>
                ) : (
                  <div className={S.startImageSearch}>
                    <h4>AI search</h4>
                    <div className={S.selectedImageCountWrapper}>
                      <div className={S.selectedImageCount}>
                        {similarImages.length}
                      </div>
                      <span>{translations(lang)['objects']}</span>
                    </div>
                    <a 
                      onClick={()=> this.handleMultipleImageSearch()} 
                      className="button">
                        {translations(lang)['selectMultipleImagesButton']} 
                    </a>
                    <div 
                      onClick={()=> this.handleReset()} 
                      className={S.clearObjects}>
                      {translations(lang)['clearSelectedObjects']}
                    </div>
                  </div>
                )
              ) : (
                <div  className={S.startImageSearch}>
                  <h4>AI search</h4>
                  {translations(lang)['selectMultipleImages']}
                </div>
              )
            }
          </div>
          )}
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
const connectedMultipleSimilarImages = connect(mapStateToProps)(MultipleSimilarImages);
export {connectedMultipleSimilarImages as MultipleSimilarImages};