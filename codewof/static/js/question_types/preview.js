var base = require('./base.js');
var delete_config = require('./delete_modal_config.js');

let solution_editor;
let initial_editor;
let preview_editor;
let drag_and_drop_row = null;
let test_cases = {};
let macros = {
    index: 0,
    max_index: 0,
    aliases: [],
    substitutes: [],
};

// Constants
const MACRO_ATTR = {
    modal_name: '#macro_modal',
    fields: [
        { name: '#id_name', value: 0 },
        { name: '#id_possible_values', value: 1},
    ],
    table_name: '#macro_table',
    save_button: '#btn_macro_save',
    save_action: save_macro,
}
const TEST_CASE_ATTR = {
    modal_name: '#test_case_modal',
    fields: [
        { name: '#id_testcase_type', value: 0 },
        { name: '#id_testcase_code', value: 1},
    ],
    table_name: '#test_case_preview',
    save_button: '#btn_test_case_save',
    save_action: save_test_case,
}

// Uses "on" for geometry, as it is a checkbox
const PARENT_TAGS = ['conditionals', 'loops', 'mathematics', 'on'];

const HTML_MAP = {
    '&lt;p&gt;': '<p>',
    '&lt;/p&gt;': '</p>',
    '&lt;code&gt;': '<code>',
    '&lt;/code&gt;': '</code>',
    '&lt;sup&gt;': '<sup>',
    '&lt;/sup&gt;': '</sup>',
    '&lt;strong&gt;': '<strong>',
    '&lt;/strong&gt;': '</strong>',
}

// Setup
$(document).ready(function() {
    // Perform initial formatting
    // Go to preview tab to render visibility-dependent items
    $('#preview-select-tab a[href="#preview"]').tab('show');
    preview_editor = base.create_new_editor("code");

    // Return to details tab
    $('#preview-select-tab a[href="#details"]').tab('show');
    solution_editor = base.create_new_editor("id_solution");
    solution_editor.on('blur', function() {
        let example_code = solution_editor.getValue();
        run_code(null, example_code);
        for (var number in test_cases) {
            update_test_case_tables(number, example_code);
        }
        update_test_cases();
    });
    initial_editor = base.create_new_editor("id_initial_code");

    // Hide form fields which are displayed differently
    $("#id_test_cases").hide();
    $("#id_macros").hide();

    setup_concepts_contexts();
    setup_drag_and_drop()
    setup_form()

    // Bind event-driven functions
    $('#preview-tab-button').on('shown.bs.tab', function (event) {
        see_preview();
    });
    $('#id_question_type').change(function () {
        update_form();
    });

    // Run once initially as this is the first active tab
    load_test_cases();
    load_macros();
    update_macro_table();

    initial_fill_form();
});

function load_test_cases() {
    // Load any initial test cases
    if (typeof test_cases_list === 'undefined') {
        return;
    }

    for (let i = 0; i < test_cases_list.length; i++) {
        let data = test_cases_list[i];
        test_cases[data.number] = data;
        test_cases[data.number]['saved_input'] = test_cases[data.number].test_code;
        // Test code is set by default
        if (question_type == 'program') {
            test_cases[data.number].test_input = test_cases[data.number]['saved_input'];
            delete test_cases[data.number].test_code;
        }
    }
}

function load_macros() {
    // Load any initial macros
    if (typeof macros_list === 'undefined') {
        return;
    }

    let value_to_store = "";

    for (let i = 0; i < macros_list.length; i++) {
        let macro = macros_list[i];
        macros.aliases.push(macro['placeholder']);
        macros.substitutes.push(macro['values']);
        value_to_store += `${macro['placeholder']}@@${macro['values'].join(',')}\n`;
    }

    // Update the form field
    $('#id_macros').val(value_to_store);
}

