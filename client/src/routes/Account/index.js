import React, { Component } from 'react'

import classNames from 'classnames';

import {Link} from 'react-router-dom';
import {connect} from 'react-redux';
import translations from '../../shared/translations';

import Wrapper from '../../components/Wrapper';
import TopNav from '../../components/TopNav';
import {ManageAccount} from '../../components/ManageAccount';

import { PasswordResetAccount } from '../../components/PasswordResetAccount';
import { Payment } from '../../components/Payment';

import { SavedObjects } from '../../components/SavedObjects';

import dataSvc from '../../api';

import * as S from './account.module.css';

class Account extends Component {

  constructor (props) {
    super(props)
    this.state = {
      lang: 'en',
      view: 1,
      accountInfo: {}
    }
    
  }

  componentDidMount = () => {
    const {user, match} = this.props;
    if(user.account_settings) {
      this.setState({lang: user.account_settings.language})
    }
    if(match) {
      const pathName = match.path.split("/").pop();
      switch(pathName) {
        case 'savedobjects':
        this.handleView(3);
        break;
        case 'subscription':
          this.handleView(2);
        break;
        case 'changepassword':
          this.handleView(4);
        break;
        default:
          this.handleView(1)
          break;
      }
    }

    dataSvc.apiUsage()
      .then((res) => {
        this.setState({
          accountInfo: res.data
        })
      })
  }

  handleView = (view) => {
    this.setState({view});
  }

  render() {
    const {lang, view, accountInfo} = this.state;
    let component;
    switch(view) {
      case 1: 
        component = <ManageAccount />;
      break;
      case 2:  
        component = <Payment lang={lang} accountInfo={accountInfo} />;
      break;
      case 3:
        component = <SavedObjects  />;
      break;
      case 4:
        component = <PasswordResetAccount />;
      break;
      default:
        component = <ManageAccount />
        break;
    }
    return (
      <Wrapper hasBG lang={lang}>
        <TopNav />
        <div className={S.gobackwrapper}>
          <Link
            className={classNames(S.goBack)} 
            to="/search/result/">
          </Link>
        </div>
        
        <div className={S.tabWrapper}>
          <div className="tabs">
            <nav className="tabs-nav">
              <Link 
                to="/search/user" 
                onClick={() => this.handleView(1)} 
                className={classNames({'active': view === 1})}>
                {translations(lang).accountOptions['profile']}
              </Link>
              <Link 
                to="/search/user/subscription" 
                onClick={() => this.handleView(2)} 
                className={classNames({'active': view === 2})}>
                {translations(lang).accountOptions['subscriptions']}
              </Link>
              <Link 
                to="/search/user/savedobjects" 
                onClick={() => this.handleView(3)} 
                className={classNames({'active': view === 3})}>
                {translations(lang).accountOptions['saved_objects']}
              </Link>
              <Link 
                to="/search/user/changepassword" 
                onClick={() => this.handleView(4)} 
                className={classNames({'active': view === 4})}>
                {translations(lang).accountOptions['change_password']}
              </Link>
            </nav>
          </div>

          <div className="tabs-pane">
            {component}
          </div>
        </div>
      </Wrapper>
    )
  }
}

const mapStateToProps = (state, ownProps) => {
  const { authentication: {user} } = state;
  return {
      user
  };
}

const connectedAccount = connect(mapStateToProps)(Account);
export {connectedAccount as Account};