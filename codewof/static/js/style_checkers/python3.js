var editor;
var CodeMirror = require('codemirror');
require('codemirror/mode/python/python.js');
var ClipboardJS = require('clipboard');
var HIGHLIGHT_CLASS = 'style-highlight';
var result_text = '';


$(document).ready(function () {
    editor = CodeMirror.fromTextArea(document.getElementById('code'), {
        mode: {
            name: 'python',
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
    var CSRF_TOKEN = jQuery('[name=csrfmiddlewaretoken]').val();

    $('#load_example_btn').click(function () {
        reset();
        editor.setValue(EXAMPLE_CODE);
    });

    $('#reset-btn').click(function () {
        reset();
    });

    $('#check_btn').click(function () {
        $('#run-checker-error').hide();
        var user_code = editor.getValue();
        if (user_code.length == 0) {
            $('#run-checker-result').text('No code submitted!');
        } else if (user_code.length > MAX_CHARACTER_COUNT) {
            var message = 'Your file is too long! We accept a maximum of ' + MAX_CHARACTER_COUNT + ' characters, and your code is ' + user_code.length + ' characters.';
            $('#run-checker-result').text(message);
        } else {
            // TODO: Add message how to reset text
            editor.setOption('readOnly', 'nocursor');
            $('.CodeMirror').addClass('read-only');
            $('#run-checker-result').text('Loading...');
            $.ajax({
                url: '/style/ajax/check/',
                type: 'POST',
                method: 'POST',
                data: JSON.stringify({
                    user_code: user_code,
                    language: 'python3',
                }),
                contentType: 'application/json; charset=utf-8',
                headers: { 'X-CSRFToken': CSRF_TOKEN },
                dataType: 'json',
                success: display_style_checker_results,
                error: display_style_checker_error,
            });
        }
    });

    $('#run-checker-result').on('click', 'div[data-line-number]', function () {
        toggle_highlight($(this), true);
    });

    // Clipboard button and event methods

    $('#copy-text-btn').tooltip({
        trigger: 'click',
        animation: true
    });

    function setTooltip(btn, message) {
        $(btn).tooltip('hide')
            .attr('data-original-title', message)
            .tooltip('show');
    }

    function hideTooltip(btn) {
        setTimeout(function () {
            $(btn).tooltip('hide');
        }, 2000);
    }

    var clipboard_button = new ClipboardJS('#copy-text-btn', {
        text: function(trigger) {
            return result_text;
        }
    });

    clipboard_button.on('success', function (e) {
        setTooltip(e.trigger, 'Copied!');
        hideTooltip(e.trigger);
    });

    clipboard_button.on('error', function (e) {
        setTooltip(e.trigger, 'Failed!');
        hideTooltip(e.trigger);
    });

});


function display_style_checker_results(data, textStatus, jqXHR) {
    if (data['success']) {
        $('#run-checker-result').html(data['result_html']);
        result_text = data['result_text'];
        $('#check_btn').hide();
        $('#reset-btn').show();
        $('#copy-text-btn').show();
    } else {
        display_style_checker_error();
    }
}


function display_style_checker_error(jqXHR, textStatus, errorThrown) {
    $('#run-checker-result').html('');
    $('#run-checker-error').show();
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


function reset() {
    editor.setValue('');
    editor.setOption('readOnly', false);
    result_text = '';
    $('#reset-btn').hide();
    $('#run-checker-error').hide();
    $('#copy-text-btn').hide();
    $('.CodeMirror').removeClass('read-only');
    $('#run-checker-result').empty();
    $('#check_btn').show();
}
