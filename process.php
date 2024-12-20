<?php
header('Content-Type: application/json');

$response = [
    'message' => '',
    'predictedDigit' => null
];

$uploadDir = __DIR__ . '/uploads/';
if (!is_dir($uploadDir)) {
    mkdir($uploadDir, 0777, true);
}

$logFile = __DIR__ . '/debug.log';
function logMessage($message) {
    global $logFile;
    file_put_contents($logFile, date('Y-m-d H:i:s') . ' - ' . $message . PHP_EOL, FILE_APPEND);
}

logMessage("Request received: " . json_encode($_POST));

if (isset($_FILES['image']) && $_FILES['image']['error'] === UPLOAD_ERR_OK) {
    $tmpName = $_FILES['image']['tmp_name'];
    $originalName = basename($_FILES['image']['name']);
    $targetPath = $uploadDir . $originalName;

    logMessage("Uploading new file: $originalName");

    if (move_uploaded_file($tmpName, $targetPath)) {
        // Redirect stderr to nul to suppress any TensorFlow logs
        $command = "/usr/bin/python3 predict_digit.py " . escapeshellarg($targetPath) . " 2>>error.log";
        logMessage("Executing command: $command");

        $output = shell_exec($command);
        logMessage("Raw Python script output: " . $output);

        $data = json_decode($output, true);

        if (isset($data['predictedDigit']) && is_numeric($data['predictedDigit'])) {
            $response['message'] = "Digit prediction successful!";
            $response['predictedDigit'] = (int)$data['predictedDigit'];
        } elseif (isset($data['error'])) {
            $response['message'] = $data['error'];
            logMessage("Python error: " . $data['error']);
        } else {
            $response['message'] = "Failed to predict the digit. Invalid output.";
            logMessage("Error: Invalid JSON response.");
        }
    } else {
        $response['message'] = "Failed to move uploaded file.";
        logMessage("Error: Failed to move uploaded file.");
    }
} else {
    $response['message'] = "No file uploaded or invalid request.";
    logMessage("Error: No file uploaded or invalid request.");
}

echo json_encode($response);
