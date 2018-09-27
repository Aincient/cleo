import React, { Component } from 'react'

import {Link} from 'react-router-dom';

import * as S from './navigation.module.css';

class Navigation extends Component {
  render () {
    return (
      <div className={S.root}>
        <Link to={'/search/'}>Home</Link>
      </div>
    )
  }
}

export default Navigation;