#!/usr/bin/env bash
# Instalación inicial de la vista PREVIEW; ejecutar una sola vez desde EC2.
# Crea servicio de publicación y vhost separado, sin editar Drive ni esforzados.com.
set -Eeuo pipefail
umask 022

readonly BASE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
readonly DEPLOY_USER="esforzados-deploy"
readonly STATE_DIR="/var/lib/esforzados"
readonly WEB_ROOT="/var/www/esforzados"
readonly CONF="/etc/nginx/conf.d/esforzados-preview.conf"
readonly SVC_DIR="/etc/systemd/system"
readonly UPDATER="/usr/local/libexec/esforzados-update"

die() { printf '[esforzados-install] ERROR: %s\n' "$*" >&2; exit 1; }
info() { printf '[esforzados-install] %s\n' "$*"; }

[[ "$EUID" -eq 0 ]] || die "Ejecuta el instalador con sudo."
for cmd in git nginx systemctl useradd getent install grep; do
  command -v "$cmd" >/dev/null 2>&1 || die "Falta dependencia: $cmd. Instálala con el gestor de paquetes del sistema."
done
[[ -f "$BASE/update.sh" && -f "$BASE/nginx-preview.conf" &&
   -f "$BASE/esforzados-update.service" && -f "$BASE/esforzados-update.timer" ]] ||
  die "Faltan archivos de despliegue; utiliza el repositorio completo."

# Evitar sobrescribir un directorio que pertenezca a otra aplicación.
if [[ -e "$WEB_ROOT" && ! -f "$WEB_ROOT/.esforzados-managed" ]]; then
  die "Ya existe $WEB_ROOT sin marca de esta instalación; revisa antes de continuar."
fi
if [[ -e "$CONF" ]] && ! grep -q '^# Managed-by: esforzados-preview-setup$' "$CONF"; then
  die "Ya existe un sitio Nginx no administrado por este instalador: $CONF"
fi

if ! getent passwd "$DEPLOY_USER" >/dev/null; then
  info "Creando usuario de servicio sin sesión de shell."
  useradd --system --home-dir "$STATE_DIR" --create-home --shell /sbin/nologin "$DEPLOY_USER"
fi

install -d -o "$DEPLOY_USER" -g "$DEPLOY_USER" -m 0755 "$STATE_DIR"
install -d -o "$DEPLOY_USER" -g "$DEPLOY_USER" -m 0755 "$WEB_ROOT"
install -d -o "$DEPLOY_USER" -g "$DEPLOY_USER" -m 0755 "$WEB_ROOT/releases"

if [[ ! -f "$WEB_ROOT/.esforzados-managed" ]]; then
  printf 'Esforzados preview managed directory\n' > "$WEB_ROOT/.esforzados-managed"
  chown "$DEPLOY_USER:$DEPLOY_USER" "$WEB_ROOT/.esforzados-managed"
  chmod 0644 "$WEB_ROOT/.esforzados-managed"
fi

install -d -m 0755 /usr/local/libexec
install -m 0755 -o root -g root "$BASE/update.sh" "$UPDATER"
install -m 0644 -o root -g root "$BASE/esforzados-update.service" "$SVC_DIR/esforzados-update.service"
install -m 0644 -o root -g root "$BASE/esforzados-update.timer" "$SVC_DIR/esforzados-update.timer"

# Configuración Nginx separada. Si falla el test, restaurar configuración previa.
backup=""
if [[ -f "$CONF" ]]; then
  backup="$(mktemp /tmp/esforzados-nginx-backup.XXXXXX)"
  cp -- "$CONF" "$backup"
fi
install -m 0644 -o root -g root "$BASE/nginx-preview.conf" "$CONF"

if ! nginx -t; then
  if [[ -n "$backup" ]]; then cp -- "$backup" "$CONF"; else rm -f -- "$CONF"; fi
  [[ -z "$backup" ]] || rm -f -- "$backup"
  die "El archivo Nginx no superó la validación. Se restauró la configuración."
fi
[[ -z "$backup" ]] || rm -f -- "$backup"

# No arrancar ni reiniciar otros servicios de aplicación; sólo recargar Nginx.
if systemctl is-active --quiet nginx; then
  systemctl reload nginx
else
  info "Nginx no estaba activo: revisa su servicio antes de exponer el sitio."
fi

systemctl daemon-reload
systemctl start esforzados-update.service
systemctl enable --now esforzados-update.timer

info "Primera versión estática colocada en $WEB_ROOT/current."
info "Timer activo: busca cambios en main aproximadamente cada cinco minutos."
info "Para el acceso público configura el DNS A de preview.esforzados.com hacia este EC2."
info "Luego de verificar DNS, emite HTTPS con certbot para preview.esforzados.com."
info "Estado del servicio: systemctl status esforzados-update.service"
info "Historial: journalctl -u esforzados-update.service -n 50 --no-pager"
