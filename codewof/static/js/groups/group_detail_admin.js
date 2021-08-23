/**
 * A set of Membership object IDs that have changed, meaning either the Role has been altered or the Membership is to
 * be deleted
 * @type {Set<any>} A set of ID ints.
 */
let changedIDs = new Set();

/**
 * A list of objects representing the original Memberships of the following format:
 *
 * { id: <int>, role: <string> }
 *
 * Used to check whether the Membership has changed or not
 * @type {*[]}
 */
let originalMemberships = [];


/**
 * Iterates through each row. Adds an object to originalMemberships. Adds onchange listeners to the select and checkbox.
 */
$(document).ready(function () {
    $("#save-button").click(performChecks);

    let table_tbody = document.getElementById("members-table-tbody");
    for (let row of table_tbody.rows) {
        let select = document.getElementById("membership-" + getID(row.id) + "-select");
        let checkbox = document.getElementById("membership-" + getID(row.id) + "-checkbox");

        originalMemberships.push(
            {
                id: getID(row.id),
                role: select.value.toString()
            }
        );

        select.onchange = checkbox.onchange = function() { rowUpdate(row, select, checkbox); };
    }
})


/**
 * Callback for changes to a row. If the select value is the same as the role of the corresponding object in
 * originalMemberships and the checkbox is unticked, it follows the row is back to the original and thus can be removed
 * from changedIDs. Otherwise, it is added to changedIDs.
 *
 * Also changes the row color depending on how the row has changed. If delete is ticked, the row is red. If the role
 * has changed, the row is yellow. If both, then the row is red.
 * @param row
 * @param select
 * @param checkbox
 */
function rowUpdate(row, select, checkbox) {
    let originalRole = originalMemberships.find(x => x.id === getID(row.id)).role.toString();
    if (select.value.toString() === originalRole && !checkbox.checked) {
        changedIDs.delete(getID(row.id));
    } else {
        changedIDs.add(getID(row.id));
    }

    if (select.value.toString() !== originalRole) {
        row.classList.add("table-warning");
    } else {
        row.classList.remove("table-warning");
    }

    if (checkbox.checked) {
        row.classList.add("table-danger");
    } else {
        row.classList.remove("table-danger");
    }
}


/**
 * Extracts the number portion of the id.
 * @param full The original HTML element id, intended to be the form of <text>-<number>.
 * @returns {number} The number part of the id as an int.
 */
function getID(full) {
    return parseInt(full.substr(full.indexOf("-") + 1, full.length));
}


/**
 * Performs validity checks. If there is at least one admin but the user is demoting themselves, a warning modal is
 * displayed first. Upon confirming, updateMemberships is called. Otherwise, updateMemberships is immediately called.
 */
function performChecks() {
    if (atLeastOneAdmin()) {
        let demoteSelf = false;
        if (document.getElementById("membership-" + currentUserMembershipID + "-select").value.toString() ===
        "Member") {
            $('#demote-self-modal').modal('show');
            $('#demote-self-modal-button').click(function () {
                demoteSelf = true;
                updateMemberships(demoteSelf);
            })
        } else {
            updateMemberships(demoteSelf);
        }
    } else {
        updateFailure("The Group needs at least one Admin.");
    }
}


/**
 * Iterates through the changedIDs, building the JSON body, then sends an HTTP request to update the memberships.
 */
function updateMemberships(demoteSelf) {
    let memberships = [];

    for (let id of changedIDs) {
        memberships.push({
            id: id,
            delete: document.getElementById("membership-" + id + "-checkbox").checked,
            role: document.getElementById("membership-" + id + "-select").value
        });
    }

    $.ajax({
        type: "PUT",
        url: membershipsUpdateURL,
        data: JSON.stringify({memberships: memberships}),
        async: true,
        cache: true,
        headers: {"X-CSRFToken": csrftoken},
        success: function(data, textStatus, xhr) { updateSuccess(demoteSelf) },
        error: function(data, textStatus, xhr) { updateFailure("An error occurred while updating the " +
            "Memberships. Try refreshing the page.") },
    });
}


/**
 * Called when the HTTP request to update the memberships succeeds. If the user is demoting themselves, the page is
 * refreshed. Otherwise, show the success alert which fades away after a period. Updates the originalMemberships list,
 * and resets changedIDs. Also removes the row or resets the row colors.
 */
function updateSuccess(refresh) {
    if (refresh) {
        location.reload();
        return;
    }

    $('#update-success-alert').show();

    $("#update-success-alert").fadeTo(5000, 500).slideUp(500, function () {
        $("#update-success-alert").slideUp(500);
    });

    for (let id of changedIDs) {
        let row = document.getElementById("membership-" + id);
        let membershipToUpdate = originalMemberships.find(x => x.id === id);

        if (document.getElementById("membership-" + id + "-checkbox").checked) {
            row.parentNode.removeChild(row);
            originalMemberships.splice(originalMemberships.indexOf(membershipToUpdate));
        } else {
            let select = document.getElementById("membership-" + id + "-select");
            membershipToUpdate.role = select.value.toString();
            row.classList.remove("table-warning");
            row.classList.remove("table-danger");
        }
    }

    changedIDs.clear();
    setLeaveButton();
}


/**
 * Called when the HTTP request to update the memberships fails. Show the error alert which fades away after a period.
 */
function updateFailure(message) {
    document.getElementById('update-danger-alert').innerText = message;
    $('#update-danger-alert').show();

    $("#update-danger-alert").fadeTo(5000, 500).slideUp(500, function () {
        $("#update-danger-alert").slideUp(500);
    });
}


/**
 * Checks there is at least one admin by iterating through the rows and incrementing a counter if the member's role is
 * Admin and is not to be deleted.
 * @returns {boolean} Whether there is at least one Admin.
 */
function atLeastOneAdmin() {
    let counter = 0;

    let table_tbody = document.getElementById("members-table-tbody");
    for (let row of table_tbody.rows) {
        let select = document.getElementById("membership-" + getID(row.id) + "-select");
        let checkbox = document.getElementById("membership-" + getID(row.id) + "-checkbox");

        if (!checkbox.checked && select.value.toString() === "Admin") {
            counter += 1;
        }
    }

    return counter > 0;
}

/**
 * Determines whether the leave button should be visible or not depending on if the user is the only admin. If so, then
 * the button is hidden. Otherwise, the button is visible.
 */
function setLeaveButton() {
    let counter = 0;

    for (let membership of originalMemberships) {
        if (membership.role === "Admin") {
            counter++;
        }
    }

    let leaveButton = document.getElementById("leave-button");
    if (counter === 1) {
        leaveButton.style.visibility = "hidden";
    } else {
        leaveButton.style.visibility = "visible";
    }
}
