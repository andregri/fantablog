import yaml
import csv
import matplotlib.pyplot as plt
import io


# Read map from ID to Fantasquadra name
id2fantasquadra = {}
with open('../../_data/fantasquadre.yml', 'r') as f:
    id2fantasquadra=yaml.safe_load(f)


def generate_file(row, svg, stat):
    id = int(row['Nome utente'])
    nome = id2fantasquadra[id]['name']
    with open(f'../../stagioni/2022_2023/pronostici/{id}.md', 'w') as f:
        # front matter
        f.write('---\n')
        f.write('layout: pronostici\n')
        f.write(f'title: I pronostici di {nome}\n')
        f.write(f'permalink: /2022_2023/pronostici/{id}\n')
        f.write(f'squadre: [1,2,3,4,5,6,7,8,9,10]\n')
        f.write('---\n')

        # classifica
        f.write('---\n')
        f.write('# I pronostici\n')
        for i in range(1,11):
            key = f'{i}° classificato'
            f.write(f'{i}. {row[key]}\n\n')

        # statistiche
        f.write(f'# Come è stato pronosticato {nome}?\n')
        f.write(f'Media: {stat["avg"]}\n\n')
        f.write(f'Mediana: {stat["mediana"]}\n\n')
        f.write('<div>' + svg + '</div>\n')


def generate_summary_file(svg):
    with open(f'../../stagioni/2022_2023/pronostici/pronostici.html', 'w') as f:
        f.write('---\n')
        f.write('layout: pronostici\n')
        f.write('title: I pronostici della stagione 2022_2023\n')
        f.write('permalink: /2022_2023/pronostici\n')
        f.write('squadre: [1,2,3,4,5,6,7,8,9,10]\n')
        f.write('---\n')
        f.write(svg)


def position2team(rows):
    # Prepare the dict
    # key is the chart position: e.g. 1st, 2nd, 3rd, etc...
    # value is the occurences of each team in that position
    # {1: {"Team1": 4, "Team2:3"}, 2: {...}, ... }
    freq_dict = {}
    for position in range(1, 11):
        freq_dict[position] = {}
        for row in rows:
            id = int(row['Nome utente'])
            fantasquadra = id2fantasquadra[id]['name']
            freq_dict[position][fantasquadra] = 0

    for row in rows:
        for i in range(1,11):
            key = f'{i}° classificato'
            fantasquadra = row[key]
            freq_dict[i][fantasquadra] += 1
    
    return freq_dict


def team2position(rows):
    # Prepare the dict
    # key is the team name
    # value is the occurences of each team in all positions (1st, 2nd, 3rd, etc...)
    # {"Team1": {1: 4, 2: 0, ...}, "Team2": {1: 0, 2: 3, ...}, ...}
    freq_dict = {}
    for row in rows:
        id = int(row['Nome utente'])
        fantasquadra = id2fantasquadra[id]['name']
        freq_dict[fantasquadra] = {}
        for position in range(1, 11):
            freq_dict[fantasquadra][position] = 0

    for row in rows:
        for i in range(1,11):
            key = f'{i}° classificato'
            fantasquadra = row[key]
            freq_dict[fantasquadra][i] += 1
    
    return freq_dict


def read_csv():
    # Read results of forecasts from csv file exported by Google Forms
    with open('../data/pronostici-2022_2023.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = []
        for row in reader:
            rows.append(row)
    
    return rows


def export_all_files(rows):
    dict = team2position(rows)
    for row in rows:
        # generate svg
        id = int(row['Nome utente'])
        fantasquadra = id2fantasquadra[id]['name']
        x = dict[fantasquadra].keys()
        y = dict[fantasquadra].values()
        svg = generate_histogram_svg(x, y)
        svg = svg.split("\n", 3)[-1]

        stat = stats(y)

        generate_file(row, svg, stat)


def export_summary_file(rows):
    svg = generate_histogram_svg_summary(rows)
    clean_svg = svg.split("\n", 3)
    generate_summary_file(clean_svg[3])


def generate_histogram_svg(x, y):
    # Return svg of the histogram x,y
    f = io.BytesIO()
    plt.figure()
    plt.xticks(range(1,11))
    plt.yticks(range(0,max(y)+1))
    plt.bar(x,y)
    plt.savefig(f, format = "svg")
    return f.getvalue().decode()


def generate_histogram_svg_summary(rows):
    f = io.BytesIO()

    data = team2position(rows)

    fig, (ax, lax) = plt.subplots(ncols=2, gridspec_kw={"width_ratios":[4, 1]})

    x = list(range(1,11))
    ax.set_xticks(x)
    ax.set_xlabel('Posizione in classifica')
    
    y = []
    y_prev = [0 for i in range(10)]

    for team, d in data.items():
        y = list(d.values())
        ax.bar(x, y, bottom=y_prev, label=team)
        y_prev = [y1+y2 for y1, y2 in zip(y,y_prev)]

    h, l = ax.get_legend_handles_labels()
    lax.legend(h, l, borderaxespad=0)
    lax.axis("off")

    plt.tight_layout()
    
    fig.savefig(f, format = "svg")
    return f.getvalue().decode()


def stats(freqs):
    res = {}

    # weighted average
    pos_freq = list(zip(range(1,11), freqs))
    inner_prod = map(lambda item: item[0]*item[1], pos_freq)
    tot = sum((p for p in inner_prod))
    res['avg'] = tot / len(freqs)

    # mediana
    n = []
    for pos, freq in pos_freq:
        for _ in range(freq):
            n.append(pos)

    res['mediana'] = n[int(len(n)/2)]
    
    return res


if __name__ == "__main__":
    rows = read_csv()
    export_all_files(rows)
    export_summary_file(rows)