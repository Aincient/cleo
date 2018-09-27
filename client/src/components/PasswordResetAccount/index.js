import React, { Component } from 'react'
import {connect} from 'react-redux';

import { alertActions } from '../../actions/alert.actions';
 
import translations from '../../shared/translations';

import dataSvc from '../../api';

import * as S from '../ManageAccount/manageaccount.module.css';

class PasswordResetAccount extends Component {

  constructor (props) {
    super(props);
    this.state = {
      new_password1: '',
      new_password2: '',
      lang: 'en',
      rules: {
        isValidLength: false,
        hasNumber: false,
        hasLetter: false,
        noSpecialChar: true
      }
    }
  }

  componentDidMount = () => {
    const {user} = this.props;
    this.setState({user: user})
    if(user.account_settings) {
      this.setState({lang: user.account_settings.language})
    } else {
      this.setState({
        user: {
          ...user,
          account_settings: {
            language: 'en'
          }
        }
      });
    }
  }

  handleChange = (e) => {
    const { name, value } = e.target;
    this.setState({
      [name]: value
    });
  }

  handleLang = (e) => {
    const {name, value} = e.target;
    const { user } = this.state;
    this.setState({
      user: {
        ...user,
        account_settings: {
          [name]: value
        }
      }
    });
  }

  handlePasswordChange = (e) => {
    const {user} = this.state;
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


  handleSave = (e) => {
    e.preventDefault();
    const { new_password1, new_password2 } = this.state;
    const { dispatch } = this.props;

    if(new_password1 || new_password2) {
      dataSvc.updatePassword(new_password1, new_password2)
        .then((res) => {
          this.setState({
            new_password1: '',
            new_password2: '',
          })
          dispatch(alertActions.success('Password has been reset'))
        }).catch(error => {
          dispatch(alertActions.error('Something went wrong'))
        })
    }
  }


  render () {
    const {new_password1, new_password2, lang} = this.state;
    return (
      <div className={S.root}>
        <div className={S.wrapper}>
          <form name="userForm" autoComplete="off" role="presentation" onSubmit={this.handleSave}>
          <div className="input-field">
              <label className={S.label} htmlFor="new_password1">{translations(lang).registerForm['password']}</label>
              <input id="new_password1" type="password" autoComplete="off" name="new_password1" value={new_password1} onChange={this.handlePasswordChange} placeholder={translations(lang).registerForm['password']}/>
              <p className="input-hint">{translations(lang).registerForm['passwordStrengthInfo']}</p>
            </div>
            <div className="input-field">
              <label className={S.label} htmlFor="new_password2">{translations(lang).registerForm['passwordAgain']}</label>
              <input id="new_password2" type="password" autoComplete="off" name="new_password2" value={new_password2} onChange={this.handleChange} placeholder={translations(lang).registerForm['passwordAgain']}/>
            </div>
            <button disabled={!new_password1 || !new_password2 || !this.state.rules.hasNumber || !this.state.rules.isValidLength} type="submit">{translations(lang)['save']}</button>
          </form>
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

const connectedPasswordResetAccount = connect(mapStateToProps)(PasswordResetAccount);
export {connectedPasswordResetAccount as PasswordResetAccount};