import { useSelector } from "react-redux";

export default function Overview() {
  const project = useSelector((s) => s.projects.current);
  if (!project) return null;

  return (
    <div>
      <h1 className="page-title">{project.title}</h1>
      <p className="muted" style={{ marginBottom: "1.25rem" }}>
        {project.description || "No description yet."}
      </p>
      <div className="card">
        <div className="muted">Members</div>
        <div style={{ marginTop: "0.5rem" }}>{project.member_count} people</div>
      </div>
    </div>
  );
}
