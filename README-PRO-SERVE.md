# Pro Serve Academy — Webflow HTML starter

This is a cleaned working copy of the supplied Kresil Webflow HTML export.
The original export is preserved separately.

## Running locally

1. Extract this ZIP.
2. Open the extracted folder in VS Code.
3. Install the **Live Server** VS Code extension if you don't already have it.
4. Right-click `index.html` and select **Open with Live Server**.
5. Work primarily in `index.html`, the other `.html` files, and `css/emmanuels-dynamite-site-352d79.webflow.css`.

Alternative with Python installed:

    python -m http.server 5500

Then visit http://localhost:5500/.

## What was fixed

- Repaired 22 missing image-path references by adding correctly named image aliases.
- Removed the unnecessary third-party review/validation snippet from the exported HTML pages.
- Kept Webflow's CSS, its JavaScript, GSAP references, the pages and template layout intact.

## Work still required

- Replace Kresil branding, stock content, images, placeholder contact details and social links.
- Replace links pointing to `kresil.webflow.io` with suitable Pro Serve Academy routes.
- Decide what to do with blank/non-exported Webflow CMS data (blog, team/faculty, careers).
- Wire all forms to a real submission backend/service. Contact and signup forms are currently nonfunctional as submissions.
- Audit and test externally loaded scripts/fonts after deployment.
- Test every route, interaction and mobile breakpoint.

## Important

Webflow exported a static HTML/CSS/JS site. Do not assume CMS functionality, form submissions, and dynamic pages are included. This is a starter only, not a completed Pro Serve Academy website.
