import React, { Component } from 'react'
import classNames from 'classnames';
import {connect} from 'react-redux';
import {userActions} from '../../actions/user.actions';
import {Link} from 'react-router-dom';

import * as S from './useroptions.module.css';

class UserOptions extends Component {
  constructor (props) {
    super(props)
    this.state = {
      username: '',
      email: '',
      first_name: '',
      last_name: '',
      lang: 'en'
    }
  }

  componentDidMount = () => {
    const {user} = this.props;
    if(user.account_settings) {
      this.setState({lang: user.account_settings.language})
    }
  }

  handleLanguage = (lang) => {
    const {dispatch, user} = this.props;
    if(lang && user) {
      let newlang = user;
      if(newlang.account_settings) {
        newlang.account_settings.language = lang;
        dispatch(userActions.update(newlang))
      } else {
        newlang.account_settings = {
          language: lang
        }
        dispatch(userActions.update(newlang))
      }
      
    }
  }

  render () {
    const {user} = this.props;
    const {lang} = this.state;
    return (
      <div>
        <div className={S.root}>
          <Link className={S.user} to={'/search/user'}>
            {user.first_name ? user.first_name : user.username}
          </Link> | <span className={classNames(S.langOption, {[S.activeLang]: lang === 'nl' })} onClick={()=> this.handleLanguage('nl')}>NL</span> <span className={classNames(S.langOption, {[S.activeLang]: lang === 'en' })} onClick={()=> this.handleLanguage('en')}>EN</span> | <a href="/search/logout">Logout</a>
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

const connectedUserOptions = connect(mapStateToProps)(UserOptions);
export {connectedUserOptions as UserOptions};