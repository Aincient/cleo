import { userConstants } from '../constants/user.constants';

let user = JSON.parse(sessionStorage.getItem('account'));
const initialState = user ? { loggedIn: true, user } : {};

export function authentication(state = initialState, action) {
  switch (action.type) {
    case userConstants.LOGIN_REQUEST:
      return {
        loggingIn: true,
        user: action.user
      };
    case userConstants.LOGIN_SUCCESS:
      return {
        loggedIn: true,
        user: action.user
      };
    case userConstants.LOGIN_FAILURE:
      return {};
    
    case userConstants.UPDATE_REQUEST:
      return {
        loggedIn: true,
        user: action.user
      };

    case userConstants.UPDATE_SUCCESS:
      return {
        loggedIn: true,
        user: action.user
      };

    case userConstants.UPDATE_FAILURE:
      return {};

    case userConstants.LOGOUT:
      return {};
    default:
      return state
  }
}