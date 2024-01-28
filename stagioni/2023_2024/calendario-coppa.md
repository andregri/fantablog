---
layout: page
title: Calendario Coppa Box 2023 - 2024
permalink: /2023_2024/calendario-coppa
---

<ul>
    {% for item in site.data.stagione_2023_2024.calendario_coppa %}
        <li>
            <a href="coppa/giornate/{{ item.giornata }}">Giornata {{ item.giornata }} - {{ item.fase }}</a>
        </li>
    {% endfor %}
</ul>

<h1>Tabellone</h1>
<table>
    <tr>
        <th>Quarti</th>
        <th></th>
        <th></th>
        <th>Semi</th>
        <th></th>
        <th></th>
        <th>Finale</th>
    </tr>
    <tr>
        <td>Medusa Team</td>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <td>Ire Framba United</td>
        <td></td>
        <td></td>
        <td>Medusa Team</td>
        <td></td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <td></td><td></td><td></td><td></td><td></td><td></td><td></td>
    </tr>
    <tr>
        <td>Reggisenal</td>
        <td></td>
        <td></td>
        <td>Pompy FC</td>
        <td></td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <td>Pompy FC</td>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
        <td>Medusa Team</td>
    </tr>
    <tr>
        <td></td><td></td><td></td><td></td><td></td><td></td><td></td>
    </tr>
    <tr>
        <td>Godopoli Sportiva</td>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
        <td><b>Real Pollo</b></td>
    </tr>
    <tr>
        <td>ApoelKan</td>
        <td></td>
        <td></td>
        <td>Godopoli Sportiva</td>
        <td></td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <td></td><td></td><td></td><td></td><td></td><td></td><td></td>
    </tr>
    <tr>
        <td>Patetico Mineiro</td>
        <td></td>
        <td></td>
        <td>Real Pollo</td>
        <td></td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <td>Real Pollo</td>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
    </tr>
</table>