module.exports = function(data, filename, mime) {
    var blob = new Blob([data], {type: mime || 'application/octet-stream'});
    var tempLink = document.createElement('a');
    tempLink.style.display = 'none';
    tempLink.href = data;
    tempLink.setAttribute('download', filename); 

    if (typeof tempLink.download === 'undefined') {
        tempLink.setAttribute('target', '_blank');
    }

    document.body.appendChild(tempLink);
    tempLink.click();
    document.body.removeChild(tempLink);
    window.URL.revokeObjectURL(data);
}