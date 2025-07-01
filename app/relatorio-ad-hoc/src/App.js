import React, { useState, useEffect } from "react";
import FieldItem from "./components/FieldItem";
import DropArea from "./components/DropArea";
import FilterSection from "./components/FilterSection";
import "./index.css";
import { getMetadata } from "./services/metadataService";
import { search } from "./services/searchService";

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

  const [data, setData] = useState([]);

  const measuresFields = ["COUNT", "SUM", "AVG", "MAX", "MIN"];

  const pascalize = (s) => s.charAt(0).toUpperCase() + s.slice(1);

  const handleSearch = async () => {
    setChartData((cd) => ({ ...cd, data: [] }));
    if (!selectedTable) return;

    // só pega filtros com valor preenchido
    const payloadFilters = filters.filter(
      (f) => f.value !== undefined && f.value !== ""
    );

    // detecta várias funções e emparelha cada uma com a coluna à direita
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
        i++; // pula a coluna que acabou de usar
      }
    }

    // mantém todas as colunas simples que NÃO foram usadas em agregação
    const remainingCols = columns.filter((c) => !usedCols.has(c));

    // monta payload
    const body = {
      table: selectedTable,
      filters: payloadFilters,
    };

    if (aggregations.length > 0) {
      body.aggregations = aggregations;
      if (grouping.length) body.grouping = grouping;
      // inclui qualquer coluna simples restante
      if (remainingCols.length) body.columns = remainingCols;
    } else {
      // sem agregações, envia tudo como colunas
      body.columns = columns;
      if (grouping.length) body.grouping = grouping;
    }

    try {
      const result = await search(body);
      setData(result);
    } catch (err) {
      console.error("Erro ao buscar dados:", err);
      alert("Erro na busca, verifique o console.");
    }
  };

  const handlePlot = async () => {
    if (!selectedTable) return;

    // 1) prepara filtros exatamente como no handleSearch
    //    (assume que `filters` é um array de { field, operator, value })
    const payloadFilters = filters.filter(
      (f) => f.value !== undefined && f.value !== ""
    );

    // 2) exige uma dimensão para plot
    if (grouping.length !== 1) {
      alert("Para plotar, arraste exatamente 1 coluna em 'Agrupamentos'.");
      return;
    }
    const dimension = grouping[0];

    // 3) emparelha funções com a coluna à direita
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

    // 4) mantém todas as colunas simples não usadas em agregação
    const remainingCols = columns.filter((c) => !usedCols.has(c));

    // 5) monta o payload exatamente como handleSearch faria
    const body = {
      table: selectedTable,
      ...(payloadFilters.length && { filters: payloadFilters }),
      grouping, // mantém todos os agrupamentos
      aggregations,
      ...(remainingCols.length && { columns: remainingCols }),
    };

    try {
      const raw = await search(body);

      // 6) remapeia e filtra nulos da dimensão
      const data = raw
        .map((row) => {
          return {
            [dimension]: row[dimension],
            ...aggregations.reduce((acc, { function: fn, field }) => {
              const alias = `${fn}.${field}`;
              acc[alias] = row[alias];
              return acc;
            }, {}),
          };
        })
        .filter((r) => r[dimension] != null);

      // 7) prepara chartData com múltiplas séries
      const xKey = dimension;
      const yKeys = aggregations.map((a) => `${a.function}.${a.field}`);
      const yNames = aggregations.map(
        (a) => `${a.function.toUpperCase()}(${a.field.split(".")[1]})`
      );

      setChartData({ data, xKey, yKeys, yNames });
    } catch (err) {
      console.error("Erro ao plotar:", err);
      alert("Falha ao plotar, veja o console.");
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
      ).flatMap(([relTable, cols]) => cols.map((col) => `${relTable}.${col}`));

      setFields([...baseFields, ...relatedFields]);
      setFilters([...baseFields, ...relatedFields]);
    } else {
      setFields([]);
      setFilters([]);
    }
  }, [selectedTable, metadata]);

  // --- NOVO: lógica para exibir só 1 coluna na tabela quando em modo agregação
  // --- Montagem de displayCols e cellKeys para renderizar a tabela ---
  let displayCols = [];
  let cellKeys = [];

  // 1) adiciona as colunas de agrupamento (se houver)
  grouping.forEach((grp) => {
    displayCols.push(grp);
    cellKeys.push(grp); // usa o alias igual ao col, ex: "Animals.agegroup"
  });

  // 2) emparelha cada função com a coluna seguinte
  for (let i = 0; i < columns.length; i++) {
    const token = columns[i];
    if (measuresFields.includes(token)) {
      const fn = token; // ex: "COUNT"
      const col = columns[i + 1]; // ex: "Animals.id"
      if (!col || measuresFields.includes(col)) {
        continue;
      }
      // header: "COUNT(Animals.id)"
      displayCols.push(`${fn}(${col})`);
      // chave do valor = alias que o back usa: "count.Animals.id"
      cellKeys.push(`${fn.toLowerCase()}.${col}`);
      i++; // pula a coluna que acabou de usar
    }
  }

  // 3) fallback quando não há agregações
  if (cellKeys.length === 0) {
    displayCols = [...columns];
    cellKeys = [...columns];
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

          <div className="actions">
            {/* se tiver select de tipo de gráfico */}
            <select
              className="select"
              value={chartType}
              onChange={(e) => setChartType(e.target.value)}
            >
              <option value="bar">Barras</option>
              <option value="line">Linha</option>
              <option value="pie">Pizza</option>
            </select>

            {/* botão Plotar */}
            <button className="btn" onClick={handlePlot}>
              📈 Plotar
            </button>
            <label> | </label>
            <button className="btn" onClick={handleSearch}>
              🔍 Pesquisar
            </button>
          </div>
          <div className="status-bar">{data.length} registros encontrados</div>

          {chartData.data.length <= 0 && (
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
          )}

          {chartData.data.length > 0 && (
            <div style={{ marginTop: 24 }}>
              {chartType === "pie" ? (
                <PieChart width={400} height={300}>
                  <Pie
                    data={chartData.data}
                    dataKey={chartData.yKeys[0]} // valor
                    nameKey={chartData.xKey} // categoria
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
