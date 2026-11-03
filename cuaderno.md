# Cuaderno de trabajo - Know Your Target - Tinder

Formato de cada entrada: cuándo - objetivo y si está en alcance - qué hice - qué salió - siguiente paso.

2026-10-28 10:40 - objetivo: programa Tinder en HackerOne consulta: API pública de HackerOne para leer el scope estructurado y la política -> in-scope: 6 comodines *.tinder.com, *.gotinder.com, *.tinderops.net, .tstaging.com, .tstaging.tools, .tinderwebstaging.com + app Android com.tinder + app iOS 547702041.     out-of-scope: go.tinder.com, www.help.tinder.com, gotinder.imgix.net, console.gotinder.com, AppsFlyer.
Programa bug bounty abierto. Reglas clave: solo pasivo en este proyecto, nada de ingeniería social, no DoS.
siguiente: whois de tinder.com (registrador, fechas, servidores DNS)

2026-10-28 10:45 - objetivo: tinder.com

WHOIS web sobre HTTPS
-> Registrante: Match Group, LLC (US). Registrar: MarkMonitor Inc. (corporativo).
-> Creado 1998-10-15; actualizado 2026-09-12; expira 2027-10-14.
-> Name servers: ns-1483.awsdns-57.org / ns-1571.awsdns-04.co.uk / ns-303.awsdns-37.com / ns-684.awsdns-21.net = AWS Route 53.
-> IP apex 52.84.150.55 (+ .54/.39/.60) = rango AWS CloudFront (CDN delante del apex).
-> Domain Status: clientDelete/Transfer/UpdateProhibited (locks anti-secuestro).
conclusiones: infraestructura AWS (Route53 + CloudFront); apex blindado -> el interés estará en subdominios y en staging (tstaging.*).
siguiente: Técnica 2 DNS con dig: NS, MX, TXT (SPF/DMARC) de tinder.com.

2026-10-28 10:50 - objetivo: tinder.com - Técnica 5 (ficheros expuestos)
$ curl https://tinder.com/robots.txt
-> Disallow: /sparks, /api, /healthcheck, /events/join , Sitemap: https://tinder.com/sitemap.xml
$ curl https://tinder.com/sitemap.xml
-> sitemaps por idioma + páginas estáticas, subdominios citados: policies.tinder.com (in), emoji.tinder.com (in), www.help.tinder.com (out)
$ curl https://tinder.com/.well-known/security.txt
-> devuelve el HTML de la SPA, no un security.txt.
del HTML de la portada:
-> SPA React (webpack: main/vendor/tinderapp/pc-webpack-runtime), Atomic CSS.
-> subdominios en alcance: api.gotinder.com (backend/API), images-ssl.gotinder.com, account.gotinder.com (portal datos).
-> terceros: Google OAuth, Facebook Login , FaceTec, Spotify, LINE, Noonlight.
-> OOS/terceros: gotinder.imgix.net, AppsFlyer, www.help.tinder.com.
-> schema.org: legalName "Tinder Inc.", parentOrganization "Match Group"; redes: instagram/tiktok/youtube/twitter/facebook/linkedin.
puntos de interés detectados: api.gotinder.com + /api + /healthcheck , portal account.gotinder.com , staging (*.tstaging.*).
siguiente: Técnica 3 completa (subfinder + crt.sh) sobre tinder.com y gotinder.com para enumerar subdominios en alcance.

2026-10-28 11:00 - objetivo: tinder.com - Técnica 3 (subdominios) - subfinder
$ subfinder -silent -d tinder.com | sort -u
-> 43 subdominios. Todos .tinder.com = en alcance menos go.tinder.com y www.help.tinder.com, help.tinder.com como OOS.
destacados:
 staging.tinder.com, staging-2.tinder.com, mainstage.tinder.com, paymainstage.tinder.com, paystaging.tinder.com  -> entornos staging/pre-prod, testrail.tinder.com  -> TestRail (gestion QA) interna expuesta
 tech.tinder.com, pay.tinder.com, api.speeddate.tinder.com, sparks.tinder.com, webviews/web/lite/open.tinder.com
  features: matchmaker, polls, events, party, speeddate, swipenight, swipelife, brand
  correo: o1..o7.email.*.tinder.com, mail.tinder.com, link.*.tinder.com
3 mejores objetivos fase activa: staging testrail.tinder.com  api.speeddate.tinder.com
siguiente: subfinder sobre gotinder.com + crt.sh (tinder.com, gotinder.com, tstaging.com) para completar y pillar staging de los otros dominios.

2026-10-28 11:15 - objetivo: tinder.com - Técnica 2 (DNS) - dig
$ dig +short NS tinder.com -> ns-*.awsdns-* = AWS Route 53.
$ dig +short MX tinder.com -> aspmx.l.google.com = Google Workspace gestiona el correo corporativo.
$ dig +short TXT tinder.com:
  -> SPF: "v=spf1 include:mail.zendesk.com include:_spf.google.com include:_spf1.tinder.com -all"
     proveedores de correo: Zendesk, Google, + SPF anidado propio. Politica -all (estricta).
  -> facebook-domain-verification = dominio verificado en Meta.
  -> varios google-site-verification.
