function updateCountdowns() {
    const now = new Date().getTime();
    document.querySelectorAll('.countdown').forEach(span => {
      const expiry = new Date(span.dataset.expiry).getTime();
      const diff = expiry - now;
      if (diff > 0) {
        const days = Math.floor(diff / (1000 * 60 * 60 * 24));
        const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
        span.textContent = `${days}d ${hours}h ${minutes}m`;
      } else {
        span.textContent = "Expired";
      }
    });
  }
  
  setInterval(updateCountdowns, 60000);
  document.addEventListener('DOMContentLoaded', updateCountdowns);
  