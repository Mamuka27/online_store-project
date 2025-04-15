
const images = [
  document.getElementById("mainImage").src,
  ...Array.from(document.querySelectorAll(".thumb")).slice(1).map(img => img.src)
];
let currentIndex = 0;

function setImage(index) {
  currentIndex = index;
  document.getElementById("mainImage").src = images[index];
  document.querySelectorAll(".thumb").forEach((thumb, i) => {
    thumb.classList.toggle("active-thumb", i === index);
  });
}

function prevImage() {
  currentIndex = (currentIndex - 1 + images.length) % images.length;
  setImage(currentIndex);
}

function nextImage() {
  currentIndex = (currentIndex + 1) % images.length;
  setImage(currentIndex);
}








document.addEventListener("DOMContentLoaded", function () {
  const countdownEl = document.getElementById("discountCountdown");
  if (!countdownEl) return;

  const expiryString = countdownEl.getAttribute("data-expiry");
  const expiryDate = new Date(expiryString.replace(/-/g, "/"));

  function updateCountdown() {
    const now = new Date();
    const diff = expiryDate - now;

    if (diff <= 0) {
      countdownEl.textContent = "Expired";
      return;
    }

    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    const hours = Math.floor((diff / (1000 * 60 * 60)) % 24);
    const minutes = Math.floor((diff / (1000 * 60)) % 60);

    countdownEl.textContent = `${days}d ${hours}h ${minutes}m`;
  }

  updateCountdown();
  setInterval(updateCountdown, 60000);
});















document.addEventListener("DOMContentLoaded", function () {

  const labels = JSON.parse(document.getElementById("price_labels").textContent);
  const basePrices = JSON.parse(document.getElementById("price_values").textContent);
  const discountPrices = JSON.parse(document.getElementById("discount_values").textContent);

  const ctx = document.getElementById("priceChart").getContext("2d");

  new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels.map(d => new Date(d).toLocaleDateString()),
      datasets: [
        {
          label: 'Base Price',
          data: basePrices,
          borderColor: 'rgba(54, 162, 235, 1)',
          backgroundColor: 'rgba(54, 162, 235, 0.3)',
          fill: true,
          tension: 0.3
        },
        {
          label: 'Sale Price',
          data: discountPrices,
          borderColor: 'rgba(255, 99, 132, 1)',
          backgroundColor: 'rgba(255, 99, 132, 0.1)',
          fill: false,
          tension: 0.4,
          pointRadius: 6,
          pointHoverRadius: 8,
          pointBackgroundColor: discountPrices.map((val, i, arr) =>
            (i > 0 && val !== null && arr[i - 1] !== null && val < arr[i - 1]) ? 'red' : 'rgba(255, 99, 132, 1)'
          ),
          borderDash: [5, 5]
        }
      ]
    },
    options: {
      responsive: true,
      animation: {
        duration: 1500,
        easing: 'easeOutBounce'
      },
      plugins: {
        legend: { position: 'top' },
        title: { display: true, text: 'Price History' },
        tooltip: {
          callbacks: {
            label: (ctx) => ctx.raw ? `₾${ctx.raw}` : 'No Discount'
          }
        }
      },
      scales: {
        y: {
          ticks: {
            callback: value => '₾' + value.toLocaleString()
          }
        }
      }
    }
  });
});





function scrollRecommendations(direction) {
  const container = document.getElementById('recommendationScroll');
  const scrollAmount = 280;
  container.scrollBy({
    left: direction * scrollAmount,
    behavior: 'smooth'
  });
}
