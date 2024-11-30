window.onload = function() {
    fetchMonthlyIncomeData();  // Call the function to fetch the monthly income data
};

// Function to fetch monthly income data

function fetchMonthlyIncomeData() {
    fetch('monthly-income-summary')  // This is the URL from where we fetch the monthly income data
        .then(response => response.json())
        .then(data => {
            console.log(data); // This will log the data fetched from the server

            // Check if the data structure is as expected
            if (data.monthly_incomes && Array.isArray(data.monthly_incomes)) {
                const months = data.monthly_incomes.map(item => item.month); // Extract month names (or keys like "2024-01")
                const incomes = data.monthly_incomes.map(item => item.total_income); // Extract total income for each month

                renderChartForIncomeByDate(months, incomes);  // Render the chart with the fetched data
            } else {
                console.error("Invalid data structure: monthly_incomes is missing or not an array.");
            }
        })
        .catch(error => console.error('Error fetching monthly income:', error));
}

// Function to render the chart for monthly income
function renderChartForIncomeByDate(months, incomes) {
    const ctx = document.getElementById('myChartForIncomeByDate').getContext('2d');

    const colors = [
        '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40', 
        '#C9CBCF', '#F7464A', '#46BFBD', '#FDB45C', '#949FB1', '#4D5360'
    ]; 
    
    const myChart = new Chart(ctx, {
        type: 'pie',  // Bar chart to display the monthly income data
        data: {
            labels: months,  // The months on the X-axis
            datasets: [{
                label: 'Total Income',  // Label for the dataset
                data: incomes,  // The total income values for each month
                backgroundColor: colors, // Assign colors to the data points
                borderColor: '#FFFFFF',  // Optional: Add a white border for segments
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true  // Make sure the Y-axis starts at zero
                }
            }
        }
    });
}

