import React from "react";

export default function DropArea({ title, fields = [], setFields }) {
  const handleDrop = event => {
    event.preventDefault();
    const fieldId = event.dataTransfer.getData("text");
    if (fields.includes(fieldId)) return;
    setFields([...fields, fieldId]);
  };

  const handleDragOver = event => {
    event.preventDefault();
    event.currentTarget.classList.add("drag-over");
  };

  const handleDragLeave = event => {
    event.currentTarget.classList.remove("drag-over");
  };

  const handleRemove = fieldIdToRemove => {
    setFields(fields.filter(f => f !== fieldIdToRemove));
  };

  return (
    <div className="report-section">
      <div className="section-title">{title}</div>
      <div
        className="report-section-columns"
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
      >
        {fields.map(fieldId => (
          <div
            key={fieldId}
            className="field-pill"
            onClick={() => handleRemove(fieldId)}
          >
            {fieldId}
          </div>
        ))}
      </div>
    </div>
  );
}
