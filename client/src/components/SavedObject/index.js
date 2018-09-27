import React, { Component, Fragment } from 'react';
import classNames from 'classnames';
import constants from '../../shared/constants';
import translations from '../../shared/translations';
import {Link} from 'react-router-dom';

import * as S from './savedobject.module.css';

class SavedObject extends Component {
  render () {
    const { object , lang, removeObject} = this.props;
    return (
      <Fragment>
       <div className={classNames(S.wrapper, "row")}>
          <div className="col-12">
            <div 
              className={S.image} 
              style={{backgroundImage: "url(" + constants.api.url + object.images_urls[0].lr + ")"}}>
            </div>
          </div>
          <div className="col-12">
            <div className={S.info}>
              <div className={S.title}>
                {lang === 'en' ? object.title_en && object.title_en.map(title=> `${title}; `) : object.title_nl && object.title_nl.map(title=> `${title}; `)}
              </div>
            </div>
          </div>
          <div className="col-12">
              <div className={S.downloadOptions}>
                <Link to={`/search/object/${object.id}`} className={classNames(S.downloadOption, "button")}>{translations(lang)['gotodetailpage']}</Link>
                <button onClick={()=> removeObject(object.fav_id)} className={classNames(S.downloadOption, "button-danger ")}>{translations(lang)['remove']}</button>
              </div>
            </div>
        </div>
       </Fragment>
    )
  }
}

export default SavedObject