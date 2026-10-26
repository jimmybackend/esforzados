# Esforzados — Portal principal del ecosistema

**Dominio principal:** https://esforzados.com/  
**Repositorio:** `jimmybackend/esforzados`  
**Estado:** portada pública inicial implementada en el repositorio; **sin despliegue a producción ni backend legal**.  
**Última actualización de decisiones:** 25 de octubre de 2026.

## 1. Visión

Transformar `esforzados.com` en la puerta de entrada clara, profesional y accesible a los servicios de Esforzados, conservando la identidad de «biosfera digital» cuando aporte valor, pero dando protagonismo a los servicios concretos y al acceso seguro de clientes.

La portada tendrá un **carrusel de cinco servicios**, navegación clara, información institucional y un acceso destacado a «Consultar mi expediente». El portal principal presentará y enlazará los servicios, sin concentrar innecesariamente su código ni acceder directamente a los datos legales.

**Los sistemas existentes siguen independientes.** Esta primera implementación es una portada pública estática; no modifica sus servicios ni contiene información privada.

## 2. Mapa de servicios

| Servicio | Dirección | Proyecto o repositorio | Situación |
| --- | --- | --- | --- |
| Portal principal | https://esforzados.com/ | `jimmybackend/esforzados` | Portada inicial implementada en el repositorio; despliegue pendiente |
| Esforzados Legal | `https://legal.esforzados.com/` | Repositorio independiente propuesto: `jimmybackend/esforzados-legal` | Propuesta; sin crear ni desplegar |
| Esforzados Edu | https://portal.esforzados.com/ | Repositorio por identificar | Servicio existente; sin cambios |
| ArcadeCloud Drive | https://drive.esforzados.com/ | `jimmybackend/s3` | Servicio existente; sin cambios |
| Esforzados Hub | https://hub.esforzados.com/ | `jimmybackend/hub-esforzados` (privado) | Servicio existente; sin cambios |
| Esforzados Chat | https://chat.esforzados.com/ (documentado; disponibilidad por verificar) | Proyecto MiChat/Chat por confirmar como responsable del despliegue | Enlace incluido en portada; integración pendiente |

Los enlaces y dominios propuestos no implican que las nuevas aplicaciones ya estén funcionando.

## 3. Estructura prevista de esforzados.com

1. **Encabezado y navegación:** identidad Esforzados, servicios, información institucional, contacto y acceso a clientes.
2. **Carrusel principal:** Legal, Edu, Drive, Hub y Chat. Cada servicio tendrá una descripción útil y un enlace a su plataforma.
3. **Servicios y soluciones:** explicación de las funciones y destinatarios de cada plataforma.
4. **Acceso a clientes legales:** acción visible «Consultar mi expediente», que conducirá al acceso seguro de Esforzados Legal.
5. **Información institucional y contacto:** presentación, condiciones y canales oficiales.
6. **Diseño adaptable:** prioridad a teléfonos, computadoras y accesibilidad.

La portada no mostrará nombres, datos o estados de expedientes privados.

## 4. Esforzados Legal

**Subdominio decidido:** `legal.esforzados.com`.

Será una plataforma independiente, conectada al portal principal y preparada para trabajar con ArcadeCloud Drive y herramientas de IA mediante integraciones controladas.

### 4.1 Tres áreas

- **Área pública:** descripción de servicios legales documentales, digitalización, transcripciones, organización de expedientes y acceso al inicio de sesión.
- **Área privada de clientes y familiares:** información de un expediente específico, historial, actuaciones verificadas, trabajo realizado, documentos, transcripciones, evidencias y pendientes autorizados.
- **Área administrativa:** alta y seguimiento de expedientes, registro de actividades, control de publicación, autorizaciones de familiares y auditoría. Debe estar separada de la vista de clientes.

### 4.2 Decisión aprobada sobre familiares

**Cada familiar expresamente autorizado para un expediente podrá consultar todo el contenido marcado como «publicado para ese expediente».**

Reglas de negocio:

