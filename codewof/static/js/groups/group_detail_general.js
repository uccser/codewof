/**
 * The path data for the thumbs up filled SVG
 * @type {string}
 */
const THUMBS_UP_FILL = "M6.956 1.745C7.021.81 7.908.087 8.864.325l.261.066c.463.116.874.456 1.012.965.22.816.533 2.511.062 4.51a9.84 9.84 0 0 1 .443-.051c.713-.065 1.669-.072 2.516.21.518.173.994.681 1.2 1.273.184.532.16 1.162-.234 1.733.058.119.103.242.138.363.077.27.113.567.113.856 0 .289-.036.586-.113.856-.039.135-.09.273-.16.404.169.387.107.819-.003 1.148a3.163 3.163 0 0 1-.488.901c.054.152.076.312.076.465 0 .305-.089.625-.253.912C13.1 15.522 12.437 16 11.5 16H8c-.605 0-1.07-.081-1.466-.218a4.82 4.82 0 0 1-.97-.484l-.048-.03c-.504-.307-.999-.609-2.068-.722C2.682 14.464 2 13.846 2 13V9c0-.85.685-1.432 1.357-1.615.849-.232 1.574-.787 2.132-1.41.56-.627.914-1.28 1.039-1.639.199-.575.356-1.539.428-2.59z";

/**
 * The path data for the thumbs up SVG
 * @type {string}
 */
const THUMBS_UP = "M8.864.046C7.908-.193 7.02.53 6.956 1.466c-.072 1.051-.23 2.016-.428 2.59-.125.36-.479 1.013-1.04 1.639-.557.623-1.282 1.178-2.131 1.41C2.685 7.288 2 7.87 2 8.72v4.001c0 .845.682 1.464 1.448 1.545 1.07.114 1.564.415 2.068.723l.048.03c.272.165.578.348.97.484.397.136.861.217 1.466.217h3.5c.937 0 1.599-.477 1.934-1.064a1.86 1.86 0 0 0 .254-.912c0-.152-.023-.312-.077-.464.201-.263.38-.578.488-.901.11-.33.172-.762.004-1.149.069-.13.12-.269.159-.403.077-.27.113-.568.113-.857 0-.288-.036-.585-.113-.856a2.144 2.144 0 0 0-.138-.362 1.9 1.9 0 0 0 .234-1.734c-.206-.592-.682-1.1-1.2-1.272-.847-.282-1.803-.276-2.516-.211a9.84 9.84 0 0 0-.443.05 9.365 9.365 0 0 0-.062-4.509A1.38 1.38 0 0 0 9.125.111L8.864.046zM11.5 14.721H8c-.51 0-.863-.069-1.14-.164-.281-.097-.506-.228-.776-.393l-.04-.024c-.555-.339-1.198-.731-2.49-.868-.333-.036-.554-.29-.554-.55V8.72c0-.254.226-.543.62-.65 1.095-.3 1.977-.996 2.614-1.708.635-.71 1.064-1.475 1.238-1.978.243-.7.407-1.768.482-2.85.025-.362.36-.594.667-.518l.262.066c.16.04.258.143.288.255a8.34 8.34 0 0 1-.145 4.725.5.5 0 0 0 .595.644l.003-.001.014-.003.058-.014a8.908 8.908 0 0 1 1.036-.157c.663-.06 1.457-.054 2.11.164.175.058.45.3.57.65.107.308.087.67-.266 1.022l-.353.353.353.354c.043.043.105.141.154.315.048.167.075.37.075.581 0 .212-.027.414-.075.582-.05.174-.111.272-.154.315l-.353.353.353.354c.047.047.109.177.005.488a2.224 2.224 0 0 1-.505.805l-.353.353.353.354c.006.005.041.05.041.17a.866.866 0 0 1-.121.416c-.165.288-.503.56-1.066.56z";


/**
 * Iterates through each membership row, building a list of emails. Then sets the href attribute of the Email All button
 * to send an email to all the emails.
 *
 * Also iterates through each feed row and adds an onchange listener and set the initial title of the thumb span.
 */
