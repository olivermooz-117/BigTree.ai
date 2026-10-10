import { NavLink, useParams } from "react-router-dom";

const tabs = [
  { path: "", label: "Overview" },
  { path: "notes", label: "Notes" },
  { path: "files", label: "Files" },
  { path: "ai", label: "AI" },
  { path: "chat", label: "Chat" },
  { path: "tasks", label: "Tasks" },
];

export default function ProjectTabs() {
  const { id } = useParams();
  const base = `/projects/${id}`;

  return (
    <nav
      style={{
        display: "flex",
        gap: "0.25rem",
        borderBottom: "1px solid var(--border)",
        marginBottom: "1.25rem",
        overflowX: "auto",
      }}
    >
      {tabs.map((t) => (
        <NavLink
          key={t.path}
          to={t.path ? `${base}/${t.path}` : base}
          end={t.path === ""}
          style={({ isActive }) => ({
            padding: "0.65rem 1rem",
            color: isActive ? "var(--accent)" : "var(--muted)",
            borderBottom: isActive ? "2px solid var(--accent)" : "2px solid transparent",
            fontWeight: isActive ? 600 : 400,
            whiteSpace: "nowrap",
          })}
        >
          {t.label}
        </NavLink>
      ))}
    </nav>
  );
}
