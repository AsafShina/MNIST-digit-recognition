document.addEventListener('DOMContentLoaded', function () {
    const uploadForm = document.getElementById('uploadForm');
    const imageInput = document.getElementById('image');
    const previewContainer = document.getElementById('previewContainer');
    const resultMsg = document.getElementById('resultMsg');

    // When user selects an image, preview it
    imageInput.addEventListener('change', function (event) {
        const file = event.target.files[0];
        previewContainer.innerHTML = '';

        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                const label = document.createElement('h3');
                label.textContent = 'Selected Image Preview:';
                const img = document.createElement('img');
                img.src = e.target.result;
                previewContainer.appendChild(label);
                previewContainer.appendChild(img);
            };
            reader.readAsDataURL(file);
        }
    });

    // Handle form submission with AJAX (XMLHttpRequest)
    uploadForm.addEventListener('submit', function (event) {
        event.preventDefault();
        resultMsg.textContent = ''; // Clear previous messages

        const formData = new FormData();
        const file = imageInput.files[0];

        if (file) {
            formData.append('image', file);
        }

        const xhr = new XMLHttpRequest();
        xhr.open('POST', 'process.php', true);

        xhr.onload = function () {
            if (xhr.status === 200) {
                try {
                    const response = JSON.parse(xhr.responseText);
                    console.log("Server response:", response);

                    if (response.message) {
                        resultMsg.textContent = response.message;
                    }

                    if (response.predictedDigit !== undefined) {
                        // Display predicted digit
                        resultMsg.textContent = "Predicted Digit: " + response.predictedDigit;
                    }

                } catch (e) {
                    console.error("Error parsing server response:", e);
                    resultMsg.textContent = 'Error: Unexpected response from server.';
                }
            } else {
                console.error("Server returned an error:", xhr.status);
                resultMsg.textContent = `Error: Failed with status ${xhr.status}`;
            }
        };

        xhr.onerror = function () {
            console.error("Error communicating with server.");
            resultMsg.textContent = 'Error: Failed to communicate with the server.';
        };

        xhr.send(formData);
    });

});
