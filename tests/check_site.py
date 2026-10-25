#!/usr/bin/env python3
"""Offline checks for the static Esforzados site (stdlib only)."""
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
FILES = ("index.html", "assets/site.css", "assets/site.js", "assets/brand.svg")


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
    assert set(page.slides) == {control for control, _ in page.controls}, "Controles no corresponden a diapositivas"
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

    ET.parse(ROOT / "assets/brand.svg")
    updater = (ROOT / "deploy/ec2/update.sh").read_text(encoding="utf-8")
    for filename in FILES:
        assert f'"{filename}"' in updater, f"El instalador no publica {filename}"
    assert "git clone" in updater and "fetch" in updater
    assert "/var/lib/esforzados/repo" in updater
    assert "/var/www/esforzados" in updater
    assert "/var/www/esforzados/repo" not in updater

    print("OK: estructura estática, carrusel, enlaces, SVG y archivos de despliegue.")


if __name__ == "__main__":
    try:
        check()
    except (AssertionError, OSError, ValueError, ET.ParseError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
