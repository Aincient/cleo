import React, { Component } from 'react'
import {Link} from 'react-router-dom';
import * as qs from 'query-string';

import { connect } from 'react-redux';

import {alertActions} from '../../actions/alert.actions';

import classNames from 'classnames';

import dataSvc from '../../api';

import * as S from './passwordresetconfirm.module.css';

import constants from '../../shared/constants';
import translations from '../../shared/translations';

import Wrapper from '../../components/Wrapper';

class PasswordResetConfirm extends Component {

  constructor(props) {
    super(props);
    this.state = {
      new_password1: '',
      new_password2: '',
      uid: '',
      token: '',
      submitted: false,
      submitFailed: false,
      initLang: 'en',
      rules: {
        isValidLength: false,
        hasNumber: false,
        hasLetter: false,
        noSpecialChar: true
      }
    }
  }

  componentDidMount = () => {
    if(localStorage.getItem('lang')) {
      this.setState({initLang: localStorage.getItem('lang')});
    }
    if(this.props.location) {
      if(this.props.location.search) {
          const parsed = qs.parse(this.props.location.search);
          if(parsed.uid || parsed.token) {
            this.setState({
              uid: parsed.uidb64,
              token: parsed.token
            })
          }
      }
    }
  }

  handleChange = (e) => {
    const {name, value} = e.target;
    this.setState({[name]: value});
  }

  handleSubmit = (e) => {
    e.preventDefault();
    this.setState({ submitted: true});
    const { new_password1, new_password2, uid, token } = this.state;
    const { dispatch } = this.props;
    if (new_password1 && new_password2) {
      
      dataSvc.passwordResetConfirm(new_password1, new_password2, uid, token)
        .then((res) => {
          
          this.props.history.push('/search/')
          dispatch(alertActions.success('Password has been reset'))
        }).catch(error => {
          this.setState({ submitted: false });
          dispatch(alertActions.error('Something went wrong'))
        })
    }
  }

  handlePasswordChange = (e) => {
    this.setState({
      new_password1: e.target.value,
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
    const { new_password1, new_password2, uid, token, submitfailed, initLang} = this.state;
  
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
              <div className={S.sub}>{translations(initLang).passwordResetConfirmForm['sub']}</div>

              <div className="input-field">
                <label className={S.label} htmlFor="new_password1">{translations(initLang).registerForm['password']}</label>
                <input id="new_password1" type="password" autoComplete="off" name="new_password1" value={new_password1} onChange={this.handlePasswordChange} placeholder={translations(initLang).registerForm['password']}/>
                <p className="input-hint">{translations(initLang).registerForm['passwordStrengthInfo']}</p>
              </div>
              <div className="input-field">
                <label className={S.label} htmlFor="new_password2">{translations(initLang).registerForm['passwordAgain']}</label>
                <input id="new_password2" type="password" autoComplete="off" name="new_password2" value={new_password2} onChange={this.handleChange} placeholder={translations(initLang).registerForm['passwordAgain']}/>
              </div>
             
              <div className="input-field">
                <button 
                  disabled={!this.state.new_password1 || !this.state.new_password2 || this.state.submitted || !this.state.rules.hasNumber || !this.state.rules.isValidLength} 
                  type="submit">
                  {translations(initLang).passwordResetConfirmForm['submit']}
                </button>
              </div>
            </form>
            <Link to="/search/">{translations(initLang).passwordResetConfirmForm['cancel']}</Link>
          </div>
        </div>
      </Wrapper>
    )
  }
}

export default connect()(PasswordResetConfirm);