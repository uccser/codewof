
var post = function(url, data, success_function) {
    //sdata.csrfmiddlewaretoken = window.CSRF_TOKEN;
    $.ajax({
        url: '/ajax/' + url + '/',
        type: 'POST',
        method: 'POST',
        data: JSON.stringify(data),
        contentType: 'application/json; charset=utf-8',
        headers: { "X-CSRFToken": window.CSRF_TOKEN },
        dataType: 'json',
        success: success_function
    });
}