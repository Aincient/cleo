import React from 'react';

import * as S from './activefacets.module.css';
import translations from '../../shared/translations';

import reactStringReplace from 'react-string-replace';

const ActiveFacets = (props) => {
 
  let translatedName = (facet, name) => {
    let tempName;
    if(facet === "importer_uid") {
      tempName = translations(props.lang).collections[name];
    } else if (name === "_") {
      tempName = (props.lang === 'en'? 'Unknown': 'Onbekend');
    } else {
      tempName =  reactStringReplace(name, /\d\d\d\d\_/ , (match) => match);
    }
   return tempName;
  }
  
  return (
    <div className={S.root}>
      { 
        Object
          .keys(props.facets)
          .map(facet => {
            return(
              props.facets[facet].map((name, index) => 
                  <span key={index} className={S.facet}>
                    {translatedName(facet, name)}
                    <span 
                      onClick={()=> props.removeFacet(name, facet)}
                      className={S.remove}>
                      X
                    </span>
                  </span>
                )
            )
          })
      }
      <span 
        onClick={()=> props.clearFacets()}
        className={S.clearFacets}>
        {translations(props.lang)['clearFilters']}
      </span>
    </div>
  )
}

export default ActiveFacets;