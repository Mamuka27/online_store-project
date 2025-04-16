document.addEventListener("DOMContentLoaded", () => {
    const labels = JSON.parse(document.getElementById("chart-labels").textContent);
    const values = JSON.parse(document.getElementById("chart-values").textContent);
  
    const ctx = document.getElementById('itemSalesChart').getContext('2d');
    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [{
          label: 'Items Sold',
          data: values,
          backgroundColor: 'rgba(0, 123, 255, 0.7)',
          borderColor: 'rgba(0, 123, 255, 1)',
          borderWidth: 1,
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: function(context) {
                return `Sold: ${context.parsed.y}`;
              }
            }
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            ticks: { stepSize: 1 }
          }
        }
      }
    });
  });
  