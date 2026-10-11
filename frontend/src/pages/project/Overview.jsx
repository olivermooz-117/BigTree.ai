import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { useSelector } from "react-redux";
import { getProject, addMember } from "../../api/projects";

export default function Overview() {
  const { id } = useParams();
  const stored = useSelector((s) => s.projects.current);
  const [project, setProject] = useState(stored);
  const [email, setEmail] = useState("");
  const [busy, setBusy] = useState(false);
  const [msg, setMsg] = useState(null);
  const [err, setErr] = useState(null);

  const reload = () => {
    getProject(id)
      .then(({ data }) => setProject(data))
      .catch(() => {});
  };

  useEffect(() => {
    reload();
  }, [id]);

  const handleInvite = async (e) => {
    e.preventDefault();
    if (!email.trim()) return;
    setBusy(true);
    setMsg(null);
    setErr(null);
    try {
      await addMember(id, { email: email.trim(), role: "member" });
      setEmail("");
      setMsg("Member added");
      reload();
    } catch (ex) {
      setErr(ex.response?.data?.error || "Could not add member");
    } finally {
      setBusy(false);
    }
  };

  if (!project) return null;

  const members = project.members || [];

  return (
    <div>
      <h1 className="page-title">{project.title}</h1>
      <p className="muted" style={{ marginBottom: "1.25rem" }}>
        {project.description || "No description yet."}
      </p>

      <div className="card" style={{ marginBottom: "1.25rem" }}>
        <div style={{ fontWeight: 600, marginBottom: "0.75rem" }}>
          Members ({members.length || project.member_count || 0})
        </div>
        {members.length > 0 ? (
          <ul style={{ listStyle: "none", marginBottom: "1rem" }}>
            {members.map((m) => (
              <li key={m.user?.id || m.user_id} style={{ padding: "0.35rem 0" }}>
                {m.user?.name || m.user?.email}{" "}
                <span className="muted">({m.role})</span>
              </li>
            ))}
          </ul>
        ) : (
          <p className="muted" style={{ marginBottom: "1rem" }}>
            Member list not loaded — invite someone below to collaborate.
          </p>
        )}

        <form onSubmit={handleInvite} style={{ display: "flex", gap: "0.5rem", flexWrap: "wrap" }}>
          <input
            type="email"
            placeholder="teammate@email.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            style={{ flex: 1, minWidth: 200 }}
          />
          <button type="submit" disabled={busy || !email.trim()}>
            {busy ? "Adding…" : "Invite member"}
          </button>
        </form>
        {msg && <p className="muted" style={{ marginTop: "0.5rem", color: "var(--accent)" }}>{msg}</p>}
        {err && <p className="error">{err}</p>}
      </div>
    </div>
  );
}
