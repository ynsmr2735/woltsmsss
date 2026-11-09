#!/usr/bin/env python3
"""content/*.html parçalarından tam sayfaları, sitemap.xml ve robots.txt üretir.

Her içerik dosyası şu satırla başlar:
<!--META {"path": "/toplu-sms-fiyatlari/", "title": "...", "description": "...", ...} -->
"""
import json, re, shutil, html
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "content"
OUT = ROOT / "site"
BASE = "https://www.woltsms.com"
TODAY = "2026-11-10"

NAV = [
    ("/", "Ana Sayfa"),
    ("/toplu-sms-fiyatlari/", "Fiyatlar"),
    ("/sms-api/", "SMS API"),
    ("/otp-sms/", "OTP SMS"),
    ("/baslikli-sms/", "Başlıklı SMS"),
    ("/blog/", "Blog"),
    ("/hakkimizda/", "Hakkımızda"),
]

ORG = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "@id": BASE + "/#organization",
    "name": "WOLTSMS",
    "url": BASE + "/",
    "sameAs": ["https://t.me/WoltSmsAdmin"],
    "contactPoint": [{
        "@type": "ContactPoint",
        "contactType": "customer support",
        "telephone": "+995558213790",
        "availableLanguage": ["Turkish"],
    }],
}

HEADER = """<header class="top"><div class="wrap">
<a class="logo" href="/">WOLT<span>SMS</span></a>
<nav class="nav" aria-label="Ana menü">{nav}</nav>
<a class="btn" href="https://www.woltsms.com/kayit">Yeni Üyelik Aç</a>
</div></header>"""

FOOTER = """<footer><div class="wrap">
<div class="cols">
<div><h4>WOLTSMS</h4>
<p>Toplu SMS, OTP SMS ve SMS API hizmeti.</p>
<p><span class="doldur">[DOLDUR: Şirket unvanı]</span><br>
<span class="doldur">[DOLDUR: Açık adres]</span><br>
Vergi dairesi / no: <span class="doldur">[DOLDUR]</span><br>
MERSİS no: <span class="doldur">[DOLDUR]</span></p></div>
<div><h4>Hizmetler</h4><ul>
<li><a href="/toplu-sms-fiyatlari/">Toplu SMS Fiyatları</a></li>
<li><a href="/sms-api/">SMS API</a></li>
<li><a href="/otp-sms/">OTP SMS</a></li>
<li><a href="/baslikli-sms/">Başlıklı SMS</a></li>
<li><a href="/blog/">Rehberler</a></li></ul></div>
<div><h4>Kurumsal</h4><ul>
<li><a href="/hakkimizda/">Hakkımızda ve İletişim</a></li>
<li><a href="/yasal/kvkk-aydinlatma-metni/">KVKK Aydınlatma Metni</a></li>
<li><a href="/yasal/kullanim-kosullari/">Kullanım Koşulları</a></li>
<li><a href="/yasal/mesafeli-satis-sozlesmesi/">Mesafeli Satış Sözleşmesi</a></li></ul></div>
<div><h4>İletişim</h4><ul>
<li><a href="https://t.me/WoltSmsAdmin" rel="noopener">Telegram: @WoltSmsAdmin</a></li>
<li><a href="https://wa.me/995558213790" rel="noopener">WhatsApp: +995 558 21 37 90</a></li>
<li>Telefon (TR): <span class="doldur">[DOLDUR]</span></li>
<li>E-posta: <span class="doldur">[DOLDUR: info@woltsms.com]</span></li></ul></div>
</div>
<p class="copy">© 2026 WOLTSMS. Tüm hakları saklıdır. · <a href="https://www.woltsms.com/login" rel="nofollow">Bayi girişi</a></p>
</div></footer>"""

PAGE = """<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{url}">
{robots}<meta property="og:type" content="{ogtype}">
<meta property="og:site_name" content="WOLTSMS">
<meta property="og:locale" content="tr_TR">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{url}">
<meta name="twitter:card" content="summary">
<link rel="stylesheet" href="/assets/style.css">
{schema}
</head>
<body>
{header}
{body}
{footer}
</body>
</html>
"""


def nav_html(path):
    out = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == path or (href == "/blog/" and path.startswith("/blog/")) else ""
        out.append(f'<a href="{href}"{cur}>{label}</a>')
    return "".join(out)


def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, indent=1) + "</script>"


def faq_schema(body):
    """<details><summary>Soru</summary><p>Cevap</p></details> bloklarından FAQPage üretir."""
    items = re.findall(r"<details>\s*<summary>(.*?)</summary>(.*?)</details>", body, re.S)
    if not items:
        return None
    strip = lambda s: html.unescape(re.sub(r"<[^>]+>", "", s)).strip()
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": strip(q),
             "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"\s+", " ", strip(a))}}
            for q, a in items
        ],
    }


