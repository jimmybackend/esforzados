#!/usr/bin/env bash
# Esforzados: actualizador NO privilegiado para portada pública estática.
# No ejecuta código del repositorio, sólo copia archivos explícitos.
set -Eeuo pipefail
umask 022

readonly REPO_URL="https://github.com/jimmybackend/esforzados.git"
readonly REPO_DIR="/var/lib/esforzados/repo"
readonly WEB_ROOT="/var/www/esforzados"
readonly RELEASES="$WEB_ROOT/releases"
readonly MARKER="$WEB_ROOT/.esforzados-managed"

log() { printf '[esforzados-update] %s\n' "$*"; }
fail() { printf '[esforzados-update] ERROR: %s\n' "$*" >&2; exit 1; }

[[ -f "$MARKER" ]] || fail "El destino no fue inicializado por install.sh."
[[ -d "$RELEASES" ]] || fail "No existe el directorio de releases."

if [[ ! -d "$REPO_DIR/.git" ]]; then
  [[ ! -e "$REPO_DIR" ]] || fail "Existe un checkout no válido; se requiere revisión manual."
  log "Descargando repositorio público (main) por primera vez."
  git clone --quiet --no-tags --depth=1 --single-branch --branch main "$REPO_URL" "$REPO_DIR"
else
  actual="$(git -C "$REPO_DIR" remote get-url origin)"
  [[ "$actual" == "$REPO_URL" ]] || fail "Origen Git inesperado: se cancela."
  git -C "$REPO_DIR" fetch --quiet --depth=1 --no-tags origin refs/heads/main
  git -C "$REPO_DIR" checkout --quiet --force -B main FETCH_HEAD
fi

sha="$(git -C "$REPO_DIR" rev-parse HEAD)"
[[ "$sha" =~ ^[0-9a-f]{40}$ ]] || fail "No fue posible verificar el commit."
target="releases/sha-$sha"
release="$WEB_ROOT/$target"

# mktemp -d crea las carpetas con permiso 0700. Nginx necesita el bit
# de lectura/ejecución (0755) en el release, además de archivos 0644.
# Reparar también versiones ya creadas con el instalador anterior.
if [[ -d "$release" && ! -L "$release" ]]; then
  [[ -d "$release/assets" && ! -L "$release/assets" ]] || fail "Assets inválidos en el release."
  chmod 0755 "$release" "$release/assets"
fi

# LISTA BLANCA: publicar sólo HTML/CSS/JS/SVG e imágenes aprobadas.
# Comprobarla ANTES del retorno por mismo SHA para reparar releases incompletos.
readonly files=("index.html" "assets/site.css" "assets/site.js" "assets/brand.svg" "assets/carousel-legal.png")
for file in "${files[@]}"; do
  [[ -f "$REPO_DIR/$file" && ! -L "$REPO_DIR/$file" ]] || fail "Archivo inválido o enlace simbólico: $file"
done
[[ -d "$REPO_DIR/assets" && ! -L "$REPO_DIR/assets" ]] || fail "Directorio assets inválido."

# Reparar versiones ya publicadas cuando se instaló un actualizador antiguo:
# puede faltar carousel-legal.png aun si current apunta al mismo commit.
# Cada archivo se copia a un temporal y se renombra atómicamente.
if [[ -d "$release" ]]; then
  [[ ! -L "$release" ]] || fail "Release no debe ser enlace simbólico."
  for file in "${files[@]}"; do
    [[ ! -L "$release/$file" ]] || fail "Archivo de destino inesperadamente es enlace: $file"
    if ! cmp -s "$REPO_DIR/$file" "$release/$file"; then
      staged_file="$(mktemp "$release/.repair.XXXXXXXX")"
      trap 'rm -f -- "${staged_file:-}"' EXIT
      install -m 0644 "$REPO_DIR/$file" "$staged_file"
      mv -Tf -- "$staged_file" "$release/$file"
      trap - EXIT
      log "Reparado archivo del release: $file"
    fi
  done
fi

if [[ -L "$WEB_ROOT/current" ]] && [[ "$(readlink "$WEB_ROOT/current")" == "$target" ]]; then
  log "Sin cambios: el sitio ya usa $sha (archivos y permisos verificados)."
  exit 0
fi

if [[ ! -d "$release" ]]; then
  stage="$(mktemp -d "$RELEASES/.stage.XXXXXXXX")"
  trap 'rm -rf -- "${stage:-}"' EXIT
  mkdir -p "$stage/assets"
  for file in "${files[@]}"; do
    install -m 0644 "$REPO_DIR/$file" "$stage/$file"
  done
  # Sin este chmod, el directorio temporal conserva 0700 y Nginx da 403/404.
  chmod 0755 "$stage" "$stage/assets"
  mv -- "$stage" "$release"
  trap - EXIT
fi

# La sustitución del enlace es atómica: los visitantes no ven una copia parcial.
link="$WEB_ROOT/.current.next.$$"
trap 'rm -f -- "$link"' EXIT
ln -s "$target" "$link"
mv -Tf -- "$link" "$WEB_ROOT/current"
trap - EXIT

log "Publicado commit $sha -> $WEB_ROOT/current"
log "Para revertir, cambiar manualmente el enlace current a un release anterior."
