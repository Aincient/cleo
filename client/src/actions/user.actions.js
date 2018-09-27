import { userConstants } from '../constants/user.constants';
import { alertActions } from '../actions/alert.actions';
import dataSvc from '../api';
import history from '../shared/history';

export const userActions = {
    login,
    logout,
    update,
    register,
};

function login(username, password, initLang) {
    return dispatch => {
        dispatch(request({ username }));

        dataSvc.login(username, password)
            .then(
                user => { 
                    dataSvc.getAccount() 
                      .then(user=> {
                        if(!user.data.account_settings) {
                            let newlang = user.data;
                            newlang.account_settings = {
                                language: initLang
                            }
                            dispatch(userActions.update(newlang))
                        }
                        sessionStorage.setItem('account', JSON.stringify(user.data));
                        dispatch(success(user.data))
                        history.push('/search/');
                        
                      });
                },
                error => {
                  dispatch(failure(error.toString()));
                  dispatch(alertActions.error(error.response.data));
              }
            );
    };

    function request(user) { return { type: userConstants.LOGIN_REQUEST, user } }
    function success(user) { return { type: userConstants.LOGIN_SUCCESS, user } }
    function failure(error) { return { type: userConstants.LOGIN_FAILURE, error } }
}

function update(user) {
  return dispatch => {
      dispatch(request(user));

      dataSvc.updateAccount(user)
          .then(
              user => { 
                sessionStorage.setItem('account', JSON.stringify(user.data));
                dispatch(success(user.data))
                window.location.reload()
              },
              error => {
              
                  dispatch(failure(error));
              }
          );
  };

  function request(user) { return { type: userConstants.UPDATE_REQUEST, user } }
  function success(user) { return { type: userConstants.UPDATE_SUCCESS, user } }
  function failure(error) { return { type: userConstants.UPDATE_FAILURE, error } }
}

function logout() {
  dataSvc.logout();
    return { type: userConstants.LOGOUT };
}

function register(user) {
    return dispatch => {
        dispatch(request(user));

        dataSvc.register(user)
            .then(
                user => { 
                    history.push('/search/')
                    dispatch(success());
                    dispatch(alertActions.success('Registration successful, please check your email.'));
                },
                error => {
                  dispatch(failure(error.toString()));
                  dispatch(alertActions.error(error.response.data));
              }
            );
    };

    function request(user) { return { type: userConstants.REGISTER_REQUEST, user } }
    function success(user) { return { type: userConstants.REGISTER_SUCCESS, user } }
    function failure(error) { return { type: userConstants.REGISTER_FAILURE, error } }
}

// prefixed function name with underscore because delete is a reserved word in javascript
// function _delete(id) {
//     return dispatch => {
//         dispatch(request(id));

//         userService.delete(id)
//             .then(
//                 user => { 
//                     dispatch(success(id));
//                 },
//                 error => {
//                     dispatch(failure(id, error));
//                 }
//             );
//     };

//     function request(id) { return { type: userConstants.DELETE_REQUEST, id } }
//     function success(id) { return { type: userConstants.DELETE_SUCCESS, id } }
//     function failure(id, error) { return { type: userConstants.DELETE_FAILURE, id, error } }
// }