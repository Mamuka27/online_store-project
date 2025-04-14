function detectCardType(input) {
    let number = input.value.replace(/\D/g, '');
    const logo = document.getElementById('cardLogo');
  
    let type = 'default';
    if (/^4/.test(number)) type = 'visa';
    else if (/^5[1-5]/.test(number) || /^2[2-7]/.test(number)) type = 'mastercard';
    else if (/^3[47]/.test(number)) type = 'amex';
    else if (/^6(?:011|5)/.test(number)) type = 'discover';
  
    const logos = {
      visa: document.getElementById('cardPathVisa').dataset.url,
      mastercard: document.getElementById('cardPathMastercard').dataset.url,
      amex: document.getElementById('cardPathAmex').dataset.url,
      discover: document.getElementById('cardPathDiscover').dataset.url,
      default: document.getElementById('cardPathDefault').dataset.url
    };
  
    logo.src = logos[type] || logos.default;
    input.value = number.replace(/(\d{4})(?=\d)/g, "$1 ").trim();
  }
  
  function fillCardForm(number, expiry, cvv, name) {
    document.getElementById('cardNumber').value = number.replace(/(\d{4})(?=\d)/g, "$1 ").trim();
    document.getElementById('expiryDate').value = expiry;
    document.getElementById('cvv').value = cvv;
    document.getElementById('cardName').value = name;
    detectCardType(document.getElementById('cardNumber'));
  }
  
  document.addEventListener('DOMContentLoaded', () => {
    const cardNumberInput = document.getElementById('cardNumber');
    const cvvInput = document.getElementById('cvv');
    const expiryInput = document.getElementById('expiryDate');
    const nameInput = document.getElementById('cardName');
  
    cardNumberInput.addEventListener('input', function () {
      let value = this.value.replace(/\D/g, '').slice(0, 16);
      this.value = value.replace(/(\d{4})(?=\d)/g, '$1 ').trim();
    });
  
    cvvInput.addEventListener('input', function () {
      this.value = this.value.replace(/\D/g, '').slice(0, 4);
    });
  
    expiryInput.addEventListener('input', function () {
      let raw = this.value.replace(/\D/g, '').slice(0, 4);
      let month = raw.slice(0, 2);
      let year = raw.slice(2);
      if (month.length === 2 && (parseInt(month) < 1 || parseInt(month) > 12)) {
        month = '12';
      }
      this.value = month + (year ? '/' + year : '');
    });
  
    nameInput.addEventListener('input', function () {
      this.value = this.value.replace(/[^a-zA-Z\s]/g, '');
    });
  });
  