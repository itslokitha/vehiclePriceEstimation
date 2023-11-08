function sendPredictionRequest(event) {
    event.preventDefault(); // Prevent the form from submitting normally
    var formElements = document.getElementById("predictionForm").elements;
    var formData = {
        year: formElements.namedItem("year").value,
        make: formElements.namedItem("make").value,
        model: formElements.namedItem("model").value,
        mileage: formElements.namedItem("mileage").value
    };

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
        displayResults(data, formData.year, formData.make, formData.model, formData.mileage);    
        renderGraph(data.averagePrice, data.lowestPrice, data.highestPrice);
        document.getElementById('prediction-result').innerText = 'Predicted Price: ' + data.prediction;
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('prediction-result').innerText = 'Error: ' + error.message;
    });
}

var myChart;

function renderGraph(averagePrice, lowestPrice, highestPrice) {
    var ctx = document.getElementById('price-chart').getContext('2d');
    if (myChart) {
        // Destroy the previous chart
        myChart.destroy();
    }
    var chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Average Price', 'Lowest Price', 'Highest Price'],
            datasets: [{
                label: 'Price',
                data: [averagePrice, lowestPrice, highestPrice],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(75, 192, 192, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(75, 192, 192, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function displayResults(data, year, make, model, mileage) {
    document.getElementById('vehicle-info').innerText = `Year: ${year}, Make: ${make}, Model: ${model}, Mileage: ${mileage}`;
    document.getElementById('predicted-price').innerText = `Predicted Price: ${data.prediction}`;

    // Display the results section and hide the form
    document.getElementById('predictionForm').classList.add('hidden');
    document.getElementById('prediction-result').classList.remove('hidden');

    // Placeholder for graph rendering logic
    renderGraph(data.averagePrice, data.lowestPrice, data.highestPrice);
}

document.getElementById("predictionForm").addEventListener("submit", sendPredictionRequest);