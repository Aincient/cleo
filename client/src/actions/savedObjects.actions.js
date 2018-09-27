import { savedObjectsConstants } from '../constants/savedobjects.constants';
import { alertActions } from '../actions/alert.actions';
import dataSvc from '../api';

export const savedObjectsActions = {
    getAll,
    add,
    remove,
};

function getAll() {
    return dispatch => {
        dispatch(request());

        dataSvc.getUserCollectionList()
            .then(
                objects => { 
                  dispatch(success(objects.data.results))
                },
                error => {
                  dispatch(failure(error.toString()));
                  dispatch(alertActions.error(JSON.stringify(error.response.data)));
              }
            );
    };

    function request(objects) { return { type: savedObjectsConstants.GETALL_REQUEST, objects } }
    function success(objects) { return { type: savedObjectsConstants.GETALL_SUCCESS, objects } }
    function failure(error) { return { type: savedObjectsConstants.GETALL_FAILURE, error } }
}

function add(id) {
  return dispatch => {
      dispatch(request(id));

      dataSvc.addObjectToCollection(id)
          .then(
              object => { 
                dispatch(success())
                dispatch(getAll())
              },
              error => {
                  dispatch(failure(error));
              }
          );
  };

  function request(object) { return { type: savedObjectsConstants.ADD_REQUEST, object } }
  function success(object) { return { type: savedObjectsConstants.ADD_SUCCESS, object } }
  function failure(error) { return { type: savedObjectsConstants.ADD_FAILURE, error } }
}

function remove(id) {
    return dispatch => {
        dispatch(request(id));

        dataSvc.removeObjectFromCollection(id)
            .then(
                object => { 
                  dispatch(success())
                  dispatch(getAll())
                },
                error => {
                  dispatch(failure(error.toString()));
                  dispatch(alertActions.error(JSON.stringify(error.response.data)));
              }
            );
    };

    function request(object) { return { type: savedObjectsConstants.REMOVE_REQUEST, object } }
    function success(object) { return { type: savedObjectsConstants.REMOVE_SUCCESS, object } }
    function failure(error) { return { type: savedObjectsConstants.REMOVE_FAILURE, error } }
}