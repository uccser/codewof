
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
        parson.getFeedback();
    });
});