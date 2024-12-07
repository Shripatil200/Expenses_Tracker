(() => {
  'use strict'

  // Graphs
  const ctx = document.getElementById('myChart');
  // eslint-disable-next-line no-unused-vars
  const myChart = new Chart(ctx, {
      type: 'line',
      data: {
          labels: [
              'January',
              'February',
              'March',
              'April',
              'May',
              'June',
              'July',
              'August',
              'September',
              'October',
              'November',
              'December'
          ],
          datasets: [
              {
                  label: 'Income',
                  data: [
                      50000, 45000, 48000, 52000, 55000, 60000, 58000, 57000, 59000, 62000, 61000, 63000
                  ],
                  lineTension: 0,
                  backgroundColor: 'transparent',
                  borderColor: '#007bff',
                  borderWidth: 4,
                  pointBackgroundColor: '#007bff'
              },
              {
                  label: 'Expenses',
                  data: [
                      40000, 35000, 37000, 40000, 42000, 45000, 43000, 44000, 46000, 48000, 47000, 50000
                  ],
                  lineTension: 0,
                  backgroundColor: 'transparent',
                  borderColor: '#ff073a',
                  borderWidth: 4,
                  pointBackgroundColor: '#ff073a'
              }
          ]
      },
      options: {
          plugins: {
              legend: {
                  display: true
              },
              tooltip: {
                  boxPadding: 3
              }
          },
          scales: {
              y: {
                  beginAtZero: true
              }
          }
      }
  });
})();
