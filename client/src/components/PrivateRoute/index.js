import React from 'react';
import { Route, Redirect } from 'react-router-dom';
 
 const PrivateRoute = ({ component: Component, ...rest }) => (
    <Route {...rest} render={props => (
        sessionStorage.getItem('account')
            ? <Component {...props} />
            : <Redirect to={{ pathname: '/search/login', state: { from: props.location } }} />
    )} />
)

export default PrivateRoute;