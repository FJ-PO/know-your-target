"""Herramientas iniciales de reconocimiento. AQUÍ PUEDES AÑADIR LAS TUYAS.

WHOIS (whois.py), DNS y crt.sh ya están implementadas y activas en lanzar.py.
DNS y crt.sh proceden de la solución del profesor (herramientas/recon.py).

Para ampliar: una tarea por función, @protegida, sin shell, con timeout,
salida recortada, errores como texto y resultados filtrados por el alcance.
Importa tu nueva función en lanzar.py y añádela a HERRAMIENTAS.

Ideas: subdominios_subfinder, wayback_urls, correos (theHarvester / hunter.io),
infraestructura_ip, correo_postura (SPF/DMARC/MTA-STS/CAA), urlscan, shodan_host.
"""

import json
import subprocess
import urllib.error
import urllib.parse
import urllib.request

from guard import protegida, filtrar
from whois import recortar

UA = "aap-recon/1.0 (educativo; IES Rafael Alberti)"
TIPOS_DNS = {"A", "AAAA", "MX", "NS", "TXT", "CNAME", "SOA"}


def _http(url: str, timeout: int = 30) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


@protegida(objetivo="dominio")
def dns_registros(dominio: str, tipo: str = "A") -> str:
    """Consulta registros DNS de un dominio. tipo: A, AAAA, MX, NS, TXT, CNAME o SOA.
    Devuelve los valores, uno por línea."""
    tipo = tipo.upper()
    if tipo not in TIPOS_DNS:
        return f"ERROR: tipo DNS no válido ({tipo}). Usa uno de: {', '.join(sorted(TIPOS_DNS))}."
    try:
        r = subprocess.run(["dig", "+short", tipo, dominio],
                           capture_output=True, text=True, timeout=20)
    except subprocess.TimeoutExpired:
        return "ERROR: dig no respondió en 20 segundos."
    except OSError as e:
        return recortar(f"ERROR: no se pudo ejecutar dig: {e}")
    if r.returncode != 0:
        return recortar(f"ERROR: dig falló ({r.returncode}): {r.stderr.strip() or 'sin detalles'}")
    salida = recortar(r.stdout.strip())
    return salida or f"Sin registros {tipo} para {dominio}."


@protegida(objetivo="dominio")
def subdominios_crtsh(dominio: str) -> str:
    """Enumera subdominios de un dominio por transparencia de certificados (crt.sh).
    Pasivo: no toca el objetivo. Devuelve solo los subdominios dentro del alcance."""
    url = f"https://crt.sh/?q=%25.{urllib.parse.quote(dominio)}&output=json"
    try:
        datos = json.loads(_http(url, timeout=90))
    except Exception as e:
        return (f"ERROR: crt.sh no respondió ({e}). crt.sh suele ir lento; "
                "puedes reintentar más tarde o añadir otra fuente de subdominios.")
    if not isinstance(datos, list) or any(
        not isinstance(fila, dict) or not isinstance(fila.get("name_value"), str)
        for fila in datos
    ):
        return "ERROR: crt.sh devolvió un formato de certificados inesperado."
    nombres = set()
    for fila in datos:
        for n in str(fila.get("name_value", "")).splitlines():
            n = n.strip().lstrip("*.").lower()
            if n:
                nombres.add(n)
    dentro, fuera = filtrar(sorted(nombres))
    cab = f"{len(dentro)} subdominios en alcance ({fuera} filtrados por estar fuera):\n"
    return recortar(cab + "\n".join(dentro))


