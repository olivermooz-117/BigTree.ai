import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import * as filesApi from "../../api/files";
import Loading from "../../components/Loading";

export default function Files() {
  const { id } = useParams();
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);

  const load = () => {
    setLoading(true);
    filesApi
      .listFiles(id)
      .then(({ data }) => setFiles(data))
      .catch((e) => setError(e.response?.data?.error || "Failed to load files"))
      .finally(() => setLoading(false));
  };

  useEffect(load, [id]);

  const handleUpload = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setUploading(true);
    setError(null);
    const form = new FormData();
    form.append("file", file);
    try {
      await filesApi.uploadFile(id, form);
      load();
    } catch (err) {
      setError(err.response?.data?.error || "Upload failed");
    } finally {
      setUploading(false);
      e.target.value = "";
    }
  };

  const handleDownload = async (f) => {
    try {
      await filesApi.downloadFile(f.id, f.filename);
    } catch {
      setError("Download failed");
    }
  };

  const handleDelete = async (f) => {
    if (!confirm(`Delete ${f.filename}?`)) return;
    try {
      await filesApi.deleteFile(f.id);
      load();
    } catch (err) {
      setError(err.response?.data?.error || "Delete failed");
    }
  };

  return (
    <div>
      <h2 className="page-title">Files</h2>
      <div className="card" style={{ marginBottom: "1.25rem" }}>
        <input type="file" onChange={handleUpload} disabled={uploading} />
        {uploading && <p className="muted" style={{ marginTop: "0.5rem" }}>Uploading…</p>}
        {error && <p className="error">{error}</p>}
      </div>
      {loading ? (
        <Loading />
      ) : files.length === 0 ? (
        <p className="muted">No files yet.</p>
      ) : (
        <div style={{ display: "grid", gap: "0.5rem" }}>
          {files.map((f) => (
            <div
              key={f.id}
              className="card"
              style={{ display: "flex", justifyContent: "space-between", alignItems: "center", gap: "1rem" }}
            >
              <div>
                <div>{f.filename}</div>
                <span className="muted">{(f.size / 1024).toFixed(1)} KB</span>
              </div>
              <div style={{ display: "flex", gap: "0.5rem" }}>
                <button type="button" className="secondary" onClick={() => handleDownload(f)}>
                  Download
                </button>
                <button type="button" className="danger" onClick={() => handleDelete(f)}>
                  Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
