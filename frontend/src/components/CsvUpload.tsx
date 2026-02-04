import { useState } from "react";
import { uploadTransactionsCSV } from "../api/transactions";

export default function CsvUpload({ onUploadSuccess }: { onUploadSuccess: () => void }) {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) return alert("Select a CSV file");

    setLoading(true);
    try {
      await uploadTransactionsCSV(file);
      alert("CSV uploaded successfully!");
      onUploadSuccess(); // 🔥 trigger dashboard refresh
    } catch (err) {
      alert("Upload failed");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white p-4 rounded shadow mt-6">
      <h2 className="font-semibold mb-2">Upload Transactions CSV</h2>
      <input type="file" accept=".csv" onChange={(e) => setFile(e.target.files?.[0] || null)} />
      <button
        onClick={handleUpload}
        disabled={loading}
        className="ml-2 bg-blue-600 text-white px-3 py-1 rounded"
      >
        {loading ? "Uploading..." : "Upload"}
      </button>
    </div>
  );
}