function setup_form() {
    // Define button actions
    $('#btn_new_macro').on("click", function() {
        create_edit_sub_form(MACRO_ATTR);
    });
    $('#btn_new_test_case').on("click", function() {
        create_edit_sub_form(TEST_CASE_ATTR);
    });
    $('#btn_save_concepts').on("click", function() {
        save_tags('concept');
    });
    $('#btn_save_contexts').on("click", function() {
        save_tags('context');
    });
    $('#btn-macro-decrease').on("click", function() {
        step_macros(-1);
    });
    $('#btn-macro-increase').on("click", function() {
        step_macros(1);
    });
    $('.btn-edit-test-case').on("click", function() {
        edit_sub_form($(this));
    });
    $('.btn-edit-macro').on("click", function() {
        edit_sub_form($(this));
    });
}

function setup_drag_and_drop(setup_target=null) {
    if(setup_target == null) {
        setup_target = $('.dnd-interactable');
    }

    // Drag-and-drop table control, from
    // https://www.therogerlab.com/sandbox/pages/how-to-reorder-table-rows-in-javascript?s=0ea4985d74a189e8b7b547976e7192ae.4122809346f6a15e41c9a43f6fcb5fd5
    setup_target.on('dragstart', function (event){
        let selected_item = event.target.tagName;
        if (selected_item == "TR") {
            drag_and_drop_row = event.target;
        } else if (selected_item == "TD") {
            drag_and_drop_row = event.target.parentNode;
        } else {
            return;
        }
        drag_and_drop_row.style.backgroundColor = "lightgrey";
    });
    setup_target.on('dragover', function (event){
        event.preventDefault();

        if (drag_and_drop_row != null && event.target.tagName == "TD") {
            // Make sure only the relevant table can be targeted
            if (!event.target.parentNode.classList.contains('dnd-interactable')) {
                return;
            }
            // Sort the list to force consistency
            let children = Array.from(event.target.parentNode.parentNode.children).sort(function(a, b) {
                // Comparing id of the output-help-text element because it is the most uniquely identifiable
                return parseInt(a.querySelector('p').id.slice(10,11)) - parseInt(b.querySelector('p').id.slice(10,11));
            });
            if (children.indexOf(event.target.parentNode)<children.indexOf(drag_and_drop_row)) {
                event.target.parentNode.before(drag_and_drop_row);
            } else {
                event.target.parentNode.after(drag_and_drop_row);
            }
        }
    });
    setup_target.on('dragend', function (event){
        setTimeout(reset_row_color, 1000, drag_and_drop_row);
        drag_and_drop_row = null;
        update_test_cases();
    });
}

function reset_row_color(row_object) {
    // Check that the row hasn't been reselected
    if (row_object != drag_and_drop_row) {
        row_object.style.backgroundColor = "#fffcf8";
    }
}

function initial_fill_form() {
    update_test_cases();
    update_form();

    renumber_table($('#macro_table'), 0);
    renumber_table($('#test_case_preview'), 0);
}

