import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import * as filesApi from "../../api/files";
import Loading from "../../components/Loading";

export default function Files() {
  const { id } = useParams();
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);

  const load = () => {
    setLoading(true);
    filesApi.listFiles(id).then(({ data }) => setFiles(data)).finally(() => setLoading(false));
  };

  useEffect(load, [id]);

  const handleUpload = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setUploading(true);
    const form = new FormData();
    form.append("file", file);
    try {
      await filesApi.uploadFile(id, form);
      load();
    } finally {
      setUploading(false);
      e.target.value = "";
    }
  };

  return (
    <div>
      <h2 className="page-title">Files</h2>
      <div className="card" style={{ marginBottom: "1.25rem" }}>
        <input type="file" onChange={handleUpload} disabled={uploading} />
        {uploading && <p className="muted" style={{ marginTop: "0.5rem" }}>Uploading…</p>}
      </div>
      {loading ? <Loading /> : files.length === 0 ? (
        <p className="muted">No files yet.</p>
      ) : (
        <div style={{ display: "grid", gap: "0.5rem" }}>
          {files.map((f) => (
            <div key={f.id} className="card" style={{ display: "flex", justifyContent: "space-between" }}>
              <span>{f.filename}</span>
              <span className="muted">{(f.size / 1024).toFixed(1)} KB</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
