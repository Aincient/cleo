import React, { Component } from 'react';

import {Link} from 'react-router-dom';

import Wrapper from '../../components/Wrapper';

import * as S from './notfound.module.css';

export default class NotFound extends Component {
  render () {
    return (
      <Wrapper hasBG>
        <div className={S.root}>
          <div className={S.wrapper}>
            <div className={S.name}>CLEO</div>
            <p>Not found</p>
            <Link to="/">Return to the homepage</Link>
          </div>
        </div>
      </Wrapper>
    )
  }
}