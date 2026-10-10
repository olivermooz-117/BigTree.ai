import { Link, useNavigate } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { logout } from "../store/authSlice";

export default function Navbar() {
  const user = useSelector((s) => s.auth.user);
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const handleLogout = () => {
    dispatch(logout());
    navigate("/login");
  };

  return (
    <header
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        padding: "0.85rem 1.5rem",
        borderBottom: "1px solid var(--border)",
        background: "var(--surface)",
      }}
    >
      <Link to="/dashboard" style={{ fontWeight: 700, fontSize: "1.15rem", color: "var(--text)" }}>
        🌳 BigTree.ai
      </Link>
      <nav style={{ display: "flex", gap: "1rem", alignItems: "center" }}>
        <Link to="/dashboard">Projects</Link>
        <Link to="/settings">Settings</Link>
        <span className="muted">{user?.name}</span>
        <button className="secondary" onClick={handleLogout}>
          Log out
        </button>
      </nav>
    </header>
  );
}
