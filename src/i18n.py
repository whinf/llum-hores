"""Textos, URLs traducidas y formatos de fecha y número en es, ca y en."""

LANGS = ("es", "ca", "en")

MONTHS = {
    "es": ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
           "agosto", "septiembre", "octubre", "noviembre", "diciembre"],
    "ca": ["gener", "febrer", "març", "abril", "maig", "juny", "juliol",
           "agost", "setembre", "octubre", "novembre", "desembre"],
    "en": ["January", "February", "March", "April", "May", "June", "July",
           "August", "September", "October", "November", "December"],
}
WEEKDAYS = {
    "es": ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"],
    "ca": ["dilluns", "dimarts", "dimecres", "dijous", "divendres", "dissabte", "diumenge"],
    "en": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
}

STRINGS = {
    "es": {
        "lang_name": "Español",
        "locale": "es_ES",
        "slug_price": "precio-luz",
        "slug_about": "sobre-la-web",
        "slug_legal": "aviso-legal",
        "slug_privacy": "privacidad",
        "slug_widget": "widget",
        "tagline": "Las horas más baratas y más verdes para usar la electricidad",
        "home_title": "Precio de la luz hoy por horas (PVPC)",
        "home_desc": "Precio de la luz por horas hoy y mañana, las mejores horas para poner la lavadora o cargar el coche y cuánta electricidad fue renovable. Datos oficiales de Red Eléctrica.",
        "day_title": "Precio de la luz el {date}",
        "day_desc": "Precio de la luz (PVPC) por horas el {date}: media {avg} €/kWh, hora más barata {cheap} y más cara {dear}. Datos de Red Eléctrica.",
        "month_title": "Precio de la luz en {month}",
        "month_desc": "Precio de la luz (PVPC) día a día y hora a hora en {month}: medias, mínimos, máximos y porcentaje renovable.",
        "archive_title": "Histórico del precio de la luz",
        "archive_desc": "Histórico del precio de la luz (PVPC) por meses, con datos diarios y horarios de Red Eléctrica.",
        "today": "Hoy",
        "tomorrow": "Mañana",
        "home": "Inicio",
        "now": "Ahora",
        "avg": "Precio medio",
        "min": "Hora más barata",
        "max": "Hora más cara",
        "unit": "€/kWh",
        "tomorrow_pending": "Los precios de mañana se publican cada día hacia las 20:30. Esta página se actualiza sola.",
        "chart_title": "Precio por horas (€/kWh)",
        "chart_desc": "Gráfico de barras con el precio de cada hora. La franja de {n} horas más barata va de {start} a {end}.",
        "cheap_window": "{n} h más baratas",
        "best_for": "Mejores horas para…",
        "best_for_note": "Coste aproximado de la energía en la mejor franja y ahorro frente a la peor franja del mismo día.",
        "saving": "ahorras {x}",
        "cost": "coste {x}",
        "appliance_washer": "Poner la lavadora",
        "appliance_dishwasher": "Poner el lavavajillas",
        "appliance_oven": "Usar el horno",
        "appliance_dryer": "Poner la secadora",
        "appliance_heater": "Calentar el termo",
        "appliance_ev": "Cargar el coche eléctrico",
        "table_hour": "Hora",
        "table_price": "Precio (€/kWh)",
        "table_level": "Nivel",
        "table_show": "Ver la tabla de precios",
        "tier_0": "Barata",
        "tier_1": "Media",
        "tier_2": "Cara",
        "mix_title": "¿Cuánta electricidad fue renovable?",
        "mix_text": "El {date}, el <strong>{pct}</strong> de la electricidad generada en España fue renovable. Emisiones: <strong>{co2} g de CO₂ por kWh</strong>.",
        "mix_sources": "Origen de la electricidad",
        "src_wind": "Eólica",
        "src_solar": "Solar",
        "src_hydro": "Hidráulica",
        "src_other_renewable": "Otras renovables",
        "src_nuclear": "Nuclear",
        "src_gas": "Gas natural",
        "src_cogeneration": "Cogeneración",
        "src_coal": "Carbón",
        "src_other_fossil": "Otras no renovables",
        "green_tip": "En España, las horas más baratas suelen coincidir con mucha producción solar o eólica. Mover el consumo a esas horas ahorra dinero y, normalmente, también emisiones.",
        "what_pvpc": "Los precios son el término de energía del PVPC (tarifa regulada 2.0TD) para la península, Baleares y Canarias. Incluyen peajes y cargos, pero no los impuestos (IVA e impuesto eléctrico) ni el término de potencia. Si tienes una tarifa de mercado libre con precio fijo, tu precio no cambia por horas.",
        "vs_prev": "{x} que el día anterior",
        "vs_week": "{x} que el mismo día de la semana pasada",
        "vs_year": "Hace un año, el precio medio fue {x} €/kWh.",
        "more": "más caro",
        "less": "más barato",
        "last_days": "Últimos días",
        "day": "Día",
        "renewable": "Renovable",
        "heatmap_title": "Precio por día y hora (€/kWh)",
        "heatmap_desc": "Mapa de calor: cada fila es un día y cada columna una hora; cuanto más oscuro, más caro.",
        "heatmap_low": "más barato",
        "heatmap_high": "más caro",
        "month_days": "Resumen de cada día",
        "prev_day": "Día anterior",
        "next_day": "Día siguiente",
        "prev_month": "Mes anterior",
        "next_month": "Mes siguiente",
        "see_day": "Ver el detalle del día",
        "see_archive": "Ver el histórico",
        "no_data": "Todavía no hay datos de precios para este día.",
        "source_line": "Datos: Red Eléctrica (REE), uso informativo. Última actualización: {t}.",
        "about": "Sobre la web",
        "legal": "Aviso legal",
        "privacy": "Privacidad",
        "feed": "RSS",
        "api": "Datos abiertos (JSON)",
        "donate": "Apoya el proyecto",
        "skip": "Saltar al contenido",
        "language": "Idioma",
        "notfound_title": "Página no encontrada",
        "notfound_text": "Esta página no existe. Vuelve al precio de la luz de hoy.",
        "widget_title": "Horas más baratas hoy",
        "widget_more": "Ver todos los precios",
        "feed_title": "Precio de la luz por horas",
        "feed_item": "{date}: la hora más barata es {h} ({p} €/kWh)",
        "choose": "Elige idioma",
        "about_body": """
<p>{site} muestra cada día el precio de la electricidad por horas en España y te dice cuándo conviene usar los aparatos que más gastan. El objetivo es doble: que pagues menos y que consumas cuando hay más energía renovable en la red.</p>
<h2>Cómo funciona</h2>
<ul>
<li>Los precios son el término de energía del PVPC (tarifa 2.0TD) que publica Red Eléctrica, con peajes y cargos y sin impuestos. Se publican hacia las 20:30 para el día siguiente.</li>
<li>Las horas se muestran en hora peninsular. Los días de cambio de hora tienen 23 o 25 horas.</li>
<li>Las franjas más baratas se calculan buscando las horas seguidas con el precio medio más bajo del día. El nivel (barata, media, cara) divide las horas del día en tres grupos iguales.</li>
<li>El porcentaje renovable y las emisiones de CO₂ son los datos diarios de generación de todo el sistema eléctrico español que publica Red Eléctrica.</li>
<li>La web se actualiza sola varias veces al día. No usa cookies ni rastreadores.</li>
</ul>
<h2>Datos abiertos y widget</h2>
<p>Puedes reutilizar los datos en JSON: <a href="{api}">{api}</a>. Si los usas, cita a Red Eléctrica como fuente.</p>
<p>Para poner las horas más baratas en tu web, copia este código:</p>
<pre><code>&lt;iframe src="{widget}" title="{widget_title}" width="320" height="300" style="border:0"&gt;&lt;/iframe&gt;</code></pre>
<h2>Código fuente</h2>
<p>El proyecto es de código abierto. Puedes ver el código, avisar de errores o proponer mejoras en <a href="{repo}">GitHub</a>.</p>
""",
        "legal_body": """
<p>{site} es un proyecto gratuito e informativo que muestra datos públicos sobre el precio de la electricidad.</p>
<h2>Titular</h2>
<p>{owner}</p>
<h2>Fuentes de los datos</h2>
<p>Los datos de precios, generación y emisiones proceden de Red Eléctrica (REE), a través de apidatos.ree.es y esios.ree.es, y se muestran con fines informativos, citando la fuente y la fecha de actualización.</p>
<h2>Responsabilidad</h2>
<p>La información se ofrece tal cual, sin garantía. Puede contener errores o retrasos. Para decisiones importantes, consulta tu factura o a tu comercializadora.</p>
""",
        "privacy_body": """
<p>Esta web no usa cookies, no tiene analítica ni publicidad y no recoge datos personales.</p>
<p>Está alojada en GitHub Pages. Como cualquier servidor web, GitHub registra la dirección IP de las visitas por motivos de seguridad. Más información en la <a href="https://docs.github.com/es/site-policy/privacy-policies/github-general-privacy-statement">declaración de privacidad de GitHub</a>.</p>
<p>Si contactas a través de GitHub, se aplican las condiciones de esa plataforma.</p>
""",
        "owner_missing": "Proyecto personal sin ánimo de lucro. Contacto: a través del <a href=\"{repo}\">repositorio en GitHub</a>.",
    },
    "ca": {
        "lang_name": "Català",
        "locale": "ca_ES",
        "slug_price": "preu-llum",
        "slug_about": "sobre-el-web",
        "slug_legal": "avis-legal",
        "slug_privacy": "privacitat",
        "slug_widget": "widget",
        "tagline": "Les hores més barates i més verdes per fer servir l'electricitat",
        "home_title": "Preu de la llum avui per hores (PVPC)",
        "home_desc": "Preu de la llum per hores avui i demà, les millors hores per posar la rentadora o carregar el cotxe i quanta electricitat va ser renovable. Dades oficials de Red Eléctrica.",
        "day_title": "Preu de la llum el {date}",
        "day_desc": "Preu de la llum (PVPC) per hores el {date}: mitjana {avg} €/kWh, hora més barata {cheap} i més cara {dear}. Dades de Red Eléctrica.",
        "month_title": "Preu de la llum: {month}",
        "month_desc": "Preu de la llum (PVPC) dia a dia i hora a hora: {month}. Mitjanes, mínims, màxims i percentatge renovable.",
        "archive_title": "Històric del preu de la llum",
        "archive_desc": "Històric del preu de la llum (PVPC) per mesos, amb dades diàries i horàries de Red Eléctrica.",
        "today": "Avui",
        "tomorrow": "Demà",
        "home": "Inici",
        "now": "Ara",
        "avg": "Preu mitjà",
        "min": "Hora més barata",
        "max": "Hora més cara",
        "unit": "€/kWh",
        "tomorrow_pending": "Els preus de demà es publiquen cada dia cap a les 20:30. Aquesta pàgina s'actualitza sola.",
        "chart_title": "Preu per hores (€/kWh)",
        "chart_desc": "Gràfic de barres amb el preu de cada hora. La franja de {n} hores més barata va de {start} a {end}.",
        "cheap_window": "{n} h més barates",
        "best_for": "Millors hores per…",
        "best_for_note": "Cost aproximat de l'energia a la millor franja i estalvi respecte de la pitjor franja del mateix dia.",
        "saving": "estalvies {x}",
        "cost": "cost {x}",
        "appliance_washer": "Posar la rentadora",
        "appliance_dishwasher": "Posar el rentaplats",
        "appliance_oven": "Fer servir el forn",
        "appliance_dryer": "Posar l'assecadora",
        "appliance_heater": "Escalfar el termo",
        "appliance_ev": "Carregar el cotxe elèctric",
        "table_hour": "Hora",
        "table_price": "Preu (€/kWh)",
        "table_level": "Nivell",
        "table_show": "Veure la taula de preus",
        "tier_0": "Barata",
        "tier_1": "Mitjana",
        "tier_2": "Cara",
        "mix_title": "Quanta electricitat va ser renovable?",
        "mix_text": "El {date}, el <strong>{pct}</strong> de l'electricitat generada a Espanya va ser renovable. Emissions: <strong>{co2} g de CO₂ per kWh</strong>.",
        "mix_sources": "Origen de l'electricitat",
        "src_wind": "Eòlica",
        "src_solar": "Solar",
        "src_hydro": "Hidràulica",
        "src_other_renewable": "Altres renovables",
        "src_nuclear": "Nuclear",
        "src_gas": "Gas natural",
        "src_cogeneration": "Cogeneració",
        "src_coal": "Carbó",
        "src_other_fossil": "Altres no renovables",
        "green_tip": "A Espanya, les hores més barates solen coincidir amb molta producció solar o eòlica. Moure el consum a aquestes hores estalvia diners i, normalment, també emissions.",
        "what_pvpc": "Els preus són el terme d'energia del PVPC (tarifa regulada 2.0TD) per a la península, les Balears i les Canàries. Inclouen peatges i càrrecs, però no els impostos (IVA i impost elèctric) ni el terme de potència. Si tens una tarifa de mercat lliure amb preu fix, el teu preu no canvia per hores.",
        "vs_prev": "{x} que el dia anterior",
        "vs_week": "{x} que el mateix dia de la setmana passada",
        "vs_year": "Fa un any, el preu mitjà va ser de {x} €/kWh.",
        "more": "més car",
        "less": "més barat",
        "last_days": "Darrers dies",
        "day": "Dia",
        "renewable": "Renovable",
        "heatmap_title": "Preu per dia i hora (€/kWh)",
        "heatmap_desc": "Mapa de calor: cada fila és un dia i cada columna una hora; com més fosc, més car.",
        "heatmap_low": "més barat",
        "heatmap_high": "més car",
        "month_days": "Resum de cada dia",
        "prev_day": "Dia anterior",
        "next_day": "Dia següent",
        "prev_month": "Mes anterior",
        "next_month": "Mes següent",
        "see_day": "Veure el detall del dia",
        "see_archive": "Veure l'històric",
        "no_data": "Encara no hi ha dades de preus per a aquest dia.",
        "source_line": "Dades: Red Eléctrica (REE), ús informatiu. Darrera actualització: {t}.",
        "about": "Sobre el web",
        "legal": "Avís legal",
        "privacy": "Privacitat",
        "feed": "RSS",
        "api": "Dades obertes (JSON)",
        "donate": "Dona suport al projecte",
        "skip": "Salta al contingut",
        "language": "Idioma",
        "notfound_title": "Pàgina no trobada",
        "notfound_text": "Aquesta pàgina no existeix. Torna al preu de la llum d'avui.",
        "widget_title": "Hores més barates avui",
        "widget_more": "Veure tots els preus",
        "feed_title": "Preu de la llum per hores",
        "feed_item": "{date}: l'hora més barata és {h} ({p} €/kWh)",
        "choose": "Tria l'idioma",
        "about_body": """
<p>{site} mostra cada dia el preu de l'electricitat per hores a Espanya i et diu quan et convé fer servir els aparells que més gasten. L'objectiu és doble: que paguis menys i que consumeixis quan hi ha més energia renovable a la xarxa.</p>
<h2>Com funciona</h2>
<ul>
<li>Els preus són el terme d'energia del PVPC (tarifa 2.0TD) que publica Red Eléctrica, amb peatges i càrrecs i sense impostos. Es publiquen cap a les 20:30 per al dia següent.</li>
<li>Les hores es mostren en hora peninsular. Els dies de canvi d'hora tenen 23 o 25 hores.</li>
<li>Les franges més barates es calculen buscant les hores seguides amb el preu mitjà més baix del dia. El nivell (barata, mitjana, cara) divideix les hores del dia en tres grups iguals.</li>
<li>El percentatge renovable i les emissions de CO₂ són les dades diàries de generació de tot el sistema elèctric espanyol que publica Red Eléctrica.</li>
<li>El web s'actualitza sol diverses vegades al dia. No fa servir galetes ni rastrejadors.</li>
</ul>
<h2>Dades obertes i widget</h2>
<p>Pots reutilitzar les dades en JSON: <a href="{api}">{api}</a>. Si les fas servir, cita Red Eléctrica com a font.</p>
<p>Per posar les hores més barates al teu web, copia aquest codi:</p>
<pre><code>&lt;iframe src="{widget}" title="{widget_title}" width="320" height="300" style="border:0"&gt;&lt;/iframe&gt;</code></pre>
<h2>Codi font</h2>
<p>El projecte és de codi obert. Pots veure el codi, avisar d'errors o proposar millores a <a href="{repo}">GitHub</a>.</p>
""",
        "legal_body": """
<p>{site} és un projecte gratuït i informatiu que mostra dades públiques sobre el preu de l'electricitat.</p>
<h2>Titular</h2>
<p>{owner}</p>
<h2>Fonts de les dades</h2>
<p>Les dades de preus, generació i emissions provenen de Red Eléctrica (REE), a través d'apidatos.ree.es i esios.ree.es, i es mostren amb finalitat informativa, citant la font i la data d'actualització.</p>
<h2>Responsabilitat</h2>
<p>La informació s'ofereix tal com és, sense garantia. Pot contenir errors o retards. Per a decisions importants, consulta la teva factura o la teva comercialitzadora.</p>
""",
        "privacy_body": """
<p>Aquest web no fa servir galetes, no té analítica ni publicitat i no recull dades personals.</p>
<p>Està allotjat a GitHub Pages. Com qualsevol servidor web, GitHub registra l'adreça IP de les visites per motius de seguretat. Més informació a la <a href="https://docs.github.com/es/site-policy/privacy-policies/github-general-privacy-statement">declaració de privacitat de GitHub</a>.</p>
<p>Si contactes a través de GitHub, s'hi apliquen les condicions d'aquesta plataforma.</p>
""",
        "owner_missing": "Projecte personal sense ànim de lucre. Contacte: a través del <a href=\"{repo}\">repositori a GitHub</a>.",
    },
    "en": {
        "lang_name": "English",
        "locale": "en_GB",
        "slug_price": "electricity-price",
        "slug_about": "about",
        "slug_legal": "legal-notice",
        "slug_privacy": "privacy",
        "slug_widget": "widget",
        "tagline": "The cheapest and greenest hours to use electricity in Spain",
        "home_title": "Electricity price today by hour in Spain (PVPC)",
        "home_desc": "Hourly electricity prices in Spain for today and tomorrow, the best hours to run the washing machine or charge your car, and how much power was renewable. Official Red Eléctrica data.",
        "day_title": "Electricity price in Spain on {date}",
        "day_desc": "Hourly electricity price (PVPC) in Spain on {date}: average {avg} €/kWh, cheapest hour {cheap}, most expensive {dear}. Red Eléctrica data.",
        "month_title": "Electricity price in Spain, {month}",
        "month_desc": "Spanish electricity price (PVPC) day by day and hour by hour in {month}: averages, lows, highs and renewable share.",
        "archive_title": "Electricity price history",
        "archive_desc": "Monthly history of the Spanish electricity price (PVPC), with daily and hourly Red Eléctrica data.",
        "today": "Today",
        "tomorrow": "Tomorrow",
        "home": "Home",
        "now": "Now",
        "avg": "Average price",
        "min": "Cheapest hour",
        "max": "Most expensive hour",
        "unit": "€/kWh",
        "tomorrow_pending": "Tomorrow's prices are published every day at around 20:30 (Spanish time). This page updates itself.",
        "chart_title": "Price by hour (€/kWh)",
        "chart_desc": "Bar chart with the price of each hour. The cheapest {n}-hour window runs from {start} to {end}.",
        "cheap_window": "cheapest {n} h",
        "best_for": "Best hours to…",
        "best_for_note": "Approximate energy cost in the best window and saving compared with the worst window of the same day.",
        "saving": "you save {x}",
        "cost": "cost {x}",
        "appliance_washer": "Run the washing machine",
        "appliance_dishwasher": "Run the dishwasher",
        "appliance_oven": "Use the oven",
        "appliance_dryer": "Run the tumble dryer",
        "appliance_heater": "Heat the water tank",
        "appliance_ev": "Charge an electric car",
        "table_hour": "Hour",
        "table_price": "Price (€/kWh)",
        "table_level": "Level",
        "table_show": "Show the price table",
        "tier_0": "Cheap",
        "tier_1": "Medium",
        "tier_2": "Expensive",
        "mix_title": "How much electricity was renewable?",
        "mix_text": "On {date}, <strong>{pct}</strong> of the electricity generated in Spain was renewable. Emissions: <strong>{co2} g of CO₂ per kWh</strong>.",
        "mix_sources": "Where the electricity came from",
        "src_wind": "Wind",
        "src_solar": "Solar",
        "src_hydro": "Hydro",
        "src_other_renewable": "Other renewables",
        "src_nuclear": "Nuclear",
        "src_gas": "Natural gas",
        "src_cogeneration": "Cogeneration",
        "src_coal": "Coal",
        "src_other_fossil": "Other non-renewables",
        "green_tip": "In Spain, the cheapest hours usually coincide with lots of solar or wind power. Shifting your consumption to those hours saves money and usually cuts emissions too.",
        "what_pvpc": "Prices are the energy term of the PVPC (the regulated 2.0TD tariff) for mainland Spain, the Balearic and Canary Islands. They include network tolls and charges, but not taxes (VAT and electricity tax) or the capacity term. If you have a fixed-price free-market tariff, your price does not change by the hour.",
        "vs_prev": "{x} than the day before",
        "vs_week": "{x} than the same day last week",
        "vs_year": "A year ago, the average price was {x} €/kWh.",
        "more": "more expensive",
        "less": "cheaper",
        "last_days": "Last few days",
        "day": "Day",
        "renewable": "Renewable",
        "heatmap_title": "Price by day and hour (€/kWh)",
        "heatmap_desc": "Heat map: each row is a day and each column an hour; the darker, the more expensive.",
        "heatmap_low": "cheaper",
        "heatmap_high": "more expensive",
        "month_days": "Daily summary",
        "prev_day": "Previous day",
        "next_day": "Next day",
        "prev_month": "Previous month",
        "next_month": "Next month",
        "see_day": "See the day in detail",
        "see_archive": "See the history",
        "no_data": "There is no price data for this day yet.",
        "source_line": "Data: Red Eléctrica (REE), for information purposes. Last update: {t}.",
        "about": "About",
        "legal": "Legal notice",
        "privacy": "Privacy",
        "feed": "RSS",
        "api": "Open data (JSON)",
        "donate": "Support the project",
        "skip": "Skip to content",
        "language": "Language",
        "notfound_title": "Page not found",
        "notfound_text": "This page does not exist. Go back to today's electricity price.",
        "widget_title": "Cheapest hours today",
        "widget_more": "See all prices",
        "feed_title": "Hourly electricity price in Spain",
        "feed_item": "{date}: the cheapest hour is {h} ({p} €/kWh)",
        "choose": "Choose your language",
        "about_body": """
<p>{site} shows the hourly electricity price in Spain every day and tells you when to use your most power-hungry appliances. The goal is twofold: to help you pay less and to use power when there is more renewable energy on the grid.</p>
<h2>How it works</h2>
<ul>
<li>Prices are the energy term of the PVPC (2.0TD tariff) published by Red Eléctrica, including tolls and charges and excluding taxes. They are published at around 20:30 for the next day.</li>
<li>Hours are shown in mainland Spanish time. Days when the clocks change have 23 or 25 hours.</li>
<li>The cheapest windows are the consecutive hours with the lowest average price of the day. The level (cheap, medium, expensive) splits the day's hours into three equal groups.</li>
<li>The renewable share and CO₂ emissions are Red Eléctrica's daily generation figures for the whole Spanish power system.</li>
<li>The site updates itself several times a day. It uses no cookies or trackers.</li>
</ul>
<h2>Open data and widget</h2>
<p>You can reuse the data as JSON: <a href="{api}">{api}</a>. If you use it, credit Red Eléctrica as the source.</p>
<p>To show the cheapest hours on your own website, copy this code:</p>
<pre><code>&lt;iframe src="{widget}" title="{widget_title}" width="320" height="300" style="border:0"&gt;&lt;/iframe&gt;</code></pre>
<h2>Source code</h2>
<p>The project is open source. You can read the code, report bugs or suggest improvements on <a href="{repo}">GitHub</a>.</p>
""",
        "legal_body": """
<p>{site} is a free, informational project that shows public data about electricity prices.</p>
<h2>Owner</h2>
<p>{owner}</p>
<h2>Data sources</h2>
<p>Price, generation and emissions data come from Red Eléctrica (REE), via apidatos.ree.es and esios.ree.es, and are shown for information purposes, citing the source and the update date.</p>
<h2>Liability</h2>
<p>The information is provided as is, without warranty. It may contain errors or delays. For important decisions, check your bill or ask your energy supplier.</p>
""",
        "privacy_body": """
<p>This website uses no cookies, has no analytics or advertising, and collects no personal data.</p>
<p>It is hosted on GitHub Pages. Like any web server, GitHub logs visitors' IP addresses for security reasons. See the <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement">GitHub privacy statement</a>.</p>
<p>If you contact us through GitHub, that platform's terms apply.</p>
""",
        "owner_missing": "Personal non-profit project. Contact: through the <a href=\"{repo}\">GitHub repository</a>.",
    },
}


