import yaml
import csv

def generate_file(row):
    id = int(row['Nome utente'])
    nome = id2fantasquadra[id]['name']
    with open(f'../out/{id}.md', 'w') as f:
        # front matter
        f.write('---\n')
        f.write('layout: pronostici\n')
        f.write(f'title: Pronostici {nome}\n')
        f.write(f'permalink: /2022-2023/pronostici/{id}\n')
        f.write(f'squadre: [1,2,3,4,5,6,7,8,9,10]\n')
        f.write('---\n')

        # classifica
        f.write('<ol>\n')
        for i in range(1,11):
            key = f'{i}° classificato'
            f.write(f'<li>{row[key]}</li>\n')
        f.write('</ol>\n')


# Read map from ID to Fantasquadra name
id2fantasquadra = {}
with open('../../_data/fantasquadre.yml', 'r') as f:
    id2fantasquadra=yaml.safe_load(f)

# Read results of forecasts from csv file exported by Google Forms
with open('../data/pronostici-2022-2023.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        generate_file(row)
