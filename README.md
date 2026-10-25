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
| Esforzados Chat | Dominio por confirmar | Proyecto existente de chat/IA por vincular | Integración por definir |

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
- [ ] Identificar y confirmar el repositorio de Edu y la ubicación definitiva de Chat.
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

