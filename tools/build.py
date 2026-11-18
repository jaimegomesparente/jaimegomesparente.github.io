#!/usr/bin/env python3
"""Build the English (/index.html) and French (/fr/index.html) pages.

    python3 tools/build.py

All the text of the site lives in TEXT below, one entry per language. Edit it
here, run the script, and commit both generated pages.
"""
import hashlib
from html import escape
from pathlib import Path
from string import Template

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://jaimegomesparente.github.io/"
GH = "https://github.com/jaimegomesparente/"


def asset(path):
    """URL with a version taken from the file's content, so browsers never keep a stale copy."""
    v = hashlib.sha1((ROOT / path).read_bytes()).hexdigest()[:8]
    return f"{path}?v={v}"


def img(name):
    """Image URL with a version taken from its content, so a new image is never hidden by a cached old one."""
    v = hashlib.sha1((ROOT / "img" / f"{name}.png").read_bytes()).hexdigest()[:8]
    return f"img/{name}.png?v={v}"

# Projects: image, repository and stack are shared; the text is per language.
PROJECTS = [
    {"id": "claylings", "repo": "the-claylings", "name": "The Claylings", "stack": "Godot 4.6 · GDScript"},
    {"id": "wooly", "repo": "wooly-caravan", "name": "Wooly Caravan", "stack": "Godot 4 · pixel art"},
    {"id": "gravity", "repo": "procedurally-generated-gravitational-simulation", "name": "Gravitational Sim", "stack": "Godot 4.6 · physics"},
    {"id": "facemask", "repo": "face-mask", "name": "Face Masker", "stack": "Python · ONNX · Streamlit"},
]
COURSES = ["nf18", "mi01", "sy02", "sy08"]

