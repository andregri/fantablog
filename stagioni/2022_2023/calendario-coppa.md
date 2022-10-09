---
layout: page
title: Calendario Coppa Box 2022 - 2023
permalink: /2022_2023/calendario-coppa
---

<ul>
    {% for item in site.data.stagione_2022_2023.calendario_coppa %}
        <li>
            <a href="coppa/giornate/{{ item.giornata }}">Giornata {{ item.giornata }} - {{ item.fase }}</a>
        </li>
    {% endfor %}
</ul>