def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "assets").mkdir(parents=True)
    shutil.copy(ROOT / "assets" / "style.css", OUT / "assets" / "style.css")
    if (ROOT / "OKU-BENI.md").exists():
        shutil.copy(ROOT / "OKU-BENI.md", OUT / "OKU-BENI.md")

    pages = []
    for f in sorted(SRC.glob("*.html")):
        text = f.read_text(encoding="utf-8")
        m = re.match(r"<!--META\s+(\{.*?\})\s*-->\s*", text, re.S)
        if not m:
            raise SystemExit(f"META yok: {f}")
        meta = json.loads(m.group(1))
        body = text[m.end():]
        path = meta["path"]
        url = BASE + path
        schemas = []
        if path == "/":
            schemas.append(ORG)
            schemas.append({"@context": "https://schema.org", "@type": "WebSite",
                            "@id": BASE + "/#website", "name": "WOLTSMS", "url": BASE + "/",
                            "inLanguage": "tr-TR", "publisher": {"@id": BASE + "/#organization"}})
        else:
            crumbs = [("Ana Sayfa", BASE + "/")]
            if path.startswith("/blog/") and path != "/blog/":
                crumbs.append(("Blog", BASE + "/blog/"))
            if path.startswith("/yasal/"):
                pass
            crumbs.append((meta.get("crumb", meta["h1"]), url))
            schemas.append({"@context": "https://schema.org", "@type": "BreadcrumbList",
                            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u}
                                                for i, (n, u) in enumerate(crumbs)]})
            crumb_html = " › ".join(
                [f'<a href="{u.replace(BASE, "")}">{n}</a>' for n, u in crumbs[:-1]] + [crumbs[-1][0]])
            body = body.replace("{{CRUMBS}}", f'<nav class="crumbs" aria-label="Sayfa yolu">{crumb_html}</nav>')
        if meta.get("type") == "article":
            schemas.append({"@context": "https://schema.org", "@type": "Article",
                            "headline": meta["h1"], "description": meta["description"],
                            "datePublished": meta.get("date", TODAY), "dateModified": meta.get("date", TODAY),
                            "inLanguage": "tr-TR", "mainEntityOfPage": url,
                            "author": {"@id": BASE + "/#organization"},
                            "publisher": {"@id": BASE + "/#organization"}})
        if meta.get("offers"):
            schemas.append({"@context": "https://schema.org", "@type": "Product",
                            "name": "WOLTSMS Toplu SMS Paketleri",
                            "description": "SMS başına ₺0,35 sabit fiyatlı toplu SMS paketleri.",
                            "brand": {"@type": "Brand", "name": "WOLTSMS"},
                            "offers": [{"@type": "Offer", "name": n, "price": p, "priceCurrency": "TRY",
                                        "availability": "https://schema.org/InStock", "url": BASE + "/toplu-sms-fiyatlari/"}
                                       for n, p in meta["offers"]]})
        fs = faq_schema(body)
        if fs:
            schemas.append(fs)
        robots = '<meta name="robots" content="noindex, follow">\n' if meta.get("noindex") else ""
        page = PAGE.format(
            title=html.escape(meta["title"], quote=True),
            description=html.escape(meta["description"], quote=True),
            url=url, robots=robots,
            ogtype="article" if meta.get("type") == "article" else "website",
            schema="\n".join(ld(s) for s in schemas),
            header=HEADER.format(nav=nav_html(path)),
            body=body.strip(), footer=FOOTER)
        dest = OUT / path.strip("/") / "index.html" if path != "/" else OUT / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(page, encoding="utf-8")
        pages.append((path, meta))

    # sitemap
    urls = []
    for path, meta in sorted(pages, key=lambda p: (p[0] != "/", p[0])):
        if meta.get("noindex"):
            continue
        prio = "1.0" if path == "/" else ("0.9" if meta.get("type") != "article" and not path.startswith("/yasal/") else "0.6")
        if path.startswith("/yasal/"):
            prio = "0.3"
        urls.append(f"  <url><loc>{BASE}{path}</loc><lastmod>{meta.get('date', TODAY)}</lastmod><priority>{prio}</priority></url>")
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls) + "\n</urlset>\n", encoding="utf-8")
    (OUT / "robots.txt").write_text(
        "User-agent: *\nAllow: /\nDisallow: /login\n\n"
        f"Sitemap: {BASE}/sitemap.xml\n", encoding="utf-8")
    print(f"{len(pages)} sayfa üretildi, sitemap'te {len(urls)} adres.")


if __name__ == "__main__":
    build()
