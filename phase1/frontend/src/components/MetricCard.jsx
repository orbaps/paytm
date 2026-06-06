export default function MetricCard({ label, value, tone = "blue", icon: Icon }) {
  const toneClass = {
    blue: "bg-sky-50 text-sky-700 border-sky-100",
    green: "bg-emerald-50 text-emerald-700 border-emerald-100",
    amber: "bg-amber-50 text-amber-700 border-amber-100",
    rose: "bg-rose-50 text-rose-700 border-rose-100",
    slate: "bg-slate-50 text-slate-700 border-slate-100"
  }[tone];

  return (
    <section className="rounded-md border border-slate-200 bg-white p-4 shadow-sm">
      <div className="flex items-center justify-between gap-3">
        <div>
          <p className="text-xs font-medium uppercase tracking-normal text-slate-500">{label}</p>
          <p className="mt-2 text-3xl font-semibold text-slate-950">{value}</p>
        </div>
        {Icon ? (
          <div className={`flex h-10 w-10 items-center justify-center rounded-md border ${toneClass}`}>
            <Icon size={20} aria-hidden="true" />
          </div>
        ) : null}
      </div>
    </section>
  );
}
