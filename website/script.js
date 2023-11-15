function sendPredictionRequest(event) {
    event.preventDefault();
    var formElements = document.getElementById("predictionForm").elements;
    var formData = {
        year: formElements.namedItem("year").value,
        make: formElements.namedItem("make").value,
        model: formElements.namedItem("model").value,
        mileage: formElements.namedItem("mileage").value
    };

    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams(formData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            throw new Error(data.error);
        }
        displayResults(data, formData.year, formData.make, formData.model, formData.mileage);
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
        myChart.destroy();
    }
    myChart = new Chart(ctx, {
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
            },
            plugins: {
                tooltip: {
                    enabled: true
                },
                datalabels: {
                    color: '#000000',
                    anchor: 'end',
                    align: 'top',
                    formatter: function(value, context) {
                        return '$' + value.toFixed(2);
                    }
                }
            }
        }
    });
}

function displayResults(data, year, make, model, mileage) {
    document.getElementById('vehicle-info').innerText = `Year: ${year}, Make: ${make}, Model: ${model}, Mileage: ${mileage}`;
    document.getElementById('predicted-price').innerText = `Predicted Price: ${data.prediction}`;
    document.getElementById('prediction-result').style.display = 'block';
    document.getElementById('back-button').style.display = 'block';
    if (data.averagePrice > 0 || data.lowestPrice > 0 || data.highestPrice > 0) {
        renderGraph(data.averagePrice, data.lowestPrice, data.highestPrice);
    } else {
        document.getElementById('price-chart').style.display = 'none';
    }
}

document.getElementById('back-button').addEventListener('click', function() {
    document.getElementById('prediction-result').style.display = 'none';
    document.getElementById('predictionForm').style.display = 'block';
    this.style.display = 'none';
});

function resetGraphDisplay() {
    document.getElementById('price-chart').style.display = 'block';
}
document.getElementById("predictionForm").addEventListener("submit", sendPredictionRequest);

document.getElementById("predictionForm").addEventListener("submit", function(event) {
    resetGraphDisplay();
    sendPredictionRequest(event);
});

document.getElementById('theme-toggle').addEventListener('change', function(event) {
    const label = document.getElementById('toggle-label');
    if (event.target.checked) {
        document.body.classList.replace('light-theme', 'dark-theme');
        label.textContent = 'Light Mode';
    } else {
        document.body.classList.replace('dark-theme', 'light-theme');
        label.textContent = 'Dark Mode';
    }
});
