import React, { Component } from 'react'

import {connect} from 'react-redux';
import * as qs from 'query-string';
import classNames from 'classnames';

import {userActions} from '../../actions/user.actions';

import { Link } from 'react-router-dom';

import translations from '../../shared/translations';

import * as S from './register.module.css';

import constants from '../../shared/constants';

import Wrapper from '../../components/Wrapper';


class Register extends Component {

  constructor(props) {
    super(props);
    this.state = {
      user: {
        username: '',
        email: '',
        password: '',
        password2: '',
      },
      submitted: false,
      privacy: false,
      initLang: 'en',
      rules: {
        isValidLength: false,
        hasNumber: false,
        hasLetter: false,
        noSpecialChar: true
      }
    };
  }

  componentDidMount = () => {
    const {user} = this.state;
    if(localStorage.getItem('lang')) {
      this.setState({initLang: localStorage.getItem('lang')});
    }
    if(this.props.location) {
      if(this.props.location.search) {
          const parsed = qs.parse(this.props.location.search);
          if(parsed.email) {
            this.setState({
              user: {
                ...user,
                email: parsed.email
              }
            })
          }
          
      }
    }
  }

  handleChange = (e) => {
    const { name, value } = e.target;
    const { user } = this.state;
    this.setState({
        user: {
          ...user,
          [name]: value
        }
    });
  }

  handlePrivacy = (e) => {
    this.setState({
      privacy:  !this.state.privacy 
    });
  }

  handleSubmit = (e) => {
    e.preventDefault();

    this.setState({ submitted: true });
    const { user } = this.state;
    const { dispatch } = this.props;
    if (user.username && user.email && user.password && user.password2) {
        dispatch(userActions.register(user));
    }
  }

  handlePasswordChange = (e) => {
    const {user} = this.state;
    this.setState({
      user: {
        ...user,
        password: e.target.value
      },
      rules: {
          hasNumber: e.target.value.match(/\d/) ? true : false,
          hasLetter: e.target.value.match(/[A-z]/) ? true : false,
          isValidLength: e.target.value.match(/^.{8,}$/) ? true : false,
          noSpecialChar: !e.target.value.match(/[ \/"]/) ? true : false
      }
    });
  }


  handleLanguage = (lang) => {
    localStorage.setItem('lang', lang);
    this.setState({initLang: lang});
  }

  render () {
    const { user, privacy, initLang } = this.state;
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
          <div className={S.wrapper}>
            <form name="login" autoComplete="off" role="presentation" onSubmit={this.handleSubmit}>
              <div className={S.name}>{constants.name}</div>
                <div className={S.sub}>{translations(initLang).registerForm['createAccount']}</div>

                <div className="input-field">
                  <label className={S.label} htmlFor="username">{translations(initLang).registerForm['username']}</label>
                  <input id="username" type="text" autoCapitalize="none" autoComplete="off" name="username" value={user.username}  onChange={this.handleChange} placeholder={translations(initLang).registerForm['username']}/>
                </div>
                <div className="input-field">
                  <label className={S.label} htmlFor="email">Email</label>
                  <input id="email" type="email" autoComplete="off" name="email" value={user.email} onChange={this.handleChange} placeholder="Email"/>
                </div>
                <div className="input-field">
                  <label className={S.label} htmlFor="password">{translations(initLang).registerForm['password']}</label>
                  <input id="password" type="password" autoComplete="off" name="password" value={user.password} onChange={this.handlePasswordChange} placeholder={translations(initLang).registerForm['password']}/>
                  <p className="input-hint">{translations(initLang).registerForm['passwordStrengthInfo']}</p>
                </div>
                <div className="input-field">
                  <label className={S.label} htmlFor="password2">{translations(initLang).registerForm['passwordAgain']}</label>
                  <input id="password2" type="password" autoComplete="off" name="password2" value={user.password2} onChange={this.handleChange} placeholder={translations(initLang).registerForm['passwordAgain']}/>
                </div>
                <div className="input-field">
                  <input id="privacy" type="checkbox" autoComplete="off" name="privacy" checked={privacy}  onChange={this.handlePrivacy} placeholder="privacy"/>
                  <label className={S.privacyLabel} htmlFor="privacy">
                    {`${translations(initLang).registerForm['agree']} `}
                    <a 
                      target="_blank"
                      rel="noopener noreferrer"
                      href={initLang === 'en' ? '/pages/en/privacy-policy/' : '/pages/nl/privacy-policy/'}>
                      {translations(initLang).registerForm['policy']}
                    </a> 
                    {` ${translations(initLang).registerForm['and']} `} 
                    <a 
                      target="_blank"
                      rel="noopener noreferrer"
                      href={initLang === 'en' ? '/pages/en/general-terms/' : '/pages/nl/algemene-voorwaarden/'}>
                      {translations(initLang).registerForm['terms']}
                    </a>
                  </label>
                </div>
                <div>
                </div>
                <div className="input-field text-center">
                  <button disabled={!user.username || !this.state.privacy || !this.state.rules.hasNumber || !this.state.rules.isValidLength} type="submit">{translations(initLang).registerForm['create']}</button>
                </div>
              </form>
              <div className="text-center">
                <Link to="/search/login">
                  {translations(initLang).registerForm['cancel']}
                </Link>
              </div>
            </div>
        </div>
      </Wrapper>
    )
  }
}

function mapStateToProps(state) {
  const { registering } = state.registration;
  return {
      registering
  };
}

const connectedRegister = connect(mapStateToProps)(Register);
export { connectedRegister as Register };