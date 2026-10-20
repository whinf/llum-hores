# Hora Verda · precio de la luz por horas

Web estática en castellano, catalán e inglés con:
- el precio de la luz (PVPC) por horas de hoy y de mañana;
- las mejores franjas para usar cada electrodoméstico;
- el porcentaje de electricidad renovable y las emisiones de CO₂.

Se actualiza sola con GitHub Actions y se publica en GitHub Pages. Funciona sin servidor, sin base de datos, sin dependencias y sin cookies.

## Cómo funciona

- `src/build.py` descarga de Red Eléctrica (REE) lo que falte, lo guarda en `data/AAAA/AAAA-MM-DD.json` y genera la web en `_site/`.
- `.github/workflows/build.yml` lo ejecuta varias veces al día:
  - después de medianoche;
  - cada hora entre las 18:35 y las 21:35 UTC, para recoger los precios de mañana;
  - por la mañana, para el mix de generación de ayer.
- Los datos nuevos se guardan con un commit automático y la web se publica.
- Si a las 22:30 faltan los precios de mañana, o falta el día de hoy, el workflow falla y GitHub te envía un email.
- `/api/v1/latest.json` publica los datos de hoy y de mañana en JSON. Lo usa la web de Cerdanyola y cualquiera puede reutilizarlo.

## Comandos locales (Python 3.12 o superior, sin instalar nada)

```bash
python -m unittest discover tests
```

```bash
python src/build.py
```

```bash
python src/build.py --offline
```

```bash
python -m http.server 8000 -d _site
```

Para cargar el histórico desde una fecha: `python src/build.py --backfill 2025-01-01`.

## Configuración (`config.json`)

- `site_name`: nombre de la web.
- `donate_url`: enlace de donación (Ko-fi o GitHub Sponsors). Si está vacío, no se muestra el botón.
- `owner`: tus datos para el aviso legal. Solo son necesarios si la web genera ingresos (ley LSSI).
- `appliances`: duración y consumo de cada electrodoméstico.
- `site_url`: solo se usa en local. En GitHub se toma automáticamente la URL de Pages, también cuando hay dominio propio.

## Datos y licencias

Los precios, la generación y las emisiones son de Red Eléctrica (apidatos.ree.es y el archivo 70 de esios.ree.es) y se muestran con fines informativos, citando la fuente y la fecha de actualización, como piden las condiciones de REE.

**Antes de poner publicidad hay que pedir permiso por escrito a REE**, porque sus condiciones no permiten el uso comercial. También hará falta un banner de consentimiento certificado.
