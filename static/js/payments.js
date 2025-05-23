document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('paymentForm');
    const paymentMethods = document.getElementsByName('paymentMethod');
    const paymentDetails = document.querySelectorAll('.payment-details');

    // Handle payment method selection
    paymentMethods.forEach(method => {
        method.addEventListener('change', function() {
            paymentDetails.forEach(details => {
                details.style.display = 'none'; // Hide all payment details
            });
            const selectedDetails = document.getElementById(`${this.value}Details`);
            if (selectedDetails) {
                selectedDetails.style.display = 'block'; // Show the selected payment details
            }
        });
    });

    // Form submission handling
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        let isValid = true;
        const selectedMethod = document.querySelector('input[name="paymentMethod"]:checked');

        if (!selectedMethod) {
            alert('Please select a payment method');
            return;
        }

        // Validate payment method-specific inputs
        switch (selectedMethod.value) {
            case 'upi':
                isValid = validateUPI();
                break;
            case 'creditCard':
                isValid = validateCard('');
                break;
            case 'debitCard':
                isValid = validateCard('debit');
                break;
            case 'cod':
                isValid = true; // No specific validation needed for COD
                break;
        }

        if (isValid) {
            try {
                const response = await fetch('/submit_payment', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(getPaymentData(selectedMethod.value)),
                });

                if (response.ok) {
                    alert('Payment Successful!');
                    window.location.href = '/customer_dashboard';
                } else {
                    throw new Error('Payment failed');
                }
            } catch (error) {
                alert('Payment failed. Please try again.');
                console.error('Error:', error);
            }
        }
    });

    function validateUPI() {
        const upiId = document.getElementById('upiId');
        const upiError = document.getElementById('upiError');
        const upiPattern = /^[a-zA-Z0-9.\-_]{2,256}@[a-zA-Z]{2,64}$/;

        if (!upiPattern.test(upiId.value)) {
            upiError.textContent = 'Please enter a valid UPI ID';
            return false;
        }
        upiError.textContent = '';
        return true;
    }

    function validateCard(prefix) {
        const cardNumber = document.getElementById(`${prefix}CardNumber`);
        const expiryDate = document.getElementById(`${prefix}ExpiryDate`);
        const cvv = document.getElementById(`${prefix}Cvv`);
        const cardName = document.getElementById(`${prefix}CardName`);

        const cardNumberError = document.getElementById(`${prefix}CardNumberError`);
        const expiryError = document.getElementById(`${prefix}ExpiryError`);
        const cvvError = document.getElementById(`${prefix}CvvError`);
        const cardNameError = document.getElementById(`${prefix}CardNameError`);

        let isValid = true;

        // Card number validation
        if (!/^\d{16}$/.test(cardNumber.value.replace(/\s/g, ''))) {
            cardNumberError.textContent = 'Please enter a valid 16-digit card number';
            isValid = false;
        } else {
            cardNumberError.textContent = '';
        }

        // Expiry date validation
        const expiryPattern = /^(0[1-9]|1[0-2])\/([0-9]{2})$/;
        if (!expiryPattern.test(expiryDate.value)) {
            expiryError.textContent = 'Please enter a valid expiry date (MM/YY)';
            isValid = false;
        } else {
            expiryError.textContent = '';
        }

        // CVV validation
        if (!/^\d{3}$/.test(cvv.value)) {
            cvvError.textContent = 'Please enter a valid 3-digit CVV';
            isValid = false;
        } else {
            cvvError.textContent = '';
        }

        // Name validation
        if (!/^[a-zA-Z\s]{3,}$/.test(cardName.value)) {
            cardNameError.textContent = 'Please enter a valid name';
            isValid = false;
        } else {
            cardNameError.textContent = '';
        }

        return isValid;
    }

    function getPaymentData(paymentMethod) {
        const data = { paymentMethod };

        switch (paymentMethod) {
            case 'upi':
                data.upiId = document.getElementById('upiId').value;
                break;
            case 'creditCard':
            case 'debitCard':
                const prefix = paymentMethod === 'creditCard' ? '' : 'debit';
                data.cardNumber = document.getElementById(`${prefix}CardNumber`).value;
                data.cardExpiry = document.getElementById(`${prefix}ExpiryDate`).value;
                data.cardCVV = document.getElementById(`${prefix}Cvv`).value;
                data.cardName = document.getElementById(`${prefix}CardName`).value;
                break;
            case 'cod':
                data.message = 'Cash on Delivery chosen.';
                break;
        }

        return data;
    }
});
