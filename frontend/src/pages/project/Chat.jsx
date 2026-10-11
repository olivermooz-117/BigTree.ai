import { useEffect, useState, useRef, useCallback } from "react";
import { useParams } from "react-router-dom";
import { useSelector } from "react-redux";
import * as chatApi from "../../api/chat";
import useSocket from "../../hooks/useSocket";
import Loading from "../../components/Loading";

export default function Chat() {
  const { id } = useParams();
  const user = useSelector((s) => s.auth.user);
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [text, setText] = useState("");
  const historyReady = useRef(false);
  const pending = useRef([]);
  const bottomRef = useRef(null);

  const onMessage = useCallback((msg) => {
    if (!historyReady.current) {
      pending.current.push(msg);
      return;
    }
    setMessages((prev) => (prev.some((m) => m.id === msg.id) ? prev : [...prev, msg]));
  }, []);

  const { send } = useSocket(id, onMessage);

  useEffect(() => {
    historyReady.current = false;
    pending.current = [];
    setLoading(true);
    chatApi
      .listMessages(id)
      .then(({ data }) => {
        const merged = [...data];
        for (const m of pending.current) {
          if (!merged.some((x) => x.id === m.id)) merged.push(m);
        }
        merged.sort((a, b) => a.id - b.id);
        setMessages(merged);
        historyReady.current = true;
      })
      .finally(() => setLoading(false));
  }, [id]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = (e) => {
    e.preventDefault();
    if (!text.trim()) return;
    send(text.trim());
    setText("");
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", height: "calc(100vh - 180px)" }}>
      <h2 className="page-title">Team chat</h2>
      <div className="card" style={{ flex: 1, overflowY: "auto", marginBottom: "1rem" }}>
        {loading ? (
          <Loading />
        ) : messages.length === 0 ? (
          <p className="muted">No messages yet. Say hi to the team.</p>
        ) : (
          messages.map((m) => (
            <div
              key={m.id}
              style={{
                marginBottom: "0.75rem",
                textAlign: m.sender?.id === user?.id ? "right" : "left",
              }}
            >
              <div className="muted" style={{ fontSize: "0.75rem" }}>
                {m.sender?.name || "Someone"}
              </div>
              <div
                style={{
                  display: "inline-block",
                  padding: "0.5rem 0.85rem",
                  borderRadius: 8,
                  background: m.sender?.id === user?.id ? "var(--accent-dim)" : "var(--surface-2)",
                  maxWidth: "80%",
                }}
              >
                {m.body}
              </div>
            </div>
          ))
        )}
        <div ref={bottomRef} />
      </div>
      <form onSubmit={handleSend} style={{ display: "flex", gap: "0.5rem" }}>
        <input placeholder="Message the team…" value={text} onChange={(e) => setText(e.target.value)} />
        <button type="submit">Send</button>
      </form>
    </div>
  );
}
