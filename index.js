const express = require("express");
const bodyParser = require("body-parser");
const { spawn } = require('child_process'); 

const app = express();

app.use(bodyParser.urlencoded({ extended: false })); // Parse URL-encoded bodies
app.use(bodyParser.json()); // Parse JSON bodies

app.listen(3000, function () {
    console.log("Server is up and running...");
});

app.get("/", function (_req, res) {
    res.sendFile(__dirname+"/login.html");
});

app.get("/index.html", function (_req, res) {
    res.sendFile(__dirname+"/index.html");
});

app.post("/", function (req, res) {
var sprintName = req.body.sprintName.trim();
var projectName = req.body.projectName.trim();
var authId = req.body.authId.trim();
var releaseVersion = req.body.releaseVersion.trim();
var testType = req.body.testType.trim();
var instancesTested = req.body.instancesTested.trim();
var platformOsVersion = req.body.platformOsVersion.trim();
var apiVersion = req.body.apiVersion.trim();
var releaseDate = req.body.releaseDate.trim();
var releaseType = req.body.releaseType.trim();
    
// Execute the Python script with the provided form data to get release notes

const pythonProcess = spawn('python', [__dirname + '\\main.py', projectName, sprintName, authId, releaseVersion, testType, instancesTested, platformOsVersion, apiVersion, releaseDate, releaseType]);


pythonProcess.stdout.on('data', (data) => {
    console.log(`Python Script Output: ${data}`);
    // You can send a response back to the client here if needed
});

pythonProcess.stderr.on('data', (data) => {
    console.error(`Error from Python Script: ${data}`);
    // You can send an error response back to the client here if needed
    res.status(500).send(`Error from Python Script: ${data}`);
});

pythonProcess.on('close', (code) => {
    if (code === 0) {
        // Python script has completed successfully
        const pdfFilePath = `${sprintName}.pdf`; // Specify the path to the generated PDF file
        // Use res.download() to automatically trigger a download of the PDF file
        res.download(pdfFilePath, `${sprintName}_report.pdf`, (err) => {
            if (err) {
                console.error("Error sending file for download:", err);
                // You can send an error response back to the client here if needed
                res.status(500).send(`Error sending file for download: ${err}`);
            } else {
                console.log("File sent for download successfully.");
            }
        });
    }
});
});
