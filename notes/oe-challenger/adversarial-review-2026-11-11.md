# Oats, Etc.: adversarial review, round 1

Mode: ADVERSARIAL. Author: OE Challenger (second set of eyes, not the builder).
Date: 2026-11-11. Repo state reviewed: commit 63e8d9c on main.

Files read: docs/oats-and-more/README.md, index.html, design-lab.html, menu-board.html, vote-live.js, vote-config.js, vote-admin.html (skimmed), integrations/oats-voting/README.md and src/index.js (skimmed for CORS and rate limiting). I also called the live Worker's /api/health and /api/polls (read only). I did not cast a vote, so I have not seen the live tally.

Not checked, and so not claimed: competitors in Boise, ingredient or rent costs, Idaho food licensing rules, trademark searches, domain or social handle availability. Anything below about those is a guess and is labeled as one.

## Ranked objections (most damaging first)

### 1. There is no demand evidence, and the current poll cannot produce any
What is there: one poll, "Which bowl would you try first?", with three options (Apple Pie, Cheddar & Egg, Mushroom & Herb). Source: index.html vote section, integrations/oats-voting/README.md.
Why it could hurt: the poll forces a choice among options the owner picked, has no "none of these" answer, shows no price, and collects no contact info. A click on a free anonymous poll says nothing about whether someone pays $8.95. The README itself says counts are "directional market feedback" and that ballots are not verified people. The risk is that a pile of votes feels like validation when it is not.
Cheap test: add a "none of these, not for me" option and a "how much would you pay" question. Add an optional email or text field for "tell me when it is real." Send it to a known audience (a named group, not the open web) so you can tell who answered. Better still, put real food in front of 20 to 30 people and ask them to rank and pay a small amount. Settles it: the share who choose "not for me", the share who leave contact info, and whether anyone pays.

### 2. Unit economics do not exist anywhere in the repo
What is there: prices ($5.95 to $10.50, add-ons $1.00 to $1.75) in index.html and menu-board.html, labeled "test prices." No food cost, labor, rent, equipment or volume anywhere.
Why it could hurt: the cheapest bowl is oatmeal, which is a low-price item by habit. If the $5.95 Classic is the entry point, it carries the thinnest margin and the most price resistance. Customization ("made your way", index.html) adds prep time and waste. I cannot tell from the repo whether any bowl makes money.
Cheap test: cost each of the six recipes per serving with real grocery receipts, then compute margin per bowl and bowls per day needed to cover rent and one wage. A common restaurant rule of thumb is food cost in the high 20s to mid 30s percent of price (a guess from general knowledge, verify before relying on it). Settles it: a one-page spreadsheet.

### 3. The core differentiator, savory oats and grits, is untested, and the design lab says so
What is there: design-lab.html lists the test question "Does a warm, neighborhood-friendly brand make unfamiliar savory oat dishes feel approachable?" and notes "Oatmeal Station" may sound breakfast-only. The homepage leans on "Sweet mornings. Savory afternoons."
Why it could hurt: if people see oatmeal as breakfast only, the afternoon half of the concept does not exist, and lunch is where the higher-priced savory bowls ($8.95 to $10.50) sit. Those bowls then compete with every other lunch bowl in town, which I have not researched.
Cheap test: a tasting of only the three savory bowls at lunchtime with a short card: would you buy this for lunch, at what price, and what would you compare it to. Settles it: purchase intent for savory at lunch, separate from sweet at breakfast.

### 4. The customer is not defined, and the one concrete segment (groups) captures nothing
What is there: the homepage speaks to everyone ("Made to fit your day"). The "For Groups" section has two calls to action ("Tell us what your team would like", "Help shape the menu") and both just link to #vote (index.html). No form, email, phone or mailto exists in the page.
Why it could hurt: catering and office breakfast is the segment most likely to give repeat, larger orders, and it currently produces zero signal. Also, grits are known to thicken and set as they cool, so hot savory bowls may travel and hold poorly for catering (a cooking-knowledge guess, test it).
Cheap test: pick one customer sentence ("office managers in downtown Boise ordering breakfast for 10") and ask 10 of them directly what they order now, from where, and what they pay. Settles it: whether the segment exists and whether it will pay.

### 5. Effort is going into brand polish ahead of validation, and no name is cleared
What is there: three brand directions, a mix-and-match design lab, and a roughly 817 KB homepage plus 600 KB of image data, all built in the last two days (git log). The README states no alternate name is trademark-cleared. "Oats, Etc." and "Oats All Ways" are descriptive, which tends to make a name hard to protect (general trademark principle, unverified for these names).
Why it could hurt: a polished brand can be abandoned if the name fails clearance or the concept fails demand. The repo, URL path and some files still say oats-and-more (README.md mentions the old name in a cart image).
Cheap test: before any more design work, do a basic name check (state business name search, USPTO search, domain and handle availability) on the one name Charles prefers. Settles it: a go or no-go on the name in under an hour.

### 6. A public claim does not hold: "Boise-area market research"
What is there: the footer of index.html reads "Concept preview · Boise-area market research · Not open for orders."
Why it could hurt: the only research in the repo is one anonymous poll. Calling it market research overstates it, and a reader could treat it as a fact claim.
Cheap fix: reword to "Concept preview · Collecting early feedback." This is the builder's file, so I have not edited it.

### 7. Poll integrity and how raw counts look in public
What is there: one ballot per browser token, rate limiting, CORS locked to the Pages origin (src/index.js). After voting, the page shows the raw tally and "N recorded votes" to every visitor (vote-live.js).
Why it could hurt: a small visible number such as "4 recorded votes" is public evidence of low interest. Duplicate ballots from clearing storage are possible, as the README admits. The three options also leave out the cheapest and the most familiar bowls (The Classic, PB & Banana), which biases results toward the three chosen.
Cheap test: hide the live count until a minimum is reached, or show only percentages. Settles it: a design choice, no data needed.

### 8. Small claim mismatches
- The name says oats, but two of six menu items are grits (Cheddar & Egg, Southwest in index.html), which are corn.
- "Easy to Take Along" (index.html) applies to cold overnight oats, but hot grits are the opposite of travel food. Unverified, test with a takeout trial.
- "Made your way" offers three bases and four add-ons in the bowl builder, so it is a small menu, not open customization.

## What I would do first (if only one thing)
Objection 1 and 3 together: one small tasting with a short card (not-for-me option, price, lunch vs breakfast, contact opt-in). It costs a few groceries and an afternoon, and it tests the two assumptions the whole business sits on.

## Open questions for Charles
- Who is the first customer you picture, in one sentence?
- Is the plan a counter, a cart or pop-up, a catering-only kitchen, or packaged product? Each changes which objections matter.
