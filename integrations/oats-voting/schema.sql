-- Oats & More separate poll database. No names, email addresses or child data.
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS polls (
 id TEXT PRIMARY KEY,
 question TEXT NOT NULL CHECK(length(question) BETWEEN 1 AND 200),
 status TEXT NOT NULL DEFAULT 'open' CHECK(status IN ('open','closed')),
 visibility TEXT NOT NULL DEFAULT 'after_vote' CHECK(visibility IN ('public','after_vote','owner')),
 created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE TABLE IF NOT EXISTS poll_options (
 id INTEGER PRIMARY KEY,
 poll_id TEXT NOT NULL REFERENCES polls(id) ON DELETE CASCADE,
 slug TEXT NOT NULL,
 label TEXT NOT NULL CHECK(length(label) BETWEEN 1 AND 120),
 position INTEGER NOT NULL,
 UNIQUE(poll_id,slug), UNIQUE(poll_id,position)
);
CREATE TABLE IF NOT EXISTS ballots (
 id INTEGER PRIMARY KEY,
 poll_id TEXT NOT NULL REFERENCES polls(id) ON DELETE CASCADE,
 voter_key TEXT NOT NULL,
 option_id INTEGER NOT NULL REFERENCES poll_options(id),
 created_at TEXT NOT NULL DEFAULT (datetime('now')),
 updated_at TEXT NOT NULL DEFAULT (datetime('now')),
 UNIQUE(poll_id,voter_key)
);
CREATE INDEX IF NOT EXISTS ballots_poll_option ON ballots(poll_id,option_id);
CREATE TABLE IF NOT EXISTS rate_events (scope TEXT NOT NULL,ts INTEGER NOT NULL);
CREATE INDEX IF NOT EXISTS rate_events_scope_ts ON rate_events(scope,ts);
INSERT OR IGNORE INTO polls (id,question,visibility) VALUES
 ('first-bowl','Which bowl would you try first?','after_vote');
INSERT OR IGNORE INTO poll_options(poll_id,slug,label,position) VALUES
 ('first-bowl','apple','Apple Pie Oats',0),
 ('first-bowl','cheddar','Cheddar & Egg Grits',1),
 ('first-bowl','mushroom','Mushroom & Herb Oats',2);
