var base = require('./base.js');
const introJS = require('intro.js');

var test_cases = {};

$(document).ready(function () {
    $('#run_code').click(function () {
        run_code(editor, true);
    });

    $('#reset_to_initial').click(function () {
        editor.setValue(initial_code);
        mark_lines_as_read_only(editor);
    });

    var editor = base.editor;

    mark_lines_as_read_only(editor);

    for (let i = 0; i < test_cases_list.length; i++) {
        data = test_cases_list[i];
        test_cases[data.id] = data
    }

    if (editor.getValue()) {
        run_code(editor, false);
    }

    setTutorialAttributes();
    $("#introjs-tutorial").click(function() {
        introJS().start().onbeforechange(function() {
            currentElement = $(this._introItems[this._currentStep].element);
            node = currentElement.prop('nodeName');
            // When looking at a full row of the table, force it to scroll to the far left
            // so the highlight only overhangs to the right
            if (node == 'TABLE' || node == 'TR') {
                currentElement = currentElement.find('td:first-of-type')
            }
            containerId = 'table-container';
            base.scroll_to_element(containerId, currentElement);
        });
    });
});


function run_code(editor, submit) {
    base.clear_submission_feedback();
    for (var id in test_cases) {
        if (test_cases.hasOwnProperty(id)) {
            var test_case = test_cases[id];
            test_case.received_output = '';
            test_case.passed = false;
            test_case.runtime_error = false;
        }
    }
    var user_code = editor.getValue();
    if (user_code.includes("\t")) {
        // contains tabs
        $("#indentation-warning").removeClass("d-none");
        return; // do not run tests
    } else {
        $("#indentation-warning").addClass("d-none");
    }
    test_cases = base.run_test_cases(test_cases, user_code, run_python_code);
    if (submit) {
        base.ajax_request(
            'save_question_attempt',
            {
                user_input: user_code,
                question: question_id,
                test_cases: test_cases,
            }
        );
    }
    base.display_submission_feedback(test_cases);
}


function mark_lines_as_read_only(editor) {
    // Lock top lines
    if (read_only_lines_top) {
        // Minus one as line count is zero indexed
        editor.markText(
            { line: 0, ch: 0 },
            { line: read_only_lines_top - 1 },
            {
                readOnly: true,
                className: 'code-read-only',
                atomic: true,
                selectLeft: true,
                inclusiveLeft: true
            }
        );
    }

    // Lock bottom lines
    if (read_only_lines_bottom) {
        var line_count = editor.lineCount();
        // Minus one as line count is zero indexed
        editor.markText(
            { line: line_count - read_only_lines_bottom - 1, ch: 0 },
            { line: line_count - 1 },
            {
                readOnly: true,
                className: 'code-read-only',
                atomic: true,
                selectRight: true,
                inclusiveRight: true
            }
        );
    }
}


function run_python_code(user_code, test_case) {
    // Configure Skulpt for running Python code
    Sk.configure({
        // Setup Skulpt to read internal library files
        read: function (x) {
            if (Sk.builtinFiles === undefined || Sk.builtinFiles["files"][x] === undefined)
                throw "File not found: '" + x + "'";
            return Sk.builtinFiles["files"][x];
        },
        inputfun: function (str) {
            return prompt(str);
        },
        inputfunTakesPrompt: true,
        // Append print() statements for test case
        output: function (received_output) {
            test_case['received_output'] += received_output;
        },
        python3: true,
        execLimit: 1000,
    });
    if (typeof user_code == 'string' && user_code.trim()) {
        try {
            Sk.importMainWithBody("<stdin>", false, user_code, true);
        } catch (error) {
            if (error.hasOwnProperty('traceback')) {
                test_case.received_output = error.toString();
                test_case.runtime_error = true;
            } else {
                throw error;
            }
        }
    } else {
        test_case.received_output = 'No Python code provided.';
        test_case.runtime_error = true;
    }
}


function setTutorialAttributes() {
    $(".question-text").attr(
        'data-intro',
        'This is a description of what the code should do. In debugging questions there will be one or more bugs in the given code that you have to find and correct in order for all the tests to pass.'
    );
    $("#python-editor").attr(
        'data-intro',
        "This is the code that contains the bug(s). Find the bug(s) and correct them. Greyed out lines cannot be edited."
    );
    $("#run_code").attr(
        'data-intro',
        "Clicking this button will run your code against the test cases."
    );
    $("#reset_to_initial").attr(
        'data-intro',
        "Click this button at any time to discard all of your changes."
    );
    $("#test-case-table").attr(
        'data-intro',
        "These are the test cases that have been run against the given code."
    );
    // the first row in the test case table
    $('#test-case-table tbody tr:nth-child(1)').attr(
        'data-intro',
        'Here is the first test case.'
    );
    // the input for the first test case
    $('#test-case-table tbody tr:nth-child(1) td:eq(0)').attr(
        'data-intro',
        'This is the test code that has been run for this particular test.'
    );
    // the expected output for the first test case
    $('#test-case-table tbody tr:nth-child(1) td:eq(1)').attr(
        'data-intro',
        'This is the output that the test code is expected to print.'
    );
    // the received output for the first test case
    $('#test-case-table tbody tr:nth-child(1) td:eq(2)').attr(
        'data-intro',
        'This is the output that has been printed by the test code.'
    );
    // the status of the first test case
    $('#test-case-table tbody tr:nth-child(1) td:eq(3)').attr(
        'data-intro',
        "A test case will pass if the received output matches the expected output. If all test cases pass the question has been solved."
    );
}
