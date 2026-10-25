# Esforzados en EC2: vista previa + actualización automática

**Estado:** scripts preparados en el repositorio. La ejecución en EC2, DNS y HTTPS aún requieren instalación y comprobación.  
**Destino elegido:** `/var/www/esforzados/` (publicación estática, **no** el checkout Git).  
**Sitio de prueba:** `preview.esforzados.com` (propuesto, no crear DNS antes de revisar la IP).

## Diseño seguro

```text
GitHub (jimmybackend/esforzados, main)
    |
    | Git HTTPS solo lectura (repo público, sin token)
    v
EC2 pequeña - systemd timer (cada ~5 minutos)
    |
    | git fetch main como usuario 'esforzados-deploy', sin sudo
    v
/var/lib/esforzados/repo/          <- checkout privado, NO servido por Nginx
    |
    | Copia LISTA BLANCA, sin ejecución de scripts del repositorio
    v
/var/www/esforzados/releases/sha-<commit>/
    |
    | Cambio atómico de enlace 'current'
    v
/var/www/esforzados/current/       <- Nginx solo archivos HTML/CSS/JS/SVG
    |
    v
preview.esforzados.com             <- subdominio aislado
```

**No modifica el servidor virtual de `drive.esforzados.com` ni el hosting actual de `esforzados.com`.** No abre SSH, no usa AWS IAM, no crea credenciales GitHub y no consume recursos de la EC2 grande.

## Requisitos antes de instalar

- Instancia **pequeña** correcta, encendida, con acceso de administración existente (SSM o SSH privado autorizado).
- Amazon Linux 2023 (o Linux compatible con Bash, Git, Nginx y systemd).
- Comprobar Nginx y servicios actuales. Nunca sustituir archivos de configuración existentes.
- Tener `git`, `nginx` y `systemd`. Si falta Git en Amazon Linux 2023: `sudo dnf install -y git`.
- DNS disponible para crear un registro A: `preview.esforzados.com` -> IPv4 pública real de la EC2 pequeña. No inventar esa IP ni reutilizar una antigua sin verificar.
- Antes de HTTPS, asegurar que el acceso HTTP puerto 80 existente permita ACME; **no abrir nuevos puertos administrativos**.
- Para HTTPS en Nginx utilizar Certbot ya instalado o configurar certificado válido por otro mecanismo, tras comprobar DNS.

## Instalación inicial (una sola vez en la EC2 pequeña)

Ejecutar mediante una sesión autorizada. Evitar pegar claves o credenciales dentro del repositorio.

```bash
# Revisar el servidor antes de cualquier cambio:
sudo nginx -t
systemctl is-active nginx
git --version

# Descargar el instalador de origen público conocido:
git clone --depth=1 --branch main https://github.com/jimmybackend/esforzados.git /tmp/esforzados-install

# Inspeccionar previamente los archivos y, si corresponde, instalar:
less /tmp/esforzados-install/deploy/ec2/install.sh
sudo bash /tmp/esforzados-install/deploy/ec2/install.sh
```

El instalador:
- Bloquea la sobrescritura de `/var/www/esforzados` si existe y no tiene su marcador.
- Crea usuario de sistema `esforzados-deploy` sin shell de acceso y los directorios exclusivos.
- Instala actualizador inmutable para el usuario de despliegue en `/usr/local/libexec/`.
- Instala un timer y servicio systemd aislados.
- Añade **solo** `/etc/nginx/conf.d/esforzados-preview.conf` para `preview.esforzados.com`.
- Comprueba `nginx -t`; ante error restaura el archivo original del nuevo vhost.
- Recarga Nginx si está activo y ejecuta la primera sincronización.
- El código PHP no se ejecuta: el preview es exclusivamente estático.

## DNS y HTTPS

1. Consultar la IPv4 pública **actual** de la EC2 pequeña.
2. Crear registro **A** `preview` en la zona DNS de `esforzados.com` apuntando a dicha IPv4.
3. Confirmar que `preview.esforzados.com` resuelve esa misma dirección.
4. Si Certbot está disponible y controla Nginx, ejecutar:
   ```bash
   sudo certbot --nginx -d preview.esforzados.com --redirect
   sudo nginx -t
   ```
5. Verificar el certificado y probar `https://preview.esforzados.com/`.

Hasta configurar DNS y un certificado válido **no prometer acceso HTTPS**. El sitio de prueba es público, **no apto para expedientes privados**.

## Actualización desde la web (sin volver a entrar por EC2)

