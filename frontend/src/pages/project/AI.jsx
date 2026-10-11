import { useEffect, useState, useRef } from "react";
import { useParams } from "react-router-dom";
import * as aiApi from "../../api/ai";
import Loading from "../../components/Loading";

export default function AI() {
  const { id } = useParams();
  const [personas, setPersonas] = useState([]);
  const [personaId, setPersonaId] = useState(null);
  const [conversations, setConversations] = useState([]);
  const [conversationId, setConversationId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);
  const [error, setError] = useState(null);
  const bottomRef = useRef(null);

  useEffect(() => {
    aiApi.listPersonas().then(({ data }) => {
      setPersonas(data);
      const def = data.find((p) => p.is_default) || data[0];
      if (def) setPersonaId(def.id);
    });
    aiApi.listConversations(id).then(({ data }) => setConversations(data)).catch(() => {});
  }, [id]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const loadConversation = async (cid) => {
    setError(null);
    setConversationId(cid);
    if (!cid) {
      setMessages([]);
      return;
    }
    try {
      const { data } = await aiApi.getMessages(id, cid);
      setMessages(data.map((m) => ({ role: m.role, content: m.content, id: m.id })));
    } catch (e) {
      setError(e.response?.data?.error || "Could not load conversation");
    }
  };

  const newChat = () => {
    setConversationId(null);
    setMessages([]);
    setError(null);
  };

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || sending) return;
    setSending(true);
    setError(null);
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
      const { data: convos } = await aiApi.listConversations(id);
      setConversations(convos);
    } catch (err) {
      const msg = err.response?.data?.error || err.message || "Something went wrong";
      setError(msg);
      setMessages((m) => [...m, { role: "assistant", content: `Error: ${msg}` }]);
    } finally {
      setSending(false);
    }
  };

  return (
    <div style={{ display: "flex", gap: "1rem", height: "calc(100vh - 180px)" }}>
      <div className="card" style={{ width: 200, overflowY: "auto", flexShrink: 0 }}>
        <button type="button" onClick={newChat} style={{ width: "100%", marginBottom: "0.75rem" }}>
          + New chat
        </button>
        {conversations.map((c) => (
          <button
            key={c.id}
            type="button"
            className="secondary"
            onClick={() => loadConversation(c.id)}
            style={{
              width: "100%",
              marginBottom: "0.35rem",
              textAlign: "left",
              fontWeight: c.id === conversationId ? 700 : 400,
              border: c.id === conversationId ? "1px solid var(--accent)" : undefined,
            }}
          >
            {c.title || `Chat #${c.id}`}
          </button>
        ))}
      </div>
      <div style={{ flex: 1, display: "flex", flexDirection: "column", minWidth: 0 }}>
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
            <p className="muted">Ask the AI to draft, brainstorm, or summarize using this project’s content.</p>
          )}
          {messages.map((m, i) => (
            <div
              key={m.id || i}
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
        {error && <p className="error" style={{ marginBottom: "0.5rem" }}>{error}</p>}
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
    </div>
  );
}
