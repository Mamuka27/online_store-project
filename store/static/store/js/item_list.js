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
  updateCountdowns();
  







  function addToCompare(itemId) {
    fetch(`/add-to-compare/${itemId}/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCookie('csrftoken'),
        'Content-Type': 'application/json',
      },
      credentials: 'same-origin',
    })
    .then(response => {
      if (response.ok) {
        window.location.href = '/compare/';
      } else {
        alert('Failed to add item to comparison list.');
      }
    })
    .catch(error => {
      console.error('Error adding to compare:', error);
    });
  }
  

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();

        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  
