import { Link } from "react-router-dom";

const features = [
  {
    number: "01",
    title: "Keep every project in one place",
    description:
      "Bring your notes, files, tasks and conversations together in a workspace your whole team can understand.",
    icon: "◫",
  },
  {
    number: "02",
    title: "Move from ideas to action",
    description:
      "Turn plans into clear next steps, track progress and keep momentum without losing the bigger picture.",
    icon: "↗",
  },
  {
    number: "03",
    title: "Work with an AI that has context",
    description:
      "Ask your project co-pilot to brainstorm, draft and summarize with the project information you provide.",
    icon: "✳",
  },
];

const steps = [
  ["Create a workspace", "Give your project a home and bring the important details together."],
  ["Invite collaboration", "Share context with teammates and keep discussions connected to the work."],
  ["Make progress visible", "Organize tasks, capture decisions and use AI to get unstuck."],
];

function TreeMark({ small = false }) {
  return (
    <span className={`brand-mark${small ? " brand-mark-small" : ""}`} aria-hidden="true">
      <span />
      <span />
      <span />
    </span>
  );
}

function ArrowIcon() {
  return <span aria-hidden="true" className="arrow-icon">↗</span>;
}

export default function Landing() {
  return (
    <main className="marketing-site">
      <header className="marketing-nav">
        <Link className="brand" to="/" aria-label="BigTree.ai home">
          <TreeMark />
          <span>BigTree<span className="brand-dot">.</span>ai</span>
        </Link>

        <nav className="marketing-nav-links" aria-label="Main navigation">
          <a href="#features">Features</a>
          <a href="#how-it-works">How it works</a>
        </nav>

        <div className="marketing-nav-actions">
          <Link className="nav-login" to="/login">Log in</Link>
          <Link className="button button-primary button-nav" to="/register">
            Get started <ArrowIcon />
          </Link>
        </div>
      </header>

      <section className="hero-section">
        <div className="hero-copy">
          <div className="eyebrow"><span className="eyebrow-dot" /> A calmer way to create together</div>
          <h1>Big ideas grow<br />better <span>together.</span></h1>
          <p className="hero-description">
            Your projects, people and AI co-pilot — finally working in the same place.
            Turn scattered ideas into thoughtful work and meaningful progress.
          </p>
          <div className="hero-actions">
            <Link className="button button-primary button-large" to="/register">
              Start building for free <ArrowIcon />
            </Link>
            <a className="text-link" href="#features">Explore the workspace <span aria-hidden="true">↓</span></a>
          </div>
          <div className="hero-proof">
            <div className="proof-avatars" aria-hidden="true">
              <span>✳</span><span>✦</span><span>↗</span>
            </div>
            <p><strong>One workspace.</strong> Ideas, teamwork and momentum.</p>
          </div>
        </div>

        <div className="hero-visual" aria-label="Preview of a BigTree project workspace">
          <div className="visual-glow" />
          <div className="workspace-window">
            <div className="window-topbar">
              <div className="window-brand"><TreeMark small /><span>BigTree<span className="brand-dot">.</span>ai</span></div>
              <div className="window-controls"><i /><i /><i /></div>
            </div>
            <div className="workspace-body">
              <aside className="mock-sidebar">
                <span className="mock-label">WORKSPACE</span>
                <div className="mock-nav-item active"><span>◫</span> Projects</div>
                <div className="mock-nav-item"><span>◷</span> Recent activity</div>
                <div className="mock-nav-item"><span>✳</span> AI co-pilot</div>
                <div className="mock-sidebar-bottom"><span className="mock-avatar">O</span><span>My workspace</span><span>⌄</span></div>
              </aside>
              <div className="mock-main">
                <div className="mock-breadcrumb">WORKSPACE <span>/</span> PROJECT OVERVIEW</div>
                <div className="mock-heading-row">
                  <div><h3>Make it happen.</h3><p>Your ideas, moving forward.</p></div>
                  <span className="mock-status"><i /> In progress</span>
                </div>
                <div className="mock-stats">
                  <div><span>OPEN TASKS</span><strong>08</strong><small>Things to move forward</small></div>
                  <div><span>PROJECT NOTES</span><strong>12</strong><small>Ideas worth keeping</small></div>
                </div>
                <div className="mock-work-grid">
                  <div className="mock-panel task-panel">
                    <div className="mock-panel-heading">Next up <span>View all ↗</span></div>
                    <div className="mock-task"><b className="task-check done">✓</b><span><strong>Shape the project vision</strong><small>Planning · Completed</small></span></div>
                    <div className="mock-task"><b className="task-check" /><span><strong>Share the first draft</strong><small>Creative · Today</small></span></div>
                    <div className="mock-task"><b className="task-check" /><span><strong>Gather team feedback</strong><small>Collaboration · Upcoming</small></span></div>
                  </div>
                  <div className="mock-panel ai-panel">
                    <div className="ai-panel-title"><span className="ai-spark">✳</span><strong>Your AI co-pilot</strong><span className="online-dot" /></div>
                    <p>Need a fresh perspective?</p>
                    <div className="ai-suggestion">Help me turn these ideas into a plan <span>↗</span></div>
                    <div className="ai-suggestion">Summarize the latest notes <span>↗</span></div>
                    <div className="mock-ai-input">Ask about this project… <span>↑</span></div>
                  </div>
                </div>
                <div className="mock-footer-note"><span>✳</span> Good work grows when everything connects.</div>
              </div>
            </div>
          </div>
          <div className="floating-note floating-note-top"><span className="floating-icon">✦</span><span><strong>Ideas into action</strong><small>One clear next step at a time</small></span></div>
          <div className="floating-note floating-note-bottom"><span className="floating-check">✓</span><span><strong>Progress feels good.</strong><small>Keep your team moving forward</small></span></div>
        </div>
        <div className="hero-bottom-line"><span>MADE FOR THE WORK THAT MATTERS</span><span>PLAN&nbsp; · &nbsp;CREATE&nbsp; · &nbsp;COLLABORATE&nbsp; · &nbsp;GROW</span></div>
      </section>

      <section className="value-strip" aria-label="What BigTree brings together">
        <div><span className="value-icon">◫</span><span><strong>Projects</strong><small>One clear home for the work</small></span></div>
        <div><span className="value-icon">☷</span><span><strong>Tasks & notes</strong><small>Keep plans moving forward</small></span></div>
        <div><span className="value-icon">↔</span><span><strong>Team chat</strong><small>Conversations with context</small></span></div>
        <div><span className="value-icon">✳</span><span><strong>AI co-pilot</strong><small>A partner for the next idea</small></span></div>
      </section>

      <section className="features-section section-shell" id="features">
        <div className="section-intro">
          <span className="section-kicker">A BETTER WAY TO WORK</span>
          <h2>Less scattered.<br /><span>More in sync.</span></h2>
          <p>Great work rarely happens in a straight line. BigTree gives your ideas room to grow while keeping the details within reach.</p>
        </div>
        <div className="feature-grid">
          {features.map((feature) => (
            <article className="feature-card" key={feature.number}>
              <div className="feature-card-top"><span className="feature-icon">{feature.icon}</span><span className="feature-number">{feature.number}</span></div>
              <h3>{feature.title}</h3>
              <p>{feature.description}</p>
              <a href="#how-it-works" className="feature-link">See how it fits <ArrowIcon /></a>
            </article>
          ))}
        </div>
      </section>

      <section className="how-section" id="how-it-works">
        <div className="how-inner">
          <div className="how-copy">
            <span className="section-kicker">START SMALL. GROW FROM THERE.</span>
            <h2>Your next good idea<br />starts <span>here.</span></h2>
            <p>Bring a little order to the creative chaos. Set up a project in minutes and build a workflow that works for you.</p>
            <Link className="button button-primary button-large" to="/register">Create your workspace <ArrowIcon /></Link>
          </div>
          <div className="steps-list">
            {steps.map(([title, description], index) => (
              <div className="step-row" key={title}>
                <span className="step-number">0{index + 1}</span>
                <div><h3>{title}</h3><p>{description}</p></div>
                {index < steps.length - 1 && <span className="step-connector" />}
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="closing-cta">
        <div className="closing-leaf" aria-hidden="true">✳</div>
        <span className="section-kicker">ROOM TO THINK. SPACE TO GROW.</span>
        <h2>Make space for<br /><span>your best work.</span></h2>
        <p>Give your ideas a home and your next project a head start.</p>
        <Link className="button button-light button-large" to="/register">Get started with BigTree.ai <ArrowIcon /></Link>
      </section>

      <footer className="marketing-footer">
        <Link className="brand footer-brand" to="/"><TreeMark small /><span>BigTree<span className="brand-dot">.</span>ai</span></Link>
        <p>Thoughtful work grows here.</p>
        <div className="footer-links"><a href="#features">Features</a><Link to="/login">Log in</Link><Link to="/register">Get started</Link></div>
        <small>© {new Date().getFullYear()} BigTree.ai. Built for ideas in motion.</small>
      </footer>
    </main>
  );
}
