import React, { Component } from 'react'

import * as S from './imagesearchresult.module.css';

import {round} from '../../helpers';

class ImageSearchResult extends Component {

  render () {
    const {instance, classified } = this.props;
    return (
      <div className={S.root}>
        <div className={S.imageWrapper}>
          <img src={instance.image} alt=""/>
        </div>
        <div className={S.classification}>
          {classified.map((item, i)=> {
            return(
              <div 
                key={i} 
                className={S.classificationItem}>
                {item[0]} 
                <span className={S.classificationItemPercentage}> {round(item[1])}%</span>
              </div>
            )
          })}
        </div>
      </div>
    )
  }
}

export default ImageSearchResult