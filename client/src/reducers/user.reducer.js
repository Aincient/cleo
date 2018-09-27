import { userConstants } from '../constants/user.constants';

let user = JSON.parse(sessionStorage.getItem('account'));
const initialState = user ? { loggedIn: true, user } : {};

export function user(state = initialState, action) {
  switch (action.type) {
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