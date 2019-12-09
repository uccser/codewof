var CodeMirror = require('codemirror');
require('codemirror/mode/python/python.js');

var EXAMPLE_CODE = `def fizzbuzz():
    for i in range(1 ,100):
        if i % 3 == 0 and i % 5 == 0 :
            print("FizzBuzz")
        elif i%3 == 0:
            print( "Fizz")
        elif  i % 5==0:
             print("Buzz")

        else:
            print(i)`;

$(document).ready(function () {
    var editor = CodeMirror.fromTextArea(document.getElementById("code"), {
        mode: {
            name: "python",
            version: 3,
            singleLineStringErrors: false
        },
        lineNumbers: true,
        textWrapping: false,
        styleActiveLine: true,
        autofocus: true,
        indentUnit: 4,
        viewportMargin: Infinity
    });

    $('#load_example_btn').click(function () {
        editor.setValue(EXAMPLE_CODE);
    });

    $('#clear_btn').click(function () {
        editor.setValue("");
    });
});
