import axios from 'axios';
import constants from './shared/constants';
import {isEmpty} from './helpers';
import queryString from 'query-string';

import {getCookie} from './helpers';

const client = axios.create({
  baseURL: constants.api.url,
  validateStatus: function (status) {
    return status >= 200 && status < 300;
  },
});


export default class dataSvc {

  static getCSRFToken = () => {
    const token = getCookie('csrftoken');
    if (token !== null) {
      return;
    }
    return client({method: 'post', url: `/csrftoken`});
  }

  static getCollection = (query, filter, page) => {
    const en_facets = '&nested_facet=period_1_en&facet=material_en&facet=primary_object_type_en&facet=object_type_en&facet=city_en&facet=country_en&facet=period_en';
    const nl_facets = '&nested_facet=period_1_nl&facet=material_nl&facet=primary_object_type_nl&facet=object_type_nl&facet=city_nl&facet=country_nl&facet=period_nl';
    let facetLang;
    if(sessionStorage.getItem('account')) {
      let userLang = JSON.parse(sessionStorage.getItem('account'));
      if(userLang.account_settings) {
        const lang = userLang.account_settings.language;
        if (lang === 'en') {
          facetLang = en_facets;
        } else {
          facetLang = nl_facets;
        }
      } else {
        facetLang = en_facets;
      }
    } else {
      facetLang = en_facets;
    }

    const pageNr = (page ? page : 1);
    let searchFacet = '';
    if(!isEmpty(filter)) {
      searchFacet  = `&${queryString.stringify(filter)}`;
    }
    if(query) {
      return client({method: 'get', url: `/api/collectionitem/?search=${query}${searchFacet}&page=${pageNr}${facetLang}&ordering=score&page_size=36`});
    } else {
      return client({method: 'get', url: `/api/collectionitem/?page=${pageNr}${searchFacet}${facetLang}&ordering=score&page_size=36`});
    }
  }

  static getFacets = () => {
    const en_facets = 'nested_facet=period_1_en&facet=material_en&facet=primary_object_type_en&facet=object_type_en&facet=city_en&facet=country_en&facet=period_en';
    const nl_facets = 'nested_facet=period_1_nl&facet=material_nl&facet=primary_object_type_nl&facet=object_type_nl&facet=city_nl&facet=country_nl&facet=period_nl';
    let facetLang;
    if(sessionStorage.getItem('account')) {
      let userLang = JSON.parse(sessionStorage.getItem('account'));
      if(userLang.account_settings) {
        const lang = userLang.account_settings.language;
        if (lang === 'en') {
          facetLang = en_facets;
        } else {
          facetLang = nl_facets;
        }
      } else {
        facetLang = en_facets;
      }
    } else {
      facetLang = en_facets;
    }
   
    return client({method: 'get', url: `/api/collectionitemfacetsonly/?${facetLang}`});
  
  }
  static getObject = (id) => {
    return client({method: 'get', url: `/api/collectionitem/${id}/`})
  }

