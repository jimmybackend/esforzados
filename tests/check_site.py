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
FILES = ("index.html", "assets/site.css", "assets/site.js", "assets/brand.svg", "assets/carousel-legal.png", "assets/carousel-drive-aws.png", "assets/carousel-hub.png")


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
    assert page.slides == ["slide-legal", "slide-drive", "slide-hub", "slide-edu", "slide-chat"], "Orden esperado: Legal, Drive, Edu, Hub, Chat"
    assert [control for control, _ in page.controls] == page.slides, "Controles desordenados respecto a diapositivas"
    assert sorted(int(i) for _, i in page.controls) == list(range(5)), "Índices del carrusel inválidos"

    for href in page.links:
        if href.startswith("#"):
            assert href[1:] in page.ids, f"Ancla interna inexistente: {href}"
        elif href.startswith("assets/"):
            assert (ROOT / href.split("?", 1)[0]).is_file(), f"Recurso local ausente: {href}"

    assert "legal.esforzados.com/" not in html, "No enlazar a un portal legal aún inexistente"
    assert "Acceso privado en preparación" in html, "Falta advertencia de portal legal no disponible"
    assert html.count("https://portal.esforzados.com/") >= 1
    assert html.count("https://drive.esforzados.com/") >= 1
    assert html.count("https://hub.esforzados.com/") >= 1

    assert 'src="assets/carousel-legal.png"' in html, "Banner aprobado de Legal no enlazado"
    assert 'src="assets/carousel-drive-aws.png"' in html, "Imagen original de Drive no enlazada"
    assert (ROOT / "assets/carousel-legal.png").read_bytes().startswith(bytes.fromhex("89504e470d0a1a0a")), "PNG de Legal inválido"
    drive = (ROOT / "assets/carousel-drive-aws.png").read_bytes()
    assert drive.startswith(bytes.fromhex("89504e470d0a1a0a")), "PNG original de Drive inválido"
    assert struct.unpack(">II", drive[16:24]) == (1916, 821), "Dimensiones de original AWS S3 inesperadas"
    git_blob = hashlib.sha1(b"blob " + str(len(drive)).encode() + bytes([0]) + drive).hexdigest()
    assert git_blob == "dd7395d4e030ead572a56c4f498a8ecd94ca02b0", "La imagen AWS S3 no coincide con el original de ArcadeCloud"
    js = (ROOT / "assets/site.js").read_text(encoding="utf-8")
    assert '["Esforzados Legal", "ArcadeCloud Drive", "Esforzados Hub", "Esforzados Edu"' in js, "Anuncios JS del carrusel desordenados"
    assert 'src="assets/carousel-hub.png"' in html, "Banner aprobado de Hub no enlazado"
    hub = (ROOT / "assets/carousel-hub.png").read_bytes()
    assert hub.startswith(bytes.fromhex("89504e470d0a1a0a")), "PNG de Hub inválido"
    assert struct.unpack(">II", hub[16:24]) == (1916, 821), "Dimensiones del banner Hub incorrectas"
    hub_blob = hashlib.sha1(b"blob " + str(len(hub)).encode() + bytes([0]) + hub).hexdigest()
    assert hub_blob == "65b98f63b809bcc03b1360e3652b6bf196623898", "El banner Hub no coincide con la versión aprobada"
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
