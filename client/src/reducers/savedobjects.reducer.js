import { savedObjectsConstants } from '../constants/savedobjects.constants';

export function savedObjects(state = {}, action) {
  switch (action.type) {
    case savedObjectsConstants.GETALL_REQUEST:
      return {
        objects: action.objects
      };
    case savedObjectsConstants.GETALL_SUCCESS:
       return {
        objects: action.objects
      };
    case savedObjectsConstants.GETALL_FAILURE:
      return {};

    case savedObjectsConstants.ADD_REQUEST:
       return {
        objects: action.objects
      };
    case savedObjectsConstants.ADD_SUCCESS:
       return {
        objects: action.objects
      };
    case savedObjectsConstants.ADD_FAILURE:
      return {};

      case savedObjectsConstants.REMOVE_REQUEST:
       return {
        objects: action.objects
      };
    case savedObjectsConstants.REMOVE_SUCCESS:
       return {
        objects: action.objects
      };
    case savedObjectsConstants.REMOVE_FAILURE:
      return {};

    default:
      return state
  }
}