1. La autorización se otorga **por persona y por expediente**, nunca por conocer un número de expediente o poseer una URL.
2. Los familiares autorizados de un mismo expediente acceden al **mismo conjunto publicado**; no se requieren permisos diferentes por archivo para esos familiares.
3. Los archivos cargados, importados, procesados o generados por IA **no se publican automáticamente**.
4. Un responsable autorizado revisa y cambia el estado de contenido a «publicado para el expediente» cuando corresponda.
5. Información interna, borradores no aprobados, estrategias de defensa y material sensible que no deba compartirse permanecen fuera del conjunto publicado.
6. «Publicado para el expediente» **no significa público en Internet**: siempre exige sesión y comprobación de autorización.
7. Puede revocarse el acceso de una persona sin borrar el historial, los archivos ni las autorizaciones de otros familiares.
8. Una cuenta autorizada para un expediente no obtiene acceso a ningún otro expediente por ese hecho.
9. Si un documento requiere visibilidad distinta entre familiares, **no debe incluirse indiscriminadamente en el conjunto común publicado**; antes se tendrá que resolver el criterio de autorización.
10. La información especialmente protegida (por ejemplo, datos de menores, testigos o víctimas) requiere evaluación y tratamiento adecuados antes de cualquier publicación.

### 4.3 Lo que verá un cliente

- **Identificación del expediente:** datos que sea apropiado mostrar a esa persona.
- **Proceso judicial:** actuaciones, acuerdos, audiencias y resoluciones con fecha, procedencia y respaldo documental cuando exista.
- **Nuestro trabajo:** solicitudes preparadas/presentadas, digitalizaciones, transcripciones, OCR, análisis y entregables, diferenciados claramente de las actuaciones judiciales.
- **Línea de tiempo:** eventos registrados, fecha y evidencia asociada.
- **Documentos publicados:** PDFs, imágenes, audios, videos y transcripciones, según disponibilidad y revisión.
- **Pendientes y próximas actividades:** sin presentar expectativas o conjeturas como resoluciones judiciales.
- **Notificaciones futuras:** únicamente cuando estén diseñadas e implementadas con control de privacidad.

Se distinguirá explícitamente **«actividad de nuestro equipo»** de **«actuación del órgano jurisdiccional»**. Los datos de estado judicial se registrarán a partir de evidencia verificable; no se inventarán movimientos ni resultados.

### 4.4 Flujo conceptual de publicación

1. Incorporación o registro de documentos/evidencias en el entorno autorizado.
2. Asociación correcta con el expediente correspondiente.
3. Procesamiento documental opcional (digitalización, OCR, transcripción o IA).
4. Revisión humana de exactitud, sensibilidad y permisos.
5. Publicación explícita en el espacio privado del expediente.
6. Consulta por el cliente y los familiares autorizados.
7. Registro de accesos/descargas y posibilidad de revocación.

## 5. Integración prevista con plataformas existentes

- **ArcadeCloud Drive:** custodia y gestión de archivos; Legal consultará únicamente recursos permitidos mediante interfaces autenticadas y autorización del servidor. Nunca se expondrán credenciales AWS ni rutas internas de almacenamiento.
- **MiChat / IA:** posibles funciones de transcripción, OCR, clasificación, búsquedas semánticas (RAG) y apoyo documental. Las respuestas generadas no reemplazan la evidencia y requieren revisión antes de compartirse.
- **Esforzados Hub:** posible integración futura de identidad. No se reutilizarán automáticamente cookies ni sesiones entre subdominios sin un diseño específico de autenticación federada.
- **Edu y demás servicios:** enlaces e integraciones independientes, sin exigir que compartan bases de datos ni repositorios.

Las integraciones anteriores son **objetivos de arquitectura**, no funcionalidades afirmadas como implementadas en Esforzados Legal.

## 6. Principios de seguridad y privacidad