function setup_concepts_contexts() {
    // Format the concept modal
    $("#id_concepts_3").parent().after($("#div_id_concept_conditionals"));
    $("#div_id_concept_conditionals").find(".custom-control-input").each(function () {
        $(this).prop("disabled", true);
    });
    $("#id_concepts_4").parent().after($("#div_id_concept_loops"));
    $("#div_id_concept_loops").find(".custom-control-input").each(function () {
        $(this).prop("disabled", true);
    });
    $("#concept_modal").children().eq(0).removeClass("modal-lg").addClass("modal-sm");

    // Format the context modal
    $("#id_contexts_0").parent().after($("#div_id_context_has_geometry"));
    $("#div_id_context_has_geometry").find(".custom-control-input").each(function () {
        $(this).prop("disabled", true);
    });
    $("#div_id_context_has_geometry").after($("#div_id_context_geometry"));
    $("#div_id_context_geometry").find(".custom-control-input").each(function () {
        $(this).prop("disabled", true);
    });
    $("#div_id_context_geometry").after($("#div_id_context_mathematics"));
    $("#div_id_context_mathematics").find(".custom-control-input").each(function () {
        $(this).prop("disabled", true);
    });

    // Add event logic
    $('#id_concepts_3').change(function () {
        toggle_radioset_active(this.checked, $("#div_id_concept_conditionals"));
    });
    $('#id_concepts_4').change(function () {
        toggle_radioset_active(this.checked, $("#div_id_concept_loops"));
    });
    $('#id_contexts_0').change(function () {
        toggle_radioset_active(this.checked, $("#div_id_context_mathematics"));
        toggle_radioset_active(this.checked, $("#div_id_context_has_geometry"));
    });
    $('#id_context_has_geometry').change(function () {
        toggle_radioset_active(this.checked, $("#div_id_context_geometry"));
    });

    // Add classes for putting on the tags
    let count = 1;
    let no_increment = ['single-condition', 'multiple-conditions', 'conditional-loops'];
    $('#div_id_concepts').find('input').each(function() {
        if(!PARENT_TAGS.includes($(this).val())) {
            $(this).attr('data-relevant-class', `concept-${count}`);
            if(!no_increment.includes($(this).val())) {
                count++;
            }
        }
    });
    $('#div_id_contexts').find('input').each(function() {
        count = $(this).val() === 'real-world-applications' ? 1 : 2;
        $(this).attr('data-relevant-class', `context-${count}`);
    });
}

// Safeguarding
function escapeHtml(str) {
    let div = document.createElement('div');
    div.appendChild(document.createTextNode(str));
    return div.innerHTML;
}

function safeQuestionText(str) {
    // Allow some HTML usage
    str = escapeHtml(str);
    for (let i of Object.keys(HTML_MAP)) {
        str = str.replace(new RegExp(i, 'g'), HTML_MAP[i])
    }
    return str;
}

// Form tab
function update_form() {
    // Refresh CodeMirror editors
    if (solution_editor != null) {
        solution_editor.refresh();
    }
    if (initial_editor != null) {
        initial_editor.refresh();
    }

    $('#div_id_solution').children('div').addClass("border");
    $('#div_id_initial_code').children('div').addClass("border");

    // Redraw the form based on the type of question
    question_type = $('#id_question_type').find(":selected").text().toLowerCase();
    $("#div_id_initial_code").css("display", "none");
    $("#div_id_read_only_lines_top").css("display", "none");
    $("#div_id_read_only_lines_bottom").css("display", "none");
    $("#div_id_lines").css("display", "none");
    if (question_type == "debugging") {
        $("#div_id_initial_code").css("display", "block");
        $("#div_id_read_only_lines_top").css("display", "block");
        $("#div_id_read_only_lines_bottom").css("display", "block");
    } else if (question_type == "parsons") {
        $("#div_id_lines").css("display", "block");
    }
}

function toggle_radioset_active(is_active, radio_container) {
    radio_container.find(".custom-control-input").each(function () {
        $(this).prop("checked", false);
        $(this).prop("disabled", !is_active);
    });
}

function update_test_cases() {
    // Updates test case table and input to account for drag-and-drop changes
    $('#id_test_cases').val('');
    $('#test_case_preview').children('tbody').children().each(function(index) {
        // Update cells
        let output_cells = $(this).children('.horizontal-overflow-cell');
        output_cells.eq(0).children('pre').attr('id', `test-case-${index + 1}-test-code`);
        output_cells.eq(1).children('pre').attr('id', `test-case-${index + 1}-output`);
        output_cells.children('p').attr('id', `test-case-${index + 1}-output-help-text`);
        let delete_cell = $(this).children('.btn-delete-test-case');
        delete_cell.off('click');
        delete_config.add_delete_listener(delete_cell, func=delete_object);
        // Fill test cases into the input
        let columns = $(this).children();
        let type = escapeHtml(columns[0].innerText.trim());
        let code = escapeHtml(columns[1].innerText.trim());
        let expected_output = escapeHtml(output_cells.eq(1).children('pre').text().trim());
        let stored_value = $('#id_test_cases').val() + `${type}@@${code}@@${expected_output}\n`;
        $('#id_test_cases').val(stored_value);
    });
}

