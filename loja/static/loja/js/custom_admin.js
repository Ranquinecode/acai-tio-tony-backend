document.addEventListener('DOMContentLoaded', function () {

    // ==========================================
    // 1. REORDENAÇÃO & LÓGICA DO COMBO (PRODUTO)
    // ==========================================
    const comboCheckbox = document.querySelector('#id_eh_combo');
    const comboGroup = document.querySelector('.item-combo-inline-group');

    if (comboCheckbox && comboGroup) {
        // Localiza a seção 'Preços e Tipo de Produto' (fieldset ou div de formulário)
        const fieldsets = document.querySelectorAll('fieldset, .form-group');
        let precosSection = null;

        fieldsets.forEach(fieldset => {
            if (fieldset.innerText && fieldset.innerText.includes('Preços e Tipo de Produto')) {
                precosSection = fieldset;
            }
        });

        // Se encontrar a seção de preços, move a tabela de combos para ficar LOGO ABAIXO dela
        if (precosSection) {
            precosSection.parentNode.insertBefore(comboGroup, precosSection.nextSibling);
        }

        // Função para mostrar/ocultar a tabela de itens do combo
        function toggleComboFields() {
            if (comboCheckbox.checked) {
                comboGroup.style.display = '';
            } else {
                comboGroup.style.display = 'none';
            }
        }

        // Aplica no carregamento inicial da página
        toggleComboFields();

        // Escuta mudanças na caixinha "É combo"
        comboCheckbox.addEventListener('change', toggleComboFields);
    }

    // ==========================================
    // 2. LÓGICA DE GRUPO DE OPÇÃO (EXCEDENTES)
    // ==========================================

    // Formulário de Edição (Tela individual de GrupoOpcao)
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

    // Tabela de Listagem do Admin (Desktop e Mobile com list_editable)
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
