import React from 'react';

import * as S from './facetoverlay.module.css';
import translations from '../../shared/translations';

import { FacetOption } from '../../components/FacetOption';

const FacetOverlay = (props) => {
  return(
    <div className={S.overlayWrapper}>
      <div className={S.overlay}>
          <div className={S.overlayHeader}>
            {props.title} <span className={S.confirm} onClick={props.handleOverlay}>{translations(props.lang)['confirm']}</span>
            <span className={S.close} onClick={props.handleOverlay}></span>
          </div>
        <div className="row">
          {props.options.map((bucket, index)=> {
            return(
              <div  key={index} className="col-12 col-md-6 col-lg-4 col-xl-3">
                <FacetOption 
                  filterHandler={props.filterHandler} 
                  raw={props.raw_title} 
                  name={bucket.key}
                  count={bucket.doc_count} 
                  checked={props.isChecked(props.raw_title, bucket.key)} />
              </div>
            ) 
          })}
      </div>
      </div>
    </div>
  )
}

export default FacetOverlay;