1. Editar la portada en GitHub (interfaz web) o utilizar una rama y PR.
2. Fusionar cambios revisados a `main`.
3. El servicio `esforzados-update.timer` busca cambios **aproximadamente cada cinco minutos**.
4. Si el código se descarga correctamente, valida que existan los archivos aprobados de lista blanca, crea una nueva versión y conmuta `current` sin interrumpir las lecturas.
5. Si GitHub no responde o un archivo falta, **la versión anterior se mantiene intacta**.

No hace falta un botón PHP de actualización pública. Para forzar una revisión **desde el servidor**, bajo autenticación del administrador: `sudo systemctl start esforzados-update.service`.

## Operación y diagnóstico

```bash
systemctl list-timers esforzados-update.timer
sudo systemctl status esforzados-update.service --no-pager
sudo journalctl -u esforzados-update.service -n 60 --no-pager
sudo nginx -t
readlink /var/www/esforzados/current
```

Si no aparece la versión nueva, verificar los logs y conectividad HTTPS a GitHub.

### Regresar a una versión anterior

Cada publicación queda en `/var/www/esforzados/releases/sha-<commit>/`. Para un rollback debe seleccionarse una revisión **real y existente** y sustituir de forma atómica el enlace `current`. Primero detener temporalmente el timer para que no republique inmediatamente la revisión más reciente:

```bash
sudo systemctl stop esforzados-update.timer
# Listar releases y seleccionar el SHA correcto; no introducir rutas externas.
sudo ls -ld /var/www/esforzados/releases/sha-*
# Realizar reversión de enlace con cuidado; el proceso requiere revisión de la ruta.
# Rehabilitar el timer tras corregir o revertir el commit en GitHub.
```

**No ejecutar `git reset --hard` en el docroot** ni colocar `.git` bajo la raíz servida. El servicio de actualización opera como usuario de sistema sin capacidad de reiniciar Nginx o administrar AWS.

## Archivos servidos (lista blanca)

- `index.html`
- `assets/site.css`
- `assets/site.js`
- `assets/brand.svg`
- `assets/carousel-legal.png`

Si el proyecto incorpora más archivos necesarios, habrá que ampliar expresamente esa lista en el script, revisarla y actualizar el instalador **de forma controlada**. No se sincroniza todo el repositorio al directorio público.

## Pendiente operativo

- [ ] Comprobar conectividad real con EC2 pequeña y que Nginx esté funcionando.
- [ ] Instalar el servicio en la EC2 pequeña mediante acceso autorizado.
- [ ] Crear DNS A para `preview.esforzados.com`.
- [ ] Configurar TLS y confirmar el certificado.
- [ ] Probar el carrusel desde teléfono y computadora.
- [ ] Comprobar una actualización de extremo a extremo editando en GitHub y fusionando a `main`.
- [ ] Revisar la portada antes de cambiar el dominio principal `esforzados.com`.

> El puente existente en `jimmybackend/s3` dispone de workflow de **estado EC2**, no de ejecución remota de comandos. Estos scripts evitan ampliar el alcance de ese puente o emplear el rol IAM de administración completa para desplegar una web estática.

## Corrección de permisos de la primera instalación (25 de octubre de 2026)

Si Nginx informa `Permission denied (13)` en `/var/www/esforzados/current/index.html`, comprobar:

```bash
sudo ls -ld "$(readlink -f /var/www/esforzados/current)"
```

El instalador inicial creó un directorio temporal con `mktemp -d` (modo `0700`) y lo trasladó al release. Los archivos son `0644`, pero el directorio necesita `0755` para que Nginx pueda recorrerlo.

**Solución puntual, sin cambiar otros sitios ni permisos recursivos:**

```bash
sudo chmod 755 "$(readlink -f /var/www/esforzados/current)"
curl -I -H 'Host: preview.esforzados.com' http://127.0.0.1/index.html
```

**Solución permanente:** `deploy/ec2/update.sh` ahora asigna `0755` a las carpetas del release al crearlo y corrige versiones previas. Como el instalador deja una copia independiente del actualizador en `/usr/local/libexec/esforzados-update`, actualizar el repositorio **no sustituye automáticamente ese ejecutable instalado**. Para actualizarlo en EC2 tras fusionar este arreglo:

```bash
git -C /tmp/esforzados-install pull --ff-only origin main
sudo install -o root -g root -m 0755 /tmp/esforzados-install/deploy/ec2/update.sh /usr/local/libexec/esforzados-update
sudo systemctl start esforzados-update.service
```

Si `/tmp/esforzados-install` ya no está disponible, descargar una copia nueva a un directorio temporal vacío antes del comando `sudo install`. **No ejecutar `install.sh` otra vez sólo para corregir permisos**, ni ejecutar `chmod -R` sobre `/var/www`.

