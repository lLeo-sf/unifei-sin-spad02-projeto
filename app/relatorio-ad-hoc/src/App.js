import React, { useState, useEffect } from "react";
import FieldItem from "./components/FieldItem";
import DropArea from "./components/DropArea";
import FilterSection from "./components/FilterSection";
import "./index.css";
import { getMetadata } from "./services/metadataService";
import { search } from "./services/searchService";

export default function App() {
  const [metadata, setMetadata]         = useState({});
  const [selectedTable, setSelectedTable] = useState("");
  const [fields, setFields]             = useState([]);
  const [filters, setFilters]           = useState([]);
  const [columns, setColumns]           = useState([]);
  const [grouping, setGrouping]         = useState([]);
  const [data, setData]                 = useState([
    { "Animals.name": "Mel" },
    { "Animals.name": "Luna" },
  ]);

  const measuresFields = ["COUNT", "SUM", "AVG", "MAX", "MIN"];

  const pascalize = (s) => s.charAt(0).toUpperCase() + s.slice(1);

  const handleSearch = async () => {
    if (!selectedTable) return;

    // 1) só pega filtros com valores
    const payloadFilters = Object.fromEntries(
      Object.entries(filters).filter(
        ([, vals]) => Array.isArray(vals) && vals.length > 0
      )
    );

    // 2) detecta se há uma função de agregação em columns
    const fn = columns.find((c) => measuresFields.includes(c));

    if (fn) {
      // deve haver exatamente 1 coluna real
      const realCols = columns.filter((c) => !measuresFields.includes(c));
      if (realCols.length !== 1) {
        alert("Para usar agregação: 1 função e 1 coluna apenas.");
        return;
      }
      // monta só aggregations
      const body = {
        table:        selectedTable,
        filters:      payloadFilters,
        grouping,     // mantém agrupamentos se houver
        aggregations: [{ function: fn.toLowerCase(), field: realCols[0] }],
      };
      try {
        const result = await search(body);
        setData(result);
      } catch (err) {
        console.error("Erro ao buscar dados:", err);
      }
    } else {
      // fluxo normal sem agregação
      const body = {
        table:    selectedTable,
        columns,
        grouping,
        filters:  payloadFilters,
      };
      try {
        const result = await search(body);
        setData(result);
      } catch (err) {
        console.error("Erro ao buscar dados:", err);
      }
    }
  };

  useEffect(() => {
    (async () => {
      try {
        const data = await getMetadata();

        // transforma as keys de relations para PascalCase
        const normalized = {};
        Object.entries(data).forEach(([table, { base, relations }]) => {
          const normRels = {};
          Object.entries(relations || {}).forEach(([relTable, fields]) => {
            normRels[pascalize(relTable)] = fields;
          });
          normalized[table] = { base, relations: normRels };
        });

        setMetadata(normalized);
      } catch (err) {
        console.error("Falha ao buscar metadata:", err);
      }
    })();
  }, []);

  useEffect(() => {
    if (selectedTable && metadata[selectedTable]) {
      const baseFields = metadata[selectedTable].base.map(
        (field) => `${selectedTable}.${field}`
      );
      const relatedFields = Object.entries(
        metadata[selectedTable].relations
      ).flatMap(([relTable, cols]) =>
        cols.map((col) => `${relTable}.${col}`)
      );

      setFields([...baseFields, ...relatedFields]);
      setFilters([...baseFields, ...relatedFields]);
    } else {
      setFields([]);
      setFilters([]);
    }
  }, [selectedTable, metadata]);

  // --- NOVO: lógica para exibir só 1 coluna na tabela quando em modo agregação
  const aggFn      = columns.find((c) => measuresFields.includes(c));
  const realCols   = columns.filter((c) => !measuresFields.includes(c));
  let displayCols  = columns;
  let aggFieldKey  = "";

  if (aggFn && realCols.length === 1) {
    // exibe apenas o header "FN(tablename.field)"
    displayCols = [`${aggFn.toUpperCase()}(${realCols[0]})`];
    // chave usada no row retornado pelo backend é "fn_fieldName"
    const fieldName = realCols[0].split(".")[1];
    aggFieldKey = `${aggFn.toLowerCase()}_${fieldName}`;
  }
  // ---------------------------------------------------------------

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
            <span>Agregações</span>
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
              onClick={handleSearch}
            >
              🔍 Pesquisar
            </button>
          </div>

          <table className="result-table">
            <thead>
              <tr>
                {displayCols.map((column) => (
                  <th key={column} className="column-header">
                    {column}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {data.map((row, rowIndex) => (
                <tr key={rowIndex}>
                  {displayCols.map((col, idx) => (
                    <td key={idx}>
                      {aggFn
                        ? row[aggFieldKey]
                        : row[col]}
                    </td>
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
          <FilterSection
            filters={filters}
            setFilters={setFilters}
            metadata={metadata}
            selectedTable={selectedTable}
          />
        </div>
      </div>
    </div>
  );
}
