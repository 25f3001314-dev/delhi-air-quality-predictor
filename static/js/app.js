let aqiChart;

function formatOneDecimal(value) {
    const numericValue = Number(value);

    if (!Number.isFinite(numericValue)) {
        return 'N/A';
    }

    return numericValue.toFixed(1);
}

function setErrorState(message) {
    const errorMessage = document.getElementById('errorMessage');

    if (errorMessage) {
        errorMessage.textContent = message;
        errorMessage.hidden = false;
    }
}

function clearErrorState() {
    const errorMessage = document.getElementById('errorMessage');

    if (errorMessage) {
        errorMessage.textContent = '';
        errorMessage.hidden = true;
    }
}

async function fetchCurrentAQI() {
    try {
        const response = await fetch('/api/current');
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        const data = await response.json();

        if (!data || data.status === 'error') {
            throw new Error(data?.message || 'AQI data is unavailable');
        }

        if (!Number.isFinite(Number(data.aqi)) || !data.category || !data.color) {
            throw new Error('AQI payload is invalid');
        }

        clearErrorState();
        
        document.getElementById('aqiNumber').textContent = data.aqi;
        document.getElementById('categoryValue').textContent = data.category;
        document.getElementById('pm25Value').textContent = data.pm25;
        document.getElementById('pm10Value').textContent = data.pm10;
        document.getElementById('temperature').textContent = formatOneDecimal(data.temperature);
        document.getElementById('humidity').textContent = `${formatOneDecimal(data.humidity)} %`;
        document.getElementById('windSpeed').textContent = `${formatOneDecimal(data.wind_speed)} km/h`;
        document.getElementById('lastUpdated').textContent = data.timestamp;

        const weatherCondition = document.getElementById('weatherCondition');

        if (weatherCondition) {
            weatherCondition.textContent = data.weather_condition || data.category || 'Current conditions';
        }
        
        // Update colors based on AQI
        document.getElementById('aqiNumber').style.color = data.color;
        document.getElementById('categoryValue').style.color = data.color;
        
    } catch (error) {
        console.error('Error fetching current AQI:', error);
        setErrorState(`Unable to load current AQI data: ${error.message}`);
    }
}

async function fetchHistoricalData() {
    try {
        const response = await fetch('/api/historical');
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        const data = await response.json();

        if (!Array.isArray(data) || data.length === 0) {
            throw new Error('Historical AQI data is unavailable');
        }
        
        // Find min and max
        const values = data.map(d => d.aqi);
        const minAqi = Math.min(...values);
        const maxAqi = Math.max(...values);
        const minIndex = values.indexOf(minAqi);
        const maxIndex = values.indexOf(maxAqi);
        
        document.getElementById('minAqi').textContent = minAqi;
        document.getElementById('maxAqi').textContent = maxAqi;
        document.getElementById('minTime').textContent = data[minIndex].timestamp;
        document.getElementById('maxTime').textContent = data[maxIndex].timestamp;
        
        renderChart(data);
    } catch (error) {
        console.error('Error fetching historical data:', error);
        setErrorState(`Unable to load historical AQI data: ${error.message}`);
    }
}

function renderChart(data) {
    const ctx = document.getElementById('aqiChart').getContext('2d');
    
    if (aqiChart) {
        aqiChart.destroy();
    }
    
    const labels = data.map(d => d.timestamp);
    const aqiValues = data.map(d => d.aqi);
    
    // Color bars based on AQI value
    const barColors = aqiValues.map(aqi => {
        if (aqi <= 50) return '#00e400';
        if (aqi <= 100) return '#ffff00';
        if (aqi <= 150) return '#ff7e00';
        if (aqi <= 200) return '#ff0000';
        if (aqi <= 300) return '#8f3f97';
        return '#7e0023';
    });
    
    aqiChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'New Delhi',
                data: aqiValues,
                backgroundColor: barColors,
                borderWidth: 0,
                barThickness: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return 'AQI: ' + context.parsed.y;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 400,
                    title: {
                        display: true,
                        text: 'AQI (US)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Time'
                    },
                    ticks: {
                        maxTicksLimit: 12
                    }
                }
            }
        }
    });
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    fetchCurrentAQI();
    fetchHistoricalData();
    
    // Refresh every 5 minutes
    setInterval(fetchCurrentAQI, 300000);
    setInterval(fetchHistoricalData, 300000);
    
    // Manual refresh button
    const refreshButton = document.querySelector('.refresh-btn');

    if (refreshButton) {
        refreshButton.addEventListener('click', () => {
            fetchCurrentAQI();
            fetchHistoricalData();
        });
    }
});
