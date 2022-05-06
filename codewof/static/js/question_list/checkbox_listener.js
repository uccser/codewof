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
        const index = $("input").index(checkbox);
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
    const indentIndex = $("input").index(indent);
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

window.onload = () => {
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
}