@protegida(objetivo="ip")
def shodan_internetdb(ip: str) -> str:
    """Consulta Shodan InternetDB sobre una IP: puertos abiertos, hostnames,
    CPEs (tecnologías), etiquetas y CVEs conocidas. Pasivo y GRATUITO: los datos
    ya están indexados por Shodan y la API no necesita clave. Pásale una IP
    (resuélvela antes con dns_registros tipo A)."""
    url = f"https://internetdb.shodan.io/{urllib.parse.quote(ip)}"
    try:
        datos = json.loads(_http(url, timeout=30))
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return f"Shodan InternetDB no tiene información indexada para {ip}."
        if e.code == 429:
            return "ERROR: Shodan InternetDB limitó la tasa (HTTP 429). Reintenta en unos segundos."
        return f"ERROR: Shodan InternetDB devolvió HTTP {e.code}."
    except Exception as e:
        return f"ERROR: no se pudo consultar Shodan InternetDB ({e})."
    if not isinstance(datos, dict):
        return "ERROR: Shodan InternetDB devolvió un formato inesperado."

    lineas = [f"IP: {datos.get('ip', ip)}"]
    for etiqueta, campo in (("Puertos", "ports"), ("Hostnames", "hostnames"),
                            ("Tecnologías (CPE)", "cpes"), ("Etiquetas", "tags"),
                            ("CVEs", "vulns")):
        valores = datos.get(campo) or []
        if valores:
            lineas.append(f"{etiqueta}: " + ", ".join(str(v) for v in valores))
    if len(lineas) == 1:
        return f"Shodan InternetDB no reporta datos para {ip}."
    return recortar("\n".join(lineas))


@protegida(objetivo="dominio")
def subdominios_subfinder(dominio: str) -> str:
    """Enumera subdominios de un dominio con subfinder (fuentes pasivas de OSINT).
    Pasivo: no toca el objetivo. Devuelve solo los subdominios dentro del alcance."""
    try:
        r = subprocess.run(["subfinder", "-silent", "-d", dominio],
                           capture_output=True, text=True, timeout=120)
    except subprocess.TimeoutExpired:
        return "ERROR: subfinder no respondió en 120 segundos."
    except FileNotFoundError:
        return "ERROR: subfinder no está instalado."
    except OSError as e:
        return recortar(f"ERROR: no se pudo ejecutar subfinder: {e}")
    if r.returncode != 0:
        return recortar(f"ERROR: subfinder falló ({r.returncode}): {r.stderr.strip() or 'sin detalles'}")
    nombres = {n.strip().lstrip("*.").lower() for n in r.stdout.splitlines() if n.strip()}
    if not nombres:
        return f"subfinder no encontró subdominios para {dominio}."
    dentro, fuera = filtrar(sorted(nombres))
    cab = f"{len(dentro)} subdominios en alcance ({fuera} filtrados por estar fuera):\n"
    return recortar(cab + "\n".join(dentro))


@protegida(objetivo="dominio")
def ficheros_expuestos(dominio: str) -> str:
    """Recupera ficheros públicos estándar del sitio: /robots.txt, /sitemap.xml y
    /.well-known/security.txt. OJO: hace 1 petición a CADA ruta del PROPIO objetivo
    (no es pasivo puro). Útil para ver rutas ocultas, mapas del sitio y contacto de
    seguridad. Devuelve el contenido recortado de cada fichero que exista."""
    base = f"https://{normalizar_host(dominio)}"
    rutas = ["/robots.txt", "/sitemap.xml", "/.well-known/security.txt"]
    bloques = []
    for ruta in rutas:
        try:
            cuerpo = _http(base + ruta, timeout=20)
        except urllib.error.HTTPError as e:
            bloques.append(f"### {ruta}\n(HTTP {e.code})")
            continue
        except Exception as e:
            bloques.append(f"### {ruta}\n(no accesible: {e})")
            continue
        cuerpo = cuerpo.strip()
        if "<html" in cuerpo[:200].lower():
            bloques.append(f"### {ruta}\n(devuelve HTML de la web, no el fichero: probablemente no existe)")
        else:
            bloques.append(f"### {ruta}\n{recortar(cuerpo, 800)}")
    return recortar("\n\n".join(bloques))


