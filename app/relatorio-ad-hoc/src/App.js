import React, { useState, useEffect } from "react";
import FieldItem from "./components/FieldItem";
import DropArea from "./components/DropArea";
import FilterSection from "./components/FilterSection";
import "./index.css";
import { getMetadata } from "./services/metadataService";
import { search } from "./services/searchService";
import { exportCsv } from "./services/exportService";

import {
  BarChart,
  Bar,
  LineChart,
  Line,
  PieChart,
  Pie,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
} from "recharts";

export default function App() {
  // Estados principais
  const [chartType, setChartType] = useState("bar");
  const [chartData, setChartData] = useState({
    data: [],
    xKey: "",
    yKeys: [],
    yNames: [],
  });
  const [metadata, setMetadata] = useState({});
  const [selectedTable, setSelectedTable] = useState("");
  const [fields, setFields] = useState([]);
  const [filters, setFilters] = useState([]);
  const [columns, setColumns] = useState([]);
  const [grouping, setGrouping] = useState([]);
  const [orderBy, setOrderBy] = useState([]); // → campos para ordenar
  const [orderDirections, setOrderDirections] = useState({}); // → direções por campo
  const [data, setData] = useState([]);

  const measuresFields = ["COUNT", "SUM", "AVG", "MAX", "MIN"];
  const pascalize = (s) => s.charAt(0).toUpperCase() + s.slice(1);

  // Função de busca (pesquisa)
  const handleSearch = async () => {
    setChartData((cd) => ({ ...cd, data: [] }));
    if (!selectedTable) return;

    // 1) Só filtros com valor preenchido
    const payloadFilters = filters.filter(
      (f) => f.value !== undefined && f.value !== ""
    );

    // 2) Detecta funções + colunas (COUNT, SUM...)
    const aggregations = [];
    const usedCols = new Set();
    for (let i = 0; i < columns.length; i++) {
      const token = columns[i];
      if (measuresFields.includes(token)) {
        const next = columns[i + 1];
        if (!next || measuresFields.includes(next)) {
          alert(`A função "${token}" precisa estar seguida de UMA coluna.`);
          return;
        }
        aggregations.push({
          function: token.toLowerCase(),
          field: next,
        });
        usedCols.add(token);
        usedCols.add(next);
        i++;
      }
    }

    // 3) Colunas simples restantes
    const remainingCols = columns.filter((c) => !usedCols.has(c));

    // 4) Monta body base
    const body = {
      table: selectedTable,
      ...(payloadFilters.length && { filters: payloadFilters }),
      ...(aggregations.length && { aggregations }),
      ...(grouping.length && { grouping }),
      ...(!aggregations.length && { columns }),
      ...(aggregations.length &&
        remainingCols.length && { columns: remainingCols }),
    };

    // 5) Adiciona ordenação se houver, usando direção escolhida
    if (orderBy.length) {
      body.order_by = orderBy.map((col) => ({
        column: col,
        direction: orderDirections[col] || "asc",
      }));
    }

    // 6) Executa a chamada
    try {
      const result = await search(body);
      setData(result);
    } catch (err) {
      console.error("Erro ao buscar dados:", err);
      alert("Erro na busca, verifique o console.");
    }
  };

  // Função de exportar CSV
  const handleExport = async () => {
    if (!selectedTable) {
      alert("Selecione antes uma tabela");
      return;
    }

    // monta filtros preenchidos
    const payloadFilters = filters.filter(
      (f) => f.value !== undefined && f.value !== ""
    );

    // reaproveita lógica de agregações
    const aggregations = [];
    const usedCols = new Set();
    for (let i = 0; i < columns.length; i++) {
      const fn = columns[i];
      if (measuresFields.includes(fn)) {
        const col = columns[i + 1];
        aggregations.push({ function: fn.toLowerCase(), field: col });
        usedCols.add(fn);
        usedCols.add(col);
        i++;
      }
    }
    const remainingCols = columns.filter((c) => !usedCols.has(c));

    // monta body igual ao /search
    const body = {
      table: selectedTable,
      ...(payloadFilters.length && { filters: payloadFilters }),
      ...(aggregations.length && { aggregations }),
      ...(!aggregations.length && { columns }),
      ...(aggregations.length &&
        remainingCols.length && { columns: remainingCols }),
    };
    if (orderBy.length) {
      body.order_by = orderBy.map((col) => ({
        column: col,
        direction: orderDirections[col] || "asc",
      }));
    }

    try {
      const blob = await exportCsv(body);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "export.csv";
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error("Erro ao exportar CSV:", err);
      alert("Falha na exportação, veja o console.");
    }
  };

  // Função de plotagem (gráfico)
  const handlePlot = async () => {
    if (!selectedTable) return;

    // 1) Prepara filtros
    const payloadFilters = filters.filter(
      (f) => f.value !== undefined && f.value !== ""
    );

    // 2) Exige exatamente 1 agrupamento para gráfico
    if (grouping.length !== 1) {
      alert("Para plotar, arraste exatamente 1 coluna em 'Agrupamentos'.");
      return;
    }
    const dimension = grouping[0];

    // 3) Detecta funções + colunas
    const aggregations = [];
    const usedCols = new Set();
    for (let i = 0; i < columns.length; i++) {
      const fn = columns[i];
      if (measuresFields.includes(fn)) {
        const col = columns[i + 1];
        if (!col || measuresFields.includes(col)) {
          alert(`A função "${fn}" precisa vir seguida de UMA coluna.`);
          return;
        }
        aggregations.push({ function: fn.toLowerCase(), field: col });
        usedCols.add(fn);
        usedCols.add(col);
        i++;
      }
    }
    if (!aggregations.length) {
      alert("Arraste ao menos uma função e a respectiva coluna.");
      return;
    }

    // 4) Colunas simples restantes
    const remainingCols = columns.filter((c) => !usedCols.has(c));

    // 5) Monta payload similar ao handleSearch
    const body = {
      table: selectedTable,
      ...(payloadFilters.length && { filters: payloadFilters }),
      grouping,
      aggregations,
      ...(remainingCols.length && { columns: remainingCols }),
    };

    // 6) Chama a API e remapeia resultados
    try {
      const raw = await search(body);
      const chartRows = raw
        .map((row) => {
          const mapped = { [dimension]: row[dimension] };
          aggregations.forEach(({ function: fn, field }) => {
            mapped[`${fn}.${field}`] = row[`${fn}.${field}`];
          });
          return mapped;
        })
        .filter((r) => r[dimension] != null);

      const xKey = dimension;
      const yKeys = aggregations.map((a) => `${a.function}.${a.field}`);
      const yNames = aggregations.map(
        (a) => `${a.function.toUpperCase()}(${a.field.split(".")[1]})`
      );

      setChartData({ data: chartRows, xKey, yKeys, yNames });
    } catch (err) {
      console.error("Erro ao plotar:", err);
      alert("Falha ao plotar, veja o console.");
    }
  };

  // Carrega metadata ao montar
  useEffect(() => {
    (async () => {
      try {
        const data = await getMetadata();
        const normalized = {};
        Object.entries(data).forEach(([table, { base, relations }]) => {
          const normRels = {};
          Object.entries(relations || {}).forEach(([relTable, cols]) => {
            normRels[pascalize(relTable)] = cols;
          });
          normalized[table] = { base, relations: normRels };
        });
        setMetadata(normalized);
      } catch (err) {
        console.error("Falha ao buscar metadata:", err);
      }
    })();
  }, []);

  // Quando seleciona tabela, ajusta fields e filtros
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

  // Prepara displayCols e cellKeys para a tabela de resultados
  let displayCols = [];
  let cellKeys = [];
  grouping.forEach((grp) => {
    displayCols.push(grp);
    cellKeys.push(grp);
  });
  for (let i = 0; i < columns.length; i++) {
    const token = columns[i];
    if (measuresFields.includes(token)) {
      const fn = token;
      const col = columns[i + 1];
      if (!col || measuresFields.includes(col)) continue;
      displayCols.push(`${fn}(${col})`);
      cellKeys.push(`${fn.toLowerCase()}.${col}`);
      i++;
    }
  }
  if (cellKeys.length === 0) {
    displayCols = [...columns];
    cellKeys = [...columns];
  }

  return (
    <div>
      <div className="header">
        <h1>RESCUEGROUPS.ORG Ad Hoc Reporting</h1>
      </div>

      <div className="main-container">
        {/* Painel esquerdo */}
        <div className="left-panel">
          <div className="panel-title">Tabelas</div>
          <select
            id="tableSelector"
            className="select"
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

        {/* Painel central */}
        <div className="center-panel">
          <div className="report-sections">
            <DropArea title="Colunas" fields={columns} setFields={setColumns} />
            <DropArea
              title="Agrupamentos"
              fields={grouping}
              setFields={setGrouping}
            />
            <DropArea
              title="Ordenações"
              fields={orderBy}
              setFields={setOrderBy}
            />
          </div>

          {/* Seleção de direção para cada campo de ordenação */}
          {orderBy.length > 0 && (
            <div className="order-directions">
              {orderBy.map((col) => (
                <div key={col} className="order-item">
                  <span>{col}</span>
                  <select
                    value={orderDirections[col] || "asc"}
                    onChange={(e) =>
                      setOrderDirections((prev) => ({
                        ...prev,
                        [col]: e.target.value,
                      }))
                    }
                  >
                    <option value="asc">Ascendente</option>
                    <option value="desc">Descendente</option>
                  </select>
                </div>
              ))}
            </div>
          )}

          <div className="report-title">Relatório Ad Hoc</div>
          <div className="actions">
            <select
              className="select"
              value={chartType}
              onChange={(e) => setChartType(e.target.value)}
            >
              <option value="bar">Barras</option>
              <option value="line">Linha</option>
              <option value="pie">Pizza</option>
            </select>

            <button className="btn" onClick={handlePlot}>
              📈 Plotar
            </button>
            <label> | </label>
            <button className="btn" onClick={handleSearch}>
              🔍 Pesquisar
            </button>
            <label> | </label>
            <button className="btn" onClick={handleExport}>
              💾 Exportar CSV
            </button>
          </div>

          <div className="status-bar">{data.length} registros encontrados</div>

          {/* Tabela ou gráfico */}
          {chartData.data.length === 0 ? (
            <table className="result-table">
              <thead>
                <tr>
                  {displayCols.map((col, idx) => (
                    <th key={idx} className="column-header">
                      {col}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {data.map((row, rowIndex) => (
                  <tr key={rowIndex}>
                    {cellKeys.map((key, idx) => (
                      <td key={idx}>{row[key]}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <div style={{ marginTop: 24 }}>
              {chartType === "pie" ? (
                <PieChart width={400} height={300}>
                  <Pie
                    data={chartData.data}
                    dataKey={chartData.yKeys[0]}
                    nameKey={chartData.xKey}
                    cx="50%"
                    cy="50%"
                    outerRadius={100}
                    label={({ payload, percent }) =>
                      `${payload[chartData.xKey]}: ${(percent * 100).toFixed(
                        0
                      )}%`
                    }
                  />
                  <Tooltip
                    formatter={(value) => [value, chartData.yNames[0]]}
                  />
                </PieChart>
              ) : chartType === "bar" ? (
                <BarChart
                  width={600}
                  height={300}
                  data={chartData.data}
                  margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
                >
                  <XAxis dataKey={chartData.xKey} />
                  <YAxis />
                  <Tooltip formatter={(value, name) => [value, name]} />
                  <Bar
                    dataKey={chartData.yKeys[0]}
                    name={chartData.yNames[0]}
                    barSize={30}
                  />
                </BarChart>
              ) : (
                <LineChart
                  width={600}
                  height={300}
                  data={chartData.data}
                  margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
                >
                  <XAxis dataKey={chartData.xKey} />
                  <YAxis />
                  <Tooltip formatter={(value, name) => [value, name]} />
                  <Line
                    type="monotone"
                    dataKey={chartData.yKeys[0]}
                    name={chartData.yNames[0]}
                    strokeWidth={2}
                  />
                </LineChart>
              )}
            </div>
          )}
        </div>

        {/* Painel direito: filtros */}
        <div className="right-panel">
          <div className="section-header">
            <span>Filtros</span>
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
