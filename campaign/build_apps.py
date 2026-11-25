"""Email 1 (apps version): the customer app and installer app, dressed in the prospect's own logo.
Usage: python3 campaign/build_apps.py            -> rebuilds campaign/emails/*.html and the subjects in queue.csv
       python3 campaign/build_apps.py --one <address> <out.html>
Business details come from campaign/contacts.csv (business, first, to, site, logo, link)."""
import csv, html, os, re, sys
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
A = "https://officeflow.measureflow.com.au/email"
INK, PAPER, ORANGE, LINE, MUTED = "#0A0A0A", "#FAF8F4", "#C1683A", "#E6E0D6", "#6B6B6B"
HEAD = "'Poppins','Helvetica Neue',Arial,sans-serif"
BODY = "'Inter','Helvetica Neue',Arial,sans-serif"
PHONE, REPLY, POST = "0412 706 791", "accounts@measureflow.com.au", "PO Box 59, Beechwood NSW 2446"
SITE = "https://officeflow.measureflow.com.au"
DEMO = SITE + "/ecosystem/"  # the 2-minute demo: website chat, reception books it, the designer's phone, the job


def esc(s): return html.escape(s or "", quote=True)
def poss(b): return b + ("'" if b.endswith("s") else "'s")


def subject(biz, first):
    return (f"{first}, your customers could have the {biz} app on their phone" if first
            else f"Your customers could have the {biz} app on their phone")


def logo_src(u):
    """Their logo through the site's image service (resized, PNG for Outlook). White logos vanish on white."""
    # A white logo vanishes on the white badge ("White-BG" is a white background, so that one is fine).
    if not u or re.search(r"white(?![-_ +]?bg)|[-_]light[-_.]", u, re.I): return ""
    if re.search(r"\.svg(\?|$)", u, re.I): return u
    return "https://officeflow.measureflow.com.au/.netlify/images?url=" + quote(u, safe="") + "&h=68&fm=png"


def icon_src(u, site="", logo=""):
    """Their app icon, picked by eye for each business (contacts.csv "icon"):
    "fav" = their website's own icon; "left" / "center" = that part of their logo cut out square (e.g. the emblem at
    the left of a wide logo); a URL = that picture; empty = their whole logo fitted into the square."""
    fit = "contain"
    if u == "fav":
        u = "https://www.google.com/s2/favicons?domain=" + site + "&sz=128"
    elif u in ("left", "center", "right"):
        fit, u = "cover&position=" + u, logo
    elif not u:
        u = logo
    if not u or re.search(r"white(?![-_ +]?bg)|[-_]light[-_.]", u, re.I): return ""
    return "https://officeflow.measureflow.com.au/.netlify/images?url=" + quote(u, safe="") + "&w=96&h=96&fit=" + fit + "&fm=png"


ICON = {}


def short(biz):
    """The name under their icon, cut short the way a phone does."""
    b = biz.replace(" & ", " ")
    return b if len(b) <= 12 else b[:11].rstrip() + "\u2026"


