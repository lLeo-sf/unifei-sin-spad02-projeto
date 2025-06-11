const tableFields = {
    Animals: [
        'id',
        'name',
        'sex',
        'ageGroup',
        'breedString',
        'speciesId',
        'statusId',
        'adoptionFeeString'
    ],
    Colors: [
        'id',
        'name',
        'hexCode'
    ],
    Organizations: [
        'id',
        'name',
        'city',
        'state',
        'phone',
        'email'
    ]
};

const tableFilters = {
    Animals: [
        'Species',
        'Status',
        'Faixa Etária'
    ],
    Colors: [
        'Cor Primária',
        'Cor Secundária'
    ],
    Organizations: [
        'Estado',
        'Cidade'
    ]
};

function onTableChange() {
    const selectedTable = document.getElementById('tableSelector').value;
    
    // Atualiza lista de fields (painel esquerdo)
    const fieldList = document.getElementById('dynamic-fields');
    fieldList.innerHTML = '';
    
    tableFields[selectedTable].forEach(field => {
        const li = document.createElement('li');
        li.className = 'field-item';
        li.draggable = true;
        li.ondragstart = (event) => drag(event, `${selectedTable}.${field}`);
        
        li.innerHTML = `<span class="field-icon">📊</span> ${selectedTable}.${field}`;
        fieldList.appendChild(li);
    });
    
    // Atualiza filtros (painel direito)
    const filterSection = document.getElementById('dynamic-filters');
    filterSection.innerHTML = '';
    
    tableFilters[selectedTable].forEach(filterName => {
        const div = document.createElement('div');
        div.className = 'filter-item';
        div.innerHTML = `
            <h4>${filterName}</h4>
            <div class="filter-values">
                <div class="filter-value">
                    <label class="checkbox-label">
                        <input type="checkbox" checked> Exemplo 1
                    </label>
                </div>
                <div class="filter-value">
                    <label class="checkbox-label">
                        <input type="checkbox"> Exemplo 2
                    </label>
                </div>
            </div>
        `;
        filterSection.appendChild(div);
    });
}
