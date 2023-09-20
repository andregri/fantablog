import yaml
import csv
import matplotlib.pyplot as plt
import io
import jinja2
from pathlib import Path

NUM_SQUADRE = 12


HERE_PATH = Path(__file__).parent.parent
OUTPUT_PATH = Path(__file__).parent.parent.parent / 'stagioni'

# Read map from ID to Fantasquadra name
id2fantasquadra = {}
with open('../../_data/fantasquadre.yml', 'r') as f:
    id2fantasquadra=yaml.safe_load(f)


def generate_file(stagione, row, svg, stat):
    teamfile_path = HERE_PATH / 'data' / stagione / 'fantasquadre.yml'
    fantasquadre_dict = {}
    with open(teamfile_path.resolve(), 'r') as f:
        data=yaml.safe_load(f)
        fantasquadre_dict = {id: dict(
            name=data[id]['name'],
            link="{{ site.baseurl }}" + f"/{stagione}/pronostici/{id}.html"
            ) for id in data}

    fantasquadra_id = int(row['Nome utente'])
    htmlfile_path = OUTPUT_PATH / stagione / 'pronostici' / f'{fantasquadra_id}.html'
    with open(htmlfile_path.resolve(), 'w') as out_f:
        templates_path = HERE_PATH / 'templates'
        templateLoader = jinja2.FileSystemLoader(templates_path.resolve())
        templateEnv = jinja2.Environment(loader=templateLoader)
        template = templateEnv.get_template('pronostici_detail.html')

        who = fantasquadre_dict[fantasquadra_id]['name']
        title = f"I pronostici di {who}"
        permalink = f'/{stagione}/pronostici/{fantasquadra_id}.html'
        outputText = template.render(
            title=title, permalink=permalink, stagione=stagione,
            summary_link="{{ site.baseurl }}" + f"/{stagione}/pronostici/pronostici.html",
            who=who, fantasquadre=fantasquadre_dict, svg=svg,
            classifica=[row[f'{i}° classificato'] for i in range(1,NUM_SQUADRE+1)],
            average="{:.1f}".format(stat["avg"]), mediana=stat["mediana"])

        out_f.write(outputText)


def generate_summary_file(stagione, svg):
    teamfile_path = HERE_PATH / 'data' / stagione / 'fantasquadre.yml'
    fantasquadre_list = []
    with open(teamfile_path.resolve(), 'r') as f:
        data=yaml.safe_load(f)
        fantasquadre_list = [dict(
            id=id,
            name=data[id]['name'],
            link="{{ site.baseurl }}"+f"/{stagione}/pronostici/{id}.html"
            ) for id in data]

    htmlfile_path = OUTPUT_PATH / stagione / 'pronostici' / 'pronostici.html'
    with open(htmlfile_path.resolve(), 'w') as out_f:
        templates_path = HERE_PATH / 'templates'
        templateLoader = jinja2.FileSystemLoader(templates_path.resolve())
        templateEnv = jinja2.Environment(loader=templateLoader)
        template = templateEnv.get_template('pronostici_summary.html')

        title = f"I pronostici della stagione {stagione}"
        permalink = f'/{stagione}/pronostici/pronostici.html'
        outputText = template.render(title=title, permalink=permalink, stagione=stagione, fantasquadre=fantasquadre_list, svg=svg)

        out_f.write(outputText)


def position2team(stagione, rows):
    # Prepare the dict
    # key is the chart position: e.g. 1st, 2nd, 3rd, etc...
    # value is the occurences of each team in that position
    # {1: {"Team1": 4, "Team2:3"}, 2: {...}, ... }
    teamfile_path = HERE_PATH / 'data' / stagione / 'fantasquadre.yml'
    fantasquadre_dict = {}
    with open(teamfile_path.resolve(), 'r') as f:
        data=yaml.safe_load(f)
        fantasquadre_dict = {id: data[id]['name'] for id in data}

    freq_dict = {}
    for position in range(1, NUM_SQUADRE+1):
        freq_dict[position] = {}
        for row in rows:
            id = int(row['Nome utente'])
            fantasquadra = fantasquadre_dict[id]
            freq_dict[position][fantasquadra] = 0

    for row in rows:
        for i in range(1,NUM_SQUADRE+1):
            key = f'{i}° classificato'
            fantasquadra = row[key]
            freq_dict[i][fantasquadra] += 1
    
    return freq_dict


