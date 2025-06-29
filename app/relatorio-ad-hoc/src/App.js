import React, { useState, useEffect } from "react";
import FieldItem from "./components/FieldItem";
import DropArea from "./components/DropArea";
import FilterSection from "./components/FilterSection";
import "./index.css";
import { getMetadata } from "./services/metadataService";

export default function App() {
  const [metadata, setMetadata] = useState({});
  const [selectedTable, setSelectedTable] = useState("");
  const [fields, setFields] = useState([]);
  const [filters, setFilters] = useState([]);
  const [columns, setColumns] = useState([]);
  const [grouping, setGrouping] = useState([]);
  const [data, setData] = useState([
    { "Animals.name": "Mel" },
    { "Animals.name": "Luna" },
  ]);

  const measuresFields = ["COUNT", "SUM", "AVG", "MAX", "MIN"];

  // Busca os metadados ao montar o componente
  useEffect(() => {
    (async () => {
      try {
        const meta = await getMetadata();
        setMetadata(meta);
      } catch (err) {
        console.error("Falha ao buscar metadata:", err);
      }
    })();
  }, []);

  // Atualiza campos e filtros quando a tabela selecionada ou os metadados mudam
  useEffect(() => {
    if (selectedTable && metadata[selectedTable]) {
      const baseFields = metadata[selectedTable].base.map(
        (field) => `${selectedTable}.${field}`
      );
      const relatedFields = Object.entries(
        metadata[selectedTable].relations
      ).flatMap(([relTable, cols]) => cols.map((col) => `${relTable}.${col}`));

      setFields([...baseFields, ...relatedFields]);
      setFilters([...baseFields, ...relatedFields]);
    } else {
      setFields([]);
      setFilters([]);
    }
  }, [selectedTable, metadata]);

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
            onChange={(e) => setSelectedTable(e.target.value)}
          >
            <option value="">Selecione uma tabela</option>
            {Object.keys(metadata).map((entity) => (
              <option key={entity} value={entity}>
                {entity}
              </option>
            ))}
          </select>

          <div className="section-header">
            <span>Funções</span>
            <span>≡</span>
          </div>
          <ul className="field-list">
            {measuresFields.map((measure) => (
              <FieldItem key={measure} fieldId={measure} icon="📈" />
            ))}
          </ul>

          <div className="section-header">
            <span>Colunas</span>
            <span>≡</span>
          </div>
          <ul className="field-list">
            {fields.map((field) => (
              <FieldItem key={field} fieldId={field} />
            ))}
          </ul>
        </div>

        <div className="center-panel">
          <div className="report-sections">
            <DropArea title="Colunas" fields={columns} setFields={setColumns} />
            <DropArea
              title="Agrupamentos"
              fields={grouping}
              setFields={setGrouping}
            />
          </div>

          <div className="report-title">Relatório Ad Hoc</div>

          <div
            style={{
              display: "flex",
              justifyContent: "flex-end",
              alignItems: "center",
              marginBottom: "10px",
            }}
          >
            <button
              style={{
                padding: "6px 12px",
                backgroundColor: "#4b89dc",
                color: "white",
                border: "none",
                borderRadius: "4px",
                cursor: "pointer",
              }}
              onClick={() => alert("Pesquisar clicado")}
            >
              🔍 Pesquisar
            </button>
          </div>

          <table className="result-table">
            <thead>
              <tr>
                {columns.map((column) => (
                  <th key={column} className="column-header">
                    {column}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {data.map((row, rowIndex) => (
                <tr key={rowIndex}>
                  {columns.map((column) => (
                    <td key={column}>{row[column]}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>

          <div className="status-bar">{data.length} registros encontrados</div>
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
