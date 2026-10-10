import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { login, clearError } from "../store/authSlice";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { status, error } = useSelector((s) => s.auth);

  const handleSubmit = async (e) => {
    e.preventDefault();
    dispatch(clearError());
    const result = await dispatch(login({ email, password }));
    if (login.fulfilled.match(result)) navigate("/dashboard");
  };

  return (
    <div className="container" style={{ maxWidth: 420, paddingTop: "3rem" }}>
      <h1 className="page-title">Log in</h1>
      <form onSubmit={handleSubmit} className="card" style={{ display: "grid", gap: "1rem" }}>
        <div>
          <label className="muted">Email</label>
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        </div>
        <div>
          <label className="muted">Password</label>
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        </div>
        {error && <p className="error">{error}</p>}
        <button type="submit" disabled={status === "loading"}>
          {status === "loading" ? "Signing in…" : "Sign in"}
        </button>
      </form>
      <p className="muted" style={{ marginTop: "1rem" }}>
        No account? <Link to="/register">Register</Link>
      </p>
    </div>
  );
}
