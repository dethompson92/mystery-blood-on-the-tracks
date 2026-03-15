# Murder Mystery Universe - Website Source

This repository contains the full static website source code for "The Murder Mystery Collective", an immersive interactive true crime experience.

## Overview
The platform hosts multiple interconnected mysteries. It is built using:
- Pure **HTML5** (Semantic structuring, accessibility)
- Pure **CSS3** (CSS Variables, Flexbox/Grid, Responsive Design)
- **Vanilla JavaScript** (No React/Vue frameworks required)
- `localStorage` and `sessionStorage` for game state and GM gating

This architecture allows the site to be hosted essentially anywhere for free, using platforms like Vercel, Surge, or GitHub Pages.

## Directory Structure
- `/assets/`: Global CSS styling and core JavaScript logic shared across mysteries.
- `/mystery-3a/`: "The Algorithm Knows" (Tech Thriller).
- `/mystery-2a/`: "The Final Prescription" (Medical Thriller).
- `/mystery-2b/`: "Blood on the Tracks" (Vintage Noir).
- `/mystery-2c/` & others: Landing pages for upcoming expansions.

## Deployment Instructions (Vercel)
This project is optimized for Vercel deployment if avoiding Netlify.
1. Ensure you have Node.js installed.
2. Open a terminal in the `/Website/` directory.
3. Run `npx vercel` (for preview) or `npx vercel --prod` (for production).
4. Follow the CLI prompts to link and deploy.

Alternatively, you can use `npx surge` for a zero-config throwaway deployment.

## Adding a New Mystery
1. Create a new folder (e.g. `mystery-4a`).
2. Create `assets/css/mystery-4a.css` defining the custom color palette variables.
3. Build the core pages: `index.html` (Brief), `suspects.html`, `evidence.html`, `solution.html`.
4. Ensure `solution.html` includes the GM portal script and requires authentication.
5. Add the new mystery to the global `mysteries.html` and the `gm-portal.html` quick reference guide.