- Autenticación robusta; autorización comprobada en el servidor para **cada** consulta o descarga.
- Aislamiento estricto entre expedientes y entre clientes.
- Acceso privado, mínimo necesario y revocable para familiares.
- Separación entre borradores, documentos internos y contenido publicado.
- Registro auditable de modificaciones, publicaciones, accesos y descargas.
- Descargas autorizadas y temporales; no exponer el almacenamiento directamente.
- Protección de sesiones, prevención de enumeración de expedientes y de ataques comunes a aplicaciones web.
- Versiones y procedencia de documentos; conservación de originales y evidencia.
- Revisión humana previa a divulgar salidas de OCR, transcripción o IA.
- Revisión de secretos y configuraciones privadas antes de desplegar cualquier integración.
- Cumplimiento de obligaciones aplicables de confidencialidad y protección de datos personales, sujeto a revisión jurídica.

**Este repositorio es público. Nunca agregar datos personales de clientes, expedientes reales, credenciales, tokens, secretos, contraseñas, evidencias reservadas ni configuraciones privadas.**

## 7. Límites de este repositorio

`jimmybackend/esforzados` será el proyecto de la **página principal**. No duplicará el backend de ArcadeCloud, el motor de IA ni las herramientas de Hub. Se propone que Legal tenga un repositorio privado independiente cuando se apruebe su creación.

Este documento registra decisiones de producto y arquitectura. **No constituye especificación de tablas, campos, API, despliegue o implementación.** Toda futura estructura técnica deberá basarse en la revisión de los sistemas y esquemas reales.

## 8. Decisiones tomadas

- [x] Crear un repositorio propio para `esforzados.com` (**ya creado**).
- [x] Presentar los cinco servicios: Legal, Edu, Drive, Hub y Chat.
- [x] Mantener **Edu en `portal.esforzados.com`**.
- [x] Diseñar **Legal en `legal.esforzados.com`**, separado del sitio principal.
- [x] Crear una experiencia privada de seguimiento de expedientes para clientes y familiares.
- [x] Permitir que cada familiar autorizado vea **todo el contenido publicado para su expediente**.
- [x] Mantener contenido interno/no publicado fuera de la vista de familiares.
- [x] Continuar **solo en fase de diseño**, sin cambios de aplicación ni despliegue.

## 9. Pendientes de diseño

- [ ] Definir identidad gráfica y contenido específico del carrusel.
- [ ] Identificar el repositorio de Edu, comprobar la disponibilidad de `chat.esforzados.com` y confirmar el proyecto responsable de su despliegue.
- [ ] Diseñar el registro e invitación de clientes y familiares y cómo verificar autorizaciones.
- [ ] Definir quién puede publicar, revisar y revocar contenido en Legal.
- [ ] Definir estados y vocabulario del seguimiento judicial y del trabajo documental.
- [ ] Definir política de documentos sensibles, conservación, auditoría y descargas.
- [ ] Evaluar integraciones reales con ArcadeCloud, MiChat y autenticación de Hub.
- [x] Implementar primera portada y carrusel público como base de diseño; revisar la apariencia tras un despliegue de prueba.
- [ ] Elaborar diseños de pantallas y flujos del **backend de Legal** antes de escribir código.
- [ ] Revisar técnicamente dependencias y seguridad antes de autorizar implementación.

---

> **Regla de trabajo:** primero comprender y aprobar el diseño; después, y solo con autorización, programar, probar e implementar.

## 10. Primera implementación de la portada (25 de octubre de 2026)

Archivos iniciales de la web institucional:

| Archivo | Función |
| --- | --- |
| `index.html` | Portada pública, carrusel de cinco servicios, tarjetas y presentación conceptual de Esforzados Legal |
| `assets/site.css` | Diseño adaptable a móvil, tablet y escritorio, colores y estilos |
| `assets/site.js` | Carrusel navegable por botones, teclado y gestos táctiles; menú móvil |
| `assets/brand.svg` | Ícono SVG local |

### Estado y límites

