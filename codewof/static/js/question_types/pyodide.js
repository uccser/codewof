importScripts("https://cdn.jsdelivr.net/pyodide/v0.27.6/full/pyodide.js");

async function initializePyodide() {
    let pyodide = await loadPyodide();
    pyodide.setStdin({
        stdin: (str) => { return prompt(str) },
    });
    return pyodide;
}

// After initial load, Pyodide is ready to use, send message to main thread to indicate worker is ready
let pyodideReadyPromise = initializePyodide();
pyodideReadyPromise.then(() => {
  postMessage({ type: "ready" });
});

/**
 * Function to run the user's Python code using Pyodide and capture the output.
 * This function listens for messages from the main thread,
 * executes the provided Python code,
 * and sends the output or error back to the main thread.
 */
onmessage = async (event) => {
  if (event.data.type === "ping") {
    postMessage({ type: "ready" });
    return;
  }
  let pyodide = await pyodideReadyPromise;
  const { user_code, test_case, program } = event.data;
  if (program) {
    console.log("Test case input list:", test_case.test_input_list);
    pyodide.setStdin({
            stdin: (str) => {
                if (test_case.test_input_list.length > 0) {
                    return test_case['test_input_list'].shift();
                } else {
                    return '';
                }
            },
        });
  }
  try {
    pyodide.runPython(`
        import sys
        from io import StringIO
        sys.stdout = StringIO()
    `);
    pyodide.runPython(user_code);
    const output = pyodide.runPython("sys.stdout.getvalue()");
    pyodide.runPython("sys.stdout = sys.__stdout__");
    postMessage({ output });
  } catch (error) {
    postMessage({ error: error.message || String(error) });
  }
};
