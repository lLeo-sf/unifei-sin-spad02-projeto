
export default function FilterSection({ filters }) {
    return (
        <div className="filter-section">
            {filters.map(filterName => (
                <div className="filter-item" key={filterName}>
                    <h4>{filterName}</h4>
                    <div className="filter-values">
                        <div className="filter-value">
                            <label className="checkbox-label">
                                <input type="text" />
                            </label>
                        </div>
                    </div>
                </div>
            ))}
        </div>
    );
}
