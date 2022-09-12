---
layout: page
title: Calendario 2022_2023
permalink: /2022_2023/calendario
---

<ul>
    {% for item in site.data.stagione_2022_2023.calendario %}
        <li>
            <a href="giornate/{{ item.giornata }}">Giornata {{ item.giornata }}</a>

            {% if item.coppa %}
                - <a href="coppa/{{ item.coppa }}">{{ item.fase_coppa }} Coppa Box</a>
            {% endif %}
        </li>
    {% endfor %}
</ul>