require('skulpt');
var CodeMirror = require('codemirror');
require('codemirror/mode/python/python.js');

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

    point_diff = parseInt(data.point_diff);
    if (point_diff > 0) {
        $("#point_toast_header").text("Points earned!");
        $("#point_toast_body").text("You earned " + point_diff.toString() +" points!");
        $(document).ready(function(){
            $("#point_toast").toast('show', {delay: 8000});
        });
    }

    achievements = data.achievements;
    if (achievements.length > 0){
        $("#achievement_toast_header").text("New achievements!");
        $("#achievement_toast_body").text(achievements);
        $(document).ready(function(){
            $("#achievement_toast").toast('show', {delay: 8000});
        });
    }

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

function update_test_case_status(test_case, user_code) {
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
    var output_element_help_text = $('#test-case-' + test_case_id + '-output-help-text');
    output_element.text(received_output);
    if (test_case.runtime_error) {
        output_element.addClass('error')
        // the following is implemented because of https://github.com/uccser/codewof/issues/351
        regex_match = /line (\d+)/.exec(received_output) // looking for line number
        if (regex_match !== null) {
            error_line_number = regex_match[1] // first capture group - should be the line number
            num_user_code_lines = user_code.split('\n').length; // number of lines in the users code
            if (error_line_number > num_user_code_lines) {
                output_element_help_text.removeClass('d-none');
            }
        }
    } else {
        output_element.removeClass('error')
        output_element_help_text.addClass('d-none');
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
            update_test_case_status(test_case, user_code);
        }
    }
    return test_cases;
}

function scroll_to_element(containerId, element) {
    // For use by the tutorials
    var container = $('#' + containerId);
    var contWidth = container.width();
    var contLeft = container.offset().left;
    var elemLeft = $(element).offset().left - contLeft; // wrt container
    var elemWidth = element.width();
    var isInView = elemLeft >= 0 && (elemLeft + elemWidth) <= contWidth;

    if (!isInView) {
        container.scrollLeft(0);
        var scrollTo = $(element).offset().left - contLeft;
        container.scrollLeft(scrollTo);
    }
}

function create_new_editor(containerId) {
    // Allows pages to have multiple editors
    return CodeMirror.fromTextArea(document.getElementById(containerId), {
        mode: {
            name: "python",
            version: 3,
            singleLineStringErrors: false
        },
        lineNumbers: true,
        textWrapping: false,
        styleActiveLine: true,
        autofocus: true,
        indentUnit: 4,
        viewportMargin: Infinity,
        // Replace tabs with 4 spaces, and remove all 4 when deleting if possible.
        // Taken from https://stackoverflow.com/questions/15183494/codemirror-tabs-to-spaces and
        // https://stackoverflow.com/questions/32622128/codemirror-how-to-read-editor-text-before-or-after-cursor-position
        extraKeys: {
            "Tab": function(cm) {
                cm.replaceSelection("    ", "end");
            },
            "Backspace": function(cm) {
                doc = cm.getDoc();
                line = doc.getCursor().line;   // Cursor line
                ch = doc.getCursor().ch;       // Cursor character

                if (doc.somethingSelected()) {  // Remove user-selected characters
                    doc.replaceSelection("");
                } else {    // Determine the ends of the selection to delete
                    from = {line, ch};
                    to = {line, ch};
                    stringToTest = doc.getLine(line).substr(Math.max(ch - 4,0), Math.min(ch, 4));

                    if (stringToTest === "    ") {  // Remove 4 spaces (dedent)
                        from = {line, ch: ch - 4};
                    } else if (ch == 0) {   // Remove last character of previous line
                        if (line > 0) {
                            from = {line: line - 1, ch: doc.getLine(line - 1).length};
                        }
                    } else {    // Remove preceding character
                        from = {line, ch: ch - 1};
                    }

                    // Delete the selection
                    doc.replaceRange("", from, to);
                }
            },
            "Delete" : function(cm) {
                doc = cm.getDoc();
                line = doc.getCursor().line;   // Cursor line
                ch = doc.getCursor().ch;       // Cursor character

                if (doc.somethingSelected()) {  // Remove user-selected characters
                    doc.replaceSelection("");
                } else {    // Determine the ends of the selection to delete
                    from = {line, ch};
                    to = {line, ch};
                    stringToTest = doc.getLine(line).substr(ch, 4);

                    if (stringToTest === "    ") {  // Remove 4 spaces (dedent)
                        to = {line, ch: ch + 4};
                    } else if (ch == doc.getLine(line).length) {   // Remove first character of next line
                        if (line < doc.size - 1) {
                            to = {line: line + 1, ch: 0};
                        }
                    } else {    // Remove following character
                        to = {line, ch: ch + 1};
                    }

                    // Delete the selection
                    doc.replaceRange("", from, to);
                }
            }
        }
    });
}

exports.ajax_request = ajax_request;
exports.clear_submission_feedback = clear_submission_feedback;
exports.display_submission_feedback = display_submission_feedback;
exports.update_test_case_status = update_test_case_status;
exports.run_test_cases = run_test_cases;
exports.scroll_to_element = scroll_to_element;
exports.create_new_editor = create_new_editor;