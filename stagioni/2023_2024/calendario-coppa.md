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
        <th></th>
    </tr>
    <tr>
        <td>Pompy FC</td>
        <td>1</td>
        <td>1</td>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <td>Team Barco F.C.</td>
        <td>1</td>
        <td>1</td>
        <td>Pompy FC</td>
        <td>0</td>
        <td>0</td>
        <td></td>
    </tr>
    <tr>
        <td></td><td></td><td></td><td></td><td></td><td></td><td></td>
    </tr>
    <tr>
        <td>MedusaTeam WFC IL BLOCCO</td>
        <td>1</td>
        <td>1</td>
        <td>MedusaTeam WFC IL BLOCCO</td>
        <td>1</td>
        <td>2</td>
        <td></td>
    </tr>
    <tr>
        <td>REAL DAVID</td>
        <td>0</td>
        <td>0</td>
        <td></td>
        <td></td>
        <td></td>
        <td>MedusaTeam WFC IL BLOCCO</td>
        <td>0</td>
    </tr>
    <tr>
        <td></td><td></td><td></td><td></td><td></td><td></td><td></td>
    </tr>
    <tr>
        <td>Real Pollo</td>
        <td>0</td>
        <td>0</td>
        <td></td>
        <td></td>
        <td></td>
        <td><b>Owl City</b></td>
        <td>1</td>
    </tr>
    <tr>
        <td>Owl City</td>
        <td>2</td>
        <td>3</td>
        <td>Owl City</td>
        <td>1</td>
        <td>0</td>
        <td></td>
    </tr>
    <tr>
        <td></td><td></td><td></td><td></td><td></td><td></td><td></td>
    </tr>
    <tr>
        <td>Paris Saint Germano</td>
        <td>0</td>
        <td>1</td>
        <td>Ire Framba United</td>
        <td>0</td>
        <td>0</td>
        <td></td>
    </tr>
    <tr>
        <td>Ire Framba United</td>
        <td>0</td>
        <td>3</td>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
    </tr>
</table>