require('skulpt');

function ajax_request(url_name, data, success_function) {
    $.ajax({
        url: '/ajax/' + url_name + '/',
        type: 'POST',
        method: 'POST',
        data: JSON.stringify(data),
        contentType: 'application/json; charset=utf-8',
        headers: { "X-CSRFToken": csrf_token },
        dataType: 'json',
        success: update_gamification
    });
}

function create_alert(type, text) {
    var alert = $('<div>');
    alert.addClass('alert alert-' + type);
    alert.attr('role', 'alert');
    alert.text(text);
    return alert;
}

function clear_submission_feedback() {
    $('#submission_feedback').empty();
}

function update_gamification(data) {
    curr_points = data.curr_points;
    $('#user_points_navbar').innerText = curr_points;
    $("#user_points_navbar").load(location.href + " #user_points_navbar"); // Add space between URL and selector.
    console.log("pointsed")
    badges = data.badges;
    console.log(badges);
    $("#toast-header").innerText = "New badges!";
    $("#toast-body").innerText = badges;
    $("#badge-toast").toast({
        delay: 3000
    });
    console.log("toasted");
}

function display_submission_feedback(test_cases) {
    var container = $('#submission_feedback');
    var total_tests = Object.keys(test_cases).length;
    var total_passed = 0;
    var total_failed = 0;
    for (var id in test_cases) {
        if (test_cases[id].passed) {
            total_passed++;
        } else {
            total_failed++;
        }
    }

    // 1: All tests passed
    if (total_passed == total_tests) {
        text = 'Great work! All the tests passed.';
        container.append(create_alert('success', text));
    } else {
        text = 'Oh no! It seems like some of the tests did not pass. Try to figure out why, and then try again.';
        container.append(create_alert('danger', text));
    }
}

function update_test_case_status(test_case) {
    var test_case_id = test_case.id;
    var expected_output = test_case.expected_output.replace(/\s*$/, '');
    var received_output = test_case.received_output.replace(/\s*$/, '');

    test_case.passed = (received_output === expected_output) && !test_case.runtime_error;

    // Update status cell
    var status_element = $('#test-case-' + test_case_id + '-status');
    var status_text = '';
    if (test_case.passed) {
        status_text = 'Passed'
    } else {
        status_text = 'Failed'
    }
    status_element.text(status_text);

    // Update output cell
    var output_element = $('#test-case-' + test_case_id + '-output');
    output_element.text(received_output);
    if (test_case.runtime_error) {
        output_element.addClass('error')
    } else {
        output_element.removeClass('error')
    }

    // Update row
    var row_element = $('#test-case-' + test_case_id + '-row');
    if (test_case.passed) {
        row_element.addClass('table-success');
        row_element.removeClass('table-danger');
    } else {
        row_element.addClass('table-danger');
        row_element.removeClass('table-success');
    }
}

function run_test_cases(test_cases, user_code, code_function) {
    // Currently runs in sequential order.
    for (var id in test_cases) {
        if (test_cases.hasOwnProperty(id)) {
            var test_case = test_cases[id];
            var code = user_code;
            if (test_case.hasOwnProperty('test_code')) {
                code = code + '\n' + test_case.test_code;
            }
            code_function(code, test_case);
            update_test_case_status(test_case);
        }
    }
    return test_cases;
}


exports.ajax_request = ajax_request;
exports.clear_submission_feedback = clear_submission_feedback;
exports.display_submission_feedback = display_submission_feedback;
exports.update_test_case_status = update_test_case_status;
exports.run_test_cases = run_test_cases;
