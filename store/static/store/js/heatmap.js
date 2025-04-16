document.addEventListener("DOMContentLoaded", function () {
    const labels = JSON.parse(document.getElementById("chart-labels").textContent);
    const viewsData = JSON.parse(document.getElementById("views-data").textContent);
    const wishlistData = JSON.parse(document.getElementById("wishlist-data").textContent);
    const orderData = JSON.parse(document.getElementById("order-data").textContent);
    const thumbsData = JSON.parse(document.getElementById("thumbs-data").textContent);
  
    const ctx = document.getElementById("heatmapChart").getContext("2d");
  
    new Chart(ctx, {
      type: "bar",
      data: {
        labels: labels,
        datasets: [
          {
            label: "Views",
            data: viewsData,
            backgroundColor: "rgba(255, 99, 132, 0.5)",
          },
          {
            label: "Wishlists",
            data: wishlistData,
            backgroundColor: "rgba(54, 162, 235, 0.5)",
          },
          {
            label: "Purchases",
            data: orderData,
            backgroundColor: "rgba(75, 192, 192, 0.5)",
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: {
          mode: "index",
          intersect: false,
        },
        plugins: {
          tooltip: {
            enabled: false,
            external: function (context) {
              const tooltipModel = context.tooltip;
              let tooltipEl = document.getElementById("chartjs-tooltip");
  
              if (!tooltipEl) {
                tooltipEl = document.createElement("div");
                tooltipEl.id = "chartjs-tooltip";
                tooltipEl.innerHTML = "<table></table>";
                tooltipEl.style.background = "#222";
                tooltipEl.style.color = "#fff";
                tooltipEl.style.borderRadius = "8px";
                tooltipEl.style.padding = "12px";
                tooltipEl.style.position = "absolute";
                tooltipEl.style.pointerEvents = "none";
                tooltipEl.style.transition = "all .1s ease";
                tooltipEl.style.zIndex = "100";
                document.body.appendChild(tooltipEl);
              }
  
              if (tooltipModel.opacity === 0) {
                tooltipEl.style.opacity = "0";
                return;
              }
  
              const index = tooltipModel.dataPoints[0].dataIndex;
              const title = tooltipModel.title[0];
              const views = viewsData[index];
              const wishes = wishlistData[index];
              const purchases = orderData[index];
              const thumb = thumbsData[index] || "/static/store/img/placeholder.png";
  
              tooltipEl.querySelector("table").innerHTML = `
                <tr><td><strong>${title}</strong></td></tr>
                <tr><td style="color:#ff6384;">🧿 Views: ${views}</td></tr>
                <tr><td style="color:#36a2eb;">❤️ Wishlists: ${wishes}</td></tr>
                <tr><td style="color:#4bc0c0;">🛒 Purchases: ${purchases}</td></tr>
                <tr><td>📷 Thumbnail:<br><img src="${thumb}" alt="thumb" width="80" height="80" style="margin-top:4px; border-radius:4px;"/></td></tr>
              `;
  
              const canvasRect = context.chart.canvas.getBoundingClientRect();
              tooltipEl.style.opacity = "1";
              tooltipEl.style.left = canvasRect.left + window.pageXOffset + tooltipModel.caretX + "px";
              tooltipEl.style.top = canvasRect.top + window.pageYOffset + tooltipModel.caretY + "px";
            },
          },
          legend: {
            position: "top",
            labels: {
              boxWidth: 20,
              padding: 15,
            },
          },
          title: {
            display: true,
            text: "Heatmap of Item Popularity",
            font: {
              size: 18,
            },
          },
        },
        scales: {
          x: {
            ticks: {
              maxRotation: 45,
              minRotation: 45,
              autoSkip: false,
            },
          },
          y: {
            beginAtZero: true,
            title: {
              display: true,
              text: "Popularity Score",
            },
          },
        },
      },
    });
  

    const rangeSelect = document.getElementById("rangeSelect");
    const customDates = document.getElementById("customDates");
    const customDatesEnd = document.getElementById("customDatesEnd");
  
    function toggleCustomDate() {
      const show = rangeSelect.value === "custom";
      customDates.style.display = show ? "block" : "none";
      customDatesEnd.style.display = show ? "block" : "none";
    }
  
    rangeSelect.addEventListener("change", toggleCustomDate);
    toggleCustomDate();
  });
  