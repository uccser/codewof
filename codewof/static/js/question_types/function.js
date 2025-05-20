var base = require('./base.js');
const introJS = require('intro.js');
let pyodide;
var test_cases = {};

async function initializePyodide() {
    pyodide = await loadPyodide();
    pyodide.setStdin({
        stdin: (str) => {return prompt(str)},
    });
}


$(document).ready(function () {
    $('#run_code').click(function () {
        if (!pyodide) {
            initializePyodide().then(() => {
                run_code(editor, true);
            });
        } else {
            run_code(editor, true);
        }
    });

    var editor = base.editor;

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
    test_cases = base.run_test_cases(test_cases, user_code, run_python_code_pyodide);
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

async function run_python_code_pyodide(user_code, test_case) {
    try {

        // Redirect standard output to capture print statements
        pyodide.runPython(`
            import sys
            from io import StringIO
            sys.stdout = StringIO()
        `);

        // Execute the user's code
        pyodide.runPython(user_code);

        // Get captured output and reset stdout
        const output = pyodide.runPython("sys.stdout.getvalue()");
        pyodide.runPython("sys.stdout = sys.__stdout__");

        test_case['received_output'] = output;
        test_case['runtime_error'] = false;
    } catch (error) {
        // Handle Python exceptions
        test_case['received_output'] = error.message;
        test_case['runtime_error'] = true;
    }
}

// async function run_python_code_pyodide(user_code, test_case) {
    // try {

    //     // Redirect standard output to capture print statements
    //     pyodide.runPython(`
    //         import sys
    //         from io import StringIO
    //         sys.stdout = StringIO()
    //     `);

    //     // Execute the user's code
    //     pyodide.runPython(user_code);

    //     // Get captured output and reset stdout
    //     const output = pyodide.runPython("sys.stdout.getvalue()");
    //     pyodide.runPython("sys.stdout = sys.__stdout__");

    //     test_case['received_output'] = output;
    //     test_case['runtime_error'] = false;
    // } catch (error) {
    //     // Handle Python exceptions
    //     test_case['received_output'] = error.message;
    //     test_case['runtime_error'] = true;
    // }
// }

// function run_python_code(user_code, test_case) {
//     // Configure Skulpt for running Python code
//     Sk.configure({
//         // Setup Skulpt to read internal library files
//         read: function (x) {
//             if (Sk.builtinFiles === undefined || Sk.builtinFiles["files"][x] === undefined)
//                 throw "File not found: '" + x + "'";
//             return Sk.builtinFiles["files"][x];
//         },
//         inputfun: function (str) {
//             return prompt(str);
//         },
//         inputfunTakesPrompt: true,
//         // Append print() statements for test case
//         output: function (received_output) {
//             test_case['received_output'] += received_output;
//         },
//         python3: true,
//         execLimit: 1000,
//     });
//     if (typeof user_code == 'string' && user_code.trim()) {
//         try {
//             Sk.importMainWithBody("<stdin>", false, user_code, true);
//         } catch (error) {
//             if (error.hasOwnProperty('traceback')) {
//                 test_case.received_output = error.toString();
//                 test_case.runtime_error = true;
//             } else {
//                 throw error;
//             }
//         }
//     } else {
//         test_case.received_output = 'No Python code provided.';
//         test_case.runtime_error = true;
//     }
// }

// function run_python_code_pyodide(user_code, test_case) {
//     console.log("Running Python code with timeout...");
//     runPythonWithTimeout(user_code, 2000)
//         .then(result => {
//             console.log("Result:", result);
//             test_case['received_output'] = result;
//             test_case['runtime_error'] = false;
//         })
//         .catch(err => {
//             console.error("Error:", err.message)
//             // Handle Python exceptions
//             test_case['received_output'] = err.message;
//             test_case['runtime_error'] = true;
//         });
// }

// function runPythonWithTimeout(code, timeoutMs = 2000) {
//   return new Promise((resolve, reject) => {
//     let finished = false;

//     // Listen for worker messages
//     pyodideWorker.onmessage = (event) => {
//       finished = true;
//       if (event.data.error) {
//         reject(new Error(event.data.error));
//       } else {
//         resolve(event.data.result);
//       }
//     };

//     // Start code execution
//     pyodideWorker.postMessage({ cmd: "runCode", code });

//     // Setup timeout to interrupt execution
//     setTimeout(() => {
//       if (!finished) {
//         // 2 stands for SIGINT (KeyboardInterrupt)
//         interruptBuffer[0] = 2;
//         reject(new Error("Execution timed out and was interrupted."));
//       }
//     }, timeoutMs);
//   });
// }


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
