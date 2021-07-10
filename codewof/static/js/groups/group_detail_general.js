/**
 * Iterates through each row, building a list of emails. Then sets the href attribute of the Email All button to send
 * an email to all the emails.
 */
$(document).ready(function () {
    let emails = []
    let table_tbody = document.getElementById("members-table-tbody")
    for (let row of table_tbody.rows) {
        emails.push(row.cells[0].innerText)
    }
    document.getElementById("email-button").href = "mailto:" + emails.join()
})