function update_macro_table() {
    // Grabs information from the form field
    let lines = escapeHtml($('#id_macros').val()).split('\n').slice(0, -1);
    for (let i = 0; i < lines.length; i++) {
        let line = lines[i].split('@@');
        let name = line[0];
        let possible_values = line[1];

        let new_row = create_macro_table_row(name, possible_values, i + 1);

        $('#macro_table').children('tbody').append(new_row);

        // Setup edit and delete buttons
        $('#macro_table').children('tbody').children('tr:last-child').children('.btn-edit-macro').on('click', function(event) {
            edit_sub_form($(this));
        });
        delete_config.add_delete_listener($('#macro_table').children('tbody').children('tr:last-child').children('.btn-delete-macro'), func=delete_object);
    }
}

function create_edit_sub_form(form_attributes, id=null) {
    let site_modal = $(form_attributes.modal_name);
    if (id === null) {
        // Create - empty the modal fields
        let inps = site_modal.find('input, textarea').not('.btn');
        inps.each(function () {
            $(this).val('');
        });
        // Set save button action
        $(form_attributes.save_button).off("click").on("click", function () {
            form_attributes.save_action();
        });
    } else {
        // Edit - fill the modal fields with relevant values
        let row_items = $(form_attributes.table_name).children('tbody').children().eq(id).children();
        for(let field of form_attributes.fields) {
            site_modal.find(field.name).val(escapeHtml(row_items[field.value].innerText));
        }

        // Set save button action
        $(form_attributes.save_button).off("click").on("click", function () {
            form_attributes.save_action(id);
        });
    }
    site_modal.modal('show');
}

function edit_sub_form(target) {
    let type = target.attr('data-form-type');
    let id = target.parent().index();
    let form_attributes = null;

    if(type === 'macro') {
        form_attributes = MACRO_ATTR;
    } else {
        form_attributes = TEST_CASE_ATTR;
    }

    create_edit_sub_form(form_attributes, id);
}

function create_macro_table_row(name, possible_values, count) {
    let name_cell = `<td>${name}</td>`;
    let values_cell = `<td>${possible_values}</td>`;

    let edit_cell = `<td class="btn-cell btn-edit-macro hover-button" data-form-type="macro">Edit</td>`;
    let delete_cell = `<td class="btn-cell btn-delete-macro hover-button delete-modal-button" data-object-name="${name}" data-object-type="macro" data-object-id="${count}">Delete</td>`;
    return `<tr>${name_cell + values_cell + edit_cell + delete_cell}</tr>`
}

function save_macro(id = null) {
    let value_to_store = '';

    // Get values from form
    let site_modal = $('#macro_modal');
    let name = escapeHtml(site_modal.find('#id_name').val());
    let possible_values = escapeHtml(site_modal.find('#id_possible_values').val());
    let stored_value = escapeHtml($('#id_macros').val());
    let count = id === null ? $('#macro_table').children('tbody').children().length : id;

    let new_row = create_macro_table_row(name, possible_values, count + 1)

    // Alter the main form and the display
    if(id === null) {
        // New
        value_to_store = stored_value + `${name}@@${possible_values}\n`;
        $('#id_macros').val(value_to_store);
        $('#macro_table').children('tbody').append(new_row);

        // Setup edit and delete buttons
        $('#macro_table').children('tbody').children('tr:last-child').children('.btn-edit-macro').on('click', function(event) {
            edit_sub_form($(this));
        });
        delete_config.add_delete_listener($('#macro_table').children('tbody').children('tr:last-child').children('.btn-delete-macro'), func=delete_object);
    } else {
        // Edit
        let lines = stored_value.split('\n').slice(0, -1);
        lines[id] = `${name}@@${possible_values}`;
        value_to_store = lines.join('\n') + '\n';

        $('#id_macros').val(value_to_store);
        $('#macro_table').children('tbody').children().eq(id).replaceWith(new_row);

        // Setup edit and delete buttons
        $('#macro_table').children('tbody').children().eq(id).children('.btn-edit-macro').on('click', function(event) {
            edit_sub_form($(this));
        });
        delete_config.add_delete_listener($('#macro_table').children('tbody').children().eq(id).children('.btn-delete-macro'), func=delete_object);
    }
    site_modal.modal('hide');

}

