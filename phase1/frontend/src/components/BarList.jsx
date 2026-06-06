export default function BarList({ title, rows, labelKey, valueKey, valueSuffix = "" }) {
  const maxValue = Math.max(1, ...rows.map((row) => Number(row[valueKey]) || 0));

  return (
    <section className="rounded-md border border-slate-200 bg-white p-4 shadow-sm">
      <div className="mb-4 flex items-center justify-between">
        <h2 className="text-sm font-semibold text-slate-900">{title}</h2>
      </div>
      <div className="space-y-3">
        {rows.length ? (
          rows.map((row) => {
            const value = Number(row[valueKey]) || 0;
            const width = `${Math.max(6, (value / maxValue) * 100)}%`;
            return (
              <div key={`${title}-${row[labelKey]}`} className="grid grid-cols-[minmax(96px,160px)_1fr_56px] items-center gap-3">
                <span className="truncate text-sm text-slate-600" title={row[labelKey]}>
                  {row[labelKey]}
                </span>
                <div className="h-2 rounded-sm bg-slate-100">
                  <div className="h-2 rounded-sm bg-sky-500" style={{ width }} />
                </div>
                <span className="text-right text-sm font-medium text-slate-900">
                  {value}
                  {valueSuffix}
                </span>
              </div>
            );
          })
        ) : (
          <p className="text-sm text-slate-500">No records</p>
        )}
      </div>
    </section>
  );
}
