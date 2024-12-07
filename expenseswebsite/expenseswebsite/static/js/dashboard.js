
fetch('/dashboard/data/')
    .then(response => response.json())
    .then(data => {
        const ctx = document.getElementById('monthlySummaryChart').getContext('2d');
        const chart = new Chart(ctx, {

            type: 'line',
            data: {
                labels: data.monthly_data.map(item => item.month),
                datasets: [{
                    label: 'Income',
                    data: data.monthly_data.map(item => item.income),
                    borderColor: 'rgba(75, 192, 192, 1)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    fill: true,
                    tension: 0.4
                }, {
                    label: 'Expense',
                    data: data.monthly_data.map(item => item.expense),
                    borderColor: 'rgba(255, 99, 132, 1)',
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    }
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Month'
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Amount'
                        },
                        beginAtZero: true
                    }
                }
            }
        });
    })
    .catch(error => console.error('Error fetching data:', error));