function create_test_case_row(type, code, count) {
    let type_cell = `<td>${type}</td>`;
    let code_cell = `<td><pre class="mb-0" id="test-case-${count}-test-code">${code}</pre></td>`;

    let error_paragraph = `<p class="output-help-text d-none" id="test-case-${count}-output-help-text">An error has occurred once our test code has been added to the end of yours. You may not have terminated your strings correctly (is there a closing quote for every opening quote?)</p>`;
    let output_cell = `<td class="horizontal-overflow-cell"><pre class="mb-0" id="test-case-${count}-output"></pre>${error_paragraph}</td>`;

    let edit_cell = `<td class="btn-cell btn-edit-test-case hover-button" data-form-type="test_case">Edit</td>`;
    let delete_cell = `<td class="btn-cell btn-delete-test-case hover-button delete-modal-button" data-object-name="${code}" data-object-type="test case" data-object-id="${count}">Delete</td></tr>`;
    return `<tr draggable="true" class="dnd-interactable">${type_cell + code_cell + output_cell + edit_cell + delete_cell}</tr>`;
}

function update_test_case_list(id, number, type, given_code) {
    // Update JS list
    new_test_case = {
        id: id,
        number: number,
        expected_output: '',
        type: type,
        received_output: '',
        saved_input: given_code,
    }

    if (question_type == 'program') {
        new_test_case.test_input = given_code;
    } else {
        new_test_case.test_code = given_code;
    }

    test_cases[new_test_case.number] = new_test_case;
}

function save_test_case(edit_id = null) {
    let value_to_store = '';

    // Get values from form
    let site_modal = $('#test_case_modal');
    let given_type = escapeHtml(site_modal.find('#id_testcase_type').val());
    let given_code = escapeHtml(site_modal.find('#id_testcase_code').val());
    let stored_value = escapeHtml($('#id_test_cases').val());
    let count = edit_id === null ? $('#test_case_preview').children('tbody').children().length + 1: parseInt(edit_id) + 1;

    // Expected output
    update_test_case_list(edit_id, count, given_type, given_code);
    let user_code = solution_editor.getValue();
    run_code([test_cases[count]], user_code);

    let generated_output = test_cases[count].received_output.trim();

    if(edit_id === null) {
        // New
        let new_row = create_test_case_row(given_type, given_code, count);
        value_to_store = stored_value + `${given_type}@@${given_code}@@${generated_output}\n`;

        // Update form and display
        $('#id_test_cases').val(value_to_store);
        $('#test_case_preview').children('tbody').append(new_row);
        setup_drag_and_drop($('#test_case_preview').children('tbody').last(new_row));
        delete_config.add_delete_listener($('#test_case_preview').children('tbody').children('tr:last-child').children('.btn-delete-test-case'), func=delete_object);
        $('#test_case_preview').children('tbody').children('tr:last-child').children('.btn-edit-test-case').on('click', function() {
            edit_sub_form($(this));
        });
    } else {
        // Edit
        let new_row = create_test_case_row(given_type, given_code, parseInt(edit_id) + 1);
        let lines = stored_value.split('\n').slice(0, -1);
        lines[edit_id] = `${given_type}@@${given_code}@@${generated_output}`;
        value_to_store = lines.join('\n') + '\n';

        // Update form and display
        $('#id_test_cases').val(value_to_store);
        $('#test_case_preview').children('tbody').children().eq(edit_id).replaceWith(new_row);
        delete_config.add_delete_listener($('#test_case_preview').children('tbody').children().eq(edit_id).children('.btn-delete-test-case'), func=delete_object);
        $('#test_case_preview').children('tbody').children().eq(edit_id).children('.btn-edit-test-case').off('click').on('click', function(){
            edit_sub_form($(this));
        });

        // Has to be looked up again because replaceWith returns the original element
        // setup_drag_and_drop($('#test_case_preview').children('tbody').children().eq(id));
    }
    site_modal.modal('hide');
    update_test_case_tables(count, user_code);
}

