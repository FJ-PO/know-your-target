# Alcance - Tinder Bug Bounty Program

- **Programa:** Tinder HackerOne
- **Enlace:** https://hackerone.com/tinder
- **Fecha de consulta:** 2026-10-28

## Dentro del alcance

| Activo | Tipo | Recompensa |
|--------|------|-----------|
| *.tinder.com | Wildcard | Sí |
| *.gotinder.com | Wildcard | Sí |
| *.tinderops.net | Wildcard | Sí |
| *.tstaging.com | Wildcard | Sí |
| *.tstaging.tools | Wildcard | Sí |
| *.tinderwebstaging.com | Wildcard | Sí |
| com.tinder | App Android | Sí |
| 547702041 | App iOS | Sí |

## Fuera del alcance 

- go.tinder.com
- www.help.tinder.com
- gotinder.imgix.net
- console.gotinder.com
- Subdominios de AppsFlyer

## Reglas que afectan a este proyecto

- **¿Herramientas automáticas?** Permitidas, pero prohibido causar daño a los sistemas.
- **¿Límite de peticiones?** No se fija un número especifico, pero exigen no degradar servicios, prohibido DoS y no dejar ningún sistema más vulnerable de como se encontró.
- **¿Prohíbe contactar con empleados o usuarios?** Sí. Prohibida la ingeniería social y manipular,filtrar,destruir datos de usuarios.
- **Requisitos de identificación (para pruebas activas, NO aplican a OSINT pasivo):**
  - Registrarse con correo @wearehackerone.com.
  - Incluir la cabecera HTTP x-hackerone: <usuario> en todo el tráfico de pruebas.
  - Ser mayor de 18 si se prueba con una cuenta de Tinder.
- **Confidencialidad:** la información obtenida es confidencial, no se divulga a terceros.
- **No escalar privilegios** ni explorar más allá de lo mínimo para probar el hallazgo.

### Regla principal del proyecto
Si aparece algo grave: no se explota ni se copia. Se anota sin el dato sensible, se avisa al profesor y, si procede, se informa por el canal del programa.

## Áreas de interés del programa 
Datos sensibles de usuario expuestos, account takeover, edición de datos de otro usuario, forzar un match, exposición de ubicación precisa del usuario.
