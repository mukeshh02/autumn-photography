# Autumn website copy

The separate Winter / Maira Weddings copy is in `winter`, on http://localhost:3001. Its files and sample content are independent of Autumn. Double-click `start-both.cmd` to start both local servers, or use each site's own `start-site.cmd`.

Reference: https://avala.bold-themes.com/autumn/home/home-02/

The portfolio now uses the fictional brand **Aarav Mehta Photography**, based in New Delhi, with sample portrait/pre-wedding/wedding packages of ₹4,999 / ₹24,999 / ₹74,999. Email (`hello@aaravmehta.example`), phone, social handle, experience and client names are placeholders. The original demo photographs remain. `personalize.py` applies these details after a fresh mirror/finalization.

The public site has been copied into `public`, including 85 HTML files, the four home designs, About/Couples pages, Services, Blog and Gallery variants, detail pages, Shop and account screens. Images, styles, scripts, and Google Fonts are stored locally.

Run `npm run dev` (or double-click `start-site.cmd`) and open http://localhost:3000. No dependency installation is required. `server.js` serves the copied files and resolves the original Blog/Gallery query-string layouts.

`mirror.py` contains the downloader; an explicitly authorized reference access cookie can be provided through the temporary `REFERENCE_COOKIE` environment variable. No browser cookies are stored in the project. After downloading, run `python finalize.py` to localize Google Fonts, remove demo analytics, and correct script order. Run `python audit.py` to check local links and resources.

Verification: the link audit checked 458 local paths with zero missing resources. Home slider, images, Blog, Gallery layout variant, Shop, and the mobile homepage were inspected in the browser. See `audit-report.json` for the file audit. `mirror-report.json` also records old font formats and unused payment icons that are missing on the source server; available font alternatives are used locally.

This is a static preview. WordPress administration, live checkout, authentication, search, and form delivery require a separate backend. Form submission is stopped locally. Third-party video/audio/map embeds and external social links still require an internet connection.
