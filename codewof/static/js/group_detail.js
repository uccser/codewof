let changedIDs = new Set()

$(document).ready(function () {
    let table_tbody = document.getElementById("members-table-tbody")
    for (let row of table_tbody.rows) {
        let select = document.getElementById("membership-" + getID(row.id) + "-select")
        let checkbox = document.getElementById("membership-" + getID(row.id) + "-checkbox")
        // console.log("membership-" + getID(row.id) + "-select")
        select.onchange = checkbox.onchange = function() {
            changedIDs.add(getID(row.id))
            // console.log(changedIDs)
        }
    }
})

function getID(full) {
    return full.substr(full.indexOf("-") + 1, full.length)
}

