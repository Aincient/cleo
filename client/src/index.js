import React from 'react';
import ReactDOM from 'react-dom';
import {App} from './App';
import 'babel-polyfill';

import {Provider} from 'react-redux';

import { store } from './shared/store';
document.addEventListener("touchstart", function() {},false);
ReactDOM.render(
  <Provider store={store}>
    <App />
  </Provider>
, document.getElementById('root'));