def team2position(stagione, rows):
    # Prepare the dict
    # key is the team name
    # value is the occurences of each team in all positions (1st, 2nd, 3rd, etc...)
    # {"Team1": {1: 4, 2: 0, ...}, "Team2": {1: 0, 2: 3, ...}, ...}
    teamfile_path = HERE_PATH / 'data' / stagione / 'fantasquadre.yml'
    fantasquadre_dict = {}
    with open(teamfile_path.resolve(), 'r') as f:
        data=yaml.safe_load(f)
        fantasquadre_dict = {id: data[id]['name'] for id in data}

    freq_dict = {}
    for id in fantasquadre_dict:
        fantasquadra = fantasquadre_dict[id]
        freq_dict[fantasquadra] = {}
        for position in range(1, NUM_SQUADRE+1):
            freq_dict[fantasquadra][position] = 0

    for row in rows:
        for i in range(1,NUM_SQUADRE+1):
            key = f'{i}° classificato'
            fantasquadra = row[key]
            freq_dict[fantasquadra][i] += 1
    
    return freq_dict


def read_csv(stagione):
    # Read results of forecasts from csv file exported by Google Forms
    csv_file_path = HERE_PATH / "data" / stagione / f"pronostici-{stagione}.csv"
    with open(csv_file_path.resolve(), newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = []
        for row in reader:
            rows.append(row)
    
    return rows


def export_all_files(stagione, rows):
    teamfile_path = HERE_PATH / 'data' / stagione / 'fantasquadre.yml'
    fantasquadre_dict = {}
    with open(teamfile_path.resolve(), 'r') as f:
        data=yaml.safe_load(f)
        fantasquadre_dict = {id: data[id]['name'] for id in data}

    dict = team2position(stagione, rows)
    for row in rows:
        # generate svg
        id = int(row['Nome utente'])
        fantasquadra = fantasquadre_dict[id]
        x = dict[fantasquadra].keys()
        y = dict[fantasquadra].values()
        svg = generate_histogram_svg(x, y)
        svg = svg.split("\n", 3)[-1]

        stat = stats(y)

        generate_file(stagione, row, svg, stat)


def export_summary_file(stagione, rows):
    svg = generate_histogram_svg_summary(stagione, rows)
    clean_svg = svg.split("\n", 3)
    generate_summary_file(stagione, clean_svg[3])


def generate_histogram_svg(x, y):
    # Return svg of the histogram x,y
    f = io.BytesIO()
    plt.figure()
    plt.xticks(range(1,NUM_SQUADRE+1))
    plt.yticks(range(0,max(y)+1))
    plt.bar(x,y)
    plt.savefig(f, format = "svg")
    return f.getvalue().decode()


def generate_histogram_svg_summary(stagione, rows):
    f = io.BytesIO()

    data = team2position(stagione, rows)

    fig, (ax, lax) = plt.subplots(ncols=2, gridspec_kw={"width_ratios":[4, 1]})

    x = list(range(1,NUM_SQUADRE+1))
    ax.set_xticks(x)
    ax.set_xlabel('Posizione in classifica')
    
    y = []
    y_prev = [0 for i in range(NUM_SQUADRE)]

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
    pos_freq = list(zip(range(1,NUM_SQUADRE+1), freqs))
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
    rows = read_csv(stagione='2023_2024')
    export_all_files(stagione='2023_2024', rows=rows)
    export_summary_file(stagione='2023_2024', rows=rows)