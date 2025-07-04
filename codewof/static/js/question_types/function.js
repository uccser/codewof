var base = require('./base.js');
const introJS = require('intro.js');

// Local Variables
let worker = new Worker("/static/js/question_types/pyodide.js");
var test_cases = {};

/* Function to initialize Pyodide and set up stdin
 * For "function" questions, stdin uses JavaScript's prompt function to get input from the user.
 */



$(document).ready(async function () {
    $('#run_code').click(async function () {
         $('#run_code').prop('disabled', true);
        $('#run_code').addClass('disabled');
         $('#run_code').attr('aria-disabled', 'true');
        await run_code(editor, true);
        $('#run_code').prop('disabled', false);
        $('#run_code').removeClass('disabled');
        $('#run_code').attr('aria-disabled', 'false');
    });

    var editor = base.editor;

    for (let i = 0; i < test_cases_list.length; i++) {
        data = test_cases_list[i];
        test_cases[data.id] = data;
    }

    if (editor.getValue()) {
        await run_code(editor, false);
    }

    setTutorialAttributes();
    $("#introjs-tutorial").click(function () {
        introJS().start().onbeforechange(function () {
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

async function run_code(editor, submit) {
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
    test_cases = await base.run_test_cases(test_cases, user_code, run_python_code_pyodide);
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

/*
// This function runs the user's Python code using Pyodide and captures the output.
// It has been marked as async to allow for asynchronous execution - but this has not been implemented yet.
async function run_python_code_pyodide(user_code, test_case) {
    try {
        // Set up stdout redirection in Python
        pyodide.runPython(`
            import sys
            from io import StringIO
            sys.stdout = StringIO()
        `);

        pyodide.runPythonAsync(user_code);

        // Get captured output and reset stdout
        const output = await pyodide.runPythonAsync("sys.stdout.getvalue()");
        await pyodide.runPythonAsync("sys.stdout = sys.__stdout__");
        test_case['received_output'] = output;
        test_case['runtime_error'] = false;
        console.log("Finished running from Pyodide");
    } catch (error) {
        test_case['received_output'] = error.message;
        test_case['runtime_error'] = true;
    }
}
*/
async function run_python_code_pyodide(user_code, test_case) {
    return await new Promise((resolve, reject) => {
        let finished = false;
        let timeoutId = setTimeout(() => {
            if (finished) return;
            finished = true;
            worker.terminate();
            worker = new Worker("/static/js/question_types/pyodide.js");
            test_case['received_output'] = "Timeout: Code execution exceeded 1 second";
            test_case['runtime_error'] = true;
            resolve(undefined); // Resolve the promise after setting the result
        }, 1000);

        worker.onmessage = (event) => {
            if (finished) return;
            finished = true;
            clearTimeout(timeoutId);
            const { output, error } = event.data;
            test_case['received_output'] = output || error;
            test_case['runtime_error'] = !!error;
            resolve(0); // Resolve the promise after setting the result
        };

        worker.onerror = (e) => {
            if (finished) return;
            finished = true;
            clearTimeout(timeoutId);
            test_case['received_output'] = "Worker error: " + e.message;
            test_case['runtime_error'] = true;
            resolve(0);
        };

        worker.postMessage({ user_code });
    });
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
