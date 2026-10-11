import { Link } from "react-router-dom";

export default function Landing() {
  return (
    <div className="container" style={{ textAlign: "center", paddingTop: "4rem" }}>
      <h1 style={{ fontSize: "2.8rem", marginBottom: "0.75rem" }}>🌳 BigTree.ai</h1>
      <p className="muted" style={{ fontSize: "1.15rem", maxWidth: 520, margin: "0 auto 2rem" }}>
        Creative collaboration workspace. Organize work into projects, chat in real time,
        and use an AI co-pilot that knows your project’s content.
      </p>
      <div style={{ display: "flex", gap: "1rem", justifyContent: "center" }}>
        <Link to="/register">
          <button>Get started</button>
        </Link>
        <Link to="/login">
          <button className="secondary">Log in</button>
        </Link>
      </div>
    </div>
  );
}
