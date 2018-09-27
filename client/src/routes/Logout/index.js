import React, { Component } from 'react'

import Wrapper from '../../components/Wrapper';

import dataSvc from '../../api';

class Logout extends Component {

  componentDidMount() {
    dataSvc.logout().then(res => this.props.history.push('/search/login'));
  }
  
  render () {
    return (
      <Wrapper hasBG>
        
      </Wrapper>
    )
  }
}

export default Logout