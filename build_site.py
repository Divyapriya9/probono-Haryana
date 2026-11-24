"""
build_site.py  -  turns the panel data below into index.html (+ sitemap, robots, CSV).
Run:  python3 build_site.py
Edit the CONFIG block, re-run, then upload the folder (see HOW_TO_PUBLISH.md).

DATA: rows with basis "Pro-Bono Basis" from the official document
"Panel of Advocates of Haryana (SLSA, DLSAs, SDLSCs)-2026"
https://cdnbbsr.s3waas.gov.in/s3e8ec28c8ef3e3c68482eef793edf3e50/uploads/2026/08/202608062084035475.pdf
It was copied by an AI reader, NOT by a person: spot-check every row against the PDF before you publish.
"""
import csv, json, os

# ============================ CONFIG ========================================
SITE_URL     = "https://divyapriya9.github.io/haryana-free-legal-aid/"   # <- change after you publish
CONTACT_TEXT = "Report a mistake or ask for a name to be removed:"
CONTACT_LINK = "https://github.com/divyapriya9/haryana-free-legal-aid/issues"  # or "mailto:you@example.com"
CONTACT_LABEL= "open an issue / write to the site owner"
# Be truthful here. Suggested wording; put YOUR real name and only claim the checking you actually did.
AUTHOR_LINE  = ("Compiled by Divyapriya with AI assistance (Claude, by Anthropic). The AI read the official PDF and wrote the "
                "code; the volunteer chose the project, directed the work and checked the entries against the PDF on DATE.")
# ============================================================================

# unit (as printed in the PDF), parent district (my mapping, verify), name, gender, enrolled on panel, years
R = [
("Ambala","Ambala","Nitesh Sahni","M","01.04.2025",29),("Ambala","Ambala","Renu Bala","F","01.04.2025",39),
("Naraingarh","Ambala","Devinder Singh","M","23.03.2026",27),
("Bhiwani","Bhiwani","Baljeet","M","17.07.2025",16),("Bhiwani","Bhiwani","Kuldeep Sharma","M","17.07.2025",16),
("Bhiwani","Bhiwani","Naveen Kumar","M","17.07.2025",18),("Bhiwani","Bhiwani","Pardeep Kumar Vashista","M","17.07.2025",18),
("Bhiwani","Bhiwani","Sunil Atri","M","17.07.2025",14),
("Tosham","Bhiwani","Pawan","M","25.03.2026",18),("Tosham","Bhiwani","Rishi Pal","M","25.03.2026",7),
("Tosham","Bhiwani","Sanjay Kumar","M","25.03.2026",16),("Tosham","Bhiwani","Suresh Kumar","M","25.03.2026",19),
("Ratia","Fatehabad","Ram Chand","M","21.04.2026",11),("Ratia","Fatehabad","Vakeel Singh","M","21.04.2026",10),
("Tohana","Fatehabad","Anoopa Sharma","F","22.04.2026",17),
]
for n,g,y in [("Abhiranjana Sharma","F",22),("Amit Kumar Tyagi","M",21),("Atul Saubhri","M",8),("Attar Singh Sandhu","M",24),
 ("Banwari Lal Bhinwal","M",23),("Bhagwanti Sethi","F",22),("Bandana Aggarwal","F",43),("Dheeraj Grover","M",16),
 ("Gopi Nath Chauhan","M",14),("Inderjeet Yadav","M",17),("Jitender Kumar","M",19),("Kavita Rani","F",18),
 ("Kulbir Singh","M",7),("Mahavir Singh Dhariwal","M",21),("Munmun Goyal","F",13),("Naresh Chandra Gupta","M",43),
 ("Neeraj Deshwal","M",12),("Neetu Kumari","F",14),("Reenu Maheshwari","F",18),("Ram Dutt Sharma","M",14),
 ("Rohini Yadav","F",15),("Raj Bala Sharma","F",25),("Sandeep Kumar","M",19),("Seema","F",15),("Sunita","F",11),
 ("Suman Sehrawat","F",14),("Tezpal Singh Yadav","M",23),("Vijay Pal","M",23),("Virender Jain","M",6),
 ("Vijay Kumar","M",10),("Vinod Budgujar","M",24),("Vinod Kumar Kaushik","M",16),("Vinita","F",12)]:
    R.append(("Gurugram","Gurugram",n,g,"07.10.2024",y))
