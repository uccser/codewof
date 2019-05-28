
var editor = ace.edit("editor");

var setup_ace = function() {
    editor.setTheme("ace/theme/xcode");
    editor.session.setMode("ace/mode/python");
    editor.setReadOnly(true);
    editor.renderer.setStyle("disabled", true);
    editor.setHighlightActiveLine(false);
    editor.setHighlightGutterLine(false);
    editor.renderer.$cursorLayer.element.style.opacity = 0;
}

var hide_results = function() {
    $('#result-table').addClass('hidden');
    $('#credit').addClass('hidden');
    $('#error').addClass('hidden');
    $('#all-correct').addClass('hidden');
    $('.program-type-analysis').removeClass('hidden');
    $('.function-type-analysis').removeClass('hidden');
}

var display_cross_and_show_error = function(error_message) {
    var cross = "https://png.icons8.com/color/50/000000/close-window.png";
    $("#correctness-img").attr("src", cross);
    $(".program-type-analysis").addClass('hidden');
    $(".function-type-analysis").addClass('hidden');
    $('#result-table').removeClass('hidden');

    $('#error').text(error_message);
    $('#error').removeClass('hidden');
}

var display_table = function(result) {
    var output = JSON.parse(result.output.slice(0, -1));
    var actual_output = output["printed"][0];
    var actual_returned = output["returned"][0];
    var is_correct = output["correct"][0];

    var tick = "https://png.icons8.com/color/50/000000/ok.png";
    var cross = "https://png.icons8.com/color/50/000000/close-window.png";

    var user_input = $("#id_params_input").val();
    var user_stdin = $("#id_debug_input").val();

    if (is_correct == true) {
        $("#correctness-img").attr("src", tick);
        $('#all-correct').removeClass('hidden');
        save_code(user_input + '\n' + user_stdin, true, false, function(result) {});
    } else {
        $("#correctness-img").attr("src", cross);
        save_code(user_input + '\n' + user_stdin, false, false, function(result) {});
    }

    if (actual_output && actual_output.length > 0) {
        $("#program-got").html(actual_output);
    } else {
        if (user_stdin.length < 1) {
            $(".program-type-analysis").addClass('hidden');
        }
    }
    if (actual_returned) {
        $("#function-got").html(actual_returned);
    } else {
        if (!user_input || user_input.length < 1) {
            $(".function-type-analysis").addClass('hidden');
        }
    }
    if (!is_func) {
        $(".function-type-analysis").addClass('hidden');
    }

    $('#result-table').removeClass('hidden');
    $('#credit').removeClass('hidden');
}

var display_results = function(result) {
    $('#loading').addClass('hidden');
    console.log(result);

    if (result.output.length > 0) {
        display_table(result);
    } 
    if (result.stderr.length > 0) {
        display_cross_and_show_error(result.stderr);
    }
    if (result.cmpinfo.length > 0) {
        display_cross_and_show_error(result.cmpinfo);
    }
}

var send_buggy_code = function(result) {
    // receive output
    console.log(result);
    console.log(result.output);
    var output = JSON.parse(result.output.slice(0, -1));
    var expected_print = output["printed"][0];
    var expected_return = output["returned"][0];

    // send buggy as normal but with single test case: user_input -> solution output
    var user_input = $("#id_params_input").val();
    var user_stdin = $("#id_debug_input").val();

    // load input and expected values into table
    $("#function-inp").html(user_input);
    $("#program-inp").html(user_stdin);
    if (expected_return) {
        $("#function-exp").html(expected_return);
    }
    if (expected_print){
        $("#program-exp").html(expected_print);
    }

    var data = {
        user_input: user_input,
        buggy_stdin: user_stdin,
        expected_print: expected_print,
        expected_return: expected_return,
        question: question_id
    }
    post('send_code', data, function (result) {
        if (result.error) {
            $('#error').text(result.error);
            $('#error').removeClass('hidden');            
        } else {
            var submission_id = result.id;
            console.log(submission_id);
            $('#loading').removeClass('hidden');
            hide_results();
            poll_until_completed(submission_id, display_results);
        }
    });
}

var check_for_errors = function(result) {
    $('#loading').addClass('hidden');

    if (result.output.length > 0) {
        send_buggy_code(result);
    }
    if (result.stderr.length > 0) {
        display_cross_and_show_error(result.stderr);
    }
    if (result.cmpinfo.length > 0) {
        display_cross_and_show_error(result.cmpinfo);
    }
}

$("#submit").click(function () {
    // send solution with user input to get expected output
    var user_input = $("#id_params_input").val();
    var user_stdin = $("#id_debug_input").val();

    var data = {
        user_input: user_input,
        buggy_stdin: user_stdin,
        question: question_id
    }
    post('send_solution', data, function(result) {
        if (result.error) {
            $('#error').text(result.error);
            $('#error').removeClass('hidden'); 
        } else {
            var submission_id = result.id;
            console.log(submission_id);
            $('#loading').removeClass('hidden');
            hide_results();
            poll_until_completed(submission_id, check_for_errors);
        }
    });
});

$('#show_solution').click(function () {
    $('#solution').html(solution);
    $('#show_solution').addClass('hidden');
});

setup_ace();