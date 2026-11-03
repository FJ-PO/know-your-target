# Mapa para la fase activa - Tinder

**Programa:** Tinder en HackerOne - https://hackerone.com/tinder



## 1. Resumen

He elegido Tinder porque tiene un programa de bug bounty público y con un alcance muy amplio. Eso da mucho terreno para hacer reconocimiento.

La idea de esta parte no es atacar nada, sino mirar desde fuera y hacerme una idea de cómo está montado Tinder, qué dominios tienen, dónde están alojados, qué tecnologías usan y por dónde podría empezar a mirar un atacante. Todo con herramientas que consultan datos públicos.

Lo que más me ha llamado la atención en general es que la web pública está bastante bien protegida va por detrás de un CDN de Amazon, tiene buenas cabeceras de seguridad y el correo está bien configurado contra suplantación, pero por otro lado hay bastantes subdominios de pruebas y herramientas internas que se pueden descubrir desde fuera.

|  | Técnica | Para qué sirve | Herramienta |
|---|---------|----------------|-------------|
| 1 | WHOIS | Ver de quién es el dominio y dónde está | WHOIS por web |
| 2 | DNS | Ver servidores, correo y configuración | dig |
| 3 | Subdominios | Encontrar todos los subdominios | subfinder |
| 4 | Huella tecnológica | Saber qué tecnologías usan | Netcraft |
| 5 | Ficheros expuestos | robots.txt, sitemap, security.txt | navegador |
| 6 | Servicios expuestos | Qué puertos o servicios se ven desde internet | InternetDB |
| 7 | Google dorks | Qué tiene indexado Google | Google |
| 8 | Correos y personas | Buscar emails o empleados | theHarvester |



## 2. Dominios y subdominios

### Dominios principales (todos dentro del alcance)

| Dominio | Para qué parece que lo usan |
|---------|------------------------------|
| tinder.com | Web principal y muchos servicios de cara al usuario |
| gotinder.com | Backend / API y servicios internos |
| tinderops.net | Operaciones e infraestructura |
| tstaging.com | Entorno de pruebas |
| tstaging.tools | Herramientas internas de pruebas |
| tinderwebstaging.com | Pruebas de la web |

Fuera de alcance : go.tinder.com, www.help.tinder.com, gotinder.imgix.net, console.gotinder.com y los subdominios de AppsFlyer.

### Subdominios más interesantes que he encontrado

Con subfinder saqué unos 40 subdominios solo de tinder.com. No los pongo todos, solo los que me parecen relevantes:

**Entornos de pruebas:**

- staging.tinder.com, staging-2.tinder.com
- mainstage.tinder.com
- paystaging.tinder.com, paymainstage.tinder.com 

**Herramientas internas:**

- testrail.tinder.com - TestRail es una herramienta para gestionar pruebas de QA
- tech.tinder.com

**API y funciones de la app:**
- api.gotinder.com - la API principal
- api.speeddate.tinder.com, speeddate.tinder.com, profile.speeddate.tinder.com
- sparks.tinder.com, matchmaker.tinder.com, polls.tinder.com, party.tinder.com, swipenight.tinder.com, events.tinder.com

**Datos de usuario y legal**

- account.gotinder.com - portal de datos de cuenta 
- policies.tinder.com - términos y política

**Correo :**

- o1.email... hasta o7.email...tinder.com y o28–o36.email.gotinder.com
- mail.tinder.com, link.tinder.com, notifications.tinder.com, newsletter.tinder.com



## 3. Infraestructura 

Casi todo apunta a Amazon Web Services:

- **DNS:** lo llevan con WS Route 53 los servidores de nombres son .awsdns-.
- **Web / CDN:** la web va por detrás de AWS CloudFront, que es una red de distribución de contenido. Esto significa que no hablas directamente con sus servidores, sino con los de Amazon, que hacen de intermediario y de escudo.
- **Tecnología de la web:** es una web moderna tipo SPA hecha con React, y por detrás usan Node.js. Esto lo vi con Netcraft.
- **Cabeceras de seguridad:** tienen puestas casi todas las recomendadas, o sea que la web pública está bien protegida en ese sentido.

**Datos del dominio (WHOIS):**

- El dominio es de Match Group la empresa dueña de Tinder y lo gestiona el registrador corporativo MarkMonitor.
- Está registrado desde 1998 y tiene candados anti-robo de dominio puestos.



## 4. Correos y personas

Tinder no deja ver correos de empleados ni nombres por medios pasivos. Con theHarvester busqué en tinder.com y gotinder.com y no salió ningún email ni ninguna persona.

Lo que si he podido descubrir es cómo tienen montado el correo:

| Proveedor | Para qué lo usan |
|-----------|------------------|
| **Google Workspace** | El correo de los empleados @tinder.com lo lleva Google |
| **Zendesk** | El soporte / centro de ayuda help.tinder.com |
| **SendGrid** | El envío masivo de correos a usuarios |
| **AWS** | Correos automáticos |

También tienen la configuración anti-suplantación del correo muy bien puesta: el DMARC está en modo reject, que es el más estricto, así que es difícil mandar correos falsos haciéndose pasar por @tinder.com.

Buzones de contacto que aparecen en fuentes públicas: help@, press@, partners@, adsales@, stories@.



## 5. Tres puntos de interés 

### 1. Los entornos de pruebas, sobre todo los de pagos
staging.tinder.com, mainstage.tinder.com, paystaging.tinder.com, paymainstage.tinder.com

**Por qué:** los entornos de pruebas suelen estar peor cuidados que el de producción porque no es el de verdad. Y hay dos que son de pagos, que es una zona sensible. Un fallo en un sitio así podría tener bastante impacto.

### 2. account.gotinder.com - el portal de datos de cuenta
**Por qué:** cuando miré los servicios expuestos con Shodan, casi todos los subdominios iban por detrás del CDN de Amazon, pero este no apunta directamente a un servidor de Amazon sin el CDN delante, y además por el puerto 80. Que vaya sin nada y además sea el portal de datos personales de la cuenta hace que sea un objetivo para revisar.

### 3. testrail.tinder.com y api.gotinder.com
**Por qué:** testrail es una herramienta interna de gestión de pruebas, que se vea desde fuera es raro, y ese tipo de paneles a veces tienen logins débiles o filtran información de cómo trabaja la empresa por dentro. Y api.gotinder.com es la API que usa la app, es por donde pasan los datos, así que es el mejor sitio para buscar fallos como acceder a datos de otro usuario.
