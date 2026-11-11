# Oats, Etc. — Modern Comfort Kitchen

A public concept-preview website for a potential sweet-and-savory grain-bowl business in Boise, Idaho.

View: https://cwarloe.github.io/businessideas/oats-and-more/

Interactive brand design studio: https://cwarloe.github.io/businessideas/oats-and-more/design-lab.html

## What is included

- Responsive homepage with six sample products and a sweet/savory filter
- **Brand design studio** with three independently structured websites: Oats, Etc. (neighborhood kitchen), Oatmeal Station (counter-service), and Oats All Ways (playful all-day bowl bar)
- Mix-and-match controls for brand, website layout, palette, headline, and hero image; URL state enables sharing individual combinations
- Original site photography is reused in `design-assets.js`, excluding the cart image carrying the old name
- Illustrative bowl-price customizer
- Live flavor voting through a separate Cloudflare Worker and D1 database
- Private poll manager with tallies, open/close controls, and CSV export
- Concept cart and corporate catering messaging
- Printable menu board: [menu-board.html](menu-board.html)

**Preview only:** Not operating, not taking orders, and no tastings are scheduled. Prices and recipes are proposals. None of the alternate business names has been professionally trademark-cleared. The design studio is not wired to the live poll, so trying alternative looks does not cast votes.

The deployed HTML pages are self-contained (inline styling, scripts and AI-generated concept imagery), so a branch-based GitHub Pages setup can serve them without a build system.

To turn on Pages: **Repository Settings → Pages → Deploy from a branch → main /docs → Save**. The site will be under /businessideas/oats-and-more/ after deployment. A future dedicated repo can be created and this site moved into its root.
