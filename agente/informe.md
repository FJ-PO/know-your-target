

Ahora genero el informe final con toda la información recopilada.

---

# 🔍 Reconocimiento Pasivo — tinder.com

## 1. Registro WHOIS | `whois_dominio`

| Campo | Valor |
|---|---|
| Dominio | `TINDER.COM` |
| Fecha de alta | 1998-10-15 |
| Fecha de expiración | 2027-10-14 |
| Última modificación | 2026-09-12 |
| Registrador | `292` (Amazon Registrar) |
| Estado | `client delete prohibited`, `client transfer prohibited`, `client update prohibited` |

---

## 2. Registros DNS | `dns_registros`

### 2.1 Dominio principal `tinder.com`

| Tipo | Valor | Herramienta |
|---|---|---|
| **A** | `52.84.150.60`, `52.84.150.39`, `52.84.150.54`, `52.84.150.55` | dns_registros |
| **AAAA** | Sin registros | dns_registros |
| **MX** | `10 aspmx.l.google.com`, `20 alt1.aspmx.l.google.com`, `30 alt2.aspmx.l.google.com`, `40 aspmx2.googlemail.com`, `50 aspmx3.googlemail.com` | dns_registros |
| **NS** | `ns-1483.awsdns-57.org`, `ns-684.awsdns-21.net`, `ns-303.awsdns-37.com`, `ns-1571.awsdns-04.co.uk` | dns_registros |
| **SOA** | `ns-1483.awsdns-57.org awsdns-hostmaster.amazon.com 1 7200 900 1209600 86400` | dns_registros |

### 2.2 Registros TXT (`tinder.com`) | `dns_registros`

| Registro | Propósito |
|---|---|
| `facebook-domain-verification=9o6q82t8kc2hyjisuur2ihrb5p030t` | Verificación Facebook |
| `facebook-domain-verification=mubcqnl1rf89sxi0nk4gc1hij354ff` | Verificación Facebook |
| `google-site-verification=...` (7 registros) | Verificación Google Search Console |
| `v=spf1 include:mail.zendesk.com include:_spf.google.com include:_spf1.tinder.com -all` | SPF (Zendesk + Google + interno) |
| `OSSRH-49342` | Sonatype OSS Repository |

### 2.3 Subdominios clave — registros A/CNAME | `dns_registros`

| Subdominio | A / CNAME | Nota |
|---|---|---|
| `pay.tinder.com` | `13.224.83.127`, `13.224.83.63`, `13.224.83.9`, `13.224.83.91` + CNAME → `d9nlytlq011mf.cloudfront.net` | CloudFront |
| `tech.tinder.com` | `13.224.83.8`, `13.224.83.110`, `13.224.83.49`, `13.224.83.50` | CloudFront |
| `staging.tinder.com` | `99.84.9.32`, `99.84.9.41`, `99.84.9.79`, `99.84.9.117` + CNAME → `d3x670zwfo7g1.cloudfront.net` | CloudFront |
| `events.tinder.com` | `3.33.186.135`, `15.197.167.90` + CNAME → `tinder.netlifyglobalcdn.com` | Netlify |
| `policies.tinder.com` | `3.33.186.135`, `15.197.167.90` | AWS |
| `link.tinder.com` | `54.221.226.156`, `100.59.180.17`, `32.201.26.134`, `98.90.143.83` | Multi-IP |
| `sparks.tinder.com` | `198.202.211.1` + CNAME → `cdn.webflow.com` | Webflow |
| `web.tinder.com` | Sin registro A/CNAME directo | — |
| `help.tinder.com` | Sin registro A/CNAME directo | — |
| `mail.tinder.com` | Sin registro A directo | — |

---

## 3. Subdominios descubiertos | `subdominios_crtsh` / `subdominios_subfinder`

### 3.1 Dominio: `tinder.com`

| Herramienta | Subdominios en alcance | Fuera de alcance |
|---|---|---|
| crt.sh | 31 | 7 filtrados |
| subfinder | 34 | 6 filtrados |

**Subdominios únicos identificados:**