R += [
("Panchkula","Panchkula","Mahender Singh","M","13.04.2026",12),("Panchkula","Panchkula","Manbir Singh Rathi","M","13.04.2026",20),
("Panchkula","Panchkula","Om Parkash","M","13.04.2026",20),("Panchkula","Panchkula","Ritu S Sharma","F","13.04.2026",26),
("Panchkula","Panchkula","Sikander Bakshi","M","13.04.2026",22),("Kalka","Panchkula","Dinesh Gupta","M","31.03.2026",17),
("Kurukshetra","Kurukshetra","Mohit Goyal","M","10.01.2025",25),("Kurukshetra","Kurukshetra","Ritu Devi","F","10.01.2025",11),
("Kurukshetra","Kurukshetra","Divya","F","10.01.2025",2),("Kurukshetra","Kurukshetra","Narender Singh","M","10.01.2025",2),
("Kurukshetra","Kurukshetra","Sachin Bansal","M","10.01.2025",8),("Kurukshetra","Kurukshetra","Sushant Singh","M","10.01.2025",8),
("Rewari","Rewari","Anita Sharma","F","25.05.2023",18),("Rewari","Rewari","Jyoti Sharma","F","25.05.2023",16),
("Rewari","Rewari","Lalita Kumari","F","25.05.2023",20),("Rewari","Rewari","Naveen Jangra","M","25.05.2023",20),
("Rewari","Rewari","Sandeep Kumar","M","25.05.2023",17),
("Rohtak","Rohtak","Mukesh","F","17.02.2026",17),("Rohtak","Rohtak","Parveen Kumar Kalson","M","17.02.2026",16),
("Sonipat","Sonipat","Rajvir Singh","M","02.08.2025",21),("Sonipat","Sonipat","Naterpal","M","02.08.2025",18),
("Sonipat","Sonipat","Jagmohan Sharma","M","02.08.2025",17),("Sonipat","Sonipat","Shiv Prasad","M","02.08.2025",17),
("Sonipat","Sonipat","Sunil Dahiya","M","02.08.2025",16),("Sonipat","Sonipat","Bijender Singh Antil","M","02.08.2025",15),
("Sonipat","Sonipat","Indu","F","02.08.2025",15),("Sonipat","Sonipat","Usha Rani","F","02.08.2025",14),
("Sonipat","Sonipat","Sonu Rani","F","02.08.2025",12),("Sonipat","Sonipat","Manoj Kumar S/o Jaipal","M","02.08.2025",12),
("Sonipat","Sonipat","Kailash Chander Dalal","M","02.08.2025",12),
("Hisar","Hisar","Parveen Singh","M","02.04.2026",16),
("Karnal","Karnal","Karan Singh Chaudhary","M","08.05.2026",4),("Karnal","Karnal","Sompal Sharma","M","08.05.2026",3),
("Karnal","Karnal","Krishan","M","08.05.2026",3),("Karnal","Karnal","Suresh Kumar","M","08.05.2026",27),
("Karnal","Karnal","Babu Ram","M","08.05.2026",27),("Karnal","Karnal","Anita Singh","F","08.05.2026",None),
("Karnal","Karnal","Shyam Singh Rana","M","08.05.2026",25),("Karnal","Karnal","Sukhdev Raj Kathuria","M","08.05.2026",6),
("Bilaspur","Yamunanagar","Arun Kumar","M","28.01.2026",21),("Bilaspur","Yamunanagar","Sanjay Singh","M","28.01.2026",15),
("Bilaspur","Yamunanagar","Anil Kumar","M","28.01.2026",19),
("Indri","Karnal","Arun Kumar","M","28.01.2026",19),("Indri","Karnal","Anil Kumar","M","28.01.2026",16),
("Assandh","Karnal","Karan Singh","M","12.11.2025",15),("Assandh","Karnal","Gurpreet Singh","M","12.11.2025",16),
("Kaithal","Kaithal","Pawan Kumar","M","03.08.2025",7),("Kaithal","Kaithal","Jai Bhagwan Sharma","M","03.08.2025",12),
("Kaithal","Kaithal","Pawan Kumar Midha","M","03.08.2025",17),("Kaithal","Kaithal","Nisha Devi","F","03.08.2025",10),
("Narwana","Jind","Rajesh","M","17.02.2026",17),("Narwana","Jind","Vikram","M","17.02.2026",21),
("Safidon","Jind","Surender Kumar","M","17.02.2026",17),("Safidon","Jind","Paryash Kumar","M","17.02.2026",18),
("SLSA Haryana","State office","Ekta Thakur","F","29.05.2026",25),("SLSA Haryana","State office","Jyoti Choudhary","F","29.05.2026",28),
]
assert len(R) == 104, len(R)            # matches the total counted in the PDF extraction