def homescreen(biz, logo_raw, site=""):
    """A phone home screen with their app on it, among the usual apps."""
    src = icon_src(ICON.get(biz, ""), site, logo_raw)
    def app(bg, glyph, label, fg="#FFFFFF"):
        return (f'<td align="center" valign="top" width="25%" style="padding:0 0 10px">'
                f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" align="center"><tr><td align="center" valign="middle" width="38" height="38" '
                f'style="width:38px;height:38px;background:{bg};border-radius:10px;font:400 19px/38px Arial,sans-serif;color:{fg}">{glyph}</td></tr></table>'
                f'<div style="font:400 8.5px/1.3 {BODY};color:#FFFFFF;padding-top:3px">{label}</div></td>')
    # Same size and corners as the other apps. A picked icon fills the whole tile, like a real app icon;
    # a whole wide logo sits centred on white; no logo shows their initials.
    tile = f'width:38px;height:38px;background:#FFFFFF;border-radius:10px'
    if src and ICON.get(biz):
        cell = (f'<td align="center" valign="middle" width="38" height="38" style="{tile}">'
                f'<img src="{esc(src)}" width="38" height="38" alt="{esc(biz)}" style="display:block;width:38px;height:38px;border:0;border-radius:10px;background:#FFFFFF"></td>')
    elif src:
        cell = (f'<td align="center" valign="middle" width="38" height="38" style="{tile.replace('#FFFFFF', lbg(biz, src))}">'
                f'<img src="{esc(src)}" width="34" alt="{esc(biz)}" style="display:block;width:34px;height:auto;max-height:34px;border:0;margin:0 auto"></td>')
    else:
        ini = "".join(x[0] for x in re.sub(r"[^A-Za-z ]", "", WORDMARK.get(biz) or biz).split()[:2]).upper()
        cell = f'<td align="center" valign="middle" width="38" height="38" style="{tile};font:700 15px/38px {HEAD};color:{INK}">{esc(ini)}</td>'
    theirs = (f'<td align="center" valign="top" width="25%" style="padding:0 0 10px">'
              f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" align="center"><tr>{cell}</tr></table>'
              f'<div style="font:700 8.5px/1.3 {BODY};color:#FFFFFF;padding-top:3px;white-space:nowrap">{esc(short(biz))}</div></td>')
    row = lambda *c: "<tr>" + "".join(c) + "</tr>"
    grid = ('<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">'
            + row(app("#34C759", "&#9990;", "Phone"), app("#34C759", "&#9993;", "Messages"), app("#FFFFFF", "&#128197;", "Calendar", INK), app("#8E8E93", "&#128247;", "Camera"))
            + row(app("#2F80ED", "&#9729;", "Weather"), theirs, app("#43A047", "&#128205;", "Maps"), app("#FFCC00", "&#9998;", "Notes", INK))
            + row(app("#1E88E5", "&#64;", "Mail"), app("#FFFFFF", "&#10047;", "Photos", "#E91E63"), app("#222222", "&#9200;", "Clock"), app("#8E8E93", "&#9881;", "Settings"))
            + '</table>')
    return (f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" align="center" style="background:{INK};border-radius:30px;width:206px">'
            f'<tr><td style="padding:9px"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#2E3B48;border-radius:23px">'
            f'<tr><td style="padding:6px 14px 0;font:600 9px/16px {BODY};color:#FFFFFF">9:41</td></tr>'
            f'<tr><td style="padding:14px 6px 14px">{grid}</td></tr></table></td></tr></table>')


def head_icon(biz, logo_raw, site, size=34):
    """Their icon (just the mark), inline after their name in the headline. Only when a proper icon was picked:
    a whole wide logo would be too small to read here, so then the headline has none."""
    src = icon_src(ICON.get(biz, ""), site, logo_raw) if ICON.get(biz) else ""
    if not src: return ""
    # A plain inline picture: every mail app keeps it on the same line as the words (Outlook drops inline tables).
    return (f'<img src="{esc(src)}" width="{size}" height="{size}" alt="" style="display:inline-block;vertical-align:middle;'
            f'width:{size}px;height:{size}px;border:0;border-radius:{size//4}px;background:#FFFFFF;margin:0 6px 6px 2px">')


def protect(html):
    """Outlook.com and the new Outlook turn the email's colours around in dark mode (black becomes pale grey, white
    becomes dark), which hides white logos and greys out the phones. They mark every colour they change with
    data-ogsc / data-ogsb, so a class per colour puts the real colours back."""
    used_b, used_c = set(), set()
    def tag(m):
        t = m.group(0)
        st = re.search(r'style="([^"]*)"', t)
        if not st: return t
        cls = []
        for h in re.findall(r'background(?:-color)?:\s*#([0-9A-Fa-f]{6})', st.group(1)) + re.findall(r'bgcolor="#([0-9A-Fa-f]{6})"', t):
            used_b.add(h.upper()); cls.append("b" + h.upper())
        for h in re.findall(r'(?<![-\w])color:\s*#([0-9A-Fa-f]{6})', st.group(1)):
            used_c.add(h.upper()); cls.append("c" + h.upper())
        if not cls: return t
        if ' class="' in t: return t.replace(' class="', ' class="' + " ".join(cls) + " ", 1)
        return t.replace(" style=", f' class="{" ".join(cls)}" style=', 1)
    html = re.sub(r"<(?:td|div|span|table|a|b|p|img)\b[^>]*>", tag, html)
    css = "".join(f"[data-ogsb] .b{h},.b{h}[data-ogsb]{{background-color:#{h}!important}}" for h in sorted(used_b))
    css += "".join(f"[data-ogsc] .c{h},.c{h}[data-ogsc]{{color:#{h}!important}}" for h in sorted(used_c))
    return html.replace("</style></head>", " " + css + "\n</style></head>", 1)