function save_tags(type) {
    $(`#${type}_tray`).empty();
    $(`#div_id_${type}s`).find(':checked').each(function() {
        if(!PARENT_TAGS.includes($(this).val())) {
            let name = $(this).siblings('label').text();
            let tag_class = $(this).attr('data-relevant-class');

            $(`#${type}_tray`).append(`<span class="${type} ${tag_class}">${name}</span>`);
        }
    });
}

function renumber_table(table, start) {
    // Helper function for deleting. Requires table to be a jquery object
    let rows = table.children('tbody').children()
    for (let index = parseInt(start); index < rows.length; index++) {
        let row = rows.eq(index);
        row.children('.btn-delete-macro').attr('data-object-id', index + 1);
        row.children('.btn-delete-test-case').attr('data-object-id', index + 1);

        row.children('.horizontal-overflow-cell').eq(0).children('pre').attr('id', `test-case-${index + 1}-test-code`);
        row.children('.horizontal-overflow-cell').eq(1).children('pre').attr('id', `test-case-${index + 1}-output`);
        row.children('.horizontal-overflow-cell').eq(1).children('p').attr('id', `test-case-${index + 1}-output-help-text`);
    }
}

function delete_object(type, id) {
    /* This is called by the modal to remove a macro or test case */
    let table;
    let field;
    if (type === 'macro') {
        table = $('#macro_table');
        field = $('#id_macros');
    } else if (type === 'test case') {
        table = $('#test_case_preview');
        field = $('#id_test_cases');
    } else {
        return;
    }
    table.children('tbody').children().eq(id - 1).remove();
    renumber_table(table, id - 1);

    // Update form field
    let lines = escapeHtml(field.val()).split('\n').slice(0, -1);
    lines.splice(id - 1, 1);
    let value_to_store = lines.join('\n');
    if (lines.length > 0) {
        value_to_store += '\n';
    }
    field.val(value_to_store);
}

// Preview tab
function see_preview() {
    // Match preview table and form input to any re-ordering
    update_test_cases();

    fill_from_form();

    update_macros();
    substitute_macros();
}

function generate_table_row(count, parts) {
    return `<tr id="test-case-${count}-row">
        <td class="macro-substitution">
            <pre class="mb-0 test-case-test-code" id="test-case-${count}-test-code">${escapeHtml(parts[1])}</pre></td>
        <td><pre class="mb-0" id="test-case-${count}-expected-output">${parts[2]}</pre></td></tr>`;
}

function fill_from_form() {
    // Reset the content of this tab to match the form
    preview_editor.setValue(solution_editor.getValue());
    preview_editor.setOption('readOnly', 'nocursor');
    preview_editor.refresh();

    let q_text = safeQuestionText($('#id_question_text').val());
    $("#preview").find('.question-text').html(q_text);

    // Reset test case table
    let parent = $('#test-case-table').children('tbody').empty();
    let count = 1;
    for(let test_case of $('#id_test_cases').val().split('\n').slice(0,-1)) {
        parts = test_case.split('@@');
        parent.append(generate_table_row(count, parts));
        count ++;
    }
}

