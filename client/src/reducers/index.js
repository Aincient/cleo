import { combineReducers } from 'redux';

import { authentication } from './auth.reducer';
import { registration } from './registration.reducer';
import { alert } from './alert.reducer';
import {savedObjects} from './savedobjects.reducer';

const rootReducer = combineReducers({
  authentication,
  registration,
  alert,
  savedObjects
});

export default rootReducer;