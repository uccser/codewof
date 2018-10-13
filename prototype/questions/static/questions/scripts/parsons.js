
function displayErrors(fb) {
    $('#feedback').addClass('hidden');

    if (fb.errors.length > 0) {
        setTimeout(() => {$('#feedback').removeClass('hidden')}, 200);
        $('#feedback').text(fb.errors[0]);
    }
}

$(document).ready(function(){
    var parson = new ParsonsWidget({
        sortableId: 'jsparsons-target',
        trashId: 'jsparsons-source',
        max_wrong_lines: 10,
        feedback_cb : displayErrors,
        can_indent: true
    });

    parson.init(initial);
    parson.shuffleLines();
    
    $("#newInstanceLink").click(function(event){
        event.preventDefault();
        parson.shuffleLines();
    });
    $("#feedbackLink").click(function(event){
        event.preventDefault();
        feedback = parson.getFeedback();
        is_correct = false;
        $('#has_saved').addClass('hidden');

        if (feedback.length < 1) {
            is_correct = true;
            $('#has_saved').removeClass('hidden');
        }

        var data = {
            user_input: initial,
            question: question_id,
            passed_tests: is_correct,
            is_save: false
        }
        var success = function(result) {};
        post('save_attempt', data, success);
    });
});