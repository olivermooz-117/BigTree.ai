import { useEffect, useState, useRef } from "react";
import { useParams } from "react-router-dom";
import * as aiApi from "../../api/ai";
import Loading from "../../components/Loading";

export default function AI() {
  const { id } = useParams();
  const [personas, setPersonas] = useState([]);
  const [personaId, setPersonaId] = useState(null);
  const [conversationId, setConversationId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    aiApi.listPersonas().then(({ data }) => {
      setPersonas(data);
      const def = data.find((p) => p.is_default) || data[0];
      if (def) setPersonaId(def.id);
    });
  }, []);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || sending) return;
    setSending(true);
    const text = input.trim();
    setInput("");
    setMessages((m) => [...m, { role: "user", content: text }]);
    try {
      const { data } = await aiApi.chat(id, {
        message: text,
        persona_id: personaId,
        conversation_id: conversationId,
      });
      setConversationId(data.conversation.id);
      setMessages((m) => [...m, { role: "assistant", content: data.reply.content }]);
    } catch {
      setMessages((m) => [...m, { role: "assistant", content: "Sorry, something went wrong." }]);
    } finally {
      setSending(false);
    }
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", height: "calc(100vh - 180px)" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "1rem" }}>
        <h2 className="page-title" style={{ margin: 0 }}>AI co-pilot</h2>
        <select
          value={personaId || ""}
          onChange={(e) => setPersonaId(Number(e.target.value))}
          style={{ width: "auto", minWidth: 160 }}
        >
          {personas.map((p) => (
            <option key={p.id} value={p.id}>{p.name}</option>
          ))}
        </select>
      </div>

      <div className="card" style={{ flex: 1, overflowY: "auto", marginBottom: "1rem" }}>
        {messages.length === 0 && (
          <p className="muted">Ask the AI to draft, brainstorm, or summarize using this project’s notes and files.</p>
        )}
        {messages.map((m, i) => (
          <div
            key={i}
            style={{
              marginBottom: "0.85rem",
              padding: "0.65rem 0.85rem",
              borderRadius: 8,
              background: m.role === "user" ? "var(--surface-2)" : "transparent",
              borderLeft: m.role === "assistant" ? "3px solid var(--accent)" : "none",
            }}
          >
            <div className="muted" style={{ fontSize: "0.75rem", marginBottom: "0.25rem" }}>
              {m.role === "user" ? "You" : "AI"}
            </div>
            <div style={{ whiteSpace: "pre-wrap" }}>{m.content}</div>
          </div>
        ))}
        {sending && <Loading text="Thinking…" />}
        <div ref={bottomRef} />
      </div>

      <form onSubmit={handleSend} style={{ display: "flex", gap: "0.5rem" }}>
        <input
          placeholder="Ask anything about this project…"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          disabled={sending}
        />
        <button type="submit" disabled={sending || !input.trim()}>Send</button>
      </form>
    </div>
  );
}
