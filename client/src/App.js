import React, { Component } from 'react';
import {
  Router,
  Route,
  Switch
} from 'react-router-dom';

import { connect } from 'react-redux';

import {isEmpty} from './helpers';

import {alertActions} from './actions/alert.actions';

import { Dashboard } from './routes/Dashboard';
import NotFound from './routes/NotFound';
import { Login } from './routes/Login';
import PasswordReset from './routes/PasswordReset';
import PasswordResetConfirm from './routes/PasswordResetConfirm';
import { Result } from './routes/Result';
import Logout from './routes/Logout';
import { Account } from './routes/Account';
import { Register } from './routes/Register';
import history from './shared/history';
import PrivateRoute from './components/PrivateRoute';
import './shared/multiDownload';
import './styles/styles.css';
const baseUrl = process.env.PUBLIC_URL;

class App extends Component {
  constructor(props) {
    super(props);

    const { dispatch } = this.props;
    history.listen((location, action) => {
      dispatch(alertActions.clear());
    });
  }

  render() {
    const { alert } = this.props;
    let messages = [];
    if(!isEmpty(alert)) {
      let mes = alert.message;
      if(typeof mes[Object.keys(mes)[0]] === "object") {
        messages = {
          type: alert.type,
          message: mes[Object.keys(mes)[0]]
        }
      } else {
        messages = {
          type: alert.type,
          message: alert.message
        }
      }
      
    }
    return (
      <div>
          {messages &&
            <div className={`alert ${messages.type}`}>{messages.message}</div>
          }
        <Router history={history}>
          <Switch>
            <PrivateRoute exact path={`${baseUrl}/search/`} component={Dashboard}/>

            <Route exact path={`${baseUrl}/search/logout`} component={Logout}/>
            <PrivateRoute  exact path={`${baseUrl}/search/user`} component={Account} />
            <PrivateRoute  exact path={`${baseUrl}/search/user/profile`} component={Account} />
            <PrivateRoute  exact path={`${baseUrl}/search/user/subscription`} component={Account} />
            <PrivateRoute  exact path={`${baseUrl}/search/user/savedobjects`} component={Account} />
            <PrivateRoute  exact path={`${baseUrl}/search/user/changepassword`} component={Account} />
            <Route exact path={`${baseUrl}/search/login`} component={Login} />
            <Route exact path={`${baseUrl}/search/register`} component={Register}/>
            <Route exact path={`${baseUrl}/search/passwordreset`} component={PasswordReset}/>
            <Route exact path={`${baseUrl}/search/passwordresetconfirm`} component={PasswordResetConfirm}/>

            <PrivateRoute exact path={`${baseUrl}/search/result/`} component={Result}/>
            <PrivateRoute exact path={`${baseUrl}/search/result/:params`} component={Result}/>
            <PrivateRoute exact path={`${baseUrl}/search/object/:id`} component={Result}/>

            <Route component={NotFound} />
          </Switch>
        </Router>
      </div>
    );
  }
}

function mapStateToProps(state) {
  const {alert} = state;
  return {
      alert
  };
}
const connectedApp = connect(mapStateToProps)(App);
export { connectedApp as App }; 