- La página del repositorio puede abrirse como sitio estático; no requiere PHP, base de datos ni credenciales.
- El carrusel presenta **Legal, Edu, Drive, Hub y Chat**. Los vínculos de los servicios existentes apuntan a sus dominios; su disponibilidad real debe comprobarse independientemente.
- Legal usa un enlace dentro de la propia portada (`#legal`), **no un login ficticio ni un enlace al subdominio que aún no se ha desplegado**.
- La sección de expediente es **una representación ilustrativa**, sin nombres, causas ni archivos reales. No permite acceso a ningún expediente.
- El contacto usa un enlace `mailto:`, sin formularios que recojan información sensible.
- Esta versión no crea ni modifica un sistema de autenticación, permisos, expedientes o APIs.
- El repositorio **no está conectado automáticamente a la publicación de `esforzados.com`**. Fusionar una rama en `main` no significa desplegar la portada en el hosting.
- Antes de conectar el dominio, validar hosting, document root, certificados HTTPS, rutas y copia de seguridad de la web actual para un despliegue reversible.

### Siguientes fases

1. Revisar la portada en pantalla de computadora y de teléfono.
2. Validar la identidad visual definitiva, textos institucionales y datos de contacto.
3. Definir y crear, mediante autorización específica, el repositorio de Esforzados Legal.
4. Diseñar identidad, gestión de clientes, autorizaciones por expediente y revisión/publicación de documentos.
5. Desarrollar y auditar Legal antes de habilitar cualquier acceso a documentos reales.
6. Preparar el despliegue seguro de la nueva portada cuando se apruebe, sin sobrescribir el sitio existente sin respaldo.


## 11. Vista previa en la EC2 pequeña con actualización automática

**Propuesta de publicación:** `preview.esforzados.com`, aislado de `esforzados.com` (sitio actual) y `drive.esforzados.com` (ArcadeCloud).

Se agregan scripts de instalación inicial y autoactualización mediante `systemd` y Nginx. La carpeta pública será **`/var/www/esforzados/current`** (enlace al release activo), con fuente privada en `/var/lib/esforzados/repo`. El repositorio público no se coloca directamente bajo el docroot.

- Manual completo: [Despliegue en EC2](deploy/ec2/README.md).
- Instalación inicial: `deploy/ec2/install.sh` (requiere ejecución autorizada en la EC2).
- Actualizaciones periódicas: `deploy/ec2/update.sh`, servicio y timer con usuario sin privilegios.
- **Cambiar desde la web:** crear/editar PR en GitHub y fusionar a `main`. La EC2 revisa la rama aproximadamente cada cinco minutos y publica una copia estática limitada a HTML, CSS, JS y SVG.
- **No se utiliza** el puente de estado de EC2 como ejecutor de comandos remotos ni se expone un webhook PHP.
- El sitio de prueba será público y no tiene autenticación ni datos de expedientes.
- **Estado de esta etapa:** configuración y código añadidos al repositorio. **La instalación real en la EC2, DNS y HTTPS no están confirmados**.

Antes de exponer el subdominio deben comprobarse la IP pública actual, los servicios Nginx existentes, la resolución DNS y el certificado HTTPS.

## 12. Carrusel Legal — imagen aprobada y puente Google Drive

- **Diseño aprobado:** escena profesional en negro, blanco y caoba con documentación jurídica, símbolos institucionales y una computadora mostrando los servicios de ArcadeCloud/Amazon S3.
- **Fuente de revisión en Google Drive:** `Developer/Esforzados/Disenos Carrusel/carousel-legal.png`.
- **Activo web en este repositorio:** `assets/carousel-legal.png` (PNG original 1672 × 941).
- La diapositiva de Legal muestra la ilustración completa y ofrece el enlace a su sección informativa. En pantallas pequeñas se preserva la imagen y se presenta texto accesible debajo.
- **No existe todavía un portal de expedientes operativo.** El contenido de la imagen es ilustrativo y no acredita movimientos de casos, consultas en tiempo real ni documentos publicados.
- El actualizador de EC2 usa una **lista blanca** de archivos. Se añadió `assets/carousel-legal.png` a `deploy/ec2/update.sh`.