TEXT = {
    "en": {
        "path": "index.html",
        "title": "Jaime Gomes-Parente — Portfolio",
        "description": "Computer science engineering student at UTC, specialising in embedded and autonomous systems. Simulations, games and tools.",
        "og": "Simulations, games and tools. Engineering student at UTC, looking for an internship from September 2027.",
        "locale": "en_GB",
        "skip": "Skip to projects",
        "nav": ["Projects", "Courses", "Contact"],
        "nav_label": "Sections",
        "kicker": "Engineering student · UTC · Embedded &amp; autonomous systems",
        "lede": "I build simulations, games and tools. I am looking for an internship from September 2027.",
        "hero_alt": "Dithered solar system: a star, four planets in orbit and a spacecraft's trajectory",
        "hero_caption": "Gravitational simulation",
        "projects": "Projects",
        "entries": "04 entries",
        "more": "View repository",
        "p": {
            "claylings": ("Three clay spearmen seen from behind on a palisade at night, looking out at a dark forest where spiders' eyes shine",
                          "Colony sim and real-time defence: autonomous clay villagers driven by state machines, 13 personality traits, dynamic weather, crafting chains, squads in formation and a procedurally generated world."),
            "wooly": ("A flock of sheep on a mountain path, a shepherd and an eagle's target sight",
                      "A transhumance roguelike: 40 sheep moving as boids, a dog with three modes, and folklore creatures, wolves and an eagle, to fend off along the trail."),
            "gravity": ("A star, planets in orbit and a spacecraft's trajectory",
                        "2D space flight in a procedurally generated solar system: Keplerian orbits, spheres of influence, a ship assembly building and live mass calculations."),
            "facemask": ("A figure whose face is pixelated inside a tracking box",
                         "Video anonymisation: face detection and tracking, stabilised mosaic, IDs to exclude or merge, re-identification. Web interface and command line."),
        },
        "courses": "UTC courses",
        "courses_note": "Labs &amp; projects",
        "c": {
            "nf18": ("Databases", "CrowdFundr: conceptual and logical models, SQL, NoSQL and a client application, in a team of four."),
            "mi01": ("VHDL", "Finite state machines and a traffic light controller with sensors."),
            "sy02": ("Statistics", "Probability, estimation and the central limit theorem in R."),
            "sy08": ("Programmable logic controllers", "PLC programming in ladder logic on an industrial system simulator."),
        },
        "contact": "Contact",
        "where": "Compiègne, France<br>French · Portuguese · English · German",
    },
    "fr": {
        "path": "fr/index.html",
        "title": "Jaime Gomes-Parente — Portfolio",
        "description": "Élève ingénieur en informatique à l'UTC, spécialisé en systèmes embarqués et autonomes. Simulations, jeux et outils.",
        "og": "Simulations, jeux et outils. Élève ingénieur à l'UTC, en recherche de stage pour septembre 2027.",
        "locale": "fr_FR",
        "skip": "Aller aux projets",
        "nav": ["Projets", "Cours", "Contact"],
        "nav_label": "Sections",
        "kicker": "Élève ingénieur · UTC · Systèmes embarqués &amp; autonomes",
        "lede": "Je construis des simulations, des jeux et des outils. Je cherche un stage pour septembre 2027.",
        "hero_alt": "Système solaire tramé : une étoile, quatre planètes en orbite et la trajectoire d'un vaisseau",
        "hero_caption": "Simulation gravitationnelle",
        "projects": "Projets",
        "entries": "04 entrées",
        "more": "Voir le dépôt",
        "p": {
            "claylings": ("Trois lanciers d'argile vus de dos sur une palissade, la nuit, face à une forêt sombre où brillent des yeux d'araignées",
                          "Colonie et défense en temps réel : des villageois d'argile autonomes pilotés par machine à états, 13 traits de personnalité, météo dynamique, chaîne d'artisanat, escouades en formation et monde généré procéduralement."),
            "wooly": ("Troupeau de moutons sur un chemin de montagne, un berger et le viseur d'un aigle",
                      "Roguelike de transhumance : 40 moutons qui se déplacent en boids, un chien à trois modes et des créatures du folklore, loups et aigle, à repousser le long des sentiers."),
            "gravity": ("Étoile, planètes en orbite et trajectoire d'un vaisseau",
                        "Vol spatial 2D dans un système solaire généré procéduralement : orbites képlériennes, sphères d'influence, atelier d'assemblage de vaisseaux et calcul de masse en temps réel."),
            "facemask": ("Silhouette dont le visage est pixelisé dans un cadre de suivi",
                         "Anonymisation vidéo : détection et suivi des visages, mosaïque stabilisée, identifiants à exclure ou fusionner, réidentification. Interface web et ligne de commande."),
        },
        "courses": "Cours UTC",
        "courses_note": "TP &amp; projets",
        "c": {
            "nf18": ("Bases de données", "CrowdFundr : MCD, MLD, SQL, NoSQL et application, en groupe de quatre."),
            "mi01": ("VHDL", "Automates finis et contrôleur de feux tricolores avec capteurs."),
            "sy02": ("Statistiques", "Probabilités, estimation et théorème central limite en R."),
            "sy08": ("Automates programmables", "Programmation d'API en Ladder sur simulateur de système industriel."),
        },
        "contact": "Contact",
        "where": "Compiègne, France<br>Français · Portugais · Anglais · Allemand",
    },
}

