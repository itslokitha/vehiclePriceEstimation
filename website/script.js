// script.js
function sendPredictionRequest(event) {
    event.preventDefault(); // Prevent the form from submitting normally
    var formElements = document.getElementById("predictionForm").elements;
    var formData = {
        year: formElements.namedItem("year").value,
        make: formElements.namedItem("make").value,
        model: formElements.namedItem("model").value,
        mileage: formElements.namedItem("mileage").value
    };
    
    // fetch('/predict', {
    //     method: 'POST',
    //     headers: {
    //         'Content-Type': 'application/x-www-form-urlencoded',
    //     },
    //     body: new URLSearchParams(formData)
    // })
    // .then(response => response.json())
    // .then(data => {
    //     document.getElementById('prediction-result').innerText = 'Predicted Price: ' + data.prediction;
    // })
    // .catch(error => {
    //     document.getElementById('prediction-result').innerText = 'Error: ' + error;
    // });

    fetch('/predict', {
        method: 'POST',
        // Ensure the Content-Type is set correctly for form data
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams(formData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json();  // Parse JSON only if the response was ok
    })
    .then(data => {
        if (data.error) {
            throw new Error(data.error);
        }
        document.getElementById('prediction-result').innerText = 'Predicted Price: ' + data.prediction;
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('prediction-result').innerText = 'Error: ' + error.message;
    });
}

document.getElementById("predictionForm").addEventListener("submit", sendPredictionRequest);