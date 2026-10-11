import { useEffect, useState } from "react";
import "./landing.css";

// ---- Edit these to match your app ----
const BRAND = "BigTree";
const LOGIN_URL = "/login";
const REGISTER_URL = "/register";

// status: "live" shows nothing, "soon" shows a "Coming soon" badge.
// Flip these as you ship features so the page never over-promises.
const FEATURES = [
  { icon: "📁", title: "Projects & roles", text: "Organize work into projects, invite teammates, and control access with owner and member roles.", status: "live" },
  { icon: "📝", title: "Notes & files", text: "Keep briefs, drafts, and assets together in one place, right next to the work.", status: "live" },
  { icon: "🤖", title: "AI co-pilot", text: "Draft, brainstorm, and summarize with an assistant built into every project, with saved history.", status: "live" },
  { icon: "🎭", title: "AI personas", text: "Switch the AI's tone with one click: an Editor, a Hype Coach, a Critic, and more.", status: "live" },
  { icon: "💬", title: "Real-time team chat", text: "Talk with your team inside the project, so conversations stay with the work.", status: "soon" },
  { icon: "🧠", title: "Project-aware answers", text: "The AI reads your project's notes and files, so replies use your real context.", status: "soon" },
  { icon: "✅", title: "Tasks & deadlines", text: "A simple board (To do, Doing, Done) to keep everyone moving.", status: "soon" },
  { icon: "🔒", title: "Private by default", text: "Only project members can see or change a project's content.", status: "live" },
];

const PERSONAS = [
  { id: "editor", name: "Editor", emoji: "✏️", blurb: "Clear, concise, no fluff.",
    reply: "Tighten it. “Create together” is fine, but it doesn't say what makes you different. Try: “Create together, with an AI that has read your whole project.” One promise, strong verbs." },
  { id: "hype", name: "Hype Coach", emoji: "🚀", blurb: "Energy and momentum.",
    reply: "Okay, this is a solid start! 🔥 Now make it LOUDER. Lead with the feeling: “Your best work, together, faster.” You're one punchy line away from something people repeat!" },
  { id: "critic", name: "Critic", emoji: "🧐", blurb: "Honest, constructive pushback.",
    reply: "It's safe, and safe is forgettable. Who is it for? What changes for them? Right now it could describe any tool. Name the audience and the outcome, then try again." },
];

const STEPS = [
  { n: "1", title: "Create a workspace", text: "Sign up in seconds and set up a home for your team." },
  { n: "2", title: "Start a project", text: "Invite teammates and add notes, files, and ideas." },
  { n: "3", title: "Ask your co-pilot", text: "Draft, brainstorm, or summarize, using your project as context." },
  { n: "4", title: "Ship together", text: "Chat, assign tasks, and keep momentum in one place." },
];

const FAQ = [
  { q: "Who is " + BRAND + " for?", a: "Creative teams, students, freelancers, and anyone who works in groups and wants AI help that understands the project." },
  { q: "What are AI personas?", a: "Presets that change how the AI responds, such as blunt and editorial, or upbeat and encouraging, so you get the tone you need." },
  { q: "Is my work private?", a: "Yes. Only members of a project can view or edit its content." },
  { q: "Is it free?", a: "You can create an account and try it for free." },
];

function useReveal() {
  useEffect(() => {
    const els = document.querySelectorAll(".bt-reveal");
    if (!("IntersectionObserver" in window)) {
      els.forEach((e) => e.classList.add("bt-in"));
      return;
    }
    const io = new IntersectionObserver(
      (entries) => entries.forEach((e) => {
        if (e.isIntersecting) { e.target.classList.add("bt-in"); io.unobserve(e.target); }
      }),
      { threshold: 0.12 }
    );
    els.forEach((e) => io.observe(e));
    return () => io.disconnect();
  }, []);
}

function Logo() {
  return (
    <a className="bt-logo" href="#top" aria-label={BRAND + " home"}>
      <svg width="28" height="28" viewBox="0 0 64 64" aria-hidden="true">
        <rect width="64" height="64" rx="14" fill="#0b1f17" />
        <circle cx="32" cy="26" r="16" fill="#34d399" />
        <circle cx="22" cy="32" r="10" fill="#10b981" />
        <circle cx="42" cy="32" r="10" fill="#10b981" />
        <rect x="29" y="38" width="6" height="16" rx="2" fill="#a7f3d0" />
      </svg>
      <span>{BRAND}<b>.ai</b></span>
    </a>
  );
}

function ProductMockup() {
  const tabs = ["Overview", "Notes", "Files", "AI", "Chat", "Tasks"];
  return (
    <div className="bt-mock" aria-hidden="true">
      <div className="bt-mock-bar"><i /><i /><i /><span>Spring Campaign</span></div>
      <div className="bt-mock-tabs">
        {tabs.map((t) => <span key={t} className={t === "AI" ? "on" : ""}>{t}</span>)}
      </div>
      <div className="bt-mock-body">
        <div className="bt-bubble me">Summarize our brand notes in 3 bullets.</div>
        <div className="bt-bubble ai">
          <small>🎭 Editor</small>
          Your voice is warm, direct, and playful. Keep sentences short. Lead with the benefit.
        </div>
        <div className="bt-bubble me">Now draft a launch tagline.</div>
        <div className="bt-bubble ai typing"><small>🎭 Editor</small><span /><span /><span /></div>
      </div>
    </div>
  );
}