### Actualizar el ejecutable instalado en EC2 (una vez)

El código de `deploy/ec2/update.sh` se almacena en GitHub, pero el servidor lo ejecuta desde una copia instalada en `/usr/local/libexec/esforzados-update`. Los cambios a esa copia **no se instalan automáticamente por el timer**. Para que el servidor publique también la imagen después de la fusión:

```bash
# En la EC2, usando el checkout temporal creado durante la instalación:
git -C /tmp/esforzados-install pull --ff-only origin main
sudo install -o root -g root -m 0755 \
  /tmp/esforzados-install/deploy/ec2/update.sh \
  /usr/local/libexec/esforzados-update
sudo systemctl start esforzados-update.service
sudo systemctl status esforzados-update.service --no-pager
ls -lh /var/www/esforzados/current/assets/carousel-legal.png
```

A partir de esa actualización del ejecutable, los cambios de contenido y esa imagen se publican periódicamente al fusionar en `main`; no hay que modificar otras configuraciones de Nginx o de ArcadeCloud. Para nuevos tipos de archivos será necesario revisar y ampliar la lista blanca de forma controlada.

## 12. Carrusel con imagen original de ArcadeCloud Drive

**Orden actualizado del carrusel principal:** Legal → **Drive** → **Hub** → Edu → Chat.

- **Segunda diapositiva:** imagen original de ArcadeCloud, mostrando Amazon S3 y servicios AWS; no se recreó ni modificó.
- **Fuente verificada:** repositorio `jimmybackend/s3`, archivo `drive/images/home/carousel-01-s3-aws.png`, commit de referencia main al importar.
- **Identidad del archivo:** Git blob SHA `dd7395d4e030ead572a56c4f498a8ecd94ca02b0`, imagen PNG `1916 × 821`.
- **Destino en este repositorio:** `assets/carousel-drive-aws.png`.
- **Presentación:** imagen completa (sin recortes) más enlace a `https://drive.esforzados.com/`. El pie mantiene la descripción accesible en pantallas pequeñas.
- **Prueba automática:** valida que el archivo incorporado conserve los bytes originales y que el orden coincida con los controles del carrusel.
- **Actualización en EC2:** `deploy/ec2/update.sh` ahora copia solamente archivos base y `assets/carousel-*.png`, para que futuras imágenes de carrusel con ese prefijo se publiquen al fusionar `main`. No publica secretos, archivos arbitrarios ni el checkout Git.
- **Paso de migración una sola vez:** como el servicio instalado utiliza una copia independiente en `/usr/local/libexec/esforzados-update`, es necesario actualizar dicha copia tras esta fusión para habilitar el nuevo patrón PNG. Ver `deploy/ec2/README.md`.

La imagen y la diapositiva se encuentran en el **portal principal**. No se cambian la portada ni las funcionalidades del repositorio `jimmybackend/s3`.

## 13. Tercera diapositiva — Esforzados Hub

- **Imagen:** `assets/carousel-hub.png` (1916 × 821), diseño aprobado con flujo de ventas y automatización.
- **Orden:** Legal, Drive, **Hub**, Edu, Chat; Legal mantiene su estilo caoba independiente y Hub conserva colores tecnológicos.
- **Contenido:** campaña, URL corta, landing, lead/CRM, notificaciones, workflow y siguiente paso sugerido por IA. Incluye mención de Mail, ERP, analítica y Chat IA.
- **Acción:** enlace a `https://hub.esforzados.com/` en el pie del banner. Las cifras del diseño son ilustrativas y no corresponden a resultados reales.
- **Origen y revisión:** imagen aprobada por el usuario; copia privada de diseño en Google Drive. Integrada por GitHub Blob SHA `65b98f63b809bcc03b1360e3652b6bf196623898`.
- **EC2:** el actualizador instalado que admite `assets/carousel-*.png` publicará este archivo automáticamente tras fusionar en `main`. Verificar que el servicio use la versión nueva; de lo contrario actualizar el ejecutable una sola vez.


## 14. Carruseles Chat privado y Edu

