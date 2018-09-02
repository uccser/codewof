
function displayErrors(fb) {
    if (fb.errors.length > 0) {
        alert(fb.errors[0]);
    }
}

$(document).ready(function(){
    var parson = new ParsonsWidget({
        sortableId: 'jsparsons-target',
        trashId: 'jsparsons-source',
        max_wrong_lines: 1,
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
        if (feedback.length < 1) {
            is_correct = true;
        }
        $.ajax({
            url: '/ajax/save_attempt/',
            type: 'POST',
            method: 'POST',
            data: {
                user_input: initial,
                question: question_id,
                passed_tests: is_correct,
                is_save: false,
                csrfmiddlewaretoken: csrf_token
            },
            dataType: 'json',
            success: function(result) {
                $('#has_saved').show();
                setTimeout(() => {$('#has_saved').hide()}, 2000);
            }
        });
    });
});