
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
    $('#all-correct').addClass('hidden');
    $('.program-type-analysis').removeClass('hidden');
    $('.function-type-analysis').removeClass('hidden');
}

var save_code = function(passed_tests, is_save) {
    var user_input = editor.getValue();

    $.ajax({
        url: '/ajax/save_attempt/',
        type: 'POST',
        method: 'POST',
        data: {
            user_input: user_input,
            question: question_id,
            passed_tests: passed_tests,
            is_save: is_save,
            csrfmiddlewaretoken: csrf_token
        },
        dataType: 'json',
        success: function(result) { }
    });
}

var poll_sphere_engine = function(id) {
    $.ajax({
        url: '/ajax/get_output/',
        type: 'POST',
        method: 'POST',
        data: {
            id: id,
            question: question_id,
            csrfmiddlewaretoken: csrf_token
        },
        dataType: 'json',
        success: function(result) {
            // TODO move to separate function and test still works
            console.log(result);
            if (result.completed) {
                
                $('#loading').addClass('hidden');

                if (result.output.length > 0) {
                    var output = JSON.parse(result.output.slice(0, -1));
                    var actual_output = output["printed"][0];
                    var actual_returned = output["returned"][0];
                    var is_correct = output["correct"][0];

                    var tick = "https://png.icons8.com/color/50/000000/ok.png";
                    var cross = "https://png.icons8.com/color/50/000000/close-window.png";

                    if (is_correct == true) {
                        $("#correctness-img").attr("src", tick);
                        $('#all-correct').removeClass('hidden');
                        save_code(true, false);
                    } else {
                        $("#correctness-img").attr("src", cross);
                        save_code(false, false);
                    }

                    if (actual_output && actual_output.length > 0) {
                        $("#program-got").html(actual_output);
                    } else {
                        $(".program-type-analysis").addClass('hidden');
                    }

                    if (actual_returned) {
                        $("#function-got").html(actual_returned);
                    } else {
                        $(".function-type-analysis").addClass('hidden');
                    }

                    $('#result-table').removeClass('hidden');
                    $('#credit').removeClass('hidden');
                } 
                if (result.stderr.length > 0) {
                    console.log(result.stderr);
                }
                if (result.cmpinfo.length > 0) {
                    console.log(result.cmpinfo);
                }
            } else {
                poll_sphere_engine(id);
            }
        }
    });
}


var poll_sphere_engine_no_display = function(id) {
    $.ajax({
        url: '/ajax/get_output/',
        type: 'POST',
        method: 'POST',
        data: {
            id: id,
            question: question_id,
            csrfmiddlewaretoken: csrf_token
        },
        dataType: 'json',
        success: function(result) {
            if (result.completed) {
                // receive output
                var output = JSON.parse(result.output.slice(0, -1));
                var expected_print = output["expected_print"][0];
                var expected_return = output["expected_return"][0];

                console.log(expected_print);
                console.log(expected_return);
                if (expected_print === null) {
                    expected_print = 'None'
                }
                if (expected_return === null) {
                    expected_return = 'None'
                }

                // send buggy as normal but with single test case: user_input -> solution output
                var user_input = $("#id_debug_input").val();

                $("#function-inp").html(user_input);
                $("#program-inp").html(user_input);

                $("#function-exp").html(expected_return);    
                $("#program-exp").html(expected_print);

                $.ajax({
                    url: '/ajax/send_code/',
                    type: 'POST',
                    method: 'POST',
                    data: {
                        user_input: user_input,
                        expected_print: expected_print,
                        expected_return: expected_return,
                        question: question_id,
                        csrfmiddlewaretoken: csrf_token
                    },
                    dataType: 'json',
                    success: function (result) {
                        var submission_id = result.id;
                        console.log(submission_id);
                        $('#loading').removeClass('hidden');
                        hide_results();
                        poll_sphere_engine(submission_id);
                    }
                });
            } else {
                poll_sphere_engine_no_display(id);
            }
        }
    });
}

$("#submit").click(function () {

    if (buggy_program) {
        // send solution with user input to get expected output
        var user_input = $("#id_debug_input").val();

        $.ajax({
            url: '/ajax/send_solution/',
            type: 'POST',
            method: 'POST',
            data: {
                user_input: user_input,
                question: question_id,
                csrfmiddlewaretoken: csrf_token
            },
            dataType: 'json',
            success: function(result) {
                var submission_id = result.id;
                console.log(submission_id);
                $('#loading').removeClass('hidden');
                hide_results();
                poll_sphere_engine_no_display(submission_id);
            }
        });

    } else {
        var user_input = editor.getValue();

        $.ajax({
            url: '/ajax/send_code/',
            type: 'POST',
            method: 'POST',
            data: {
                user_input: user_input,
                question: question_id,
                csrfmiddlewaretoken: csrf_token
            },
            dataType: 'json',
            success: function (result) {
                var submission_id = result.id;
                console.log(submission_id);
                $('#loading').removeClass('hidden');
                hide_results();
                poll_sphere_engine(submission_id);
            }
        });
    }
});

$('#show_solution').click(function () {
    $('#solution').html(solution);
    $('#show_solution').addClass('hidden');
});

setup_ace();