**Orden final autorizado:** Legal → Drive → Hub → **Chat** → **Edu**.

- **Chat:** `assets/carousel-chat.png` (1916 × 821), Git blob `cc096d418be6c23ec282ccd90ab4b611a5183aba`. Plataforma privada para equipos autorizados que utiliza IA de Amazon Bedrock y archivos de ArcadeCloud Drive, proyectos y transcripciones JSON. El diseño es conceptual, no contiene casos reales. CTA hacia `https://chat.esforzados.com/` (acceso privado).
- **Edu:** `assets/carousel-edu.png` (1916 × 821), Git blob `bee20aa889e64e5a904bee4a54b72f9463026fd2`. Plataforma académica para escuelas y diplomados en línea, con alumnos, calendarios académicos, programas de estudio, tareas, exámenes, boletas y pagos. CTA hacia `https://edu.esforzados.com/`.
- **Origen:** diseños generados y aprobados, subidos a Google Drive `Developer/Esforzados/Disenos Carrusel/` e importados a blobs GitHub conservando sus bytes exactos.
- **Actualización EC2:** el script existente acepta `assets/carousel-*.png`, por lo que los nuevos banners se publican mediante `esforzados-update.service` sin cambiar Nginx ni otros servicios. La ilustración de Chat no implica acceso público a archivos ni conversaciones.


## 15. Identidad visual institucional y contacto (25 de octubre de 2026)

- Dos banners revisados y autorizados, ambos de **1916 × 821 píxeles**. Se mantienen las cinco diapositivas y el orden **Legal → Drive → Hub → Chat → Edu**.
- **Legal:** `assets/carousel-legal.png`, imagen de oficina jurídica caoba que incluye en la pantalla de la computadora la imagen de la tecnología AWS/S3 de ArcadeCloud Drive. SHA Git `466c8edc395df8d3095e0a06d3dc0646da0c270c`.
- **Drive:** `assets/carousel-drive-aws.png`, composición S3/AWS con nueva paleta institucional negro, dorado, café y cedro. SHA Git `c2c089eecbdad852d5fe5b39bfc7f740e12aa27e`.
- Ambas versiones se guardaron en Google Drive, carpeta `Developer/Esforzados/Disenos Carrusel/`, con los nombres `carousel-legal-aprobado-20261025.png` y `carousel-drive-cedro-aprobado-20261025.png`. Se importaron a GitHub conservando los mismos bytes y SHA.
- **Pie:** “Contacto y soporte”, número `+52 55 8645 8862` (enlace `tel:`), `soporte@esforzados.com` (enlace `mailto:`), “Servidor privado de Esforzados.” y copyright centrado.
- El CSS mantiene una proporción panorámica uniforme para Legal y Drive, sin agrandar Legal al rotar el carrusel. El actualizador existente publica automáticamente `assets/carousel-*.png` sin modificar Nginx.

## 16. Carrusel responsivo y footer sin saltos (25 de octubre de 2026)

- `assets/site.css` apila las cinco diapositivas sobre una única celda CSS Grid. Las diapositivas ocultas conservan el atributo `hidden` y `visibility:hidden` para no ser interactivas, pero siguen aportando su altura al cálculo de la cuadrícula. Así la altura del carrusel es constante al avanzar manualmente o por autoplay, aunque varíe la longitud de los pies de imagen.
- Cada imagen original se muestra completa con proporción `1916 / 821` y enlaces intactos a sus respectivos portales. No se reemplazaron PNG ni textos de contacto.
- La página usa un cuerpo flexible con altura mínima de viewport estable (`100svh`), ubicando el footer después del carrusel sin que cambie de posición durante la rotación.
- Ajustes para tabletas y móviles (760 y 380 píxeles): pies de imagen legibles, controles compactos y correo/teléfono capaces de acomodarse sin desbordar.
- Prueba en `tests/check_site.py`: asegura que los controles y las imágenes se conservan, que todas las imágenes declaran la misma proporción y que existen las reglas antisalto y responsivas.
