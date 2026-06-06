import { Activity, Banknote, CalendarClock, Database, RefreshCw, TrendingUp } from "lucide-react";
import { useCallback, useEffect, useState } from "react";
import { apiGet } from "./api/client.js";
import BarList from "./components/BarList.jsx";
import DataTable from "./components/DataTable.jsx";
import MetricCard from "./components/MetricCard.jsx";
import UploadPanel from "./components/UploadPanel.jsx";

const emptySummary = {
  bank_count: 0,
  outage_count: 0,
  planned_outage_count: 0,
  unplanned_outage_count: 0,
  maintenance_notice_count: 0,
  npci_statistic_count: 0
};

const emptyTrends = {
  outages_by_bank: [],
  outages_by_month: [],
  average_downtime_by_bank: [],
  planned_vs_unplanned: []
};

export default function App() {
  const [summary, setSummary] = useState(emptySummary);
  const [trends, setTrends] = useState(emptyTrends);
  const [maintenance, setMaintenance] = useState([]);
  const [statistics, setStatistics] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const loadDashboard = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const [summaryData, trendsData, maintenanceData, statisticsData] = await Promise.all([
        apiGet("/dashboard/summary"),
        apiGet("/dashboard/trends"),
        apiGet("/maintenance?limit=8"),
        apiGet("/statistics?limit=8")
      ]);
      setSummary(summaryData);
      setTrends(trendsData);
      setMaintenance(maintenanceData);
      setStatistics(statisticsData);
    } catch (loadError) {
      setError(loadError.message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadDashboard();
  }, [loadDashboard]);

  return (
    <main className="min-h-screen bg-slate-100">
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex max-w-7xl flex-col gap-4 px-4 py-5 sm:flex-row sm:items-center sm:justify-between lg:px-6">
          <div>
            <p className="text-xs font-semibold uppercase tracking-normal text-sky-600">Paytm Smart Reserve AI</p>
            <h1 className="mt-1 text-2xl font-semibold text-slate-950">Phase 1 Data Collection Platform</h1>
          </div>
          <button
            className="inline-flex h-10 items-center justify-center gap-2 rounded-md border border-slate-300 bg-white px-4 text-sm font-medium text-slate-800 hover:bg-slate-50 disabled:opacity-50"
            type="button"
            onClick={loadDashboard}
            disabled={loading}
          >
            <RefreshCw size={16} aria-hidden="true" />
            Refresh
          </button>
        </div>
      </header>

      <div className="mx-auto max-w-7xl space-y-5 px-4 py-5 lg:px-6">
        {error ? (
          <div className="rounded-md border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-700">{error}</div>
        ) : null}

        <section className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          <MetricCard label="Banks" value={summary.bank_count} icon={Banknote} tone="blue" />
          <MetricCard label="Outages" value={summary.outage_count} icon={Activity} tone="rose" />
          <MetricCard label="Planned Outages" value={summary.planned_outage_count} icon={CalendarClock} tone="amber" />
          <MetricCard label="Unplanned Outages" value={summary.unplanned_outage_count} icon={TrendingUp} tone="slate" />
          <MetricCard label="Maintenance Notices" value={summary.maintenance_notice_count} icon={CalendarClock} tone="green" />
          <MetricCard label="NPCI Statistics" value={summary.npci_statistic_count} icon={Database} tone="blue" />
        </section>

        <UploadPanel onImported={loadDashboard} />

        <section className="grid gap-4 lg:grid-cols-2">
          <BarList title="Outages By Bank" rows={trends.outages_by_bank} labelKey="name" valueKey="count" />
          <BarList title="Outages By Month" rows={trends.outages_by_month} labelKey="month" valueKey="count" />
          <BarList
            title="Average Downtime"
            rows={trends.average_downtime_by_bank}
            labelKey="bank_name"
            valueKey="average_duration_minutes"
            valueSuffix="m"
          />
          <BarList title="Planned vs Unplanned" rows={trends.planned_vs_unplanned} labelKey="label" valueKey="count" />
        </section>

        <section className="grid gap-4 xl:grid-cols-2">
          <DataTable
            title="Maintenance Notices"
            rows={maintenance}
            columns={[
              { key: "id", label: "ID" },
              { key: "bank_id", label: "Bank ID" },
              { key: "title", label: "Title" },
              { key: "maintenance_start", label: "Start", render: (row) => formatDate(row.maintenance_start) },
              { key: "maintenance_end", label: "End", render: (row) => formatDate(row.maintenance_end) }
            ]}
          />
          <DataTable
            title="NPCI Statistics"
            rows={statistics}
            columns={[
              { key: "id", label: "ID" },
              { key: "bank_id", label: "Bank ID" },
              { key: "month", label: "Month", render: (row) => `${row.year}-${String(row.month).padStart(2, "0")}` },
              { key: "success_rate", label: "Success %" },
              { key: "technical_decline", label: "TD %" },
              { key: "business_decline", label: "BD %" }
            ]}
          />
        </section>
      </div>
    </main>
  );
}

function formatDate(value) {
  if (!value) return "";
  return new Intl.DateTimeFormat("en-IN", {
    dateStyle: "medium",
    timeStyle: "short"
  }).format(new Date(value));
}
