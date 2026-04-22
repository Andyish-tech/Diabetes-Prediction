const express = require('express');
const cors = require('cors');
const { spawn } = require('child_process');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3001;

app.use(cors());
app.use(express.json());

// Main prediction endpoint
app.post('/api/predict', (req, res) => {
    const inputData = req.body;
    
    // Convert object to JSON string to pass as a command line argument
    const jsonString = JSON.stringify(inputData);
    
    // Determine the absolute path to the Python script
    const pythonScriptPath = path.resolve(__dirname, '..', 'ml', 'predict.py');
    
    // Spawn a child process to run the Python script
    // We assume 'python' is mapped correctly in the host environment.
    const pythonProcess = spawn('python', [pythonScriptPath, jsonString]);

    let dataString = '';
    let errorString = '';

    // Capture standard output from the Python script
    pythonProcess.stdout.on('data', (data) => {
        dataString += data.toString();
    });

    // Capture standard error
    pythonProcess.stderr.on('data', (data) => {
        errorString += data.toString();
    });

    // Handle process completion
    pythonProcess.on('close', (code) => {
        if (code !== 0 || errorString) {
            console.error(`Python script exited with code ${code}`);
            console.error(errorString);
            return res.status(500).json({ success: false, error: 'Failed to perform prediction' });
        }

        try {
            // Trim and parse the JSON returned by Python
            const result = JSON.parse(dataString.trim());
            return res.json(result);
        } catch (error) {
            console.error("Failed to parse Python output:", dataString);
            return res.status(500).json({ success: false, error: 'Invalid response from prediction engine' });
        }
    });
});

app.listen(PORT, () => {
    console.log(`Backend server is running on http://localhost:${PORT}`);
});
