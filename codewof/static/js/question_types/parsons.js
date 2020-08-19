var base = require('./base.js');
var Sortable = require('sortablejs');
const introJS = require('intro.js');

var test_cases = {};
var indent_increment = '    ';

$(document).ready(function(){
    var all_sortables = document.getElementsByClassName('parsons-drag-container');
    Array.prototype.forEach.call(all_sortables, function (element) {
        new Sortable(element, {
            group: 'parsons', // set both lists to same group
            animation: 150,
            swapThreshold: 0.4,
            fallbackOnBody: true,
            onStart: function (event) {
                $('.parsons-drag-top-container').addClass('dragging');
            },
            onEnd: function (event) {
                $('.parsons-drag-top-container').removeClass('dragging');
            },
        });
    });

    $('#run_code').click(function () {
        run_code(true);
    });

    for (let i = 0; i < test_cases_list.length; i++) {
        data = test_cases_list[i];
        test_cases[data.id] = data
    }

    setTutorialAttributes();
    $("#introjs-tutorial").click(function() {
        introJS.introJs().start();
    });
});

function run_code(submit) {
    base.clear_submission_feedback();
    for (var id in test_cases) {
        if (test_cases.hasOwnProperty(id)) {
            var test_case = test_cases[id];
            test_case.received_output = '';
            test_case.passed = false;
            test_case.runtime_error = false;
        }
    }
    var user_code = get_user_code();
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

function get_user_code() {
    var indent = '';
    var code = '';
    var top_element = $('#user-code-lines');
    code = traverse_code_container(top_element, indent, true);
    return code;
}

function traverse_code_container(container, indent, is_top) {
    var container_code = '';
    var lines = container.children('.parsons-draggable-line');
    if (lines.length > 0) {
        if (!is_top) {
            indent += indent_increment;
        }
        lines.each(function() {
            var line = $(this);
            var line_code = line.children('.parsons-line-content').text().trim();
            container_code += indent + line_code + '\n';
            var line_container = line.children('.parsons-drag-container');
            container_code += traverse_code_container(line_container, indent, false);
        });
        if (!is_top) {
            indent = indent.substring(0, indent_increment.length);
        }
    }
    return container_code;
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
        'This is the question you will be solving. It will tell you what your code should return (or print) for certain inputs.'
    );
    $("#available-lines").attr(
        'data-intro',
        "These are the lines you can choose from to build your solution. Drag and drop the lines you want into the 'Your solution' box. Not all lines may be needed for the solution."
    );
    $("#user-code-lines").attr(
        'data-intro',
        "This is where you will drop lines from the 'Available lines' section to build your solution. This is the code that will be run against the test cases when you click the 'Run code' button."
    );
    $("#test-case-table").attr(
        'data-intro',
        "These are the test cases that will be run against your code."
    );
    // the first row in the test case table
    $('#test-case-table tbody tr:nth-child(1)').attr(
        'data-intro',
        'Here is the first test case.'
    );
    // the input for the first test case
    $('#test-case-table tbody tr:nth-child(1) td:eq(0)').attr(
        'data-intro',
        'This is how your code will be called for this particular test.'
    );
    // the expected output for the first test case
    $('#test-case-table tbody tr:nth-child(1) td:eq(1)').attr(
        'data-intro',
        'This is the output that the test expects your code to return (or print) for the given input.'
    );
    // the received output for the first test case
    $('#test-case-table tbody tr:nth-child(1) td:eq(2)').attr(
        'data-intro',
        'This is the output that your code has returned (or printed) for the given input.'
    );
    // the status of the first test case
    $('#test-case-table tbody tr:nth-child(1) td:eq(3)').attr(
        'data-intro',
        "This is the status of the test. It will say one of three things: 'Not yet run', 'Passed' or 'Failed'.\
        'Not yet run' means your code has not yet been run against the test case.\
        'Passed' means the received output matched the expected output. The test case has passed.\
        'Failed' means the received output did not match the expected output. The test case has failed."
    );
}
