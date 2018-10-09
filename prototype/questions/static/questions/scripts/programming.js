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

var show_save_icon = function(result) {
    $('#has_saved').removeClass('hidden');
    setTimeout(() => {$('#has_saved').addClass('hidden')}, 2000);
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
        if (got_return_array[i] && is_func) {
            has_return_contents = true;
            $("#function-got" + i).html(got_return_array[i]);
        }
    }

    $('#result-table').removeClass('hidden');
    $('#credit').removeClass('hidden');
    
    var user_input = editor.getValue();
    if (all_correct) {
        $('#all-correct').removeClass('hidden');
        save_code(user_input, true, false, show_save_icon);
    } else {
        save_code(user_input, false, false, show_save_icon);
    }
    if (!has_print_contents) {
        $(".program-type-analysis").addClass('hidden');
    }
    if (!has_return_contents) {
        $(".function-type-analysis").addClass('hidden');
    }
}

var display_results = function(result) {
    $('#loading').addClass('hidden');
    var user_input = editor.getValue();

    if (result.output.length > 0) {
        display_table(result);
    }
    if (result.stderr.length > 0) {
        $('#error').text(result.stderr);
        $('#error').removeClass('hidden');
        save_code(user_input, false, false, show_save_icon);
    }
    if (result.cmpinfo.length > 0) {
        $('#error').text(result.cmpinfo);
        $('#error').removeClass('hidden');
        save_code(user_input, false, false, show_save_icon);
    }
}

$("#submit").click(function () {
    var user_input = editor.getValue();

    var data = {
        user_input: user_input,
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
});

$('#save').click(function () {
    var user_input = editor.getValue();
    save_code(user_input, false, true, show_save_icon);
});

$('#show_solution').click(function () {
    $('#solution').html(solution);
    $('#show_solution').addClass('hidden');
});

setup_ace();