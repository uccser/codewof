var editor = ace.edit("editor");

var setup_ace = function() {
    editor.setTheme("ace/theme/xcode");
    editor.session.setMode("ace/mode/python");
}

var hide_results = function() {
    $('#result-table').addClass('hidden');
    $('#credit').addClass('hidden');
    $('#error').addClass('hidden');
    $('#all-correct').addClass('hidden');
    $('#has_saved').addClass('hidden');
    $('.program-type-analysis').removeClass('hidden');
    $('.function-type-analysis').removeClass('hidden');
}

var save_code = function(passed_tests, is_save) {
    var user_input = editor.getValue();

    var data = {
        user_input: user_input,
        question: question_id,
        passed_tests: passed_tests,
        is_save: is_save
    }
    var success = function(result) {
        $('#has_saved').removeClass('hidden');
        setTimeout(() => {$('#has_saved').addClass('hidden')}, 2000);
    }
    post('save_attempt', data, success);
}

var display_table = function(result) {
    var output = JSON.parse(result.output.slice(0, -1));
    var got_output_array = output["printed"];
    var got_return_array = output["returned"];
    var correctness_array = output["correct"];

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

    $('#result-table').removeClass('hidden');
    $('#credit').removeClass('hidden');
    
    if (all_correct) {
        $('#all-correct').removeClass('hidden');
        save_code(true, false);
    } else {
        save_code(false, false);
    }
    if (!has_print_contents) {
        $(".program-type-analysis").addClass('hidden');
    }
    if (!has_return_contents) {
        $(".function-type-analysis").addClass('hidden');
    }
}

var poll_sphere_engine = function(id) {
    var data = {
        id: id,
        question: question_id
    }
    var success = function(result) {
        if (result.completed) {     
            $('#loading').addClass('hidden');

            if (result.output.length > 0) {
                display_table(result);
            } 
            if (result.stderr.length > 0) {
                $('#error').text(result.stderr);
                $('#error').removeClass('hidden');
                save_code(false, false);
            }
            if (result.cmpinfo.length > 0) {
                $('#error').text(result.cmpinfo);
                $('#error').removeClass('hidden');
                save_code(false, false);
            }
        } else {
            poll_sphere_engine(id);
        }
    }
    post('get_output', data, success);
}

$("#submit").click(function () {
    var user_input = editor.getValue();

    var data = {
        user_input: user_input,
        question: question_id
    }
    var success = function (result) {
        var submission_id = result.id;
        console.log(submission_id);
        $('#loading').removeClass('hidden');
        hide_results();
        poll_sphere_engine(submission_id);
    }
    post('send_code', data, success);
});

$('#save').click(function () {
    save_code(false, true);
});

$('#show_solution').click(function () {
    $('#solution').html(solution);
    $('#show_solution').addClass('hidden');
});

setup_ace();