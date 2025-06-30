import React from 'react';

const OPERATORS = [
  { value: '=',     label: '='    },
  { value: '!=',    label: '≠'    },
  { value: '>',     label: '>'    },
  { value: '>=',    label: '≥'    },
  { value: '<',     label: '<'    },
  { value: '<=',    label: '≤'    },
  { value: 'in',    label: 'in'   },
  { value: 'not_in',label: 'not in' },
  { value: 'like',  label: 'like' }
];

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

  const handleOperatorChange = (field, op) => {
    const next = filters.filter(f => f.field !== field);
    const existing = filters.find(f => f.field === field);
    if (existing && existing.value !== undefined && existing.value !== '') {
      next.push({ ...existing, operator: op });
    } else {
      next.push({ field, operator: op, value: '' });
    }
    setFilters(next);
  };

  const handleValueChange = (field, value) => {
    const next = filters.filter(f => f.field !== field);
    if (value !== '') {
      const existing = filters.find(f => f.field === field);
      const operator = existing ? existing.operator : '=';
      next.push({ field, operator, value });
    }
    setFilters(next);
  };

  const getFilter = (field) => filters.find(f => f.field === field) || {};

  return (
    <div className="filter-section">
      {allFields.map(field => {
        const { operator = '=', value = '' } = getFilter(field);
        return (
          <div key={field} className="filter-item">
            <label>{field}</label>
            <select
              value={operator}
              onChange={e => handleOperatorChange(field, e.target.value)}
            >
              {OPERATORS.map(op => (
                <option key={op.value} value={op.value}>
                  {op.label}
                </option>
              ))}
            </select>
            <input
              type="text"
              value={value}
              placeholder="valor"
              onChange={e => handleValueChange(field, e.target.value)}
            />
          </div>
        );
      })}
    </div>
  );
}