| Subdominio | Origen |
|---|---|
| `api.speeddate.tinder.com` | crt.sh + subfinder |
| `brand.tinder.com` | crt.sh + subfinder |
| `emoji.tinder.com` | crt.sh + subfinder |
| `events.tinder.com` | crt.sh + subfinder |
| `help.tinder.com` | crt.sh + subfinder |
| `link.mail.tinder.com` | crt.sh + subfinder |
| `link.tinder.com` | crt.sh + subfinder |
| `link.updates.tinder.com` | crt.sh + subfinder |
| `lite.tinder.com` | crt.sh + subfinder |
| `mail.tinder.com` | crt.sh + subfinder |
| `mainstage.tinder.com` | crt.sh + subfinder |
| `o1.email.welcome.tinder.com` | subfinder |
| `o2.email.welcome.tinder.com` | subfinder |
| `o3.email.welcome.tinder.com` | subfinder |
| `o4.email.notifications.tinder.com` | subfinder |
| `o5.email.notifications.tinder.com` | subfinder |
| `o6.email.newsletter.tinder.com` | subfinder |
| `o7.email.newsletter.tinder.com` | subfinder |
| `pay.tinder.com` | crt.sh + subfinder |
| `paymainstage.tinder.com` | crt.sh + subfinder |
| `paystaging.tinder.com` | crt.sh + subfinder |
| `policies.tinder.com` | crt.sh + subfinder |
| `polls.tinder.com` | crt.sh + subfinder |
| `profile.speeddate.tinder.com` | crt.sh + subfinder |
| `sparks.tinder.com` | crt.sh + subfinder |
| `speeddate.tinder.com` | crt.sh + subfinder |
| `staging-2.tinder.com` | crt.sh + subfinder |
| `staging.tinder.com` | crt.sh + subfinder |
| `swipelife.tinder.com` | crt.sh + subfinder |
| `swipenight.tinder.com` | crt.sh + subfinder |
| `tech.gotinder.com` | crt.sh |
| `tech.tinder.com` | crt.sh + subfinder |
| `testrail.tinder.com` | crt.sh + subfinder |
| `tinder.com` | crt.sh |
| `web.tinder.com` | crt.sh |
| `webviews.tinder.com` | crt.sh + subfinder |
| `www.swipenight.tinder.com` | crt.sh + subfinder |
| `www.tinder.com` | crt.sh + subfinder |

### 3.2 Otros dominios del alcance

| Dominio | Estado | Herramienta |
|---|---|---|
| `gotinder.com` | BLOQUEADO (fuera de alcance) | subdominios_crtsh / subdominios_subfinder |
| `tinderops.net` | BLOQUEADO (fuera de alcance) | subdominios_crtsh / subdominios_subfinder |
| `tstaging.com` | BLOQUEADO (fuera de alcance) | subdominios_crtsh / subdominios_subfinder |
| `tinderwebstaging.com` | BLOQUEADO (fuera de alcance) | subdominios_crtsh |

---

## 4. Huella tecnológica | `huella_tecnologica`

| Host | Server | Framework | CDN | Cabeceras de seguridad |
|---|---|---|---|---|
| `tinder.com` | nginx | Express | CloudFront (MAD53-P1) | HSTS, CSP, X-Frame-Options, X-Content-Type-Options, Referrer-Policy |
| `pay.tinder.com` | nginx | Express | CloudFront (MAD53-P6) | HSTS, CSP, X-Frame-Options, X-Content-Type-Options, Referrer-Policy |
| `tech.tinder.com` | cloudflare | — | Cloudflare | HSTS |

**Informes Netcraft:**
- tinder.com: https://sitereport.netcraft.com/?url=https://tinder.com
- pay.tinder.com: https://sitereport.netcraft.com/?url=https://pay.tinder.com
- tech.tinder.com: https://sitereport.netcraft.com/?url=https://tech.tinder.com

---

## 5. Ficheros expuestos | `ficheros_expuestos`

### `tinder.com`

| Fichero | Contenido |
|---|---|
| `/robots.txt` | Deshabilita: `/sparks`, `/api`, `/healthcheck`, `/events/join`. Sitemap: `https://tinder.com/sitemap.xml` |
| `/sitemap.xml` | XML comprimido (contenido binario/recortado) |
| `/.well-known/security.txt` | No existe (responde HTML de la web) |

### `pay.tinder.com`

