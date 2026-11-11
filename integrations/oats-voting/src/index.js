/**
 * Oats, Etc. concept-poll API.
 * Based on the separate Charles Fan Club D1 polling approach, NOT its DB.
 * Accepts votes only from the approved GitHub Pages origin; CORS is not authentication.
 * Requires D1 binding DB and a 32+ character ADMIN_TOKEN Worker secret.
 */
const SITE_ORIGIN = "https://cwarloe.github.io";
const TOKEN_FORMAT = /^[A-Za-z0-9_-]{43}$/;

function reply(data, status = 200, headers = {}) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { "content-type": "application/json; charset=utf-8",
      "cache-control": "no-store", "x-content-type-options": "nosniff", ...headers }
  });
}
function cors(request) {
  const origin = request.headers.get("Origin");
  return origin === SITE_ORIGIN
    ? { "Access-Control-Allow-Origin": SITE_ORIGIN, "Vary": "Origin",
        "Access-Control-Allow-Methods": "GET, POST, PATCH, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, X-Ballot-Token, Authorization",
        "Access-Control-Max-Age": "600" }
    : { Vary: "Origin" };
}
function makeToken() {
  const bytes = crypto.getRandomValues(new Uint8Array(32));
  return btoa(String.fromCharCode(...bytes)).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/g, "");
}
async function digest(s) {
  const bytes = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(s));
  return Array.from(new Uint8Array(bytes), x => x.toString(16).padStart(2, "0")).join("");
}
async function keyedDigest(secret, message) {
  const key = await crypto.subtle.importKey("raw", new TextEncoder().encode(secret),
    { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  const signature = await crypto.subtle.sign("HMAC", key, new TextEncoder().encode(message));
  return Array.from(new Uint8Array(signature), x => x.toString(16).padStart(2, "0")).join("");
}
async function isAdmin(req, env) {
  const auth = req.headers.get("Authorization") || "";
  const supplied = auth.startsWith("Bearer ") ? auth.slice(7) : "";
  if (supplied.length < 32) return false;
  // compare fixed-length hashes to avoid content-dependent string length timing.
  const [a, b] = await Promise.all([digest(supplied), digest(env.ADMIN_TOKEN)]);
  let different = 0;
  for (let i = 0; i < a.length; i++) different |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return different === 0;
}
async function throttle(env, scope, limit, windowSeconds) {
  const now = Math.floor(Date.now() / 1000);
  const result = await env.DB.prepare(
    "INSERT INTO rate_events (scope, ts) SELECT ?1, ?2 WHERE (SELECT COUNT(*) FROM rate_events WHERE scope=?1 AND ts>?3) < ?4"
  ).bind(scope, now, now - windowSeconds, limit).run();
  if (Math.random() < 0.03)
    await env.DB.prepare("DELETE FROM rate_events WHERE ts<?").bind(now - 86400).run();
  return result.meta?.changes === 1;
}
async function ballotIdentity(req, env, pollId) {
  const token = req.headers.get("X-Ballot-Token");
  if (!token || !TOKEN_FORMAT.test(token)) return null;
  return { token, key: await digest(pollId + ":" + token) };
}
async function pollDetails(env, id, identity, admin = false) {
  const poll = await env.DB.prepare("SELECT id, question, status, visibility, created_at FROM polls WHERE id=?").bind(id).first();
  if (!poll) return null;
  const myRow = identity ? await env.DB.prepare(
    "SELECT option_id FROM ballots WHERE poll_id=? AND voter_key=?"
  ).bind(id, identity.key).first() : null;
  const { results } = await env.DB.prepare(
    "SELECT o.id, o.slug, o.label, COUNT(b.id) AS votes FROM poll_options o LEFT JOIN ballots b ON b.option_id=o.id AND b.poll_id=o.poll_id WHERE o.poll_id=? GROUP BY o.id ORDER BY o.position"
  ).bind(id).all();
  const total = results.reduce((sum, opt) => sum + Number(opt.votes), 0);
  const show = admin || poll.visibility === "public" ||
    (poll.visibility === "after_vote" && (!!myRow || poll.status === "closed"));
  return {
    poll, voted: !!myRow,
    my_choice: myRow ? results.find(x => x.id === myRow.option_id)?.slug ?? null : null,
    options: results.map(x => ({ slug: x.slug, label: x.label, ...(show ? { votes: Number(x.votes) } : {}) })),
    results: show ? { total_voters: total } : null,
    results_hidden_reason: show ? null : "Vote to see the current results."
  };
}
async function readJSON(req) {
  if (!(req.headers.get("content-type") || "").toLowerCase().startsWith("application/json")) return null;
  try { return await req.json(); } catch { return null; }
}
function safeId(s) { return typeof s === "string" && /^[a-z0-9-]{3,40}$/.test(s); }
function csvCell(s) {
  const value = String(s ?? "");
  // Neutralize spreadsheet formulas in CSV opened with Excel or Sheets.
  const safe = /^[\s]*[=+\-@]/.test(value) ? "'" + value : value;
  return '"' + safe.replace(/"/g, '""') + '"';
}
async function handler(req, env) {
  if (!env.DB || !env.ADMIN_TOKEN || env.ADMIN_TOKEN.length < 32) {
    return reply({ error: "Voting service is not configured." }, 503);
  }
  const url = new URL(req.url);
  const path = url.pathname.replace(/\/+$/, "") || "/";
  if (path === "/api/health" && req.method === "GET") return reply({ ok: true, service: "oats-voting" });

  if (path === "/api/polls" && req.method === "GET") {
    const { results } = await env.DB.prepare(
      "SELECT id, question, status FROM polls WHERE status='open' ORDER BY created_at DESC"
    ).all();
    return reply({ polls: results });
  }

  const pollMatch = /^\/api\/polls\/([a-z0-9-]+)$/.exec(path);
  if (pollMatch && req.method === "GET") {
    const id = pollMatch[1];
    const identity = await ballotIdentity(req, env, id);
    const data = await pollDetails(env, id, identity);
    return data ? reply(data) : reply({ error: "Poll not found." }, 404);
  }

  const voteMatch = /^\/api\/polls\/([a-z0-9-]+)\/vote$/.exec(path);
  if (voteMatch && req.method === "POST") {
    const id = voteMatch[1];
    const data = await pollDetails(env, id, null);
    if (!data) return reply({ error: "Poll not found." }, 404);
    if (data.poll.status !== "open") return reply({ error: "This poll is closed." }, 403);
    const body = await readJSON(req);
    if (!body || typeof body.choice !== "string") return reply({ error: "Choose a valid bowl." }, 400);
    const target = data.options.find(o => o.slug === body.choice);
    if (!target) return reply({ error: "Unknown bowl." }, 400);

    const identity = await ballotIdentity(req, env, id);
    const existing = identity ? await env.DB.prepare(
      "SELECT id FROM ballots WHERE poll_id=? AND voter_key=?").bind(id, identity.key).first() : null;
    const ip = req.headers.get("CF-Connecting-IP") || "unknown";
    const network = await keyedDigest(env.ADMIN_TOKEN, "ip:" + ip);
    if (!(await throttle(env, "network-minute:" + network, 20, 60)))
      return reply({ error: "Voting is busy on this network. Try again shortly." }, 429);
    if (!existing && !(await throttle(env, "new-vote:" + id + ":" + network, 60, 3600)))
      return reply({ error: "Too many new votes from this network. Try again later." }, 429);

    const token = identity?.token || makeToken();
    const key = identity?.key || await digest(id + ":" + token);
    const opt = await env.DB.prepare("SELECT id FROM poll_options WHERE poll_id=? AND slug=?").bind(id, body.choice).first();
    await env.DB.prepare(
      "INSERT INTO ballots (poll_id, voter_key, option_id) VALUES (?,?,?) " +
      "ON CONFLICT(poll_id,voter_key) DO UPDATE SET option_id=excluded.option_id, updated_at=datetime('now')"
    ).bind(id, key, opt.id).run();
    const view = await pollDetails(env, id, { token, key });
    // Only new visitors receive a new token. Frontend stores it on this browser.
    if (!identity) view.ballot_token = token;
    return reply(view);
  }

  const admin = path.startsWith("/api/admin");
  if (admin) {
    if (!(await isAdmin(req, env))) return reply({ error: "Administrator token required." }, 401);
    if (path === "/api/admin/polls" && req.method === "GET") {
      const { results } = await env.DB.prepare("SELECT id, question, status, visibility, created_at FROM polls ORDER BY created_at DESC").all();
      return reply({ polls: results });
    }
    if (path === "/api/admin/polls" && req.method === "POST") {
      const b = await readJSON(req);
      if (!b || !safeId(b.id) || typeof b.question !== "string" || !Array.isArray(b.options))
        return reply({ error: "Supply id, question and options." }, 400);
      const q = b.question.trim();
      const labels = b.options.map(x => typeof x === "string" ? x.trim() : "");
      if (!q || q.length > 200 || labels.length < 2 || labels.length > 12 ||
          labels.some(x => !x || x.length > 120) || new Set(labels).size !== labels.length)
        return reply({ error: "Question or options invalid." }, 400);
      const slugs = labels.map(x => x.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "").slice(0, 40));
      if (slugs.some(x => !x) || new Set(slugs).size !== slugs.length)
        return reply({ error: "Options must produce distinct URLs; rename similar choices." }, 400);
      if (b.visibility != null && !["public", "after_vote", "owner"].includes(b.visibility))
        return reply({ error: "Unknown results visibility." }, 400);
      if (await env.DB.prepare("SELECT id FROM polls WHERE id=?").bind(b.id).first())
        return reply({ error: "Poll ID already exists." }, 409);
      await env.DB.batch([
        env.DB.prepare("INSERT INTO polls (id,question,visibility) VALUES (?,?,?)").bind(b.id, q, b.visibility || "after_vote"),
        ...labels.map((label,i) => env.DB.prepare("INSERT INTO poll_options (poll_id,slug,label,position) VALUES (?,?,?,?)").bind(b.id,slugs[i],label,i))
      ]);
      return reply({ id:b.id, created:true }, 201);
    }
    const patch = /^\/api\/admin\/polls\/([a-z0-9-]+)$/.exec(path);
    if (patch && req.method === "PATCH") {
      const b = await readJSON(req);
      if (!b || !["open", "closed"].includes(b.status))
        return reply({ error: "Status must be open or closed." }, 400);
      const row = await env.DB.prepare("UPDATE polls SET status=? WHERE id=?").bind(b.status, patch[1]).run();
      return row.meta?.changes ? reply({ id:patch[1],status:b.status }) : reply({error:"Poll not found."},404);
    }
    const results = /^\/api\/admin\/polls\/([a-z0-9-]+)\/results$/.exec(path);
    if (results && req.method === "GET") {
      const data = await pollDetails(env, results[1], null, true);
      return data ? reply(data) : reply({ error: "Poll not found." }, 404);
    }
    const exportMatch = /^\/api\/admin\/polls\/([a-z0-9-]+)\/export\.csv$/.exec(path);
    if (exportMatch && req.method === "GET") {
      const data = await pollDetails(env, exportMatch[1], null, true);
      if (!data) return reply({ error: "Poll not found." }, 404);
      const rows = [["option","votes"], ...data.options.map(x => [x.label,x.votes])];
      return new Response(rows.map(r => r.map(csvCell).join(",")).join("\r\n")+"\r\n",{
        headers: {"content-type":"text/csv; charset=utf-8", "cache-control":"no-store",
          "content-disposition": 'attachment; filename="' + exportMatch[1] + '-results.csv"'}
      });
    }
  }
  return reply({ error: "Not found." }, 404);
}
export default {
  async fetch(request, env) {
    const headers = cors(request);
    if (request.method === "OPTIONS") {
      return new Response(null, { status: request.headers.get("Origin") === SITE_ORIGIN ? 204 : 403, headers });
    }
    if (["POST","PATCH"].includes(request.method)) {
      if (request.headers.get("Origin") !== SITE_ORIGIN)
        return reply({ error:"Request origin not allowed." },403,headers);
      if (!(request.headers.get("content-type") || "").startsWith("application/json"))
        return reply({ error:"JSON requests only." },415,headers);
    }
    try {
      const response = await handler(request, env);
      const h = new Headers(response.headers);
      Object.entries(headers).forEach(([k,v])=>h.set(k,v));
      h.set("x-frame-options","DENY");
      return new Response(response.body, { status:response.status, headers:h });
    } catch (err) {
      console.error("Voting API error", err);
      return reply({ error:"Voting temporarily unavailable." },500,headers);
    }
  }
};