def art(kind, biz, logo_raw, site, w, h, alt):
    """A picture from /email-art (web/netlify/edge-functions/email-art.tsx) drawn with their logo, so dark mode and
    Outlook can't change it."""
    q = {"k": kind, "n": biz}
    if logo_src(logo_raw) or (logo_raw and biz in DARK): q["l"] = logo_raw
    if biz in DARK: q["dk"] = "1"
    if WORDMARK.get(biz): q["w"] = WORDMARK[biz]
    ic = icon_src(ICON.get(biz, ""), site, logo_raw)
    if kind == "home" and ic: q["i"] = ic
    u = "https://officeflow.measureflow.com.au/email-art?" + "&".join(f"{k}={quote(v, safe='')}" for k, v in q.items())
    return (f'<img src="{esc(u)}" width="{w}" height="{h}" alt="{esc(alt)}" '
            f'style="display:block;width:{w}px;max-width:100%;height:auto;border:0;margin:0 auto">')


# Logos that are white or very light (made for a dark website header) sit on black, not white (contacts.csv logo_bg).
DARK = set()


def lbg(biz, logo):
    return "#0A0A0A" if logo and biz in DARK else "#FFFFFF"


# No usable logo: their name as their website writes it (contacts.csv "wordmark", e.g. "BRAESIDE JOINERY").
WORDMARK = {}


def logo_or_name(logo, biz, h, size=13, color=INK):
    if logo:
        return f'<img src="{esc(logo)}" alt="{esc(biz)}" height="{h}" style="display:block;height:{h}px;width:auto;max-width:170px;border:0;margin:0 auto">'
    return f'<span style="font:700 {size}px/1.2 {HEAD};color:{color}">{esc(WORDMARK.get(biz) or biz)}</span>'


def row(l, r, rc="#2A2A2A"):
    return (f'<tr><td style="font:400 11px/1.5 {BODY};color:#2A2A2A;padding:2px 0">{l}</td>'
            f'<td align="right" style="font:600 11px/1.5 {BODY};color:{rc};padding:2px 0;white-space:nowrap">{r}</td></tr>')


def card(title, inner):
    return (f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#FFFFFF;border:1px solid {LINE};border-radius:10px;margin:0 0 7px">'
            f'<tr><td style="padding:8px 10px"><div style="font:700 11.5px/1.3 {BODY};color:{INK};padding-bottom:3px">{title}</div>{inner}</td></tr></table>')


def pills(*names):
    return "".join(f'<span style="display:inline-block;background:#F4E6DC;color:#8A4524;border-radius:999px;padding:1px 7px;font:600 10px/1.6 {BODY};margin:2px 3px 0 0">{n}</span>' for n in names)


def phone(logo, biz, screen):
    return (f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" align="center" style="background:{INK};border-radius:34px;width:236px">'
            f'<tr><td style="padding:10px">'
            f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#F4F1EC;border-radius:26px">'
            f'<tr><td align="center" style="padding:6px 0 0;background:{lbg(biz, logo)}"><div style="width:70px;height:16px;background:{INK};border-radius:0 0 10px 10px;margin:0 auto"></div></td></tr>'
            f'<tr><td align="center" style="background:{lbg(biz, logo)};padding:10px 12px 9px;border-bottom:1px solid {LINE}">{logo_or_name(logo, biz, 26)}</td></tr>'
            f'<tr><td style="padding:10px 10px 12px">{screen}</td></tr></table></td></tr></table>')


