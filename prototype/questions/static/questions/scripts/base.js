
var post = function(url, data, success_function) {
    data.csrfmiddlewaretoken = window.CSRF_TOKEN;
    $.ajax({
        url: '/ajax/' + url + '/',
        type: 'POST',
        method: 'POST',
        data: data,
        dataType: 'json',
        success: success_function
    });
}