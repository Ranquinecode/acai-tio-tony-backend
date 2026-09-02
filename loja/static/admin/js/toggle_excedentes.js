document.addEventListener('DOMContentLoaded', function () {
    const permitirCheckbox = document.querySelector('#id_permitir_exceder');
    const precoField = document.querySelector('.field-preco_item_excedente');
    const limiteField = document.querySelector('.field-limite_excedente');

    function toggleFields() {
        if (!permitirCheckbox) return;
        const isChecked = permitirCheckbox.checked;
        if (precoField) precoField.style.display = isChecked ? '' : 'none';
        if (limiteField) limiteField.style.display = isChecked ? '' : 'none';
    }

    if (permitirCheckbox) {
        toggleFields();
        permitirCheckbox.addEventListener('change', toggleFields);
    }
});
