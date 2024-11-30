// const renderChart = (data, labels) => {
//     var ctx = document.getElementById("myChartForIncome").getContext("2d");
//     var myChartForIncome = new Chart(ctx, {
//       type: "doughnut",
//       data: {
//         labels: labels,
//         datasets: [
//           {
//             label: "Last 6 months income",
//             data: data,
//             backgroundColor: [
//               "rgba(255, 99, 132, 0.2)",
//               "rgba(54, 162, 235, 0.2)",
//               "rgba(255, 206, 86, 0.2)",
//               "rgba(75, 192, 192, 0.2)",
//               "rgba(153, 102, 255, 0.2)",
//               "rgba(255, 159, 64, 0.2)",
//             ],
//             borderColor: [
//               "rgba(255, 99, 132, 1)",
//               "rgba(54, 162, 235, 1)",
//               "rgba(255, 206, 86, 1)",
//               "rgba(75, 192, 192, 1)",
//               "rgba(153, 102, 255, 1)",
//               "rgba(255, 159, 64, 1)",
//             ],
//             borderWidth: 1,
//           },
//         ],
//       },
//       options: {
//         title: {
//           display: true,
//           text: "Income per source",
//         },
//       },
//     });
//   };
  
//   const getChartData = () => {
//     console.log("fetching");
//     fetch("income_source_summary")
//       .then((res) => res.json())
//       .then((results) => {
//         console.log("results", results);
//         const source_data = results.income_source_data;
//         const [labels, data] = [
//           Object.keys(source_data),
//           Object.values(source_data),
//         ];
  
//         renderChart(data, labels);
//       });
//   };
  
//   document.onload = getChartData();
  


const renderChart = (data, labels, colors) => {
  var ctx = document.getElementById("myChartForIncome").getContext("2d");
  var myChartForIncome = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Last 6 months income",
          data: data,
          backgroundColor: colors, // Use the passed color array for background
          borderColor: colors.map(color => color), // Same colors for borders
          borderWidth: 1,
        },
      ],
    },
    options: {
      title: {
        display: true,
        text: "Income per source",
      },
    },
  });
};

const getChartData = () => {
  console.log("fetching");
  fetch("income_source_summary")
    .then((res) => res.json())
    .then((results) => {
      console.log("results", results);
      const source_data = results.income_source_data;
      const [labels, data] = [
        Object.keys(source_data),
        Object.values(source_data),
      ];

      // Array of color codes
      const colorArray = [
        "#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF", 
        "#FF9F40", "#FF5733", "#C70039", "#900C3F", "#581845",
        "#FFC300", "#DAF7A6", "#A1C4FD", "#F0B27A", "#76D7C4", 
        "#F39C12"
      ];

      // If there are more sources than colors, extend the array
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
