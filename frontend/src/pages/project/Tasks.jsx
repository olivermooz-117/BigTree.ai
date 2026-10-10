import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import * as tasksApi from "../../api/tasks";
import Loading from "../../components/Loading";

const COLUMNS = [
  { key: "todo", label: "To do" },
  { key: "doing", label: "Doing" },
  { key: "done", label: "Done" },
];

export default function Tasks() {
  const { id } = useParams();
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [title, setTitle] = useState("");

  const load = () => {
    setLoading(true);
    tasksApi.listTasks(id).then(({ data }) => setTasks(data)).finally(() => setLoading(false));
  };

  useEffect(load, [id]);

  const handleCreate = async (e) => {
    e.preventDefault();
    if (!title.trim()) return;
    await tasksApi.createTask(id, { title: title.trim() });
    setTitle("");
    load();
  };

  const move = async (task, status) => {
    await tasksApi.updateTask(task.id, { status });
    load();
  };

  if (loading) return <Loading />;

  return (
    <div>
      <h2 className="page-title">Tasks</h2>
      <form onSubmit={handleCreate} style={{ display: "flex", gap: "0.5rem", marginBottom: "1.25rem" }}>
        <input placeholder="New task…" value={title} onChange={(e) => setTitle(e.target.value)} />
        <button type="submit">Add</button>
      </form>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: "1rem" }}>
        {COLUMNS.map((col) => (
          <div key={col.key} className="card">
            <div style={{ fontWeight: 600, marginBottom: "0.75rem" }}>{col.label}</div>
            {tasks
              .filter((t) => t.status === col.key)
              .map((t) => (
                <div
                  key={t.id}
                  style={{
                    padding: "0.6rem",
                    marginBottom: "0.5rem",
                    background: "var(--surface-2)",
                    borderRadius: 8,
                  }}
                >
                  <div>{t.title}</div>
                  <div style={{ display: "flex", gap: "0.35rem", marginTop: "0.4rem" }}>
                    {COLUMNS.filter((c) => c.key !== t.status).map((c) => (
                      <button
                        key={c.key}
                        className="secondary"
                        style={{ fontSize: "0.75rem", padding: "0.2rem 0.5rem" }}
                        onClick={() => move(t, c.key)}
                      >
                        → {c.label}
                      </button>
                    ))}
                  </div>
                </div>
              ))}
          </div>
        ))}
      </div>
    </div>
  );
}
