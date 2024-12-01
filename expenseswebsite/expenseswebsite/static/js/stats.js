

const renderChart = (data, labels, colors) => {
  var ctx = document.getElementById("myChartForExpense").getContext("2d");
  var myChartForExpense = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Last 6 months expenses",
          data: data,
          backgroundColor: colors,  // Use the passed color array for background
          borderColor: colors.map(color => color),  // Same colors for borders
          borderWidth: 1,
        },
      ],
    },
    options: {
      title: {
        display: true,
        text: "Expenses per category",
      },
    },
  });
};

const getChartData = () => {
  console.log("fetching");
  fetch("expense_category_summary")
    .then((res) => res.json())
    .then((results) => {
      console.log("results", results);
      const category_data = results.expense_category_data;
      const [labels, data] = [
        Object.keys(category_data),
        Object.values(category_data),
      ];

      // Array of color codes
      const colorArray = [
        "#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF", 
        "#FF9F40", "#FF5733", "#C70039", "#900C3F", "#581845",
        "#FFC300", "#DAF7A6", "#A1C4FD", "#F0B27A", "#76D7C4", 
        "#F39C12"
      ];

      // If there are more categories than colors, you could repeat the colors or extend the array
      if (data.length > colorArray.length) {
        const times = Math.ceil(data.length / colorArray.length);
        const extendedColors = Array(times).fill(colorArray).flat().slice(0, data.length);
        renderChart(data, labels, extendedColors);
      } else {
        renderChart(data, labels, colorArray.slice(0, data.length));
      }
    });
};

document.onload = getChartData();
