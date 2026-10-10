import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { register, clearError } from "../store/authSlice";

export default function Register() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { status, error } = useSelector((s) => s.auth);

  const handleSubmit = async (e) => {
    e.preventDefault();
    dispatch(clearError());
    const result = await dispatch(register({ name, email, password }));
    if (register.fulfilled.match(result)) navigate("/dashboard");
  };

  return (
    <div className="container" style={{ maxWidth: 420, paddingTop: "3rem" }}>
      <h1 className="page-title">Create account</h1>
      <form onSubmit={handleSubmit} className="card" style={{ display: "grid", gap: "1rem" }}>
        <div>
          <label className="muted">Name</label>
          <input value={name} onChange={(e) => setName(e.target.value)} required />
        </div>
        <div>
          <label className="muted">Email</label>
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        </div>
        <div>
          <label className="muted">Password</label>
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required minLength={8} />
        </div>
        {error && <p className="error">{error}</p>}
        <button type="submit" disabled={status === "loading"}>
          {status === "loading" ? "Creating…" : "Create account"}
        </button>
      </form>
      <p className="muted" style={{ marginTop: "1rem" }}>
        Already have an account? <Link to="/login">Log in</Link>
      </p>
    </div>
  );
}
