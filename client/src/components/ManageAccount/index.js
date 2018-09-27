import React, { Component } from 'react'
import {connect} from 'react-redux';

import { userActions } from '../../actions/user.actions';
 
import translations from '../../shared/translations';

import * as S from './manageaccount.module.css';

class ManageAccount extends Component {

  constructor (props) {
    super(props);
    this.state = {
      user: {
        username: '',
        email: '',
        first_name: '',
        last_name: '',
        account_settings: {
          language: 'en'
        }
      },
      lang: 'en'
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
    const { user } = this.state;
    this.setState({
      user: {
        ...user,
        [name]: value
      }
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


  handleSave = (e) => {
    e.preventDefault();
    const { user } = this.state;
    const { dispatch } = this.props;
    if(user.username) {
      dispatch(userActions.update(user))
    }
  }


  render () {
    const {lang, user} = this.state;
    return (
      <div className={S.root}>
        <div className={S.wrapper}>
          <form name="userForm" autoComplete="off" role="presentation" onSubmit={this.handleSave}>
            <div className="input-field">
              <label htmlFor="username">{translations(lang).editForm['username']}</label>
              <input id="username" type="text" readOnly autoComplete="off" name="username" value={user.username} placeholder={translations(lang).editForm['username']}/>
            </div>
            <div className="input-field">
              <label htmlFor="email">{translations(lang).editForm['email']}</label>
              <input id="email" type="text" autoComplete="off" name="email" value={user.email} onChange={this.handleChange} placeholder={translations(lang).editForm['email']}/>
            </div>
            <div className="input-field">
              <label htmlFor="first_name">{translations(lang).editForm['first_name']}</label>
              <input id="first_name" type="text" autoComplete="off" name="first_name" value={user.first_name} onChange={this.handleChange} placeholder={translations(lang).editForm['first_name']}/>
            </div>
            <div className="input-field">
              <label htmlFor="last_name">{translations(lang).editForm['last_name']}</label>
              <input id="last_name" type="text" autoComplete="off" name="last_name" value={user.last_name} onChange={this.handleChange} placeholder={translations(lang).editForm['last_name']}/>
            </div>
            <div className="input-field">
              <label htmlFor="language">{translations(lang).editForm['language']}</label>
              <select name="language" value={user.account_settings ? user.account_settings.language : 0} onChange={this.handleLang} id="language">
                <option disabled>Select language</option>
                <option value="en">English</option>
                <option value="nl">Nederlands</option>
              </select>
            </div>
            <button type="submit">{translations(lang)['save']}</button>
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

const connectedManageAccount = connect(mapStateToProps)(ManageAccount);
export {connectedManageAccount as ManageAccount};