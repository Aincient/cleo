import React, { Component } from 'react'
import {Link, Redirect} from 'react-router-dom';

import { connect } from 'react-redux';

import classNames from 'classnames';

import { userActions } from '../../actions/user.actions';

import * as S from './login.module.css';

import constants from '../../shared/constants';
import translations from '../../shared/translations';

import Wrapper from '../../components/Wrapper';

class Login extends Component {

  constructor(props) {
    super(props);
    this.state = {
      username: '',
      password: '',
      submitted: false,
      loginFailed: false,
      initLang: 'en'
    }
  }

  componentDidMount = () => {
    if(localStorage.getItem('lang')) {
      this.setState({initLang: localStorage.getItem('lang')});
    }
  }

  handleChange = (e) => {
    const {name, value} = e.target;
    this.setState({[name]: value});
  }

  handleSubmit = (e) => {
    e.preventDefault();
    this.setState({ submitted: true, loginFailed: false });
    const { username, password, initLang } = this.state;
    const { dispatch } = this.props;
    if (username && password) {
      dispatch(userActions.login(username, password, initLang))
    }
  }

  handleLanguage = (lang) => {
    localStorage.setItem('lang', lang);
    this.setState({initLang: lang});
  }

  render () {
    const { username, password, loginFailed, initLang} = this.state;
    if ( sessionStorage.getItem('account') ) {
      return <Redirect to="/search/"/>
    }
    
    return (
      <Wrapper hasBG lang={initLang}>
        <div className={S.root}>
          <div className={S.langWrapper}>
            <span 
              className={classNames(S.langOption, {[S.activeLang]: initLang === 'nl' })} 
              onClick={()=> this.handleLanguage('nl')}>
              NL
            </span> 
            <span 
              className={classNames(S.langOption, {[S.activeLang]: initLang === 'en' })} 
              onClick={()=> this.handleLanguage('en')}>
              EN
            </span>
          </div>
          <div className={S.loginWrapper}>
            <form name="login" autoComplete="off" role="presentation" onSubmit={this.handleSubmit}>
              <div className={S.name}>{constants.name}</div>

              <div className="input-field">
                <input type="text" autoComplete="off" autoCapitalize="none" name="username" value={username} onChange={this.handleChange} placeholder={translations(initLang).loginForm['username']}/>
              </div>
              <div className="input-field">
                <input type="password" autoComplete="off" name="password" value={password} onChange={this.handleChange} placeholder={translations(initLang).loginForm['password']} />
                <p className={classNames(S.passwordResetLink, "input-hint")}>
                  <Link to="/search/passwordreset">{translations(initLang).loginForm['passwordReset']}</Link>
                </p>
              </div>
              {
                loginFailed && <div>{translations['loginFailed']}</div>
              }
              <div className="input-field">
                <button  disabled={!this.state.username} type="submit">{translations(initLang).loginForm['login']}</button>
              </div>
            </form>
            <Link to="/search/register">{translations(initLang).loginForm['noAccount']}</Link>
          </div>
        </div>
      </Wrapper>
    )
  }
}

function mapStateToProps(state) {
  const { loggingIn } = state.authentication;
  return {
      loggingIn
  };
}
const connectedLoginPage = connect(mapStateToProps)(Login);
export { connectedLoginPage as Login }; 
