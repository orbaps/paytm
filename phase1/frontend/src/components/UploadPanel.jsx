import { Upload } from "lucide-react";
import { useState } from "react";
import { apiUpload } from "../api/client.js";

const DATASETS = [
  ["banks", "Banks"],
  ["outages", "Outages"],
  ["maintenance_notices", "Maintenance"],
  ["npci_statistics", "NPCI statistics"]
];

export default function UploadPanel({ onImported }) {
  const [dataset, setDataset] = useState("banks");
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("");
  const [busy, setBusy] = useState(false);

  async function submit(event) {
    event.preventDefault();
    if (!file) return;

    setBusy(true);
    setStatus("");
    try {
      const result = await apiUpload(dataset, file);
      setStatus(`Imported ${result.imported}; failed ${result.failed}`);
      onImported?.();
    } catch (error) {
      setStatus(error.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <section className="rounded-md border border-slate-200 bg-white p-4 shadow-sm">
      <div className="mb-4 flex items-center justify-between">
        <h2 className="text-sm font-semibold text-slate-900">Data Import</h2>
      </div>
      <form className="grid gap-3 sm:grid-cols-[160px_1fr_auto]" onSubmit={submit}>
        <select
          className="h-10 rounded-md border border-slate-300 bg-white px-3 text-sm text-slate-900"
          value={dataset}
          onChange={(event) => setDataset(event.target.value)}
        >
          {DATASETS.map(([value, label]) => (
            <option key={value} value={value}>
              {label}
            </option>
          ))}
        </select>
        <input
          className="h-10 rounded-md border border-slate-300 bg-white px-3 py-2 text-sm text-slate-900"
          type="file"
          accept=".csv,.json,.xlsx,.xls"
          onChange={(event) => setFile(event.target.files?.[0] || null)}
        />
        <button
          className="inline-flex h-10 items-center justify-center gap-2 rounded-md bg-paytm-navy px-4 text-sm font-medium text-white hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-50"
          type="submit"
          disabled={!file || busy}
        >
          <Upload size={16} aria-hidden="true" />
          Upload
        </button>
      </form>
      {status ? <p className="mt-3 text-sm text-slate-600">{status}</p> : null}
    </section>
  );
}
