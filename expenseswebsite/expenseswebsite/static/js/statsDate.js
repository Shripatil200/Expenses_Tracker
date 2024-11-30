
// statsDate.js
window.onload = function() {
    fetchMonthlyExpenseData();  // Call the function to fetch the monthly expense data
};

// Function to fetch monthly expense data
function fetchMonthlyExpenseData() {
    fetch('monthly-expense-summary')  // This is the URL from where we fetch the monthly expense data
        .then(response => response.json())
        .then(data => {
            console.log(data); // This will log the data fetched from the server

            const months = data.monthly_expenses.map(item => item.month); // Extract month names (or keys like "2024-01")
            const expenses = data.monthly_expenses.map(item => item.total_expense); // Extract total expenses for each month

            renderChartForExpenseByDate(months, expenses);  // Render the chart with the fetched data
        })
        .catch(error => console.error('Error fetching monthly expenses:', error));
}

// Function to render the chart for expenses by month
function renderChartForExpenseByDate(months, expenses) {
    const ctx = document.getElementById('myChartForExpenseByDate').getContext('2d');

    const colors = [
        '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40', 
        '#C9CBCF', '#F7464A', '#46BFBD', '#FDB45C', '#949FB1', '#4D5360'
    ]; 
    
    const myChart = new Chart(ctx, {
        type: 'pie',  // We are using a line chart to display the monthly trend
        data: {
            labels: months,  // The months on the X-axis
            datasets: [{
                label: 'Total Expenses',  // Label for the dataset
                data: expenses,  // The total expense values for each month
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
