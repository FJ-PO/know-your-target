# Comparativa

## 3.1 La comparación

| Dato | Lo encontré yo | Lo encontró el agente | ¿Coincide? | Observaciones |
|---|---|---|---|---|
| Registrador del dominio | MarkMonitor | 292 (Amazon Registrar) | No | El 292 es correcto, pero el agente le puso mal el nombre: se inventó Amazon. |
| Fechas del dominio (alta y caducidad) | 1998 / 2027 | 1998 / 2027 | Sí | Igual por los dos lados. |
| Servidores DNS | AWS Route 53 | AWS Route 53 | Sí | Los ns-*.awsdns-*. |
| Servidor de correo (MX) | Google Workspace | Google Workspace | Sí | aspmx.l.google.com. |
| SPF (anti-suplantación) | Zendesk + Google + -all | Zendesk + Google + -all | Sí | -- |
| Proveedor de envío masivo | SendGrid | No lo encontró | No | Omisión del agente. |
| Subdominios en alcance (tinder.com) | Unos 43 (subfinder) | Unos 37 únicos (crt.sh + subfinder) | Parcial | -- |
| Subdominios de gotinder.com | Sí (api, account, images-ssl) | No lo encontró | No | El guard le bloqueó el dominio raíz gotinder.com. |
| account.gotinder.com (EC2 directo, puerto 80) | Sí | No lo encontró | No | No llegó a él. |
| Infraestructura (CDN) | AWS CloudFront | AWS CloudFront | Sí | -- |
| Stack web | React/SPA + Node/Express | nginx + Express | Sí | El agente lo vio por cabeceras, yo con Netcraft. |
| Cabeceras de seguridad | HSTS, CSP, X-Frame, etc. | HSTS, CSP, X-Frame, etc. | Sí | -- |
| Ficheros expuestos (robots.txt) | /sparks, /api, /healthcheck, /events/join | /sparks, /api, /healthcheck, /events/join | Sí | -- |
| Shodan (servicios por IP) | Alguna IP consultada | Todo bloqueado | No | En el scope.txt no hay IPs, así que el guard bloqueó todas las consultas por IP. |

Resumen con números:

| | Yo | El agente |
|---|---|---|
| Subdominios en alcance | Unos 43 | Unos 37 |
| Tiempo | Unas 2 horas | 4 min 37 s |
| Coste | --           | 58 458 tokens de entrada + 9 050 de salida (67 508 en total) |
| Llamadas a herramientas | -- | 49 (15 bloqueadas por el guard) |

El agente encontró casi lo mismo que yo en mucho menos tiempo, pero se dejó cosas fuera y metió un dato inventado.

## 3.2 Los fallos del agente

### Se inventó el registrador

El informe del agente dice: Registrador 292 (Amazon Registrar). Pero en la traza, la herramienta de whois solo devolvió esto: Entidad (registrar) 292.

El 292 es un número de IANA, y ese número es MarkMonitor, no Amazon. 

El modelo vio un número suelto, no supo qué era y rellenó "Amazon Registrar" por su cuenta. Ninguna herramienta le dio la palabra Amazon. Esto es grave porque el prompt le prohíbe escribir datos que no vengan de una herramienta, y aun así lo hizo. 

### Intentos fuera de alcance (bloqueados por el guard)

Hubo 15 intentos bloqueados en la traza. 

Se repiten dos casos:

- Dominio raíz de otros dominios del programa. Intentó buscar subdominios de gotinder.com y le salió BLOQUEADO y lo mismo con tinderops.net, tstaging.com y tinderwebstaging.com. Causa: mis comodines cubren los subdominios pero no el dominio raíz. El guard hizo lo correcto.

- IPs: Intentó Shodan sobre la IP 52.84.150.60 y 7 IPs más, y todas salieron BLOQUEADO. 

  Causa: no hay ninguna IP en mi scope.txt.

## 3.3 Reflexión

¿Qué hizo mejor el agente y qué hice mejor yo?

El agente fue mucho más rápido y muy ordenado: whois, DNS, subdominios y lo demás, sin saltarse pasos y citando la herramienta de cada dato. Yo lo hice mejor en el criterio: supe saltar del comodín *.gotinder.com a subdominios concretos como account.gotinder.com, relacioné las IPs 167.89.x con SendGrid y no me inventé el registrador.

¿Por qué falló?

- El invento del registrador es culpa del modelo, no del prompt ni del scope: el prompt le prohibía inventar y aun así lo hizo.
- Shodan: no metí ninguna IP, así que toda consulta por IP quedó fuera. Si quisiera usar Shodan tendría que autorizar las IPs o los rangos.

¿Me fiaría del informe del agente sin revisarlo?

No. El informe está muy bien presentado y da sensación de ser fiable pero no lo es: coló un "Amazon Registrar" que es falso. 

Siempre tendría que comprobar tres cosas:

1. Que cada dato tenga de verdad una herramienta detrás en la traza.
2. Los datos que el modelo interpreta contrastándolos con la salida tal cual de la herramienta.
3. Lo que falta por culpa del alcance.
