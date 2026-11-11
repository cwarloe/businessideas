# Oats & More — voting service

Cloudflare Worker + D1 SQLite API modeled on Charles Fan Club's polling feature.
It uses its own separate database, with no child or family data. The customer-facing
website stays on GitHub Pages at
https://cwarloe.github.io/businessideas/oats-and-more/.

## Live deployment

Deployed November 10, 2026 to a separate Worker and D1 database:

- API: https://oats-and-more-voting.charles-warloe.workers.dev
- Database: `oats-and-more-votes`
- Voting: https://cwarloe.github.io/businessideas/oats-and-more/
- Admin: https://cwarloe.github.io/businessideas/oats-and-more/vote-admin.html

The admin token is stored as a Cloudflare Worker secret, never in this repository.
A private access file was provided to the owner. Rotate the `ADMIN_TOKEN` secret
in Cloudflare if needed, then use the new value in the admin dashboard.

Live validation covered voting, vote updates without duplicate ballots,
returning-browser identity, results, rejected origins, and admin authentication.
The validation ballot was removed after testing.

## Setup in another Cloudflare account

1. From this folder, run npx wrangler login, unless already logged in.
2. Run npx wrangler d1 create oats-and-more-votes.
3. Copy the new database UUID into this folder's wrangler.toml.
4. Make a random 32+ character ADMIN_TOKEN in a password manager.
   Never commit the secret to GitHub.
5. Run npx wrangler d1 execute oats-and-more-votes --remote --file=./schema.sql.
6. Run npx wrangler deploy (initially replies that configuration is incomplete).
7. Run npx wrangler secret put ADMIN_TOKEN, then paste the secret when prompted.
   This creates a new Worker version with the required secret.
8. Verify the deployed URL, e.g. https://YOUR-WORKER.workers.dev/api/health,
   and GET /api/polls/first-bowl before enabling website voting.
9. Enter the Worker origin into docs/oats-and-more/vote-config.js (no trailing slash).
   The GitHub Pages homepage will then submit real votes automatically.

The separate admin dashboard at docs/oats-and-more/vote-admin.html can show
tallies, create more polls, open/close polls, and download aggregate CSV counts.
It requires the secret ADMIN_TOKEN, typed in only when using the dashboard.

## API contract

GET /api/health — check ready
GET /api/polls — list open polls
GET /api/polls/first-bowl — options; counts after vote
POST /api/polls/first-bowl/vote — JSON { "choice": "apple" }
Returns ballot_token on first vote; keep it in the visitor browser and send
X-Ballot-Token on subsequent calls. Re-voting updates the existing ballot.

GET /api/admin/polls — list all polls (Bearer secret required)
POST /api/admin/polls — create {id, question, options: [labels], visibility}
PATCH /api/admin/polls/{id} — {status:"open"|"closed"}
GET /api/admin/polls/{id}/results — current tally
GET /api/admin/polls/{id}/export.csv — aggregate CSV

## Security and accuracy notes

- One ballot per browser secret, NOT a verified human. Clearing storage,
  multiple browsers and automation may produce duplicates. Treat counts as
  directional market feedback rather than a scientific survey.
- Rate limiting slows repeat anonymous new ballots. Add Turnstile if
  fraud becomes an issue or the campaign draws significant traffic.
- Browser CORS allows the GitHub Pages origin, but is not authentication.
- No names, emails or other contact information are collected.
- Results are normally shown after voting; owner-only polls keep counts private.
- Database and Worker quotas depend on Cloudflare's plan and usage.
- Tested against the deployed Cloudflare D1 instance. Counts remain directional feedback, not verified unique people.

## Source examples reused

Charles Fan Club D1: https://github.com/cwarloe/Charles-Fan-Club/blob/main/migrations/0001_polls.sql
Charles Fan Club polls: https://github.com/cwarloe/Charles-Fan-Club/tree/main/functions/api/polls
Charles Fan Club admin: https://github.com/cwarloe/Charles-Fan-Club/blob/main/public/polls/admin.html
