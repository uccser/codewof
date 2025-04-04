$(document).ready(function() {
    $('.delete-modal-button').on("click", function() {
        let name = $(this).attr('data-object-name');
        let obj_type = $(this).attr('data-object-type');
        let id = $(this).attr('data-object-id');
        let url = $(this).attr('data-delete-url');

        open_delete_modal(name, obj_type, id, url)
    });
});

function truncate(str, maxlength) {
    return (str.length > maxlength)
        ? str.slice(0, maxlength - 1) + '…'
        : str
}

function add_delete_listener(button, func=null) {
    // Button is a jquery object
    button.on("click", function() {
        let name = $(this).attr('data-object-name');
        let obj_type = $(this).attr('data-object-type');
        let id = $(this).attr('data-object-id');
        let url = $(this).attr('data-delete-url');

        open_delete_modal(name, obj_type, id, url, func)
    });
}

function open_delete_modal(object_name, object_type, object_id, url=null, func=null) {
    // Show the object name
    $('#delete-modal').find('#modal_title_id').text(`Delete ${object_type}?`)
    $('#delete-modal').find('#delete-warning-message').text(`Are you sure you want to delete "${object_name}"?`)
    let delete_button = $('#delete-modal').find('#btn_delete_request');
    delete_button.val(`Delete ${object_type}`)

    // Set up the form to request deletion
    delete_button.off('click');
    delete_button.attr('form', undefined);
    if (url !== null) {
        let delete_form = $('#deleteForm');
        delete_form.attr('action', url);
        delete_button.attr('form', 'deleteForm');
    } else if (func !== null) {
        delete_button.on('click', function() {
            func(object_type, object_id);
            $('#delete-modal').modal('hide');
        });
    }

    // Show the modal
    $('#delete-modal').modal('show');
}

exports.add_delete_listener = add_delete_listener;