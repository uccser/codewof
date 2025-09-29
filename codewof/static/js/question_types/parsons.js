var base = require('./base.js');
var Sortable = require('sortablejs');
const introJS = require('intro.js');

// Local Variables
var test_cases = {};
var indent_increment = '    ';


$(document).ready(async function(){
    var all_sortables = document.getElementsByClassName('parsons-drag-container');
    $('#run_code').prop('disabled', true);
    $('#run_code').addClass('disabled');
    $('#run_code').attr('aria-disabled', 'true');
    await base.waitForWorkerReady();
    $('#run_code').prop('disabled', false);
    $('#run_code').removeClass('disabled');
    $('#run_code').attr('aria-disabled', 'false');
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

    $('#run_code').click(async function () {
        // disable the button to prevent multiple clicks
        $('#run_code').prop('disabled', true);
        $('#run_code').addClass('disabled');
        $('#run_code').attr('aria-disabled', 'true');
        // Run the code
        await run_code(true);
        // Re-enable the button after running the code
        $('#run_code').prop('disabled', false);
        $('#run_code').removeClass('disabled');
        $('#run_code').attr('aria-disabled', 'false');
    });

    for (let i = 0; i < test_cases_list.length; i++) {
        data = test_cases_list[i];
        test_cases[data.id] = data
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

async function run_code(submit) {
    await base.clear_submission_feedback();
    for (var id in test_cases) {
        if (test_cases.hasOwnProperty(id)) {
            var test_case = test_cases[id];
            test_case.received_output = '';
            test_case.passed = false;
            test_case.runtime_error = false;
        }
    }
    var user_code = get_user_code();
    test_cases = await base.run_test_cases(test_cases, user_code, base.run_python_code_pyodide);
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

function setTutorialAttributes() {
    $(".question-text").attr(
        'data-intro',
        'This is a description of what the code should do. It will tell you what your code should return (or print) for certain inputs.\
        Pay close attention to whether your code should return or print a value!'
    );
    $("#available-lines").attr(
        'data-intro',
        "These are the lines you can choose from to build your solution. Drag and drop the lines you want into the 'Your solution' box. Not all lines may be needed for the solution."
    );
    $("#user-code-lines").attr(
        'data-intro',
        "This is where you will drop lines from the 'Available lines' section to build your solution. This is the code that will be run against the test cases."
    );
    $("#run_code").attr(
        'data-intro',
        "Clicking this button will run your code against the test cases."
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
        'This is the test code that is run for this particular test.'
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
