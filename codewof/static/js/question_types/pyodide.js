let pyodideReadyPromise = loadPyodide();
let interruptBuffer = null;

self.onmessage = async (event) => {
  // Handle interrupt buffer setup
  if (event.data.cmd === "setInterruptBuffer") {
    interruptBuffer = event.data.interruptBuffer;
    const pyodide = await pyodideReadyPromise;
    pyodide.setInterruptBuffer(interruptBuffer);
    return;
  }

  // Handle code execution
  if (event.data.cmd === "runCode") {
    const pyodide = await pyodideReadyPromise;
    try {
      // Clear interrupt buffer before running code
      if (interruptBuffer) interruptBuffer[0] = 0;
      const result = await pyodide.runPythonAsync(event.data.code);
      self.postMessage({ result });
    } catch (error) {
      self.postMessage({ error: error.message });
    }
    return;
  }
};

// Function to run Python code with a timeout
function runPythonWithTimeout(code) {
    const timeoutMs = 2000; // Set the timeout duration (in milliseconds)
    return new Promise((resolve, reject) => {
        let finished = false;

        // Listen for worker messages
        pyodideWorker.onmessage = (event) => {
        finished = true;
        if (event.data.error) {
            reject(new Error(event.data.error));
        } else {
            resolve(event.data.result);
        }
        };

        // Start code execution
        pyodideWorker.postMessage({ cmd: "runCode", code });

        // Setup timeout to interrupt execution
        setTimeout(() => {
        if (!finished) {
            // 2 stands for SIGINT (KeyboardInterrupt)
            interruptBuffer[0] = 2;
            reject(new Error("Execution timed out and was interrupted."));
        }
        }, timeoutMs);
    });
}

exports.runPythonWithTimeout = runPythonWithTimeout;
