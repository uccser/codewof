var editor = ace.edit("editor");

var setup_ace = function() {
    editor.setTheme("ace/theme/xcode");
    editor.session.setMode("ace/mode/python");
}

var hide_results = function() {
    $('#result-table').hide();
    $('#credit').hide();
    $('#error').hide();
    $('#all-correct').hide();
    $('#has_saved').hide();
    $('.program-type-analysis').show();
    $('.function-type-analysis').show();
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
        success: function(result) {
            $('#has_saved').show();
            setTimeout(() => {$('#has_saved').hide()}, 2000);
        }
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
                
                $('#loading').hide();

                if (result.output.length > 0) {
                    var output = JSON.parse(result.output.slice(0, -1));
                    var got_output_array = output["printed"];
                    var got_return_array = output["returned"];
                    var correctness_array = output["correct"];
                    console.log(correctness_array);

                    var all_correct = true;
                    var has_print_contents = false;
                    var has_return_contents = false;
                    var tick = "https://png.icons8.com/color/50/000000/ok.png";
                    var cross = "https://png.icons8.com/color/50/000000/close-window.png";

                    for (var i = 0; i < correctness_array.length; i++) {
                        if (correctness_array[i] == false) {
                            all_correct = false;
                            $("#correctness-img" + i).attr("src", cross);
                        } else {
                            $("#correctness-img" + i).attr("src", tick);
                        }
                        if (got_output_array[i] && got_output_array[i].length > 0) {
                            has_print_contents = true;
                            $("#program-got" + i).html(got_output_array[i]);
                        }
                        console.log(got_return_array);
                        if (got_return_array[i]) {
                            has_return_contents = true;
                            $("#function-got" + i).html(got_return_array[i]);
                        }
                    }

                    $('#result-table').show();
                    $('#credit').show();
                    
                    if (all_correct) {
                        $('#all-correct').show();
                        save_code(true, false);
                    } else {
                        save_code(false, false);
                    }
                    if (!has_print_contents) {
                        $(".program-type-analysis").hide();
                    }
                    if (!has_return_contents) {
                        $(".function-type-analysis").hide();
                    }
                } 
                if (result.stderr.length > 0) {
                    $('#error').text(result.stderr);
                    $('#error').show();
                    save_code(false, false);
                }
                if (result.cmpinfo.length > 0) {
                    $('#error').text(result.cmpinfo);
                    $('#error').show();
                    save_code(false, false);
                }
            } else {
                poll_sphere_engine(id);
            }
        }
    });
}

$("#submit").click(function () {
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
            $('#loading').show();
            hide_results();
            poll_sphere_engine(submission_id);
        }
    });
});

$('#save').click(function () {
    save_code(false, true);
});

$('#show_solution').click(function () {
    $('#solution').html(solution);
    $('#show_solution').hide();
});

$('#loading').hide();
hide_results();
setup_ace();