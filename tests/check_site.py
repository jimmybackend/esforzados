#!/usr/bin/env python3
"""Offline checks for the static Esforzados site (stdlib only)."""
from __future__ import annotations

from html.parser import HTMLParser
import hashlib
import struct
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
FILES = ("index.html", "assets/site.css", "assets/site.js", "assets/brand.svg", "assets/carousel-legal.png", "assets/carousel-drive-aws.png", "assets/carousel-hub.png", "assets/carousel-chat.png", "assets/carousel-edu.png")


class Page(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.links: list[str] = []
        self.slides: list[str] = []
        self.controls: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = dict(attrs)
        if data.get("id"):
            self.ids.append(data["id"])
        if tag in ("a", "link") and data.get("href"):
            self.links.append(data["href"])
        if tag == "img" and data.get("src"):
            self.links.append(data["src"])
        if tag == "article" and data.get("aria-roledescription") == "diapositiva":
            self.slides.append(data.get("id", ""))
        if tag == "button" and "carousel-dot" in (data.get("class") or "").split():
            self.controls.append((data.get("aria-controls", ""), data.get("data-go", "")))


def check() -> None:
    for filename in FILES:
        path = ROOT / filename
        assert path.is_file() and not path.is_symlink(), f"Falta archivo local: {filename}"

    page = Page()
    html = INDEX.read_text(encoding="utf-8")
    page.feed(html)
    assert len(set(page.ids)) == len(page.ids), "IDs HTML duplicados"
    assert len(page.slides) == 5, "Se necesitan cinco diapositivas"
    assert len(page.controls) == 5, "Se necesitan cinco botones"
    assert page.slides == ["slide-legal", "slide-drive", "slide-hub", "slide-chat", "slide-edu"], "Orden esperado: Legal, Drive, Edu, Hub, Chat"
    assert [control for control, _ in page.controls] == page.slides, "Controles desordenados respecto a diapositivas"
    assert sorted(int(i) for _, i in page.controls) == list(range(5)), "Índices del carrusel inválidos"

    for href in page.links:
        if href.startswith("#"):
            assert href[1:] in page.ids, f"Ancla interna inexistente: {href}"
        elif href.startswith("assets/"):
            assert (ROOT / href.split("?", 1)[0]).is_file(), f"Recurso local ausente: {href}"

    # La portada pública presenta solamente header, carrusel y footer.
    assert html.count("<section ") == 1, "Se espera solamente la sección del carrusel"
    assert '<header class="site-header">' in html and '<footer class="footer">' in html
    assert '<h1 class="sr-only" id="hero-intro">' in html, "Falta título accesible"
    assert "NUESTROS SERVICIOS" not in html and "NUESTRA VISIÓN" not in html
    assert "Seguimiento de mi caso" not in html and "Hablemos de lo que" not in html
    assert "Acceso privado en preparación" not in html, "Sección Legal antigua aún presente"
    # Solo el logo arriba y el copyright centrado abajo; sin menús duplicados.
    assert 'data-slide-target=' not in html and 'id="menu-principal"' not in html
    assert '<nav ' not in html and 'menu-toggle' not in html
    assert 'class="footer-top"' not in html and 'class="brand-footer"' not in html
    assert html.count("Todos los derechos reservados.") == 1
    assert html.count("Contacto y soporte") == 1
    assert 'href="tel:+525586458862">Esforzados Legal · +52 55 8645 8862</a>' in html
    assert 'href="mailto:soporte@esforzados.com">soporte@esforzados.com</a>' in html
    assert "Servidor privado de Esforzados." in html
    assert 'class="container footer-contact"' in html
    assert '<div class="container footer-bottom"><small>© <span id="year">2026</span> Esforzados. Todos los derechos reservados.</small></div>' in html
    assert "Tecnología con propósito" not in html
    assert 'href="#legal"' not in html and 'href="#servicios"' not in html

    destinations = (
        ("legal", "carousel-legal.png", "https://legal.esforzados.com/"),
        ("drive", "carousel-drive-aws.png", "https://drive.esforzados.com/"),
        ("hub", "carousel-hub.png", "https://hub.esforzados.com/"),
        ("chat", "carousel-chat.png", "https://chat.esforzados.com/"),
        ("edu", "carousel-edu.png", "https://portal.esforzados.com/"),
    )
    assert html.count('class="artwork-image-link"') == 5
    for service, image, destination in destinations:
        section = html[html.index(f'id="slide-{service}"'):]
        section = section[:section.index("</article>")]
        assert re.search(
            r'<a class="artwork-image-link" href="' + re.escape(destination) +
            r'"[^>]*>\s*<img src="assets/' + re.escape(image) + r'"[^>]*>\s*</a>',
            section,
        ), f"Imagen del carrusel {service} no enlaza a {destination}"
        assert re.search(r'<a class="button [^"]*" href="' + re.escape(destination) + r'"', section), f"Botón {service} no enlaza al destino esperado"

    css = (ROOT / "assets/site.css").read_text(encoding="utf-8")
    assert ".footer-bottom {display:flex;align-items:center;justify-content:center;text-align:center;" in css
    assert ".artwork-image-link {display:block;width:100%;cursor:pointer;}" in css
    assert ".footer-contact { padding: 28px 0 10px; text-align: center;" in css
    assert "aspect-ratio: 1672 / 941" not in css
    assert "aspect-ratio: 1916 / 821" in css

    # La altura de la cuadrícula la determina la diapositiva más alta,
    # incluso cuando otra está seleccionada; el footer nunca salta.
    assert "display: grid;" in css and "grid-template-columns: minmax(0, 1fr);" in css
    assert ".carousel-stage > .slide[hidden] {" in css
    hidden_style = css.split(".carousel-stage > .slide[hidden] {", 1)[1].split("}", 1)[0]
    assert "display: flex !important;" in hidden_style
    assert "visibility: hidden;" in hidden_style
    assert "pointer-events: none;" in hidden_style
    assert "grid-area: 1 / 1;" in css
    assert "min-height: 100svh;" in css and ".footer { flex-shrink: 0; }" in css
    assert "@media (max-width: 760px)" in css and "@media (max-width: 380px)" in css
    assert "flex-direction: column; gap: 8px;" in css, "Contacto debe ajustarse en móviles estrechos"
    assert html.count('width="1916" height="821"') == 5, "Todas las imágenes deben declarar las mismas medidas"

    assert 'src="assets/carousel-legal.png"' in html, "Banner aprobado de Legal no enlazado"
    assert 'src="assets/carousel-drive-aws.png"' in html, "Imagen aprobada de Drive no enlazada"
    legal = (ROOT / "assets/carousel-legal.png").read_bytes()
    assert legal.startswith(bytes.fromhex("89504e470d0a1a0a")), "PNG de Legal inválido"
    assert struct.unpack(">II", legal[16:24]) == (1916, 821), "Dimensiones de Legal deben coincidir con Drive"
    legal_git_sha = hashlib.sha1(b"blob " + str(len(legal)).encode() + bytes([0]) + legal).hexdigest()
    assert legal_git_sha == "466c8edc395df8d3095e0a06d3dc0646da0c270c", "Imagen de Legal no coincide con la aprobada"
    drive = (ROOT / "assets/carousel-drive-aws.png").read_bytes()
    assert drive.startswith(bytes.fromhex("89504e470d0a1a0a")), "PNG original de Drive inválido"
    assert struct.unpack(">II", drive[16:24]) == (1916, 821), "Dimensiones de original AWS S3 inesperadas"
    git_blob = hashlib.sha1(b"blob " + str(len(drive)).encode() + bytes([0]) + drive).hexdigest()
    assert git_blob == "c2c089eecbdad852d5fe5b39bfc7f740e12aa27e", "La imagen Drive no coincide con la versión en cedro aprobada"
    js = (ROOT / "assets/site.js").read_text(encoding="utf-8")
    assert '["Esforzados Legal", "ArcadeCloud Drive", "Esforzados Hub", "Esforzados Chat"' in js, "Anuncios JS del carrusel desordenados"
    assert 'serviceNavigation' not in js and 'menu-principal' not in js, "Quedó JavaScript de los menús retirados"
    assert 'src="assets/carousel-hub.png"' in html, "Banner aprobado de Hub no enlazado"
    hub = (ROOT / "assets/carousel-hub.png").read_bytes()
    assert hub.startswith(bytes.fromhex("89504e470d0a1a0a")), "PNG de Hub inválido"
    assert struct.unpack(">II", hub[16:24]) == (1916, 821), "Dimensiones del banner Hub incorrectas"
    hub_blob = hashlib.sha1(b"blob " + str(len(hub)).encode() + bytes([0]) + hub).hexdigest()
    assert hub_blob == "65b98f63b809bcc03b1360e3652b6bf196623898", "El banner Hub no coincide con la versión aprobada"
    for service, expected_sha in (
        ("chat", "cc096d418be6c23ec282ccd90ab4b611a5183aba"),
        ("edu", "bee20aa889e64e5a904bee4a54b72f9463026fd2"),
    ):
        assert f'src="assets/carousel-{service}.png"' in html, f"Banner {service} no enlazado"
        data = (ROOT / f"assets/carousel-{service}.png").read_bytes()
        assert data.startswith(bytes.fromhex("89504e470d0a1a0a")), f"PNG {service} inválido"
        assert struct.unpack(">II", data[16:24]) == (1916, 821), f"Dimensiones {service} incorrectas"
        blob_sha = hashlib.sha1(b"blob " + str(len(data)).encode() + bytes([0]) + data).hexdigest()
        assert blob_sha == expected_sha, f"Banner {service} no coincide con la imagen aprobada"

    assert html.index('id="slide-chat"') < html.index('id="slide-edu"')
    assert 'Acceso privado Chat' in html
    assert 'https://portal.esforzados.com/' in html
    ET.parse(ROOT / "assets/brand.svg")
    updater = (ROOT / "deploy/ec2/update.sh").read_text(encoding="utf-8")
    for filename in ("index.html", "assets/site.css", "assets/site.js", "assets/brand.svg"):
        assert f'"{filename}"' in updater, f"El actualizador no publica {filename}"
    assert '"$REPO_DIR"/assets/carousel-*.png' in updater, "Falta patrón estricto para recursos PNG"
    assert 'files+=("assets/${source_image##*/}")' in updater, "El actualizador no incorpora los PNG del carrusel"
    assert "git clone" in updater and "fetch" in updater
    assert "/var/lib/esforzados/repo" in updater
    assert "/var/www/esforzados" in updater
    assert "/var/www/esforzados/repo" not in updater
    # mktemp -d nace 0700; Nginx no puede atravesar esas carpetas
    # si el actualizador olvida convertirlas explícitamente a 0755.
    assert 'chmod 0755 "$stage" "$stage/assets"' in updater
    assert 'chmod 0755 "$release" "$release/assets"' in updater
    # Evitar que el publicador ignore un PNG faltante porque ya se publicó el SHA.
    assert 'cmp -s "$REPO_DIR/$file" "$release/$file"' in updater
    assert 'Reparado archivo del release' in updater
    assert updater.index('files=("index.html"') < updater.index('if [[ -L "$WEB_ROOT/current" ]]')
    assert updater.index('Reparar versiones ya publicadas') < updater.index('if [[ -L "$WEB_ROOT/current" ]]')

    print("OK: sitio, carrusel, permisos y reparación automática de imágenes faltantes.")


if __name__ == "__main__":
    try:
        check()
    except (AssertionError, OSError, ValueError, ET.ParseError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
