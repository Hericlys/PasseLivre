document.addEventListener('DOMContentLoaded', (event) => {
    const numberInputs = document.querySelectorAll('input.number');
    
    numberInputs.forEach(input => {
        const span = input.nextElementSibling;

        input.addEventListener('input', (e) => {
            const value = input.value;
            if (/^\d*$/.test(value)) {
                input.classList.remove('invalid');
                input.classList.add('valid');
                span.classList.add('valid');
            } else {
                input.classList.add('invalid');
                input.classList.remove('valid');
                span.classList.remove('valid');
            }
        });

        input.addEventListener('keypress', (e) => {
            if (!/\d/.test(e.key)) {
                e.preventDefault();
            }
        });
    });
});