export default function Landing() {
  const [open, setOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const [persona, setPersona] = useState(PERSONAS[0]);
  useReveal();

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 8);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  const close = () => setOpen(false);

  return (
    <div className="bt" id="top">
      <a className="bt-skip" href="#main">Skip to content</a>

      <header className={"bt-nav" + (scrolled ? " scrolled" : "")}>
        <div className="bt-wrap bt-nav-in">
          <Logo />
          <button className="bt-burger" aria-label="Toggle menu" aria-expanded={open} onClick={() => setOpen(!open)}>
            {open ? "✕" : "☰"}
          </button>
          <nav className={"bt-links" + (open ? " open" : "")}>
            <a href="#features" onClick={close}>Features</a>
            <a href="#personas" onClick={close}>AI personas</a>
            <a href="#how" onClick={close}>How it works</a>
            <a href="#faq" onClick={close}>FAQ</a>
            <a className="bt-link-login" href={LOGIN_URL}>Log in</a>
            <a className="bt-btn bt-btn-sm" href={REGISTER_URL}>Get started</a>
          </nav>
        </div>
      </header>

      <main id="main">
        <section className="bt-hero">
          <div className="bt-wrap bt-hero-grid">
            <div>
              <p className="bt-pill">✨ Collaboration, with an AI co-pilot</p>
              <h1>Where creative teams and <em>AI</em> build together.</h1>
              <p className="bt-lead">
                {BRAND} gives every project a shared workspace for notes, files, and team chat,
                plus an AI co-pilot that helps you draft, brainstorm, and summarize in the tone you choose.
              </p>
              <div className="bt-cta">
                <a className="bt-btn" href={REGISTER_URL}>Start free</a>
                <a className="bt-btn bt-btn-ghost" href={LOGIN_URL}>Try the demo</a>
              </div>
              <ul className="bt-trust">
                <li>🔒 Private projects</li><li>🎭 Switchable AI tone</li><li>⚡ Free to start</li>
              </ul>
            </div>
            <ProductMockup />
          </div>
        </section>

        <section id="features" className="bt-sec">
          <div className="bt-wrap">
            <h2>Everything your project needs, in one place</h2>
            <p className="bt-sub">Stop juggling docs, chat apps, and AI tabs.</p>
            <div className="bt-grid">
              {FEATURES.map((f) => (
                <article key={f.title} className="bt-card bt-reveal">
                  <span className="bt-ic">{f.icon}</span>
                  <h3>{f.title} {f.status === "soon" && <em className="bt-badge">Coming soon</em>}</h3>
                  <p>{f.text}</p>
                </article>
              ))}
            </div>
          </div>
        </section>

        <section id="personas" className="bt-sec bt-alt">
          <div className="bt-wrap bt-narrow">
            <h2>One AI. Your choice of voice.</h2>
            <p className="bt-sub">Pick a persona and the same question gets a different kind of help.</p>
            <div className="bt-tabs" role="tablist">
              {PERSONAS.map((p) => (
                <button key={p.id} role="tab" aria-selected={persona.id === p.id}
                  className={persona.id === p.id ? "on" : ""} onClick={() => setPersona(p)}>
                  {p.emoji} {p.name}
                </button>
              ))}
            </div>
            <div className="bt-demo" role="tabpanel">
              <p className="bt-demo-q"><b>You:</b> Give me feedback on my tagline: “Create together.”</p>
              <p className="bt-demo-a"><b>{persona.emoji} {persona.name}:</b> {persona.reply}</p>
              <small className="bt-note">{persona.blurb} Example response for illustration.</small>
            </div>
          </div>
        </section>

        <section id="how" className="bt-sec">
          <div className="bt-wrap">
            <h2>From idea to shipped in four steps</h2>
            <ol className="bt-steps">
              {STEPS.map((s) => (
                <li key={s.n} className="bt-reveal"><b>{s.n}</b><h3>{s.title}</h3><p>{s.text}</p></li>
              ))}
            </ol>
          </div>
        </section>

        <section className="bt-sec bt-alt">
          <div className="bt-wrap">
            <h2>Keep the whole team moving</h2>
            <p className="bt-sub">Tasks, chat, and AI help sit side by side.</p>
            <div className="bt-board" aria-hidden="true">
              {[
                { t: "To do", c: ["Write launch copy", "Collect brand assets"] },
                { t: "Doing", c: ["Design hero section"] },
                { t: "Done", c: ["Project kickoff", "Pick AI persona"] },
              ].map((col) => (
                <div key={col.t} className="bt-col bt-reveal">
                  <h4>{col.t}</h4>
                  {col.c.map((c) => <div key={c} className="bt-task">{c}</div>)}
                </div>
              ))}
            </div>
          </div>
        </section>

        <section id="faq" className="bt-sec">
          <div className="bt-wrap bt-narrow">
            <h2>Frequently asked questions</h2>
            {FAQ.map((f) => (
              <details key={f.q}><summary>{f.q}</summary><p>{f.a}</p></details>
            ))}
          </div>
        </section>

        <section className="bt-sec bt-final">
          <div className="bt-wrap bt-narrow bt-center">
            <h2>Ready to build something great?</h2>
            <p className="bt-sub">Create your free workspace in under a minute.</p>
            <div className="bt-cta bt-cta-center">
              <a className="bt-btn" href={REGISTER_URL}>Create free account</a>
              <a className="bt-btn bt-btn-ghost" href={LOGIN_URL}>Log in</a>
            </div>
          </div>
        </section>
      </main>

      <footer className="bt-foot">
        <div className="bt-wrap bt-foot-in">
          <p>© {new Date().getFullYear()} {BRAND}.ai</p>
          <nav><a href="#features">Features</a><a href="#faq">FAQ</a><a href={LOGIN_URL}>Log in</a></nav>
        </div>
      </footer>
    </div>
  );
}
