document.addEventListener('DOMContentLoaded', function () {
    // 1. Formulário de Edição (Tela individual de GrupoOpcao)
    const permitirForm = document.querySelector('#id_permitir_exceder');
    const fieldPreco = document.querySelector('.field-preco_item_excedente');
    const fieldLimite = document.querySelector('.field-limite_excedente');

    function toggleFormFields() {
        if (!permitirForm) return;
        const checked = permitirForm.checked;
        if (fieldPreco) fieldPreco.style.display = checked ? '' : 'none';
        if (fieldLimite) fieldLimite.style.display = checked ? '' : 'none';
    }

    if (permitirForm) {
        toggleFormFields();
        permitirForm.addEventListener('change', toggleFormFields);
    }

    // 2. Tabela de Listagem do Admin (Desktop e Mobile com list_editable)
    const rows = document.querySelectorAll('#result_list tbody tr');
    rows.forEach(row => {
        const checkbox = row.querySelector('.field-permitir_exceder input[type="checkbox"]');
        const cellPreco = row.querySelector('.field-preco_item_excedente');
        const cellLimite = row.querySelector('.field-limite_excedente');

        function toggleRowCells() {
            if (!checkbox) return;
            const checked = checkbox.checked;
            if (cellPreco) cellPreco.style.visibility = checked ? 'visible' : 'hidden';
            if (cellLimite) cellLimite.style.visibility = checked ? 'visible' : 'hidden';
        }

        if (checkbox) {
            toggleRowCells();
            checkbox.addEventListener('change', toggleRowCells);
        }
    });
});
