import React, { Component } from 'react'
import {connect} from 'react-redux';

import translations from '../../shared/translations';

import * as S from './breadcrumb.module.css';

class BreadCrumb extends Component {
  
  constructor(props) {
    super(props);

    this.state = {
      lang: 'en'
    }
  }

  componentDidMount = () => {
    const {user} = this.props;
    if(user.account_settings) {
      this.setState({lang: user.account_settings.language})
    }
  }
  render () {
    const {query, count} = this.props;
    const {lang} = this.state;
    return (
      <div className={S.root}>
        <div className={S.wrapper}>
          {count} {translations(lang)['results']} {query ? ` ${translations(lang)['for']} ${query}`: ''}
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

const connectedBreadCrumb = connect(mapStateToProps)(BreadCrumb);
export {connectedBreadCrumb as BreadCrumb};