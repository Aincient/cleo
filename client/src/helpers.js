var hasOwnProperty = Object.prototype.hasOwnProperty;

export function isEmpty(obj) {

    // null and undefined are "empty"
    if (obj == null) return true;

    // Assume if it has a length property with a non-zero value
    // that that property is correct.
    if (obj.length > 0)    return false;
    if (obj.length === 0)  return true;

    // If it isn't an object at this point
    // it is empty, but it can't be anything *but* empty
    // Is it empty?  Depends on your application.
    if (typeof obj !== "object") return true;

    // Otherwise, does it have any properties of its own?
    // Note that this doesn't handle
    // toString and valueOf enumeration bugs in IE < 9
    for (var key in obj) {
        if (hasOwnProperty.call(obj, key)) return false;
    }

    return true;
}

export function generateKey(pre) {
    return `${ pre }_${ new Date().getTime() }`;
}

export function getPrevObj(id, objects) {
    if(id && objects) {
        return objects.findIndex(x=> x.id === id) -1;
    }
}

export function getNextObj(id, objects) {
    if(id && objects) {
        return objects.findIndex(x=> x.id === id) +1;
    }
}

export function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
        let cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
        }
        }
    }
    return cookieValue;
}

export function round(number_string){
    let number = (Math.round(parseFloat(number_string) * 10000)/100).toFixed(2);

    if (number === '100.00'){
        return '99.99';
    }

    return number;
}