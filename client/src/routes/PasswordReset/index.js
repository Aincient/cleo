import React, { Component } from 'react'
import { Link}  from 'react-router-dom';


import { connect } from 'react-redux';

import { alertActions } from '../../actions/alert.actions';

import classNames from 'classnames';

import dataSvc from '../../api';

import * as S from './passwordreset.module.css';

import constants from '../../shared/constants';
import translations from '../../shared/translations';

import Wrapper from '../../components/Wrapper';

class PasswordReset extends Component {

  constructor(props) {
    super(props);
    this.state = {
      email: '',
      submitted: false,
      submitFailed: false,
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
    const { email } = this.state;
    const { dispatch } = this.props;
    if (email) {
      
      dataSvc.passwordReset(email)
        .then((res) => {
          
          this.props.history.push('/search/')
          dispatch(alertActions.success('Email has been send'))
        })
    }
  }

  handleLanguage = (lang) => {
    localStorage.setItem('lang', lang);
    this.setState({initLang: lang});
  }

  render () {
    const { email, initLang} = this.state;
  
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
              <div className={S.sub}>{translations(initLang).passwordResetForm['sub']}</div>

              <div className="input-field">
                <input 
                  disabled={this.state.submitted}
                  type="email" 
                  autoComplete="off" 
                  autoCapitalize="none" 
                  name="email" 
                  value={email} 
                  onChange={this.handleChange} 
                  placeholder="Email"/>
              </div>
             
              <div className="input-field">
                <button 
                  disabled={!this.state.email || this.state.submitted} 
                  type="submit">
                  {translations(initLang).passwordResetForm['submit']}
                </button>
              </div>
            </form>
            <Link to="/search/">{translations(initLang).passwordResetForm['cancel']}</Link>
          </div>
        </div>
      </Wrapper>
    )
  }
}

export default connect()(PasswordReset);