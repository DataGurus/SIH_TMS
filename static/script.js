class TouristRegistration {
    constructor() {
        this.formData = {
            name: '',
            email: '',
            phone: '',
            documentNumber: ''
        };
        this.selectedDocumentType = 'aadhaar';
        this.errors = {};
        this.isSubmitting = false;

        this.documentOptions = {
            aadhaar: {
                label: 'Aadhaar Card',
                placeholder: 'Enter 12-digit Aadhaar number',
                format: 'XXXX XXXX XXXX'
            },
            pan: {
                label: 'PAN Card',
                placeholder: 'Enter 10-character PAN number',
                format: 'ABCDE1234F'
            },
            passport: {
                label: 'Passport',
                placeholder: 'Enter Passport number',
                format: 'A1234567'
            }
        };

        this.initializeEventListeners();
    }

    initializeEventListeners() {
        // Form inputs
        document.getElementById('name').addEventListener('input', (e) => {
            this.formData.name = e.target.value;
            this.clearError('name');
        });

        document.getElementById('email').addEventListener('input', (e) => {
            this.formData.email = e.target.value;
            this.clearError('email');
        });

        document.getElementById('phone').addEventListener('input', (e) => {
            const formatted = this.formatPhoneNumber(e.target.value);
            e.target.value = formatted;
            this.formData.phone = formatted;
            this.clearError('phone');
        });

        document.getElementById('documentNumber').addEventListener('input', (e) => {
            const formatted = this.formatDocumentNumber(e.target.value);
            e.target.value = formatted;
            this.formData.documentNumber = formatted;
            this.clearError('documentNumber');
        });

        // Dropdown
        document.getElementById('documentDropdown').addEventListener('click', () => {
            this.showDocumentPicker();
        });

        // Modal
        document.getElementById('modalCloseButton').addEventListener('click', () => {
            this.hideDocumentPicker();
        });

        document.getElementById('documentModal').addEventListener('click', (e) => {
            if (e.target.id === 'documentModal') {
                this.hideDocumentPicker();
            }
        });

        // Document options
        document.querySelectorAll('.option-item').forEach(item => {
            item.addEventListener('click', () => {
                const type = item.getAttribute('data-type');
                this.selectDocumentType(type);
            });
        });

        // Form submission
        document.getElementById('registrationForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleSubmit();
        });

        // Success modal
        document.getElementById('successButton').addEventListener('click', () => {
            this.hideSuccessModal();
            this.resetForm();
        });
    }

    formatPhoneNumber(text) {
        const cleaned = text.replace(/\D/g, '');
        const limited = cleaned.slice(0, 10);

        if (limited.length >= 6) {
            return `${limited.slice(0, 5)} ${limited.slice(5)}`;
        }
        return limited;
    }

    formatDocumentNumber(text) {
        if (this.selectedDocumentType === 'aadhaar') {
            const cleaned = text.replace(/\D/g, '');
            const limited = cleaned.slice(0, 12);
            return limited.replace(/(\d{4})(?=\d)/g, '$1 ');
        } else if (this.selectedDocumentType === 'pan') {
            return text.toUpperCase().slice(0, 10);
        } else if (this.selectedDocumentType === 'passport') {
            return text.toUpperCase().slice(0, 8);
        }
    }

    validateForm() {
        const newErrors = {};

        // Name validation
        if (!this.formData.name.trim()) {
            newErrors.name = 'Name is required';
        } else if (this.formData.name.trim().length < 2) {
            newErrors.name = 'Name must be at least 2 characters';
        }

        // Email validation
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!this.formData.email.trim()) {
            newErrors.email = 'Email is required';
        } else if (!emailRegex.test(this.formData.email)) {
            newErrors.email = 'Please enter a valid email address';
        }

        // Phone validation
        const phoneRegex = /^[6-9]\d{9}$/;
        if (!this.formData.phone.trim()) {
            newErrors.phone = 'Phone number is required';
        } else if (!phoneRegex.test(this.formData.phone.replace(/\s+/g, ''))) {
            newErrors.phone = 'Please enter a valid 10-digit phone number';
        }

        // Document number validation
        if (!this.formData.documentNumber.trim()) {
            if (this.selectedDocumentType === 'aadhaar') {
                newErrors.documentNumber = 'Aadhaar number is required';
            } else if (this.selectedDocumentType === 'pan') {
                newErrors.documentNumber = 'PAN number is required';
            } else if (this.selectedDocumentType === 'passport') {
                newErrors.documentNumber = 'Passport number is required';
            }
        } else {
            if (this.selectedDocumentType === 'aadhaar') {
                const aadhaarRegex = /^\d{12}$/;
                if (!aadhaarRegex.test(this.formData.documentNumber.replace(/\s+/g, ''))) {
                    newErrors.documentNumber = 'Aadhaar number must be 12 digits';
                }
            } else if (this.selectedDocumentType === 'pan') {
                const panRegex = /^[A-Z]{5}[0-9]{4}[A-Z]{1}$/;
                if (!panRegex.test(this.formData.documentNumber.toUpperCase())) {
                    newErrors.documentNumber = 'PAN number format: ABCDE1234F';
                }
            } else if (this.selectedDocumentType === 'passport') {
                const passportRegex = /^[A-PR-WY][0-9]{7}$/; 
                if (!passportRegex.test(this.formData.documentNumber.toUpperCase())) {
                    newErrors.documentNumber = 'Passport format: A1234567';
                }
            }
        }

        this.errors = newErrors;
        this.displayErrors();
        return Object.keys(newErrors).length === 0;
    }

    displayErrors() {
        // Clear all error states
        document.querySelectorAll('.input-container').forEach(container => {
            container.classList.remove('error');
        });
        document.querySelectorAll('.error-text').forEach(error => {
            error.textContent = '';
        });

        // Display new errors
        Object.keys(this.errors).forEach(field => {
            const container = document.getElementById(`${field}Container`);
            const errorElement = document.getElementById(`${field}Error`);

            if (container) container.classList.add('error');
            if (errorElement) errorElement.textContent = this.errors[field];
        });
    }

    clearError(field) {
        if (this.errors[field]) {
            delete this.errors[field];
            const container = document.getElementById(`${field}Container`);
            const errorElement = document.getElementById(`${field}Error`);

            if (container) container.classList.remove('error');
            if (errorElement) errorElement.textContent = '';
        }
    }

    showDocumentPicker() {
        const modal = document.getElementById('documentModal');
        const dropdown = document.getElementById('documentDropdown');

        dropdown.classList.add('open');
        modal.classList.add('show');
    }

    hideDocumentPicker() {
        const modal = document.getElementById('documentModal');
        const dropdown = document.getElementById('documentDropdown');

        dropdown.classList.remove('open');
        modal.classList.remove('show');
    }

    selectDocumentType(type) {
        this.selectedDocumentType = type;
        this.formData.documentNumber = '';

        // Update UI
        const selectedText = document.getElementById('selectedDocumentText');
        const documentLabel = document.getElementById('documentLabel');
        const documentInput = document.getElementById('documentNumber');
        const formatHint = document.getElementById('formatHint');

        const option = this.documentOptions[type];
        selectedText.textContent = option.label;
        documentLabel.textContent = `${option.label} Number`;
        documentInput.placeholder = option.placeholder;
        documentInput.value = '';
        formatHint.textContent = `Format: ${option.format}`;

        // Update option selection
        document.querySelectorAll('.option-item').forEach(item => {
            const isSelected = item.getAttribute('data-type') === type;
            item.classList.toggle('selected', isSelected);
            const checkmark = item.querySelector('.checkmark');
            checkmark.style.opacity = isSelected ? '1' : '0';
        });

        this.hideDocumentPicker();
        this.clearError('documentNumber');
    }

    async handleSubmit() {
        if (this.isSubmitting) return;

        // Update form data from inputs
        this.formData.name = document.getElementById('name').value;
        this.formData.email = document.getElementById('email').value;
        this.formData.phone = document.getElementById('phone').value;
        this.formData.documentNumber = document.getElementById('documentNumber').value;

        if (!this.validateForm()) return;

        this.isSubmitting = true;
        this.updateSubmitButton(true);

        try {
            // Simulate API call
            await new Promise(resolve => setTimeout(resolve, 2000));

            this.showSuccessModal();
        } catch (error) {
            alert('Registration failed. Please try again.');
        } finally {
            this.isSubmitting = false;
            this.updateSubmitButton(false);
        }
    }

    updateSubmitButton(loading) {
        const button = document.getElementById('submitButton');
        const buttonText = document.getElementById('submitButtonText');

        if (loading) {
            button.disabled = true;
            buttonText.innerHTML = '<span class="loading-spinner"></span>Creating Account...';
        } else {
            button.disabled = false;
            buttonText.textContent = 'Create Account';
        }
    }

    showSuccessModal() {
        const modal = document.getElementById('successModal');
        modal.classList.add('show');
    }

    hideSuccessModal() {
        const modal = document.getElementById('successModal');
        modal.classList.remove('show');
    }

    resetForm() {
        this.formData = {
            name: '',
            email: '',
            phone: '',
            documentNumber: ''
        };
        this.selectedDocumentType = 'aadhaar';
        this.errors = {};

        // Reset form inputs
        document.getElementById('registrationForm').reset();
        document.getElementById('documentNumber').value = '';

        // Reset document type to Aadhaar
        this.selectDocumentType('aadhaar');

        // Clear all errors
        this.displayErrors();
    }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    new TouristRegistration();
});
