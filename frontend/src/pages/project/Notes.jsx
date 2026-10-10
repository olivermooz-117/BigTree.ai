import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import * as notesApi from "../../api/notes";
import Loading from "../../components/Loading";

export default function Notes() {
  const { id } = useParams();
  const [notes, setNotes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [title, setTitle] = useState("");
  const [body, setBody] = useState("");

  const load = () => {
    setLoading(true);
    notesApi.listNotes(id).then(({ data }) => setNotes(data)).finally(() => setLoading(false));
  };

  useEffect(load, [id]);

  const handleCreate = async (e) => {
    e.preventDefault();
    if (!title.trim()) return;
    await notesApi.createNote(id, { title: title.trim(), body });
    setTitle("");
    setBody("");
    load();
  };

  return (
    <div>
      <h2 className="page-title">Notes</h2>
      <form onSubmit={handleCreate} className="card" style={{ display: "grid", gap: "0.75rem", marginBottom: "1.25rem" }}>
        <input placeholder="Note title" value={title} onChange={(e) => setTitle(e.target.value)} />
        <textarea rows={4} placeholder="Body…" value={body} onChange={(e) => setBody(e.target.value)} />
        <button type="submit">Add note</button>
      </form>
      {loading ? <Loading /> : notes.length === 0 ? (
        <p className="muted">No notes yet.</p>
      ) : (
        <div style={{ display: "grid", gap: "0.75rem" }}>
          {notes.map((n) => (
            <div key={n.id} className="card">
              <div style={{ fontWeight: 600 }}>{n.title}</div>
              <p style={{ marginTop: "0.4rem", whiteSpace: "pre-wrap" }}>{n.body}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