def build(biz, first, email, site, logo, link):
    logo_raw, logo = logo, logo_src(logo)
    site = re.sub(r"^https?://(www\.)?", "", site or "").rstrip("/")
    _i = icon_src(ICON.get(biz, ""), site, logo_raw) if ICON.get(biz) else ""
    if _i and "&i=" not in link: link += "&i=" + quote(_i, safe="")
    book = ("mailto:" + REPLY + "?subject=" + quote(f"Show me \u2013 {biz}") + "&body="
            + quote(f"Hi Paul,\n\nI'd like a 20-minute walkthrough of AI Office Flow for {biz}.\n\nBest days and times for me:\n\nPhone:\n"))
    site = re.sub(r"^https?://(www\.)?", "", site or "").rstrip("/")
    hi = f"Hi {esc(first)}," if first else f"Hi {esc(biz)} team,"
    pre = "Keep your customers and trades in the loop, with your logo on every screen."
    t = lambda s: f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">{s}</table>'
    cust = (f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#FFFFFF;border-radius:12px;margin:0 0 9px;box-shadow:0 4px 12px rgba(0,0,0,.12)">'
            f'<tr><td style="padding:8px 10px;font:400 11px/1.4 {BODY};color:{INK}"><b style="font-size:11.5px">{esc(biz)}</b> <span style="color:{MUTED}">now</span><br>'
            f'Your install starts Monday at 7am. Dave and Ben will be there.</td></tr></table>'
            f'<div style="font:700 15px/1.2 {HEAD};color:{INK}">Sarah&#8217;s job folder</div>'
            f'<div style="font:400 10.5px/1.6 {BODY};color:{MUTED};padding-bottom:7px">Kitchen, 14 Ocean Street</div>'
            + card("Your documents", t(row("Contract", "&#10003; Signed", "#2F7A4A") + row("Variation: pantry", "&#10003; Signed", "#2F7A4A")))
            + card("Your drawings", pills("Plan", "Elevations", "Benchtops"))
            + card("Your job timeline", t(row("Delivery", "Fri") + row("Install, 2 days", "Mon 7am") + row("Stone template", "Wed")))
            + card("Payments", t(row("Deposit", "&#10003; Paid", "#2F7A4A") + row("Pre-install", "Due Fri", MUTED))))
    inst = (f'<div style="font:700 15px/1.2 {HEAD};color:{INK}">My jobs</div>'
            f'<div style="font:400 10.5px/1.6 {BODY};color:{MUTED};padding-bottom:7px">Dave &middot; {esc(biz)}</div>'
            + card("Sarah, 14 Ocean Street", f'<div style="font:400 10.5px/1.5 {BODY};color:{MUTED}">Mon &middot; 2 days &middot; delivered Fri</div>'
                   + pills("Drawings", "Cut list", "Trade schedule", "Customer")
                   + f'<div style="background:{INK};color:#FFFFFF;border-radius:8px;text-align:center;font:600 11px/1 {BODY};padding:8px 0;margin-top:6px">Photos and sign-off</div>')
            + card("Mark, 3 Hill Road", f'<div style="font:400 10.5px/1.5 {BODY};color:{MUTED}">Next Mon &middot; 1 day</div>' + pills("Drawings", "Trade schedule"))
            + card("Trade schedule, Ocean St", t(row("Plumber", "Wed 8am") + row("Electrician", "Wed 1pm") + row("Stone template", "Wed"))))
    bullet = lambda s: f'<tr><td valign="top" width="18" style="color:{ORANGE};font:700 14px/1.55 {BODY}">&#10003;</td><td style="font:400 14px/1.55 {BODY};color:#2A2A2A;padding-bottom:5px">{s}</td></tr>'
    col = lambda title, items: (f'<td class="c2" width="50%" valign="top" style="padding:0 6px"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#FFFFFF;border:1px solid {LINE};border-radius:12px">'
                                f'<tr><td style="padding:16px 16px 10px"><div style="font:700 16px/1.3 {HEAD};color:{INK};padding-bottom:8px">{title}</div>{t("".join(bullet(i) for i in items))}</td></tr></table></td>')
    tile = (f'<table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr><td align="center" valign="middle" width="64" height="64" '
            f'style="width:64px;height:64px;background:{lbg(biz, logo)};border:1px solid {LINE};border-radius:15px;padding:4px">{logo_or_name(logo, biz, 22, 10)}</td></tr></table>')
    return protect(f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="light only"><meta name="supported-color-schemes" content="light only">
<title>{esc(subject(biz, first))}</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Poppins:wght@600;700&display=swap" rel="stylesheet">
<style>
 body{{margin:0;padding:0;background:#EFEBE4}} a{{color:{ORANGE}}}
 @media (max-width:620px){{ .w{{width:100%!important}} .px{{padding-left:20px!important;padding-right:20px!important}}
   .h1{{font-size:27px!important}} .br{{display:block!important;width:100%!important}}
   .lg{{display:block!important;width:100%!important;text-align:left!important;padding-top:16px!important}} .lg table{{margin:0!important}}
   .ph{{display:block!important;width:100%!important;padding:0 0 22px!important}} .c2{{display:block!important;width:100%!important;padding:0 0 12px!important}} }}
</style></head>
<body style="margin:0;padding:0;background:#EFEBE4">
<div style="display:none;max-height:0;overflow:hidden;opacity:0;color:#EFEBE4">{pre}&#8199;&#65279;&#847;&#8199;&#65279;&#847;&#8199;&#65279;&#847;</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#EFEBE4"><tr><td align="center" style="padding:28px 12px">
<table role="presentation" class="w" width="600" cellpadding="0" cellspacing="0" border="0" style="width:600px;background:{PAPER};border-radius:16px;overflow:hidden">

<tr><td class="px" style="background:{INK};padding:20px 32px">
 <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
  <td class="br" style="padding:0"><table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr>
   <td width="42" style="width:42px;min-width:42px;padding-right:10px"><img src="{A}/aof-icon.png" width="32" height="32" alt="AI Office Flow" style="display:block;border:0;border-radius:7px"></td>
   <td style="font:700 17px/1 {HEAD};color:#FFFFFF;white-space:nowrap">AI Office <span style="color:{ORANGE}">Flow</span></td></tr></table></td>
  <td class="lg" align="right" style="padding:0"><table role="presentation" cellpadding="0" cellspacing="0" border="0" align="right"><tr>
   <td style="padding:0">{art("badge", biz, logo_raw, site, 200, 52, biz)}</td></tr></table></td>
 </tr></table></td></tr>

<tr><td class="px" style="background:{INK};padding:18px 32px 34px">
 <div style="font:600 11px/1 {BODY};letter-spacing:2.2px;color:{ORANGE};text-transform:uppercase">Prepared for {esc(biz)}</div>
 <div class="h1" style="font:700 31px/1.15 {HEAD};color:#FFFFFF;padding-top:12px">Keep your customers and trades in the loop, with <span style="color:{ORANGE}">{esc(biz)}</span> {head_icon(biz, logo_raw, site)} on every screen</div>
 <div style="font:400 15px/1.6 {BODY};color:#CFCAC2;padding-top:14px">Your customers get their own app. So do your installers. Both carry your logo, and so does every email and text the system sends.</div>
</td></tr>

<tr><td class="px" style="padding:30px 32px 28px;font:400 16px/1.65 {BODY};color:#2A2A2A">
 <p style="margin:0 0 16px">{hi}</p>
 <p style="margin:0 0 16px">I&#8217;m Paul Snelling. I ran a kitchen business for over 25 years.</p>
 <p style="margin:0 0 16px">The calls that ate my day weren&#8217;t new enquiries. They were customers asking &#8220;where are we up to?&#8221;, and installers ringing for a drawing or a measurement from site.</p>
 <p style="margin:0">So I built AI Office Flow: one system that runs the office side of a kitchen business, from the first enquiry to handover. The two apps are the part your customers and trades see, and they carry your name, not mine.</p>
</td></tr>

<tr><td class="px" style="background:#F1ECE4;padding:30px 26px 10px">
 <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
  <td class="ph" width="50%" valign="top" align="center" style="padding:0 6px">
   <div style="font:700 15px/1.3 {HEAD};color:{INK};padding-bottom:3px">The customer app</div>
   <div style="font:400 12px/1.4 {BODY};color:{MUTED};padding-bottom:12px">On your customer&#8217;s phone</div>
   <a href="{esc(link)}" style="text-decoration:none">{art("cust", biz, logo_raw, site, 236, 494, "The " + biz + " customer app")}</a></td>
  <td class="ph" width="50%" valign="top" align="center" style="padding:0 6px">
   <div style="font:700 15px/1.3 {HEAD};color:{INK};padding-bottom:3px">The installer app</div>
   <div style="font:400 12px/1.4 {BODY};color:{MUTED};padding-bottom:12px">On your installers&#8217; and trades&#8217; phones</div>
   <a href="{esc(link)}" style="text-decoration:none">{art("inst", biz, logo_raw, site, 236, 494, "The " + biz + " installer app")}</a></td>
 </tr></table>
 <div style="font:400 12px/1.5 {BODY};color:{MUTED};text-align:center;padding:14px 0 18px">Made-up jobs, shown with the {esc(biz)} logo.</div>
</td></tr>

<tr><td class="px" style="padding:22px 26px 6px">
 <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
  {col("Your customers get", ["Their quote to view and sign online", "Drawings and variations, always the latest", "Payments, invoices and what&#8217;s due", "Install dates and who&#8217;s coming", "A note on their phone when anything changes"])}
  {col("Your installers get", ["Every job they&#8217;re on, nearest first", "Drawings, cut list and trade schedule on site", "Customer details and access notes", "Photos and sign-off from the job", "Dates that move when you move them"])}
 </tr></table></td></tr>

<tr><td class="px" style="padding:26px 32px 4px">
 <div style="font:600 11px/1 {BODY};letter-spacing:2.2px;color:{ORANGE};text-transform:uppercase;padding-bottom:10px">Behind the apps</div>
 <div style="font:700 20px/1.3 {HEAD};color:{INK};padding-bottom:12px">One system for the whole job</div>
 <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
  <td class="c2" width="50%" valign="top" style="padding:0 8px 0 0">{t("".join(bullet(i) for i in ["Website chat that answers enquiries at 9pm and books measures", "Every call, chat and enquiry becomes a numbered job", "Quotes from your own forms, signed online", "Follow-ups that go out by themselves"]))}</td>
  <td class="c2" width="50%" valign="top" style="padding:0 0 0 8px">{t("".join(bullet(i) for i in ["Designer diary and installs in Google Calendar", "Factory and site packs: drawings, cut lists, trade schedules", "Deposits and invoices straight into Xero", "Every job&#8217;s profit at a glance"]))}</td>
 </tr></table></td></tr>

<tr><td class="px" style="padding:18px 32px 4px">
 <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#FFFFFF;border:1px solid {LINE};border-radius:12px"><tr>
  <td class="c2" width="236" align="center" valign="middle" style="padding:18px 6px 18px 18px">{art("home", biz, logo_raw, site, 206, 252, "The " + biz + " app on a phone home screen")}</td>
  <td class="c2" valign="middle" style="padding:0"><div style="padding:18px 20px;font:400 15px/1.6 {BODY};color:#2A2A2A"><div style="font:700 18px/1.3 {HEAD};color:{INK};padding-bottom:8px">Your app on their phone</div>Customers and installers add the {esc(biz)} app with one tap, and your icon sits on their home screen with everything else they use. It opens straight to their job, with no logins or passwords.</div></td>
 </tr></table></td></tr>

<tr><td class="px" align="center" style="padding:32px 32px 8px">
 <table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr><td align="center" bgcolor="{ORANGE}" style="border-radius:10px">
  <a href="{esc(book)}" style="display:inline-block;padding:16px 28px;font:700 16px/1 {HEAD};color:#FFFFFF;text-decoration:none;border-radius:10px">Book my 20-minute walkthrough &rarr;</a>
 </td></tr></table>
 <div style="font:400 15px/1.6 {BODY};color:#2A2A2A;padding-top:14px">I&#8217;ll show you the system set up for {esc(biz)}: your logo, your forms, your process. No obligation.</div>
 <div style="font:400 14px/1.6 {BODY};color:{MUTED};padding-top:6px">Or just reply &#8220;show me&#8221;. Prefer to look first? <a href="{esc(link)}" style="color:{ORANGE}">See the {esc(biz)} apps</a> &middot; <a href="{DEMO}" style="color:{ORANGE}">Watch the demo</a></div>
</td></tr>

<tr><td class="px" style="padding:24px 32px 30px;font:400 16px/1.65 {BODY};color:#2A2A2A">
 <table role="presentation" cellpadding="0" cellspacing="0" border="0" style="border-top:1px solid {LINE};width:100%"><tr><td style="padding-top:18px">
  <div style="font:700 16px/1.3 {HEAD};color:{INK}">Paul Snelling</div>
  <div style="font:400 14px/1.6 {BODY};color:{MUTED}">Founder, AI Office Flow<br>
   <span style="color:{INK}">{PHONE}</span> &middot; <a href="mailto:{REPLY}" style="color:{ORANGE};text-decoration:none">{REPLY}</a><br>
   <a href="{SITE}" style="color:{ORANGE};text-decoration:none">officeflow.measureflow.com.au</a> &middot; <a href="{DEMO}" style="color:{ORANGE};text-decoration:none">See the demo</a></div>
 </td></tr></table>
</td></tr>

<tr><td class="px" style="background:{INK};padding:22px 32px;font:400 12px/1.6 {BODY};color:#9A958D">
 <span style="color:#FFFFFF;font-weight:600">MeasureFlow &middot; AI Office Flow</span> &middot; {POST}<br>
 I&#8217;m writing because {esc(email)} is publicly listed for {esc(biz)} business enquiries.
 Not for you? <a href="mailto:{REPLY}?subject=Unsubscribe%20{esc(email)}" style="color:{ORANGE}">Unsubscribe</a> or reply &#8220;no thanks&#8221; and I won&#8217;t email again.
</td></tr>
</table></td></tr></table></body></html>""")


def follow_subject(biz):
    return f"Following up: the {biz} apps"


def build_follow(biz, first, email, site, logo, link):
    """Email 2: a short follow-up 3 working days after Email 1, in the same look."""
    logo_raw, logo = logo, logo_src(logo)
    site = re.sub(r"^https?://(www\.)?", "", site or "").rstrip("/")
    _i = icon_src(ICON.get(biz, ""), site, logo_raw) if ICON.get(biz) else ""
    if _i and "&i=" not in link: link += "&i=" + quote(_i, safe="")
    book = ("mailto:" + REPLY + "?subject=" + quote(f"Show me \u2013 {biz}") + "&body="
            + quote(f"Hi Paul,\n\nI'd like a 20-minute walkthrough of AI Office Flow for {biz}.\n\nBest days and times for me:\n\nPhone:\n"))
    nope = ("mailto:" + REPLY + "?subject=" + quote(f"No thanks \u2013 {biz}") + "&body="
            + quote(f"Thanks Paul, not for us right now. Please take {email} off your list.\n"))
    site = re.sub(r"^https?://(www\.)?", "", site or "").rstrip("/")
    hi = f"Hi {esc(first)}," if first else f"Hi {esc(biz)} team,"
    pre = f"A quick follow-up, with the {biz} apps ready to look at."
    tile = (f'<table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr><td align="center" valign="middle" width="64" height="64" '
            f'style="width:64px;height:64px;background:{lbg(biz, logo)};border:1px solid {LINE};border-radius:15px;padding:4px">{logo_or_name(logo, biz, 22, 10)}</td></tr></table>')
    return protect(f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="light only"><meta name="supported-color-schemes" content="light only">
<title>{esc(follow_subject(biz))}</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Poppins:wght@600;700&display=swap" rel="stylesheet">
<style>
 body{{margin:0;padding:0;background:#EFEBE4}} a{{color:{ORANGE}}}
 @media (max-width:620px){{ .w{{width:100%!important}} .px{{padding-left:20px!important;padding-right:20px!important}}
   .h1{{font-size:25px!important}} .br{{display:block!important;width:100%!important}}
   .lg{{display:block!important;width:100%!important;text-align:left!important;padding-top:16px!important}} .lg table{{margin:0!important}} }}
</style></head>
<body style="margin:0;padding:0;background:#EFEBE4">
<div style="display:none;max-height:0;overflow:hidden;opacity:0;color:#EFEBE4">{esc(pre)}&#8199;&#65279;&#847;&#8199;&#65279;&#847;&#8199;&#65279;&#847;</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#EFEBE4"><tr><td align="center" style="padding:28px 12px">
<table role="presentation" class="w" width="600" cellpadding="0" cellspacing="0" border="0" style="width:600px;background:{PAPER};border-radius:16px;overflow:hidden">

<tr><td class="px" style="background:{INK};padding:20px 32px">
 <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
  <td class="br" style="padding:0"><table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr>
   <td width="42" style="width:42px;min-width:42px;padding-right:10px"><img src="{A}/aof-icon.png" width="32" height="32" alt="AI Office Flow" style="display:block;border:0;border-radius:7px"></td>
   <td style="font:700 17px/1 {HEAD};color:#FFFFFF;white-space:nowrap">AI Office <span style="color:{ORANGE}">Flow</span></td></tr></table></td>
  <td class="lg" align="right" style="padding:0"><table role="presentation" cellpadding="0" cellspacing="0" border="0" align="right"><tr>
   <td style="padding:0">{art("badge", biz, logo_raw, site, 200, 52, biz)}</td></tr></table></td>
 </tr></table></td></tr>

<tr><td class="px" style="background:{INK};padding:18px 32px 30px">
 <div style="font:600 11px/1 {BODY};letter-spacing:2.2px;color:{ORANGE};text-transform:uppercase">Following up for {esc(biz)}</div>
 <div class="h1" style="font:700 28px/1.18 {HEAD};color:#FFFFFF;padding-top:12px">Your apps are ready to look at, with <span style="color:{ORANGE}">{esc(biz)}</span> {head_icon(biz, logo_raw, site)} on every screen</div>
</td></tr>

<tr><td class="px" style="padding:30px 32px 6px;font:400 16px/1.65 {BODY};color:#2A2A2A">
 <p style="margin:0 0 16px">{hi}</p>
 <p style="margin:0 0 16px">Just following up in case my last email got buried.</p>
 <p style="margin:0">I set up a preview of the customer and installer apps with the {esc(biz)} logo on them. It takes two minutes to look.</p>
</td></tr>

<tr><td class="px" style="padding:20px 32px 4px">
 <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#FFFFFF;border:1px solid {LINE};border-radius:12px"><tr>
  <td width="88" align="center" valign="middle" style="padding:16px 0 16px 16px">{tile}</td>
  <td valign="middle" style="padding:16px;font:400 14px/1.55 {BODY};color:#2A2A2A"><b style="color:{INK}">Your customers and trades, kept in the loop.</b> Quotes, drawings, payments and install dates on your customers&#8217; phones. Jobs, drawings and trade schedules on your installers&#8217;. All with your logo.<br>
   <a href="{esc(link)}" style="color:{ORANGE};font-weight:600;text-decoration:none">See the {esc(biz)} apps &rarr;</a></td>
 </tr></table></td></tr>

<tr><td class="px" align="center" style="padding:30px 32px 8px">
 <table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr><td align="center" bgcolor="{ORANGE}" style="border-radius:10px">
  <a href="{esc(book)}" style="display:inline-block;padding:16px 28px;font:700 16px/1 {HEAD};color:#FFFFFF;text-decoration:none;border-radius:10px">Book my 20-minute walkthrough &rarr;</a>
 </td></tr></table>
 <div style="font:400 15px/1.6 {BODY};color:#2A2A2A;padding-top:14px">If it&#8217;s worth 20 minutes, I&#8217;ll walk you through the whole system, set up for {esc(biz)}.</div>
 <table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin-top:18px"><tr><td align="center" style="border:1px solid #CFC8BD;border-radius:10px">
  <a href="{esc(nope)}" style="display:inline-block;padding:11px 22px;font:600 14px/1 {BODY};color:{MUTED};text-decoration:none;border-radius:10px">Not for us right now</a>
 </td></tr></table>
 <div style="font:400 13px/1.6 {BODY};color:{MUTED};padding-top:8px">Tap it and I won&#8217;t email again. This is my last email either way.</div>
</td></tr>

<tr><td class="px" style="padding:24px 32px 30px">
 <table role="presentation" cellpadding="0" cellspacing="0" border="0" style="border-top:1px solid {LINE};width:100%"><tr><td style="padding-top:18px">
  <div style="font:700 16px/1.3 {HEAD};color:{INK}">Paul Snelling</div>
  <div style="font:400 14px/1.6 {BODY};color:{MUTED}">Founder, AI Office Flow<br>
   <span style="color:{INK}">{PHONE}</span> &middot; <a href="mailto:{REPLY}" style="color:{ORANGE};text-decoration:none">{REPLY}</a><br>
   <a href="{SITE}" style="color:{ORANGE};text-decoration:none">officeflow.measureflow.com.au</a> &middot; <a href="{DEMO}" style="color:{ORANGE};text-decoration:none">See the demo</a></div>
 </td></tr></table>
</td></tr>

<tr><td class="px" style="background:{INK};padding:22px 32px;font:400 12px/1.6 {BODY};color:#9A958D">
 <span style="color:#FFFFFF;font-weight:600">MeasureFlow &middot; AI Office Flow</span> &middot; {POST}<br>
 I&#8217;m writing because {esc(email)} is publicly listed for {esc(biz)} business enquiries.
 Not for you? <a href="mailto:{REPLY}?subject=Unsubscribe%20{esc(email)}" style="color:{ORANGE}">Unsubscribe</a> or reply &#8220;no thanks&#8221;.
</td></tr>
</table></td></tr></table></body></html>""")


def slug(s): return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


if __name__ == "__main__":
    people = {r["to"].lower(): r for r in csv.DictReader(open(os.path.join(HERE, "contacts.csv")))}
    # Greet the person the address belongs to (Paul, 26 Nov 2026): if there's no first name but the address is a
    # person's (e.g. alex@) and that name matches an owner found by the List builder, use it.
    DET = os.path.join(HERE, "details.csv")
    det = {r["to"].lower(): r for r in csv.DictReader(open(DET))} if os.path.exists(DET) else {}
    for a, r in people.items():
        if r["first"]: continue
        local = a.split("@")[0]
        names = re.findall(r"[A-Za-z]+", (det.get(a, {}).get("owner_first") or ""))
        hit = [x for x in names if x.lower() == local]
        if hit: r["first"] = hit[0].capitalize()
    WORDMARK.update({r["business"]: r.get("wordmark", "") for r in people.values() if r.get("wordmark")})
    DARK.update({r["business"] for r in people.values() if r.get("logo_bg") == "dark"})
    ICON.update({r["business"]: r.get("icon", "") for r in people.values() if r.get("icon")})
    if len(sys.argv) > 2 and sys.argv[1] == "--follow":
        r = people[sys.argv[2].lower()]
        open(sys.argv[3], "w").write(build_follow(r["business"], r["first"], r["to"], r["site"], r["logo"], r["link"]))
        print(follow_subject(r["business"])); sys.exit()
    if len(sys.argv) > 2 and sys.argv[1] == "--one":
        r = people[sys.argv[2].lower()]
        open(sys.argv[3], "w").write(build(r["business"], r["first"], r["to"], r["site"], r["logo"], r["link"]))
        print(subject(r["business"], r["first"])); sys.exit()
    Q = os.path.join(HERE, "queue.csv"); rows = list(csv.DictReader(open(Q))); fields = list(rows[0].keys()); n = 0
    for q in rows:
        r = people.get(q["to"].lower())
        if not r or q["status"] != "queued": continue
        open(os.path.join(HERE, "emails", q["html_file"]), "w").write(build(r["business"], r["first"], r["to"], r["site"], r["logo"], r["link"]))
        q["subject"] = subject(r["business"], r["first"]); n += 1
    with open(Q, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
    print("rebuilt", n)
