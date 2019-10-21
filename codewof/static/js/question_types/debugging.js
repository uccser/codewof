var base = require('./base.js');
var CodeMirror = require('codemirror');
require('codemirror/mode/python/python.js');

var test_cases = {};

$(document).ready(function () {
    $('#run_code').click(function () {
        run_code(editor, true);
    });

    $('#reset_to_initial').click(function () {
        editor.setValue(initial_code);
        mark_lines_as_read_only(editor);
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
        // Replace tabs with 4 spaces. Taken from https://stackoverflow.com/questions/15183494/codemirror-tabs-to-spaces
        extraKeys: {
            "Tab": function(cm) {
                cm.replaceSelection("    ", "end");
            }
        }
    });

    mark_lines_as_read_only(editor);

    for (let i = 0; i < test_cases_list.length; i++) {
        data = test_cases_list[i];
        test_cases[data.id] = data
    }

    if (editor.getValue()) {
        run_code(editor, false);
    }
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
    console.log(user_code);
    user_code = user_code.replace(/(.*?)\t/gm, "    ");
    console.log(user_code);
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
