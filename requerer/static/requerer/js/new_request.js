class NumericInput {
    constructor(inputElement) {
        this.inputElement = inputElement;
        this.minLength = this.inputElement.getAttribute('minlength');
        this.maxLength = this.inputElement.getAttribute('maxlength');
        this.initialize();
    }

    initialize() {
        this.inputElement.addEventListener('input', (e) => this.validateInput(e));
    }

    validateInput(e) {
        // Remove caracteres não numéricos
        this.inputElement.value = this.inputElement.value.replace(/[^0-9]/g, '');

        // Verifica se o valor excede o comprimento máximo permitido
        if (this.inputElement.value.length > this.maxLength) {
            this.inputElement.value = this.inputElement.value.substring(0, this.maxLength);
        }

        // Opcional: Aplicar estilo quando o valor está abaixo do comprimento mínimo
        if (this.inputElement.value.length < this.minLength) {
            this.inputElement.style.borderColor = 'red';  // Muda a borda para vermelho, por exemplo
        } else {
            this.inputElement.style.borderColor = '';  // Restaura a cor da borda
        }
    }
}

// Inicialize a classe para todos os elementos com a classe 'number'
document.addEventListener('DOMContentLoaded', () => {
    const inputElements = document.querySelectorAll('.number');
    inputElements.forEach(inputElement => new NumericInput(inputElement));
});
