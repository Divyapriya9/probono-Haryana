# Publishing the Haryana Free Legal Aid site (free)

## Before you publish: 5 checks
1. **Spot-check the data.** `build_site.py` holds 104 Pro-Bono rows copied from the official PDF by an AI reader.
   Open the PDF, search "Pro-Bono Basis", and compare names, dates and years row by row (Bhiwani and Tosham first).
2. **Fill CONFIG** at the top of `build_site.py` (SITE_URL, contact link), then run `python3 build_site.py`.
3. **Ask the DLSA in writing** (email or a letter handed in at the ADR Centre, District Courts Complex, Bhiwani): "May I publish the
   panel list and a how-to-apply guide as a free public information page? Please link it from your site if you agree." Keep the reply.
4. **Confirm the helplines** (01664-245933, 15100, 14454) on hslsa.gov.in, nalsa.gov.in and tele-law.in.
5. **Legal comfort.** Bar Council Rule 36 limits how advocates may be advertised, and the Madras High Court has held that
   directories which rank or filter lawyers can be indirect solicitation. This site avoids that on purpose: alphabetical order, no ranking,
   no personal phone numbers, and the route to a lawyer is the DLSA. Do not add "best lawyer" labels, star ratings, or direct call
   buttons for individual lawyers. Ask a local advocate to read it once. I am not a lawyer.

## Put it on GitHub Pages (free) - step by step
**A. Easiest: in the browser (no software)**
1. Go to github.com -> Sign up (free). Verify your email.
2. Click **+ -> New repository**. Name: `haryana-free-legal-aid`. Choose **Public**. Tick "Add a README" (you will replace it). Create.
3. Click **Add file -> Upload files**. Drag in: `index.html`, `robots.txt`, `sitemap.xml`, `panel_pro_bono_haryana.csv`,
   `build_site.py`, `template.html`, `README.md`, `LICENSE`. Click **Commit changes**.
4. **Settings -> Pages**. Under "Build and deployment": Source = **Deploy from a branch**, Branch = **main**, folder = **/ (root)**. Save.
5. Wait 1-2 minutes. The page shows your address: `https://YOURNAME.github.io/haryana-free-legal-aid/`.
6. Open `build_site.py`, set `SITE_URL`, `CONTACT_LINK` (use `https://github.com/YOURNAME/haryana-free-legal-aid/issues`) and `AUTHOR_LINE`
   with your real name. Run `python3 build_site.py` on your Mac and upload the new `index.html`, `sitemap.xml`, `robots.txt`
   (Add file -> Upload files, same names overwrite).
7. Repository **Settings -> General -> Features: tick Issues** so people can report mistakes.

**B. With the Mac terminal (best for updates)**
```
brew install git            # or install from git-scm.com; skip if `git --version` works
cd ~/Desktop/haryana-free-legal-aid        # the unzipped folder
git init
git add .
git commit -m "First version"
git branch -M main
git remote add origin https://github.com/YOURNAME/haryana-free-legal-aid.git
git push -u origin main     # GitHub asks you to log in; use a Personal Access Token as the password, or install GitHub Desktop
```
Later updates: edit, run `python3 build_site.py`, then `git add . && git commit -m "Update panel" && git push`.
(GitHub Desktop - desktop.github.com - does the same with buttons.)

**C. Your own address (optional, paid)**: buy a domain, then Pages -> Custom domain. Not needed.

Rules: Pages is free for public repositories; do not put passwords, phone numbers of private people or database dumps in it.
Never upload your MySQL password or `.sql` files with unverified personal data.

## Get people to find it
- **Google Search Console** (search.google.com/search-console): add your URL, verify, submit `sitemap.xml`. Do the same on **Bing Webmaster Tools**.
- Use plain words people search: "free lawyer Bhiwani", "DLSA Bhiwani", "मुफ़्त वकील भिवानी". They are already in the page title and text.
- **Ask for links**: DLSA Bhiwani / HSLSA, District Bar Association, Bhiwani NGOs, Panchayats, CSC (Common Service Centre) operators, libraries, colleges' law departments.
- **Offline**: print a one-page poster with a QR code (any free QR generator) for the court complex, CSCs, panchayat offices, bus stands.
- **WhatsApp**: share the link in local groups; the page works on small phones.
- Update monthly: re-check the panel page `haryana.nalsa.gov.in/?p=8599`, edit `build_site.py`, rebuild, re-upload.

## Later (optional)
- Add every panel advocate (all 1,573) marked as Paid / Pro-Bono / Ex-Servicemen, since all are free to the citizen.
- Add a Hindi toggle and a page per district.
- Keep your MySQL database private. Only the exported CSV/HTML goes online.
