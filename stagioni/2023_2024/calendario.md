---
layout: page
title: Calendario 2023_2024
permalink: /2023_2024/calendario
---

<ul>
    {% for item in site.data.2023_2024.calendario %}
        <li>
            <a href="giornate/{{ item.giornata }}">Giornata {{ item.giornata }}</a>

            {% if item.coppa %}
                - <a href="coppa/{{ item.coppa }}">{{ item.fase_coppa }} Coppa Box</a>
            {% endif %}
        </li>
    {% endfor %}
</ul>