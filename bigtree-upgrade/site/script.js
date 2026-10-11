// Set this to your backend route (e.g. "/api/waitlist") once it exists.
const FORM_ENDPOINT = "";

document.getElementById("yr").textContent = new Date().getFullYear();

const burger = document.querySelector(".burger"), links = document.getElementById("links");
burger.addEventListener("click", () => {
  const open = links.classList.toggle("open");
  burger.setAttribute("aria-expanded", open);
});
links.querySelectorAll("a").forEach(a => a.addEventListener("click", () => links.classList.remove("open")));

const io = new IntersectionObserver(es => es.forEach(e => {
  if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
}), { threshold: .12 });
document.querySelectorAll(".reveal").forEach(el => io.observe(el));

const form = document.getElementById("lead"), msg = document.getElementById("msg");
form.addEventListener("submit", async ev => {
  ev.preventDefault();
  const email = form.email.value.trim();
  msg.className = "msg";
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) { msg.textContent = "Please enter a valid email."; msg.classList.add("err"); return; }
  if (!FORM_ENDPOINT) { msg.textContent = "Form not connected yet — set FORM_ENDPOINT in script.js."; msg.classList.add("err"); return; }
  try {
    const r = await fetch(FORM_ENDPOINT, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ email }) });
    if (!r.ok) throw new Error();
    msg.textContent = "You're on the list — thank you! 🌳"; form.reset();
  } catch { msg.textContent = "Something went wrong. Please try again."; msg.classList.add("err"); }
});
