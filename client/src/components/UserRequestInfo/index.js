import React, { Component, Fragment } from 'react'
import classNames from 'classnames';
import {Link} from 'react-router-dom';
 
import translations from '../../shared/translations';

import * as S from './userrequestinfo.module.css';

class UserRequestInfo extends Component {

  render () {
    const {userInfo, lang} = this.props;
    return (
      <Fragment>
        {userInfo.num_requests_left === 0 && userInfo.scope === 'authenticated_user' ? (
          <div className={S.root}>
            <div className={classNames(S.wrapper, 'alert')}>
              {translations(lang)['buynewnotice']}: <Link to="/search/user/subscription/">{translations(lang)['buynewnoticebutton']}</Link>
            </div>
          </div>
        ): null
        }
      </Fragment>
    )
  }
}

export default UserRequestInfo