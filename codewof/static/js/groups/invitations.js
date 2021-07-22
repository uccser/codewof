/**
 * Iterates through all the Invitation Accept and Reject buttons and adds onclick listeners.
 */
$(document).ready(function () {
     let invitationAcceptLinks = document.getElementsByClassName("invitation-accept-link");
     for (let link of invitationAcceptLinks) {
         let invitationID = getID(link.parentNode.parentNode.id);
         link.onclick = function () { acceptInvitation(invitationID) }
     }

     let invitationRejectLinks = document.getElementsByClassName("invitation-reject-link");
     for (let link of invitationRejectLinks) {
         let invitationID = getID(link.parentNode.parentNode.id);
         link.onclick = function () { rejectInvitation(invitationID) }
     }
})


/**
 * Extracts the number portion of the id.
 * @param full The original HTML element id, intended to be the form of <text>-<number>.
 * @returns {number} The number part of the id as an int.
 */
function getID(full) {
    return parseInt(full.substr(full.indexOf("-") + 1, full.length));
}


/**
 * Sends an ajax request to accept an Invitation, then refreshes the page upon success.
 * @param invitationID The ID of the Invitation to accept.
 */
function acceptInvitation(invitationID) {
    $.ajax({
        type: "POST",
        url: getAcceptURL(invitationID),
        async: true,
        cache: true,
        headers: {"X-CSRFToken": csrftoken},
        success: function(data, textStatus, xhr) { location.reload(); },
    });
}

/**
 * Sends an ajax request to reject an Invitation. Upon success, removes the card for that invitation and sets the text
 * if there are no more invitations.
 * @param invitationID The ID of the Invitation to reject.
 */
function rejectInvitation(invitationID) {
    $.ajax({
        type: "DELETE",
        url: getRejectURL(invitationID),
        async: true,
        cache: true,
        headers: {"X-CSRFToken": csrftoken},
        success: function(data, textStatus, xhr) {
            document.getElementById("invitation-" + invitationID).remove();
            let invitationsDiv = document.querySelector('#invitations-div');
            let invitationsCards = invitationsDiv.querySelectorAll('.card');
            if (invitationsCards.length === 0) {
                let element = document.createElement("p");
                element.appendChild(document.createTextNode('You have no invitations.'));
                document.getElementById("invitations-div").appendChild(element);
            }
        },
    });
}
