import React, { Component, Fragment } from 'react'
import {connect} from 'react-redux';
import classNames from 'classnames';
import {isEmpty} from '../../helpers';
import SavedObject from '../SavedObject';
import translations from '../../shared/translations';
import dataSvc from '../../api';

import * as S from './savedobjects.module.css';

class SavedObjects extends Component {

  constructor(props) {
    super(props);
    this.state = {
      lang: 'en',
      saved_objects: {},
      objects: {},
      isDropdownOpen: false
    }
  }

  componentDidMount = () => {
    const {user} = this.props;
    if(user.account_settings) {
      this.setState({lang: user.account_settings.language})
    }
    dataSvc.getUserCollection()
      .then(res=> {
        this.setState({
          saved_objects: res.data.results
        })
      })

    document.addEventListener('mousedown', this.handleClickOutside);
  }

  componentWillMount = () => {
    document.removeEventListener('mousedown', this.handleClickOutside);
  }

  setWrapperRef = (node) => {
    this.wrapperRef = node;
  }
  
  removeObject = (id) => {
    if(id) {
      dataSvc.removeObjectFromCollection(id)
        .then(res => {
          dataSvc.getUserCollection()
            .then(res=> {
              this.setState({
                saved_objects: res.data.results
              })
            })
        })
    }
  }

  handleClickOutside = (event) => {
    if (this.wrapperRef && !this.wrapperRef.contains(event.target)) {
      this.setState({isDropdownOpen: false})
    }
  }

  toggleDownloadMenu = () => {
    this.setState({isDropdownOpen: !this.state.isDropdownOpen});
  }

  render () {
    const {lang, saved_objects, isDropdownOpen} = this.state;
    return (
      <Fragment>
        <div className={S.savedObjectOptions}>
         
          {!isEmpty(saved_objects) && 
            <div 
            ref={this.setWrapperRef}
            className={classNames("dropdown", {['active']: isDropdownOpen})}
            onClick={() => this.toggleDownloadMenu()}>
            <button type="button" className={classNames(S.downloadObject, 'dropdown-trigger button')}>{translations(lang)['donwloadAllObjects']}</button>
            <div className={classNames("dropdown-menu", S.dropdownMenu)}>
              <a
                href={`/account/usercollectionitemfavourites/export_all/?docformat=xlsx`}
                download="object">
                  {translations(lang)['donwloadAllObjects']} (Excel)
              </a>
              <a
                href={`/account/usercollectionitemfavourites/export_all/`}
                download="object">
                  {translations(lang)['donwloadAllObjects']} (CSV)
              </a>
            </div>
          </div>
          }
        </div>
        <div className="row">
          {!isEmpty(saved_objects) ? (
            saved_objects.map((obj, index) => <div key={index} className="col-12 col-md-4"><SavedObject  object={obj} lang={lang} removeObject={this.removeObject} /></div>)
          ): (<div className="text-center">{translations(lang)['noSavedObjects']}</div>)}
        </div>
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

const connectedSavedObjects = connect(mapStateToProps)(SavedObjects);
export {connectedSavedObjects as SavedObjects};