import React from "react";

const MEASURE_FIELDS = ["COUNT", "SUM", "AVG", "MAX", "MIN"];

export default function DropArea({ title, fields = [], setFields }) {
  const handleDrop = (event) => {
    event.preventDefault();
    const fieldId = event.dataTransfer.getData("text");

    // não duplica
    if (fields.includes(fieldId)) return;

    const hasFn = fields.some((c) => MEASURE_FIELDS.includes(c));
    const isFn  = MEASURE_FIELDS.includes(fieldId);

    // 1) se vier função e já tiver outra, bloqueia
    if (isFn && hasFn) {
      alert("Só pode aplicar uma função de agregação por vez.");
      return;
    }

    // 2) se já houver função e este for coluna, permite só uma
    if (hasFn && !isFn) {
      const realCols = fields.filter((c) => !MEASURE_FIELDS.includes(c));
      if (realCols.length >= 1) {
        alert("Para agregação, só arraste 1 coluna após a função.");
        return;
      }
    }

    // adiciona (seja função ou coluna)
    setFields([...fields, fieldId]);
  };

  const handleDragOver = (event) => {
    event.preventDefault();
    event.currentTarget.classList.add("drag-over");
  };

  const handleDragLeave = (event) => {
    event.currentTarget.classList.remove("drag-over");
  };

  const handleRemove = (fieldIdToRemove) => {
    setFields(fields.filter((f) => f !== fieldIdToRemove));
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
        {fields.map((fieldId) => (
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
