
var poll_until_completed = function(id, on_completed) {
    var data = {
        id: id,
        question: question_id
    }
    post('get_output', data, function(result) {
        if (result.completed) {
            on_completed(result);
        } else {
            poll_until_completed(id, on_completed);
        }
    });
}

var save_code = function(user_code, passed_tests, is_save, success) {
    var data = {
        user_input: user_code,
        question: question_id,
        passed_tests: passed_tests,
        is_save: is_save
    }
    post('save_attempt', data, success);
}