$(document).ready(function () {
    $("#email-button").click(emailGroup);

    if (feedEnabled) {
        let feed_tbody = document.getElementById("feed-table-tbody");
        for (let row of feed_tbody.rows) {
            let checkbox = row.querySelector('.thumb');
            let path = row.querySelector('.thumb-path');
            let countColumn = row.querySelector('.td-like-count')
            let id = getID(row.id)
            checkbox.onchange = function () {
                toggleThumpsUp(checkbox, path, countColumn, id)
            }
            let likeSpan = countColumn.querySelector('.span-like-count');
            if (attemptLikeNames[id].length > 0) {
                $(likeSpan).attr('data-original-title', attemptLikeNames[id].join("<br>"));
            } else {
                $(likeSpan).attr('data-original-title', "None");
            }
        }
    }

    $(function () {
      $('[data-toggle="tooltip"]').tooltip({html: true})
    })
})


/**
 * Makes a request to obtain the email addresses of the members of the group, then opens the user's email client.
 */
function emailGroup() {
    $.ajax({
        type: "GET",
        url: emailURL,
        async: true,
        cache: true,
        headers: {"X-CSRFToken": csrftoken},
        success: function(data, textStatus, xhr) {
            location.href = "mailto:" + data.emails.join();
        },
        error: function (data, textStatus, xhr) {

        }
    });
}


/**
 * Updates a key value in the attemptLikeNames object, which is for tracking the list of names of users that have liked
 * an attempt (<attempt id> : <array of strings>). Used to build the title of the thumb span.
 * @param id The ID of the attempt the likes are for.
 * @param likeSpan The thumbs up span to update.
 * @param adding A boolean, true if the user is liking the attempt, false otherwise.
 */
function updateAttemptLikeNames(id, likeSpan, adding) {
    if (adding) {
        attemptLikeNames[id].splice(sortedIndex(attemptLikeNames[id], userFullName), 0, userFullName);
    } else {
        attemptLikeNames[id].splice(attemptLikeNames[id].indexOf(userFullName), 1);
    }
}


/**
 * Returns the index to insert an object in an array while maintaining sorted order. Taken from
 * https://stackoverflow.com/a/21822316.
 * @param array The array to insert into.
 * @param value The value to insert.
 * @returns {number} The index to insert at.
 */
function sortedIndex(array, value) {
    var low = 0,
        high = array.length;

    while (low < high) {
        var mid = (low + high) >>> 1;
        if (array[mid] < value) low = mid + 1;
        else high = mid;
    }
    return low;
}


/**
 * Handles when the thumb checkbox is toggled by sending an appropriate request, then changes the thumb path upon
 * success. Also updates the like counter and tooltip name list.
 * @param checkbox The checkbox input for the like button.
 * @param path The SVG path to change.
 * @param countColumn The td column for the like count.
 * @param id The ID of the attempt to like/dislike.
 */
function toggleThumpsUp(checkbox, path, countColumn, id) {
    let likeSpan = countColumn.querySelector('.span-like-count');
    checkbox.disabled = true;
    if (checkbox.checked) {
        $.ajax({
            type: "POST",
            url: getLikeURL(id),
            async: true,
            cache: true,
            headers: {"X-CSRFToken": csrftoken},
            success: function(data, textStatus, xhr) {
                path.setAttribute("d", THUMBS_UP_FILL);
                likeSpan.innerText = parseInt(countColumn.innerText) + 1;
                updateAttemptLikeNames(id, likeSpan, true)
                $(likeSpan).attr('data-original-title', attemptLikeNames[id].join("<br>"));
                checkbox.disabled = false;
            },
            error: function (data, textStatus, xhr) {
                checkbox.checked = false;
                checkbox.disabled = false;
            }
        });
    } else {
        $.ajax({
            type: "DELETE",
            url: getUnlikeURL(id),
            async: true,
            cache: true,
            headers: {"X-CSRFToken": csrftoken},
            success: function(data, textStatus, xhr) {
                path.setAttribute("d", THUMBS_UP);
                likeSpan.innerText = parseInt(countColumn.innerText) - 1;
                updateAttemptLikeNames(id, likeSpan, false)
                if (attemptLikeNames[id].length > 0) {
                    $(likeSpan).attr('data-original-title', attemptLikeNames[id].join("<br>"));
                } else {
                    $(likeSpan).attr('data-original-title', "None");
                }
                checkbox.disabled = false;
            },
            error: function (data, textStatus, xhr) {
                checkbox.checked = true;
                checkbox.disabled = false;
            }
        });
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
