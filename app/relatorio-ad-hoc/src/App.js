
import { useState, useEffect } from 'react';
import FieldItem from './components/FieldItem';
import DropArea from './components/DropArea';
import FilterSection from './components/FilterSection';
import './index.css';

const tableFields = {
    Animals: {
        base: [
            'id',
            'name',
            'sex',
            'ageGroup',
            'breedString',
            'speciesId',
            'statusId',
            'adoptionFeeString'
        ],
        relations: {
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
        }
    },
    Organizations: {
        base: [
            'id',
            'name',
            'city',
            'state',
            'phone',
            'email'
        ],
        relations: {}
    }
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

export default function App() {
    const [selectedTable, setSelectedTable] = useState('Animals');
    const [fields, setFields] = useState([]);
    const [filters, setFilters] = useState([]);
    const [columns, setColumns] = useState([]);

    useEffect(() => {
        const baseFields = tableFields[selectedTable].base.map(field => `${selectedTable}.${field}`);

        const relatedFields = Object.entries(tableFields[selectedTable].relations).flatMap(([relatedTable, fields]) =>
            fields.map(field => `${relatedTable}.${field}`)
        );

        setFields([...baseFields, ...relatedFields]);
        setFilters(tableFilters[selectedTable]);
    }, [selectedTable]);

    return (
        <div>
            <div className="header">
                <h1>RESCUEGROUPS.ORG Ad Hoc Reporting</h1>
            </div>
            <div className="main-container">
                <div className="left-panel">
                    <div className="panel-title">Tabelas</div>
                    <select
                        id="tableSelector"
                        value={selectedTable}
                        onChange={e => setSelectedTable(e.target.value)}
                    >
                        <option value="Animals">Animais</option>
                        <option value="Colors">Cores</option>
                        <option value="Organizations">Organizações</option>
                    </select>

                    <div class="section-header" onclick="toggleSection('fields-section')">
                        <span>Colunas</span>
                        <span>≡</span>
                    </div>

                    <ul id="dynamic-fields" className="field-list">
                        {fields.map(field => (
                            <FieldItem key={field} fieldId={field} />
                        ))}
                    </ul>
                </div>

                <div className="center-panel">
                    <div className="report-sections">
                        <DropArea title="Colunas" fields={columns} setFields={setColumns} />
                        <DropArea title="Agrupamentos" />
                    </div>

                    <div className="report-title">Relatório Ad Hoc</div>

                    <table className="result-table">
                        <thead>
                            <tr>
                                {columns.map(column => (
                                    <th key={column} className="column-header">{column}</th>
                                ))}
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                {columns.map(column => (
                                    <td key={column}>Exemplo</td>
                                ))}
                            </tr>
                        </tbody>
                    </table>

                    <div className="status-bar">
                        5 registros encontrados | Última atualização: 06/05/2025 14:30
                    </div>
                </div>

                <div className="right-panel">
                    <div className="section-header">
                        <span>Filters</span>
                        <span>≡</span>
                    </div>
                    <FilterSection filters={filters} />
                </div>
            </div>
        </div>
    );
}
