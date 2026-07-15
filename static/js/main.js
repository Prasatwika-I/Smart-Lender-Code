document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    if (!form) return;

    // Credit History warning banner dynamic toggle
    const creditHistorySelect = document.getElementById('Credit_History');
    const creditWarning = document.getElementById('creditWarning');

    if (creditHistorySelect && creditWarning) {
        // Run once on load to set initial state (if values pre-filled)
        toggleCreditWarning(creditHistorySelect.value);

        creditHistorySelect.addEventListener('change', function () {
            toggleCreditWarning(this.value);
        });
    }

    function toggleCreditWarning(value) {
        if (value === '0.0') {
            creditWarning.classList.remove('d-none');
        } else {
            creditWarning.classList.add('d-none');
        }
    }

    // Single page form validation and submit loading state
    form.addEventListener('submit', function (event) {
        let valid = true;
        const requiredInputs = form.querySelectorAll('[required]');

        requiredInputs.forEach(input => {
            if (!input.value.trim()) {
                input.classList.add('is-invalid');
                valid = false;
            } else {
                input.classList.remove('is-invalid');
                
                // Numeric fields check
                if (input.type === 'number') {
                    const val = parseFloat(input.value);
                    if (isNaN(val) || val < 0) {
                        input.classList.add('is-invalid');
                        valid = false;
                    }
                }
            }
        });

        if (!valid) {
            event.preventDefault();
            // Scroll to the first invalid element
            const firstInvalid = form.querySelector('.is-invalid');
            if (firstInvalid) {
                firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
                firstInvalid.focus();
            }
        } else {
            // Show loading spinner on the submit button
            const submitBtn = document.getElementById('submitBtn');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = `
                    <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                    Analyzing Credit Profile...
                `;
            }
        }
    });

    // Remove is-invalid class dynamically on input/change
    form.querySelectorAll('input, select').forEach(element => {
        element.addEventListener('input', function () {
            if (this.value.trim()) {
                this.classList.remove('is-invalid');
            }
        });
        element.addEventListener('change', function () {
            if (this.value.trim()) {
                this.classList.remove('is-invalid');
            }
        });
    });
});