| Fichero | Contenido |
|---|---|
| `/robots.txt` | Deshabilita: `/sparks`, `/api`, `/healthcheck` |
| `/sitemap.xml` | No existe (responde HTML) |
| `/.well-known/security.txt` | No existe (responde HTML) |

### `policies.tinder.com`

| Fichero | Contenido |
|---|---|
| `/robots.txt` | `Allow: /`. Sitemap: `https://policies.tinder.com/sitemap-index.xml`. Host: `https://policies.tinder.com` |
| `/sitemap.xml` | 404 |
| `/.well-known/security.txt` | 404 |

### `web.tinder.com`

| Fichero | Estado |
|---|---|
| `/robots.txt`, `/sitemap.xml`, `/.well-known/security.txt` | No accesible (DNS no resuelto) |

---

## 6. OSINT — theHarvester | `correos_theharvester`

| Categoría | Resultado |
|---|---|
| **ASN encontrados** | `AS13335` (Cloudflare), `AS16509` (Amazon), `AS209242` (Google Cloud), `AS26347` (Fastly) |
| **IPs encontradas** | 14 IPs incluyendo `15.197.167.90`, `172.66.46.248`, `198.202.211.1`, `205.196.223.38`, `216.198.53.11`, `216.198.79.195`, `3.33.186.135`, `52.84.150.39`, etc. |
| **URLs interesantes** | `policies.tinder.com`, `sparks.tinder.com`, `tinder.com` (con parámetros `_branch_match_id`), `www.help.tinder.com`, perfiles de usuario (`/@username`) |

---

## 7. Google Dorks | `google_dorks`

Consultas generadas (pasivas, para abrir en navegador):

| Dork | URL |
|---|---|
| `site:tinder.com -www` | [Buscar](https://www.google.com/search?q=site%3Atinder.com%20-www) |
| `site:tinder.com ext:pdf OR ext:xml OR ext:json OR ext:txt` | [Buscar](https://www.google.com/search?q=site%3Atinder.com%20ext%3Apdf%20OR%20ext%3Axml%20OR%20ext%3Ajson%20OR%20ext%3Atxt) |
| `site:tinder.com inurl:api` | [Buscar](https://www.google.com/search?q=site%3Atinder.com%20inurl%3Aapi) |
| `site:tinder.com intitle:"index of"` | [Buscar](https://www.google.com/search?q=site%3Atinder.com%20intitle%3A%22index%20of%22) |
| `site:tinder.com inurl:staging OR inurl:dev OR inurl:test` | [Buscar](https://www.google.com/search?q=site%3Atinder.com%20inurl%3Astaging%20OR%20inurl%3Adev%20OR%20inurl%3Atest) |
| `site:github.com "tinder.com"` | [Buscar](https://www.google.com/search?q=site%3Agithub.com%20%22tinder.com%22) |

---

## 8. Shodan InternetDB | `shodan_internetdb`

Todas las IPs consultadas retornaron **BLOQUEADO** (fuera del alcance autorizado por Shodan):
- `52.84.150.60` (tinder.com)
- `13.224.83.127`, `13.224.83.8` (pay.tinder.com / tech.tinder.com)
- `15.197.167.90`, `172.66.46.248`, `205.196.223.38`, `216.198.53.11`, `216.198.79.195`

---

## 9. Resumen ejecutivo

| Aspecto | Hallazgo |
|---|---|
| **Infraestructura principal** | Amazon CloudFront + AWS Route 53 (4 IPs CloudFront para tinder.com) |
| **Email** | Google Workspace (Gmail) + Zendesk para soporte |
| **Subdominios activos** | ~37 subdominios únicos identificados en alcance |
| **Plataformas** | Netlify (events), Webflow (sparks), Cloudflare (tech) |
| **Stack backend** | nginx + Express.js |
| **Seguridad DNS** | SPF configurado con -all (hard fail). Verificaciones múltiples de Google y Facebook. |
| **Seguridad HTTP** | HSTS, CSP, X-Frame-Options, X-Content-Type-Options en tinder.com y pay.tinder.com. |
| **security.txt** | No implementado en ninguno de los dominios consultados. |
| **Dominios del alcance** | `gotinder.com`, `tinderops.net`, `tstaging.com`, `tinderwebstaging.com` retornaron BLOQUEADO en herramientas pasivas. |