$ dig +short TXT _spf1.tinder.com -> "v=spf1 ip4:54.236.202.181 ip4:54.236.222.140 ~all"
  -> 2 IPs AWS EC2 para correo transaccional directo.
$ dig +short TXT _dmarc.tinder.com -> "v=DMARC1; p=reject; pct=100; rua=mailto:...@ag.us.dmarcian.com"
  -> DMARC p=reject al 100%, informes a dmarcian. Postura anti-spoofing solida.

2026-10-28 11:30 - objetivo: varios subdominios - Técnica 6 (servicios expuestos) - Shodan InternetDB
metodo: dig +short A host para sacar IP, luego curl https://internetdb.shodan.io/ IP.
$ apex 52.84.150.55 -> CloudFront (d32crgxhn81thf.cloudfront.net), 80/443.
$ 54.236.202.181 / .222.140 -> "No information available" en Shodan.
$ api.gotinder.com    -> 65.8.202.109  = CloudFront, 80/443, sin vulns.
$ staging.tinder.com  -> 99.84.9.41    = CloudFront, 80/443, sin vulns.
$ tech.tinder.com     -> 13.224.83.49  = CloudFront, sin vulns.
$ pay.tinder.com      -> 13.224.83.63  = CloudFront, sin vulns.
$ account.gotinder.com-> 98.80.62.9    = EC2 DIRECTO (ec2-98-80-62-9.compute-1.amazonaws.com), SOLO puerto 80, sin vulns.
$ testrail.tinder.com -> sin A (CNAME, TestRail gestionado externo probablemente).
La mayoria del perimetro va tras CloudFront, pero account.gotinder.com apunta a una instancia EC2
expuesta directa, sin el CDN delante, y en puerto 80. Portal de datos de cuenta -> punto de interes para fase activa.
siguiente: Técnica 4 (huella tecnologica, Netcraft) o Técnica 7 (Google dorks). Pendientes tambien 8 (correos).

2026-10-28 11:45 · objetivo: www.tinder.com · Técnica 4 (huella tecnologica) - Netcraft
fuente: sitereport.netcraft.com/?url=https://www.tinder.com informe publico de Netcraft.
tecnologias detectadas:

  - Cloud/CDN: AWS CloudFront.
  - App server: Express.js -> backend/edge en Node.js .
  - Cliente: JavaScript + Google Hosted Libraries.
  - Transporte: SSL/TLS, Gzip.
  - Cabeceras seguridad: HSTS, X-Frame-Options, X-XSS-Protection, X-Content-Type-Options, Referrer-Policy, CSP -> web securizada.
  - Doctype HTML5 + viewport.
conclusiones: stack confirmado = AWS CloudFront + Node/Express + SPA JS; postura de cabeceras de seguridad completa.
siguiente: Técnica 7 (Google dorks) y Técnica 8 (correos).

2026-10-28 12:00 - objetivo: comodines en alcance - Técnica 7
dorks ejecutados en Google:
  site:tinder.com -www | site:gotinder.com | site:tstaging.com | site:tinderops.net
  site:tinder.com ext:pdf|xml|json|txt | site:tinder.com inurl:api | intitle:"index of"
  site:inurl:staging|dev|test | site:github.com "gotinder.com"
hallazgos:

  - subdominios indexados por Google (site:tinder.com -www): help.tinder.com (Centro de ayuda Zendesk, ruta /hc/ -> confirma
    include:mail.zendesk.com del SPF, policies.tinder.com (/terms, /contact - legal), events.tinder.com Tinder Events, quedadas presenciales. El resto son paginas de marketing (/about, /places, /destinos, /download, /faq, /giftcard).
  - github.com/fbessez/tinder -> doc no oficial de la API api.gotinder.com (2019).
  - correos citados bajo gotinder.com: help@, partners@, press@, adsales@, stories@ -> pista Técnica 8.
  - re-confirmados: api.gotinder.com, images-ssl.gotinder.com.
  Conclusión: Google solo indexa lo publico.
    siguiente: Técnica 8 (correos: theHarvester/Hunter.io).

2026-10-28 12:40 - objetivo: tinder.com + gotinder.com - Técnica 8 (correos y personas) - theHarvester
herramienta: theHarvester 5.0.0
$ theHarvester -d tinder.com   -b crtsh,duckduckgo,otx,hackertarget,urlscan,rapiddns -> 42 hosts, 24 IPs, 0 correos, 0 personas.
$ theHarvester -d gotinder.com -b (idem) -> 68 hosts, 47 IPs, 0 correos, 0 personas.
infraestructura de correo deducida de las IPs/hosts:

  - 167.89.74.x / 167.89.76.x = rango SendGrid -> hosts o1..o7.email.*.tinder.com, o28..o36.email.gotinder.com.
  - Google Workspace = buzones corporativos.
  - AWS EC2 propio = transaccional.
buzones funcionales: help@, press@, partners@, adsales@, stories@ gotinder.com.