@protegida(objetivo="dominio")
def huella_tecnologica(dominio: str) -> str:
    """Huella tecnológica del sitio. OJO: hace 1 petición al PROPIO objetivo para
    leer sus cabeceras HTTP (servidor, framework, CDN, cabeceras de seguridad), y
    además devuelve el enlace al informe público de Netcraft para profundizar sin
    tocar el objetivo. Pásale el dominio o host exacto."""
    host = normalizar_host(dominio)
    url = f"https://{host}/"
    reveladoras = ("server", "x-powered-by", "via", "x-cache", "x-amz-cf-id",
                   "x-amz-cf-pop", "x-served-by", "x-aspnet-version")
    seguridad = ("strict-transport-security", "content-security-policy",
                 "x-frame-options", "x-content-type-options", "referrer-policy")
    lineas = []
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=20) as r:
            cab = {k.lower(): v for k, v in r.headers.items()}
        lineas.append("Tecnología (cabeceras):")
        for h in reveladoras:
            if cab.get(h):
                lineas.append(f"  {h}: {cab[h]}")
        presentes = [h for h in seguridad if h in cab]
        lineas.append("Cabeceras de seguridad presentes: " +
                      (", ".join(presentes) if presentes else "ninguna"))
    except Exception as e:
        lineas.append(f"No se pudieron leer las cabeceras de {url} ({e}).")
    lineas.append(f"Informe Netcraft (abrir en navegador): "
                  f"https://sitereport.netcraft.com/?url=https://{host}")
    return recortar("\n".join(lineas))


@protegida(objetivo="dominio")
def google_dorks(dominio: str) -> str:
    """Genera consultas (Google dorks) para encontrar ficheros, subdominios y
    rutas indexadas del dominio. NO consulta Google (lo bloquea el scraping): te
    devuelve las URLs de búsqueda listas para abrir en el navegador. Pasivo."""
    d = normalizar_host(dominio)
    dorks = [
        f"site:{d} -www",
        f"site:{d} ext:pdf OR ext:xml OR ext:json OR ext:txt",
        f"site:{d} inurl:api",
        f'site:{d} intitle:"index of"',
        f"site:{d} inurl:staging OR inurl:dev OR inurl:test",
        f'site:github.com "{d}"',
    ]
    lineas = [f"Dorks para {d} (ábrelos en el navegador):"]
    for q in dorks:
        lineas.append(f"  {q}")
        lineas.append(f"    https://www.google.com/search?q={urllib.parse.quote(q)}")
    return recortar("\n".join(lineas))


@protegida(objetivo="dominio")
def correos_theharvester(dominio: str) -> str:
    """Busca correos, hosts y personas del dominio con theHarvester usando solo
    fuentes OSINT pasivas (crt.sh, DuckDuckGo, OTX, HackerTarget, urlscan, RapidDNS).
    Pasivo: no toca el objetivo. Devuelve el resumen recortado de theHarvester."""
    fuentes = "crtsh,duckduckgo,otx,hackertarget,urlscan,rapiddns"
    try:
        r = subprocess.run(["theHarvester", "-d", dominio, "-b", fuentes],
                           capture_output=True, text=True, timeout=240)
    except subprocess.TimeoutExpired:
        return "ERROR: theHarvester no respondió en 240 segundos."
    except FileNotFoundError:
        return "ERROR: theHarvester no está instalado."
    except OSError as e:
        return recortar(f"ERROR: no se pudo ejecutar theHarvester: {e}")
    salida = (r.stdout or "").strip()
    if not salida:
        return recortar(f"theHarvester no devolvió datos. stderr: {r.stderr.strip() or 'sin detalles'}")
    return recortar(salida)


def normalizar_host(objetivo: str) -> str:
    """Deja un host limpio (sin esquema, ruta ni puerto) para construir URLs."""
    t = objetivo.strip().lower()
    if "://" in t:
        t = t.split("://", 1)[1]
    t = t.split("/", 1)[0].split("?", 1)[0].split("#", 1)[0]
    if t.count(":") == 1 and not t.startswith("["):
        t = t.split(":", 1)[0]
    return t.rstrip(".")
