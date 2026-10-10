import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { fetchProjects, createProject } from "../store/projectSlice";
import Loading from "../components/Loading";

export default function Dashboard() {
  const dispatch = useDispatch();
  const { items, status } = useSelector((s) => s.projects);
  const [title, setTitle] = useState("");
  const [creating, setCreating] = useState(false);

  useEffect(() => {
    dispatch(fetchProjects());
  }, [dispatch]);

  const handleCreate = async (e) => {
    e.preventDefault();
    if (!title.trim()) return;
    setCreating(true);
    await dispatch(createProject({ title: title.trim() }));
    setTitle("");
    setCreating(false);
  };

  return (
    <div className="container">
      <h1 className="page-title">Your projects</h1>

      <form onSubmit={handleCreate} className="card" style={{ display: "flex", gap: "0.75rem", marginBottom: "1.5rem" }}>
        <input
          placeholder="New project title…"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
        <button type="submit" disabled={creating || !title.trim()}>
          {creating ? "Creating…" : "Create"}
        </button>
      </form>

      {status === "loading" && <Loading />}
      {status === "succeeded" && items.length === 0 && (
        <p className="muted">No projects yet. Create one above.</p>
      )}

      <div style={{ display: "grid", gap: "0.75rem" }}>
        {items.map((p) => (
          <Link key={p.id} to={`/projects/${p.id}`} className="card" style={{ display: "block", color: "inherit" }}>
            <div style={{ fontWeight: 600 }}>{p.title}</div>
            <div className="muted" style={{ marginTop: "0.25rem" }}>
              {p.member_count} member{p.member_count !== 1 ? "s" : ""} · {p.role}
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