def t(lang, key, **kw):
    text = STRINGS[lang][key]
    return text.format(**kw) if kw else text


def fmt_num(lang, x, decimals):
    s = f"{x:.{decimals}f}"
    return s if lang == "en" else s.replace(".", ",")


def fmt_price(lang, p_mwh):
    """€/MWh -> texto en €/kWh con 4 decimales."""
    return fmt_num(lang, p_mwh / 1000, 4)


def fmt_eur(lang, x):
    return f"€{x:.2f}" if lang == "en" else f"{fmt_num(lang, x, 2)} €"


def fmt_pct(lang, x, decimals=1):
    return f"{x:.{decimals}f}%" if lang == "en" else f"{fmt_num(lang, x, decimals)} %"


def _of(lang, month_index):
    name = MONTHS[lang][month_index]
    if lang == "ca":
        return ("d'" if name[0] in "aeiou" else "de ") + name
    return "de " + name


def fmt_date(lang, d, weekday=True, year=True):
    if lang == "en":
        s = f"{d.day} {MONTHS['en'][d.month - 1]}" + (f" {d.year}" if year else "")
        return f"{WEEKDAYS['en'][d.weekday()]}, {s}" if weekday else s
    s = f"{d.day} {_of(lang, d.month - 1)}" + (f" de {d.year}" if year else "")
    return f"{WEEKDAYS[lang][d.weekday()]}, {s}" if weekday else s


def fmt_month(lang, year, month):
    name = MONTHS[lang][month - 1]
    return f"{name} {year}" if lang == "en" else f"{name} de {year}"
