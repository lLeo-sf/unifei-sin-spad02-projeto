
export default function FieldItem({ fieldId }) {
    const handleDragStart = (event) => {
        event.dataTransfer.setData('text', fieldId);
    };

    return (
        <li className="field-item" draggable onDragStart={handleDragStart}>
            <span className="field-icon">📊</span> {fieldId}
        </li>
    );
}
