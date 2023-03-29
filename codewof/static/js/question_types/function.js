var base = require('./base.js');
var CodeMirror = require('codemirror');
require('codemirror/mode/python/python.js');
const introJS = require('intro.js');

var test_cases = {};

$(document).ready(function () {
    $('#run_code').click(function () {
        run_code(editor, true);
    });

    var editor = CodeMirror.fromTextArea(document.getElementById("code"), {
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
        'This is a description of what the function should do. It will tell you what your function should return (or print) in order to pass the tests.\
        Pay close attention to whether your function should return or print a value!'
    );
    $("#python-editor").attr(
        'data-intro',
        "This is where you enter your code to solve the problem."
    );
    $("#run_code").attr(
        'data-intro',
        "Clicking this button will run your code against the test cases."
    );
    $("#test-case-table").attr(
        'data-intro',
        "These are the test cases that will be run against your function."
    );
    // the first row in the test case table
    $('#test-case-table tbody tr:nth-child(1)').attr(
        'data-intro',
        'Here is the first test case.'
    );
    // the input for the first test case
    $('#test-case-table tbody tr:nth-child(1) td:eq(0)').attr(
        'data-intro',
        'This is the test code that is run for this particular test. Pay close attention to the input that is passed to the function.'
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