La prueba HTTP con cabecera Host verifica únicamente el bloque virtual de Esforzados; cualquier cambio de DNS o nombre de host se maneja por separado. El sitio sigue siendo un **preview público sin datos de expedientes**.

> **Imagen Legal (2026-10-25):** tras fusionar, actualizar una vez el ejecutable instalado en EC2 con la versión de `deploy/ec2/update.sh` que añade el PNG a la lista blanca. Véase README principal, sección «Carrusel Legal». Sin ese paso el timer actualizará el HTML pero no copiará el PNG.

## Incidencia: carrusel Legal muestra texto alternativo / PNG no visible

**Síntoma:** `index.html` aparece, pero la imagen del primer slide no carga; `ls /var/www/esforzados/current/assets/carousel-legal.png` informa que no existe. El repositorio Git en EC2 sí tiene `assets/carousel-legal.png`.

**Causa:** el instalador copió `deploy/ec2/update.sh` una sola vez a `/usr/local/libexec/esforzados-update`. Un `git pull` dentro de `/tmp/esforzados-install` **no actualiza automáticamente** ese ejecutable. La versión anterior publicaba cuatro archivos y omitía el nuevo PNG. Además, al encontrar el mismo commit ya publicado, no lo reparaba.

**Corrección en el repositorio:** el actualizador ahora:
- exige el PNG en la lista blanca;
- comprueba y repara archivos faltantes del release existente incluso cuando el commit es igual;
- copia cambios mediante archivo temporal y renombrado atómico;
- mantiene los permisos normales para Nginx.

**Aplicar una sola vez en EC2 pequeña**, sin editar configuraciones de Nginx:

```bash
git -C /tmp/esforzados-install pull --ff-only origin main
sudo install -o root -g root -m 0755 \
  /tmp/esforzados-install/deploy/ec2/update.sh \
  /usr/local/libexec/esforzados-update
sudo systemctl start esforzados-update.service
ls -lh /var/www/esforzados/current/assets/carousel-legal.png
curl -I -H 'Host: preview.50.17.162.57.sslip.io' \
  http://127.0.0.1/assets/carousel-legal.png
```

El último comando debe devolver `200 OK` y `Content-Type: image/png`. Si el checkout temporal se eliminó, vuelve a clonarlo en una carpeta temporal nueva, revisa el script y realiza el paso de instalación.

**Importante:** el timer se encarga de publicar en el futuro los cambios de HTML, CSS, JS, SVG y el PNG ya incorporado a la lista blanca. Añadir un **nuevo nombre** de recurso a la lista en el repositorio vuelve a requerir actualizar el ejecutable local o configurar un mecanismo explícito de distribución del updater con revisión de seguridad.

## Incorporar la diapositiva 2 — ArcadeCloud Drive (imagen AWS S3 original)

El archivo `assets/carousel-drive-aws.png` ya está en el repositorio principal y conserva los bytes exactos de la imagen `drive/images/home/carousel-01-s3-aws.png` en `jimmybackend/s3`.

En esta versión, el actualizador acepta `assets/carousel-*.png` además de los cuatro archivos base y repara releases existentes. Esto hace que **futuras imágenes con ese prefijo no requieran modificar otra vez el script**.

**Importante:** el actualizador del EC2 quedó copiado en `/usr/local/libexec/esforzados-update` durante la instalación inicial. Aunque `main` se sincronice automáticamente, ese ejecutable no cambia solo. Actualízalo **una vez** después de fusionar el cambio, sin ejecutar el instalador completo:

```bash
git -C /tmp/esforzados-install pull --ff-only origin main
sudo install -o root -g root -m 0755 \
    /tmp/esforzados-install/deploy/ec2/update.sh \
    /usr/local/libexec/esforzados-update
sudo systemctl start esforzados-update.service
ls -lh /var/www/esforzados/current/assets/carousel-drive-aws.png
curl -I -H 'Host: preview.50.17.162.57.sslip.io' \
    http://127.0.0.1/assets/carousel-drive-aws.png
```

El último comando debe devolver `200 OK` con `Content-Type: image/png`. Si el directorio temporal `/tmp/esforzados-install` ya no existe, clonar nuevamente el repositorio **en un directorio temporal vacío**, inspeccionar el script y repetir la copia del ejecutable. No cambiar los vhosts de Nginx de otros servicios.

La página sigue siendo una vista **pública y temporal** por HTTP: no usarla para clientes, sesiones ni expedientes.
