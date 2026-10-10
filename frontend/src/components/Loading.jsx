export default function Loading({ text = "Loading…" }) {
  return (
    <div style={{ padding: "2rem", textAlign: "center", color: "var(--muted)" }}>
      {text}
    </div>
  );
}