def iso(d): dd, mm, yy = d.split("."); return f"{yy}-{mm}-{dd}"

# Serial numbers (Sr. No.) as printed in the PDF, so anyone can find the row. Rows of a unit are in PDF order.
SERIALS = {
    "Ambala": [30, 31], "Naraingarh": [51], "Bhiwani": list(range(74, 79)), "Tosham": [125, 128, 131, 136],
    "Ratia": [250, 260], "Tohana": [277], "Gurugram": list(range(326, 359)), "Panchkula": [1092, 1093, 1095, 1098, 1104],
    "Kalka": [1116], "Kurukshetra": list(range(794, 800)), "Rewari": list(range(1187, 1192)), "Rohtak": [1134, 1137],
    "Sonipat": list(range(1290, 1301)), "Hisar": [398], "Karnal": list(range(643, 651)), "Bilaspur": [1518, 1519, 1522],
    "Indri": [668, 669], "Assandh": [676, 681], "Kaithal": [696, 708, 710, 721], "Narwana": [592, 593],
    "Safidon": [611, 612], "SLSA Haryana": [1572, 1573],
}
_i = {}
def next_sr(unit):
    k = _i.get(unit, 0); _i[unit] = k + 1
    return SERIALS[unit][k]
rows = [dict(unit=u, district=d, name=n, gender=g, panel_since=iso(s), years=y, basis="Pro-Bono Basis", sr_no=next_sr(u))
        for u, d, n, g, s, y in R]
assert all(_i[u] == len(v) for u, v in SERIALS.items())   # every serial used exactly once
# order: Bhiwani region first, then A-Z by district, then A-Z by name.  NOT ranked by experience (see README).
rows.sort(key=lambda r: (0 if r["district"] == "Bhiwani" else 1, r["district"], r["unit"], r["name"].lower()))

here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, "panel_pro_bono_haryana.csv"), "w", newline="", encoding="utf-8-sig") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

tpl = open(os.path.join(here, "template.html"), encoding="utf-8").read()
html = (tpl.replace("__DATA__", json.dumps(rows, ensure_ascii=False))
           .replace("__SITE_URL__", SITE_URL).replace("__CONTACT_TEXT__", CONTACT_TEXT)
           .replace("__AUTHOR__", AUTHOR_LINE).replace("__CONTACT_LINK__", CONTACT_LINK).replace("__CONTACT_LABEL__", CONTACT_LABEL))
open(os.path.join(here, "index.html"), "w", encoding="utf-8").write(html)
open(os.path.join(here, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}sitemap.xml\n")
open(os.path.join(here, "sitemap.xml"), "w").write(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    f'  <url><loc>{SITE_URL}</loc><changefreq>monthly</changefreq></url>\n</urlset>\n')
print(f"OK: {len(rows)} rows -> index.html, sitemap.xml, robots.txt, panel_pro_bono_haryana.csv")
