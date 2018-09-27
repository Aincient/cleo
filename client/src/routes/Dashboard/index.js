import React, { Component } from 'react'

import Wrapper from '../../components/Wrapper';
import { Search } from '../../components/Search';
import TopNav from '../../components/TopNav';

import {connect} from 'react-redux';

import UserRequestInfo from '../../components/UserRequestInfo';

import dataSvc from '../../api';


class Dashboard extends Component {
  constructor (props) {
    super(props)
    this.state = {
      userInfo: {},
      lang: 'en'
    }
    if(sessionStorage.getItem('searchQuery')) {
      sessionStorage.removeItem('searchQuery');
    }
     if (sessionStorage.getItem('facets')) {
      sessionStorage.removeItem('facets');   
    }
    if (sessionStorage.getItem('multipleImageSearch')) {
      sessionStorage.removeItem('multipleImageSearch');
    }
    if(sessionStorage.getItem('hasMultipleAIImageSearchedClicked')) {
      sessionStorage.removeItem('hasMultipleAIImageSearchedClicked')
    }
  }

  componentDidMount = () => {
    const {user} = this.props;
    window.scrollTo(0, 0);
    dataSvc.apiUsage()
      .then(res=> {
        this.setState({
          userInfo: res.data
        })
      })
    
    if(user.account_settings) {
      this.setState({lang: user.account_settings.language})
    } 
  }
  
  render () {
    const {userInfo, lang} = this.state;
    return (
      <Wrapper hasBG lang={lang}>
        <TopNav />
        <UserRequestInfo 
          userInfo={userInfo} 
          lang={lang} />
        <Search userInfo={userInfo} />
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

const connectedDashboard = connect(mapStateToProps)(Dashboard);
export {connectedDashboard as Dashboard};