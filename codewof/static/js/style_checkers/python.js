var editor;
var CodeMirror = require('codemirror');
require('codemirror/mode/python/python.js');

var HIGHLIGHT_CLASS = 'style-highlight';
var EXAMPLE_CODE = `def fizzbuzz():
    for i in range(1 ,100):
        if i % 3 == 0 and i % 5 == 0 :
            print("FizzBuzz")
        elif i%3 == 0:
            print( "Fizz")
        elif  i % 5==0:
             print("Buzz")

        else:
            print(i)`;

$(document).ready(function () {
    editor = CodeMirror.fromTextArea(document.getElementById("code"), {
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
        viewportMargin: Infinity
    });
    var CSRF_TOKEN = jQuery("[name=csrfmiddlewaretoken]").val();

    $('#load_example_btn').click(function () {
        clear();
        editor.setValue(EXAMPLE_CODE);
    });

    $('#clear_btn').click(function () {
        clear();
    });

    $('#check_btn').click(function () {
        $('#run-checker-result').text('Loading...');
        $.ajax({
            url: '/style/ajax/check/',
            type: 'POST',
            method: 'POST',
            data: JSON.stringify({
                user_code: editor.getValue(),
                language: 'python3',
            }),
            contentType: 'application/json; charset=utf-8',
            headers: { 'X-CSRFToken': CSRF_TOKEN },
            dataType: 'json',
            success: display_style_checker_results,
        });
    });

    $('#run-checker-result').on('click', 'div[data-line-number]', function () {
        toggle_highlight($(this), true);
    });
});


function display_style_checker_results(data, textStatus, jqXHR) {
    $('#run-checker-result').html(data['feedback_html']);
}


function toggle_highlight(issue_button, remove_existing) {
    var line_number = issue_button.data('line-number') - 1;
    if (issue_button.hasClass(HIGHLIGHT_CLASS)) {
        editor.removeLineClass(line_number, 'background', HIGHLIGHT_CLASS);
        issue_button.removeClass(HIGHLIGHT_CLASS);
    } else {
        // Remove existing highlights
        if (remove_existing) {
            $('div[data-line-number].' + HIGHLIGHT_CLASS).each(function () {
                toggle_highlight($(this), false);
            });
        }
        issue_button.addClass(HIGHLIGHT_CLASS);
        editor.addLineClass(line_number, 'background', HIGHLIGHT_CLASS);
    }
}


function clear() {
    editor.setValue("");
    $('#run-checker-result').empty();
}