function custom_split(str) {
    // Splits str on comma UNLESS it is preceded by a backslash
    // Done this way as lookbehind regex is not supported on all browsers.

    // Split on each comma
    let parts = str.split(',');
    let output = [];
    for(let i = 0; i < parts.length; i++) {
        let part = parts[i];
        // If any of the split strings ends in a backslash, the comma was escaped and we rejoin the strings
        while (part.slice(-1) === '\\') {
            i++;
            if (i >= parts.length) {
                break;
            }
            part = part.slice(0, -1) + ',' + parts[i];
        }
        output.push(part);
    }
    return output;
}

function update_macros() {
    let macro_form_field = $('#id_macros').val();
    macros.max_index = 0;
    if (macro_form_field !== "") {
        let lines = macro_form_field.split('\n').slice(0,-1);
        macros.aliases = [];
        macros.substitutes = [];
        let max_usable_length = null;
        for(let line of lines) {
            let parts = line.split('@@')
            let substitution = custom_split(escapeHtml(parts[1]));
            macros.aliases.push(parts[0]);
            macros.substitutes.push(substitution);
            if (max_usable_length == null || max_usable_length > substitution.length) {
                max_usable_length = substitution.length;
            }
        }
        macros.max_index = Math.max(0, max_usable_length - 1);
        macros.index = 0;
        $('#btn-macro-decrease').attr("disabled", true);
        $('#btn-macro-increase').attr("disabled", false);
        $('#macro-cycle-text').text(macros.index);
        if (macros.max_index == 0) {
            $('#btn-macro-increase').attr("disabled", true);
            $('#macro-cycle-text').text('Disabled');
        }
    }
}

function step_macros(change) {
    macros.index += change;

    // Safeguarding
    if (macros.index < 0 || macros.index > macros.max_index) {
        macros.index -= change;
        return;
    }

    // Reset the preview, then perform substitution
    fill_from_form();
    substitute_macros();
    $('#macro-cycle-text').text(macros.index);

    // Disable buttons if we've reached the end of the list
    $('#btn-macro-decrease').attr("disabled", false);
    $('#btn-macro-increase').attr("disabled", false);
    if (macros.index == 0) {
        $('#btn-macro-decrease').attr("disabled", true);
    } else if (macros.index == macros.max_index) {
        $('#btn-macro-increase').attr("disabled", true);
    }
}

function substitute_macros() {
    // Fetch the parts to substitute
    let example_code = preview_editor.getValue();
    let question_text = $("#preview").find('.question-text').html();
    let preview_test_cases = [];
    let test_cases_text = [];
    $('#test-case-table').find('.macro-substitution').each(function () {
        preview_test_cases.push($(this));
        test_cases_text.push($(this).text().trim());
    });

    let input_type = question_type === "program" ? 'test_input' : 'test_code' ;

    // Perform replacement
    for (var number in test_cases) {
        if (test_cases.hasOwnProperty(number)) {
            test_cases[number][input_type] = test_cases[number]['saved_input'];
        }
    }
    for (let i = 0; i < macros.aliases.length; i++) {
        let pattern = '@' + macros.aliases[i];
        let substitute = macros.substitutes[i][macros.index];

        example_code = example_code.replaceAll(pattern, substitute);
        question_text = question_text.replaceAll(pattern, substitute);
        for (let j = 0; j < test_cases_text.length; j++) {
            test_cases_text[j] = test_cases_text[j].replaceAll(pattern, substitute);
        }
        for (var number in test_cases) {
            if (test_cases.hasOwnProperty(number)) {
                test_cases[number][input_type] = test_cases[number][input_type].replaceAll(pattern, substitute)
            }
        }
    }

    // Update page
    $("#preview").find('.question-text').html(safeQuestionText(question_text));
    preview_editor.setValue(example_code);
    run_code(null, example_code, macro_update=false);
    for (var number in test_cases) {
        preview_test_cases[number].children().text(test_cases_text[number]);
        update_test_case_tables(number, example_code);
    }
}