PAGE = Template("""<!doctype html>
<html lang="$lang">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>$title</title>
<meta name="description" content="$description">
<meta property="og:title" content="$title">
<meta property="og:description" content="$og">
<meta property="og:type" content="website">
<meta property="og:url" content="$url">
<meta property="og:locale" content="$locale">
<link rel="canonical" href="$url">
<link rel="alternate" hreflang="en" href="$site">
<link rel="alternate" hreflang="fr" href="${site}fr/">
<link rel="alternate" hreflang="x-default" href="$site">
<meta name="color-scheme" content="light dark">
<link rel="icon" href="${base}favicon.svg" type="image/svg+xml">
<link rel="preload" href="${base}fonts/archivo-black.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="${base}$css">
</head>
<body>
<a class="skip" href="#projects">$skip</a>

<div class="page">

<header class="top">
  <span class="brand">J. Gomes-Parente — Portfolio</span>
  <nav aria-label="$nav_label">
    <a href="#projects">$nav0</a>
    <a href="#courses">$nav1</a>
    <a href="#contact">$nav2</a>
    <span class="lang">$switch</span>
  </nav>
</header>

<main>

<section class="hero">
  <div class="hero-text">
    <p class="kicker">$kicker</p>
    <h1>Jaime<br>Gomes-<br>Parente</h1>
    <p class="lede">$lede</p>
  </div>
  <figure class="plate">
    <img class="px" src="${base}$hero_img" width="288" height="180" alt="$hero_alt">
    <figcaption><span>FIG. 00</span><span>$hero_caption</span></figcaption>
  </figure>
</section>

<section id="projects" aria-labelledby="projects-title">
  <div class="section-head">
    <h2 id="projects-title">$projects</h2>
    <span>$entries</span>
  </div>
  <div class="cards">
$cards
  </div>
</section>

<section id="courses" aria-labelledby="courses-title">
  <div class="section-head">
    <h2 id="courses-title">$courses</h2>
    <span>$courses_note</span>
  </div>
  <ul class="courses">
$course_rows
  </ul>
</section>

</main>

<footer id="contact" class="contact">
  <h2>$contact</h2>
  <div class="links">
    <a href="mailto:gomesparentejaime@gmail.com">gomesparentejaime@gmail.com</a>
    <a href="https://github.com/jaimegomesparente">github.com/jaimegomesparente</a>
    <a href="https://www.linkedin.com/in/jaime-gomes-parente-1195a4270">LinkedIn</a>
  </div>
  <p>$where</p>
</footer>

</div>
</body>
</html>
""")

CARD = Template("""
    <article class="card">
      <a href="$href">
        <span class="plate"><img class="px" src="${base}$src" width="288" height="180" loading="lazy" alt="$alt"></span>
        <span class="meta"><span>FIG. $n</span><span>$stack</span></span>
        <h3>$name</h3>
        <p>$desc</p>
        <span class="more">$more</span>
      </a>
    </article>""")

COURSE = Template("""    <li><a href="$href"><span class="code">$code</span><span class="ctitle">$title</span><span>$desc</span></a></li>""")


def build(lang):
    t = TEXT[lang]
    base = "" if lang == "en" else "../"
    if lang == "en":
        switch = '<span aria-current="true">EN</span> / <a href="fr/" hreflang="fr" lang="fr" aria-label="Version française">FR</a>'
    else:
        switch = '<a href="../" hreflang="en" lang="en" aria-label="English version">EN</a> / <span aria-current="true">FR</span>'
    cards = "\n".join(
        CARD.substitute(base=base, href=GH + p["repo"], src=img(p["id"]), n=f"{i:02d}", stack=escape(p["stack"]),
                        name=escape(p["name"]), alt=escape(t["p"][p["id"]][0]), desc=escape(t["p"][p["id"]][1]),
                        more=t["more"])
        for i, p in enumerate(PROJECTS, 1))
    rows = "\n".join(
        COURSE.substitute(href=GH + c, code=c.upper(), title=escape(t["c"][c][0]), desc=escape(t["c"][c][1]))
        for c in COURSES)
    fields = {k: v for k, v in t.items() if isinstance(v, str)}
    fields.update({k: escape(t[k]) for k in ("description", "og", "hero_alt")})
    fields.update(lang=lang, base=base, css=asset("style.css"), hero_img=img("gravity"), site=SITE, url=SITE + ("" if lang == "en" else "fr/"), switch=switch,
                  cards=cards, course_rows=rows, nav0=t["nav"][0], nav1=t["nav"][1], nav2=t["nav"][2])
    html = PAGE.substitute(fields)
    out = ROOT / t["path"]
    out.parent.mkdir(exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(out.relative_to(ROOT))


for lang in TEXT:
    build(lang)
