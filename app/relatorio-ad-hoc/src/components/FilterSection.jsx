import React from 'react';

export default function FilterSection({
  filters,
  setFilters,
  metadata,
  selectedTable
}) {
  if (!selectedTable || !metadata[selectedTable]) return null;

  const base = metadata[selectedTable].base;
  const relations = metadata[selectedTable].relations;
  const relationFields = Object.entries(relations || {})
    .flatMap(([relTable, fields]) =>
      fields.map(f => `${relTable}.${f}`)
    );
  const allFields = [
    ...base.map(f => `${selectedTable}.${f}`),
    ...relationFields
  ];

  const handleChange = (field, text) => {
    const values = text.split(' ').map(s => s.trim()).filter(Boolean);

    const next = { ...filters };
    if (values.length) next[field] = values;
    else delete next[field];

    setFilters(next);
  };

  return (
    <div className="filter-section">
      {allFields.map(field => (
        <div key={field} className="filter-item">
          <label>{field}</label>
          <input
            type="text"
            value={(filters[field] || []).join(' ')}
            placeholder="val1 val2 …"
            onChange={e => handleChange(field, e.target.value)}
          />
        </div>
      ))}
    </div>
  );
}