// Running Python code
function run_code(cases_to_run=null, user_code, macro_update=true) {
    if (cases_to_run === null) {
        cases_to_run = test_cases;
    }

    if (macro_update) {
        update_macros();
    }
    for (var id in cases_to_run) {
        if (test_cases.hasOwnProperty(id)) {
            var test_case = cases_to_run[id];
            test_case['received_output'] = '';
            test_case.runtime_error = false;
        }
    }

    // Check indentation
    if (user_code.includes("\t")) {
        // contains tabs
        $("#indentation-warning").removeClass("d-none");
        return; // do not run tests
    } else {
        $("#indentation-warning").addClass("d-none");
    }
    cases_to_run = run_draft_test_cases(cases_to_run, user_code, run_python_code);
    // Manually update the test case
    for (var id in cases_to_run) {
        if (test_cases.hasOwnProperty(id)) {
            var test_case = cases_to_run[id];
        }
    }
}

function run_draft_test_cases(cases_to_run, user_code, code_function) {
    // Currently runs in sequential order.
    for (var number in cases_to_run) {
        if (cases_to_run.hasOwnProperty(number)) {
            var test_case = cases_to_run[number];
            var code = user_code;
            if (test_case.hasOwnProperty('test_code')) {
                code = code + '\n' + test_case.test_code;
            }
            if (test_case.hasOwnProperty('test_input')) {
                test_case.test_input_list = test_case.test_input.split('\n');
            }
            code_function(code, test_case);
        }
    }
    return cases_to_run;
}

function run_python_code(user_code, test_case) {
    // Configure Skulpt for running Python code
    Sk.configure({
        // Setup Skulpt to read internal library files
        read: function (x) {
            if (Sk.builtinFiles === undefined || Sk.builtinFiles["files"][x] === undefined)
                throw "File not found: '" + x + "'";
            return Sk.builtinFiles["files"][x];
        },
        inputfun: function (str) {
            if (question_type != "program") {
                return prompt(str);
            }

            // Program questions
            if (test_case.test_input_list.length > 0) {
                return test_case['test_input_list'].shift();
            } else {
                return '';
            }
        },
        inputfunTakesPrompt: true,
        // Append print() statements for test case
        output: function (received_output) {
            test_case['received_output'] += received_output;
        },
        python3: true,
        execLimit: 1000,
    });
    if (typeof user_code == 'string' && user_code.trim()) {
        try {
            Sk.importMainWithBody("<stdin>", false, user_code, true);
        } catch (error) {
            if (error.hasOwnProperty('traceback')) {
                test_case.received_output = error.toString();
                test_case.runtime_error = true;
            } else {
                throw error;
            }
        }
    } else {
        test_case.received_output = 'No Python code provided.';
        test_case.runtime_error = true;
    }
}

function update_test_case_tables(number, user_code) {
    let received_output = test_cases[number].received_output.replace(/\s*$/, '');

    // Update output cells
    let output_element = $('#test-case-' + number + '-output, #test-case-' + number + '-expected-output');
    let output_element_help_text = $('#test-case-' + number + '-output-help-text');
    output_element.text(received_output);
    if (test_cases[number].runtime_error) {
        output_element.addClass('error')
        // the following is implemented because of https://github.com/uccser/codewof/issues/351
        regex_match = /line (\d+)/.exec(received_output) // looking for line number
        if (regex_match !== null) {
            error_line_number = regex_match[1] // first capture group - should be the line number
            num_user_code_lines = user_code.split('\n').length; // number of lines in the users code
            if (error_line_number > num_user_code_lines) {
                output_element_help_text.removeClass('d-none');
            }
        }
    } else {
        output_element.removeClass('error')
        output_element_help_text.addClass('d-none');
    }
}