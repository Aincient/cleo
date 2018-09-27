import React from 'react';
import translations from '../../shared/translations';
import * as S from './facetoption.module.css';
import {connect} from 'react-redux';

const FacetOption = (props) => {
  const {raw, checked, user} = props;
  let lang;
  if(user.account_settings) {
    lang = user.account_settings.language;
  }
  let name;
  if(props.raw === "importer_uid") {
    name = translations(lang).collections[props.name];
  } else if (props.name === "_") {
    name = (lang === 'en'? 'Unknown': 'Onbekend');
  } else {
    name = props.name;
  }
  return(
    <div className={S.filterOption}>
      <input 
        id={name}
        className={S.filterOptionCheckbox}
        type="checkbox"
        checked={checked || ''}
        name={raw}
        onChange={()=> {return}}
       />
      <label 
        htmlFor={name} 
        onClick={(e) => props.filterHandler(props.name, raw, e)}>
        <span className={S.filterOptionName}>{name}</span>
      </label>
      <span className={S.filterOptionCount}>{props.count}</span>
    </div>
  )
}

const mapStateToProps = (state, ownProps) => {
  const { authentication: {user} } = state;
  return {
      user
  };
}

const connectedFacetOption = connect(mapStateToProps)(FacetOption);
export {connectedFacetOption as FacetOption};