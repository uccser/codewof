importScripts("https://cdn.jsdelivr.net/pyodide/v0.27.6/full/pyodide.js");

async function initializePyodide() {
    let pyodide = await loadPyodide();
    pyodide.setStdin({
        stdin: (str) => { return prompt(str) },
    });
    return pyodide;
}

let pyodideReadyPromise = initializePyodide();

onmessage = async (event) => {
  let pyodide = await pyodideReadyPromise;
  const { user_code } = event.data;
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
