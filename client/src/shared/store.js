import { createStore, applyMiddleware } from 'redux';
import thunkMiddleware from 'redux-thunk';
import { createLogger } from 'redux-logger';
import rootReducer from '../reducers';

const loggerMiddleware = createLogger();

let middleware = [thunkMiddleware];

if(process.env.NODE_ENV !== 'production') {
    middleware = [...middleware, loggerMiddleware]
}

export const store = createStore(
    rootReducer,
    applyMiddleware(
        ...middleware
    )
);