$(document).ready(function () {
     let invitationAcceptLinks = document.getElementsByClassName("invitation-accept-link");
     for (let link of invitationAcceptLinks) {
        let invitationID = link.parentNode.parentNode.id
         link.onclick = function () { acceptInvitation(invitationID) }
     }

     let invitationRejectLinks = document.getElementsByClassName("invitation-reject-link");
     for (let link of invitationRejectLinks) {
        let invitationID = link.parentNode.parentNode.id
         link.onclick = function () { rejectInvitation(invitationID) }
     }
})


function acceptInvitation(invitationID) {
    console.log("Accepted: " + invitationID)
}

function rejectInvitation(invitationID) {
    console.log("Rejected: " + invitationID)
}
