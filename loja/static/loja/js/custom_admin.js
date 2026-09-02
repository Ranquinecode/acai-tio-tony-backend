document.addEventListener('DOMContentLoaded', function () {

    // ==========================================
    // 1. REORDENAÇÃO & LÓGICA DO COMBO (PRODUTO)
    // ==========================================
    const comboCheckbox = document.querySelector('#id_eh_combo');
    const comboGroup = document.querySelector('.item-combo-inline-group, #itens_combo-group');

    if (comboCheckbox && comboGroup) {
        // Localiza a seção 'Preços e Tipo de Produto'
        const fieldsets = document.querySelectorAll('fieldset, .form-group');
        let precosSection = null;

        fieldsets.forEach(fieldset => {
            if (fieldset.innerText && fieldset.innerText.includes('Preços e Tipo de Produto')) {
                precosSection = fieldset;
            }
        });

        if (precosSection) {
            precosSection.parentNode.insertBefore(comboGroup, precosSection.nextSibling);
        }

        function toggleComboFields() {
            if (comboCheckbox.checked) {
                comboGroup.style.display = '';
            } else {
                comboGroup.style.display = 'none';
            }
        }

        toggleComboFields();
        comboCheckbox.addEventListener('change', toggleComboFields);
    }

    // ==========================================
    // 2. EXIBIÇÃO CONDICIONAL DE PREÇO CAMADA EXTRA (PRODUTO)
    // ==========================================
    const fieldPrecoCamadaExtra = document.querySelector('.field-preco_camada_extra');
    if (fieldPrecoCamadaExtra) {
        // Verifica se há alguma indicação visual de cobrança de camada extra
        const checkCamadaExtra = () => {
            const ehCustomizavel = document.querySelector('#id_eh_customizavel');
            if (ehCustomizavel && !ehCustomizavel.checked) {
                fieldPrecoCamadaExtra.style.display = 'none';
            } else {
                fieldPrecoCamadaExtra.style.display = '';
            }
        };

        const ehCustomizavelCheck = document.querySelector('#id_eh_customizavel');
        if (ehCustomizavelCheck) {
            checkCamadaExtra();
            ehCustomizavelCheck.addEventListener('change', checkCamadaExtra);
        }
    }

    // ==========================================
    // 3. LÓGICA DE GRUPO DE OPÇÃO (EXCEDENTES)
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
    const rows = document.querySelectorAll('#result_list tbody tr, table tbody tr');
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
