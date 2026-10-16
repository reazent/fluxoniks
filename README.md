# Fluxoniks — GHG & Sustainability Consulting

Modern, static marketing site for **Fluxoniks**, a standards-based GHG accounting, LCA,
climate disclosure and sustainable finance consultancy serving the US and Canada.

Built as a zero-build static site (plain HTML/CSS/JS) — ideal for **Cloudflare Pages** free tier.

## Tech & structure

- **No framework, no build step.** Plain HTML5 + CSS + vanilla JS.
- `index.html`, `services.html`, `approach.html`, `contact.html` — pages
- `css/styles.css` — all styles (CSS variables, responsive, reduced-motion aware)
- `js/main.js` — mobile nav, header scroll shadow, scroll reveal, contact form handling
- `favicon.svg` — brand mark
- `_headers` — Cloudflare Pages security headers + long-cache rules for assets
- `robots.txt`, `sitemap.xml` — SEO

## Local preview

```bash
python3 -m http.server 8080
# then open http://localhost:8080
```

## Deploy to Cloudflare Pages (free tier)

1. **Push this repo to GitHub** (see below) under your `reazent` account.
2. Go to **Cloudflare → Workers & Pages → Create → Pages → Connect to Git**.
   - Select the GitHub account `reazent` and authorize Cloudflare.
   - Select the `fluxoniks` repository.
   - **Framework preset:** None (just static).
   - **Build command:** *(leave blank — no build)*
   - **Build output directory:** `/` (or `.` — the repo root is the site root).
   - **Environment:** Production.
   - **Save and Deploy.**
3. Cloudflare builds and deploys in seconds. You get a `*.pages.dev` URL instantly.
4. **Add the custom domain** `fluxoniks.com`:
   - Cloudflare Pages → your project → **Custom domains → Set up a custom domain**.
   - Enter `fluxoniks.com`. Cloudflare auto-creates the DNS records if the domain is
     already on your Cloudflare account; otherwise add the CNAME/ALIAS as instructed.
   - Add `www.fluxoniks.com` too (redirects to the apex automatically).
   - SSL is issued automatically. It may take a few minutes to go live.

> If `fluxoniks.com` is **registered elsewhere** (not on Cloudflare), point the domain's
> nameservers to Cloudflare first (recommended, free), OR add a CNAME pointing
> `<your-project>.pages.dev` and let Cloudflare proxy it.

## Enable the contact form (optional, free)

The contact form currently runs client-side only (graceful fallback + email prompt). To
make it deliver real submissions for free:

1. Create a free account at **Formspree** (formspree.io).
2. Create a new form and copy the endpoint (e.g. `https://formspree.io/f/xxxxxxxx`).
3. In `contact.html`, set the form `action` and `method`:

   ```html
   <form class="contact-form" id="contactForm"
         action="https://formspree.io/f/xxxxxxxx" method="POST" novalidate>
   ```

4. Commit and push. Submissions arrive in your inbox; Formspree can also forward to
   `hello@fluxoniks.com`.

> Other free alternatives: **Cloudflare Forms**, **Web3Forms**, **Formspark**. Any
> provider that accepts a form `POST` will work without changing the styling.

## Update content

- Service copy lives in `services.html` (one `<article class="service">` per line).
- Brand colours live as CSS variables at the top of `css/styles.css`.
- No pricing appears on the site — pricing is provided on request after a scoping call.

## License

© Fluxoniks. All rights reserved.