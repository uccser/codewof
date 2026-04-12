let selected = null;

$(document).ready(function() {
    // Select this question when clicked
    $('.qc-card-draft').on("click", function() {
        select($(this));
    });
});

function select(new_selection) {
    if (selected !== null) {
        selected.find('.qc-buttons, .qc-delete, .img-selected-true').addClass('d-none');
        selected.find('.qc-tags, .img-selected-false').removeClass('d-none');
        selected.removeClass('qc-complete');
    }

    if (!new_selection.is(selected)) {
        new_selection.find('.qc-tags, .img-selected-false').addClass('d-none');
        new_selection.find('.qc-buttons, .qc-delete, .img-selected-true').removeClass('d-none');
        new_selection.addClass('qc-complete');

        selected = new_selection;
    } else {
        selected = null;
    }
}