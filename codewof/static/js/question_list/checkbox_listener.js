/**
 * This checkbox listener dynamically checks, unchecks, enables, and disables checkboxes for filters in the "Filter
 * Questions" panel on the Questions page, based on the indentation of filters. This includes automatically checking
 * and disabling indented filters that belong to a filter that has been checked, and unchecking and enabling filters
 * that belong to a filter that has been unchecked. Additionally, this is also performed on load of the page, based on
 * which filters have been checked.
 */

var filterSummaryText;
var allCheckboxes;

function getElementIndex(element) {
    let index = 0;
    while ((element = element.previousElementSibling)) {
        index++;
    }
    return index;
}

function getCheckboxes(indentLevel) {
    return document.querySelectorAll(`[data-indent-level="${indentLevel}"]`);
}

function getCheckboxIndexesAndArray(checkboxes) {
    const checkboxIndexes = [];
    const checkboxArray = [];
    for (const checkbox of checkboxes) {
        const index = [...document.querySelectorAll("input")].indexOf(checkbox);
        checkboxIndexes.push(index);
        checkboxArray.push(checkbox);
    }
    return [checkboxIndexes, checkboxArray];
}

function modifyCheckboxes(index, checkboxIndexes, checkboxArray, event) {
    while (true) {
        const nextIndex = checkboxIndexes.indexOf(index);
        if (nextIndex !== -1) {
            const checkboxChecked = event.currentTarget.checked;
            checkboxArray[nextIndex].checked = checkboxChecked;
            checkboxArray[nextIndex].disabled = checkboxChecked;
        } else {
            break;
        }
        index++;
    }
}

function addCheckboxListener(indent, checkboxes) {
    const indentIndex = [...document.querySelectorAll("input")].indexOf(indent);
    indent.addEventListener("change", (event) => {
        const [checkboxIndexes, checkboxArray] = getCheckboxIndexesAndArray(checkboxes);
        modifyCheckboxes(indentIndex + 1, checkboxIndexes, checkboxArray, event);
    });
}

function modifyCheckboxesOnLoad(checkboxes) {
    for (const checkbox of checkboxes) {
        if (checkbox.checked) {
            const event = new Event('change');
            checkbox.dispatchEvent(event);
        }
    }
}

function updateFilterSummary() {
    /**
     * Update the summary of applied filters.
     */
    var filter_count = 0;

    allCheckboxes.forEach(function (checkbox) {
        if (checkbox.checked && !checkbox.disabled) {
            filter_count++;
        }
    });

    if (filter_count == 1) {
        filterSummaryText.textContent = '1 filter applied';
    } else {
        filterSummaryText.textContent = `${filter_count} filters applied`;
    }
};

window.onload = () => {
    filterSummaryText = document.getElementById('filter-summary-text');

    const checkboxesIndentOne = getCheckboxes(1);
    const checkboxesIndentTwo = getCheckboxes(2);
    const checkboxesIndentThree = getCheckboxes(3);
    for (const indentOne of checkboxesIndentOne) {
        addCheckboxListener(indentOne, [...checkboxesIndentTwo, ...checkboxesIndentThree]);
    }
    for (const indentTwo of checkboxesIndentTwo) {
        addCheckboxListener(indentTwo, checkboxesIndentThree);
    }
    modifyCheckboxesOnLoad([...checkboxesIndentOne, ...checkboxesIndentTwo]);

    allCheckboxes = document.querySelectorAll('#question-filter input');
    allCheckboxes.forEach(function (checkbox) {
        checkbox.addEventListener('change', updateFilterSummary);
    });
    updateFilterSummary();
}