  static searchCollectionAI = (objects) => {
    const idarr = {id: objects }
    return client({
      method: 'get',
      url: `/api/collectionitem/find_similar_items/?${queryString.stringify(idarr)}`,
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      },
      credentials: 'same-origin',
    })
  }

  static login = (username, password) => {
    let lang;
    if(localStorage.getItem('lang')) {
      if(localStorage.getItem('lang') === 'en') {
        lang = 'en'
      } else {
        lang = 'nl'
      }
    }

    return client({
      method: 'post',
      url: `/rest-auth/login/`,
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
        'Accept-Language': lang
      },
      credentials: 'same-origin',
      data: {
        username: username,
        password: password
      }
    })
  }

  static getAccount = () => {
    return client({
      method: 'get',
      url: `/rest-auth/user/`,
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      },
      credentials: 'same-origin',
    });
  }

  static updateAccount = (account) => {
    return client({
      method: 'put',
      url: `/rest-auth/user/`,
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      },
      credentials: 'same-origin',
      data: account
    });
  }

  static updatePassword = (new_password1, new_password2) => {
    let lang;
    if(localStorage.getItem('lang')) {
      if(localStorage.getItem('lang') === 'en') {
        lang = 'en'
      } else {
        lang = 'nl'
      }
    }
    return client({
      method: 'post',
      url: `/rest-auth/password/change/`,
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
        'Accept-Language': lang
      },
      credentials: 'same-origin',
      data: {
        "new_password1": new_password1,
        "new_password2": new_password2
      }
    });
  }

  static register = (user) => {
    let lang;
    if(localStorage.getItem('lang')) {
      if(localStorage.getItem('lang') === 'en') {
        lang = 'en'
      } else {
        lang = 'nl'
      }
    }
    return client({
        method: 'post',
        url: `/rest-auth/registration/`,
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken'),
          'Accept-Language': lang
        },
        credentials: 'same-origin',
        data: {
          username: user.username,
          email: user.email,
          password1: user.password,
          password2: user.password2
        }
    })
  }

  static logout = () => {
    return client({
      method: 'post',
      url: `/rest-auth/logout/`,
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      },
      credentials: 'same-origin',})
      .then(res => sessionStorage.clear());
  }

  static getUserCollectionList = () => {
    return client({
      method: 'get',
      url: `/account/usercollectionitemfavourites/`,
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      },
      credentials: 'same-origin'
    })
  }

  static getUserCollection = () => {
    return client({
      method: 'get',
      url: `/account/usercollectionitemfavourites/show_indexes/`,
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      },
      credentials: 'same-origin'
    })
  }

  static addObjectToCollection = (id) => {
    return client({
      method: 'post',
      url: `/account/usercollectionitemfavourites/`,
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      },
      credentials: 'same-origin',
      data: {
        "collection_item": id
      }})
  }

  static removeObjectFromCollection = (id) => {
    return client({
      method: 'delete',
      url: `/account/usercollectionitemfavourites/${id}/`,
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      },
      credentials: 'same-origin',
      })
  }

  static apiUsage = () => {
    return client({
      method: 'get',
      url: `/account/userapiusage/`,
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      },
      credentials: 'same-origin'
    })
  }

  static imageUpload = (image) => {
    return client({
      method: 'post',
      url: `/account/usersearchimages/`,
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      },
      credentials: 'same-origin',
      data: {
        "image": image
      }
    })
  }

  static getImageResultCollection = (id, page) => {
    const pageNr = (page ? page : 1);
    return client({
      method: 'get',
      url: `/account/usersearchimagefindsimilar/${id}/?page=${pageNr}`,
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      },
      credentials: 'same-origin'
    })
  }

  static getImageResultCollectionWithFacets = (id, filter, page) => {
    const en_facets = '&facet=material_en&facet=primary_object_type_en&facet=object_type_en&facet=city_en&facet=country_en&facet=period_en';
    const nl_facets = '&facet=material_nl&facet=primary_object_type_nl&facet=object_type_nl&facet=city_nl&facet=country_nl&facet=period_nl';
    let facetLang;
    if(sessionStorage.getItem('account')) {
      let userLang = JSON.parse(sessionStorage.getItem('account'));
      if(userLang.account_settings) {
        const lang = userLang.account_settings.language;
        if (lang === 'en') {
          facetLang = en_facets;
        } else {
          facetLang = nl_facets;
        }
      } else {
        facetLang = en_facets;
      }
    } else {
      facetLang = en_facets;
    }

    const pageNrImage = (page ? page : 1);
    let searchFacet = '';
    if(!isEmpty(filter)) {
      searchFacet  = `&${queryString.stringify(filter)}`;
    }
    return client({method: 'get', url: `/api/collectionitem/?page=${pageNrImage}${searchFacet}${facetLang}&user_search_image_id=${id}&ordering=score&page_size=36`});
  }

  static checkoutOrder = (product) => {
    return client({
        method: 'post',
        url: `/subscriptions/orders/checkout/`,
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken')
        },
        credentials: 'same-origin',
        data: {
          product: product,
            amount: 1,
        }
    })
  }


  static passwordReset = (email) => {
    return client({
      method: 'post', 
      url: `/rest-auth/password/reset/`,
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      },
      credentials: 'same-origin',
      data: {
        "email": email
      }})
  }

  static passwordResetConfirm = (new_password1, new_password2, uid, token) => {
    return client({
      method: 'post', 
      url: `/rest-auth/password/reset/confirm/`,
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      },
      credentials: 'same-origin',
      data: {
        "new_password1": new_password1,
        "new_password2": new_password2,
        "uid": uid,
        "token": token
      }})
  }

  static getProdcuts = () => {
    return client({
      method: 'get',
      url: `/subscriptions/products/`,
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      },
      credentials: 'same-origin'
    })
  }

}

