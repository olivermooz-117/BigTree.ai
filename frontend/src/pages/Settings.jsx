import { useSelector } from "react-redux";

export default function Settings() {
  const user = useSelector((s) => s.auth.user);

  return (
    <div className="container" style={{ maxWidth: 480 }}>
      <h1 className="page-title">Profile</h1>
      <div className="card" style={{ display: "grid", gap: "0.75rem" }}>
        <div>
          <span className="muted">Name</span>
          <div>{user?.name}</div>
        </div>
        <div>
          <span className="muted">Email</span>
          <div>{user?.email}</div>
        </div>
      </div>
    </div>
  );
}
