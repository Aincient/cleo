import React, { Component } from 'react'
import classNames from 'classnames';

import Navigation from '../../components/Navigation';
import {UserOptions} from '../../components/UserOptions';

import * as S from './topnav.module.css';

class TopNav extends Component {
  render () {
    return (
      <div className={classNames(S.root, 'row')}>
        <div className="col-2">
          <Navigation />
        </div>
        <div className="col-10">
          <UserOptions />
        </div>
      </div>
    )
  }
}

export default TopNav