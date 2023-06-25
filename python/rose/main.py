from pathlib import Path
from roster import Rosters
import yaml
import jinja2
import argparse

HERE_PATH = Path(__file__).parent.parent
OUTPUT_PATH = Path(__file__).parent.parent.parent / 'stagioni'


if __name__ == "__main__":    
    # CLI definitions
    parser = argparse.ArgumentParser(description='''
        Genera i file delle rose a partire da un file excel

        es. python main.py 2022_2023 asta_iniziale
    ''')
    parser.add_argument('stagione', type=str, help='stagione e.g. 2022_2023')
    parser.add_argument('file', type=str, help='nome del file excel e.g. asta_iniziale')
    args = parser.parse_args()

    # Create map of ids and team names
    teamfile_path = HERE_PATH / 'data' / args.stagione / 'fantasquadre.yml'
    fantasquadre_dict = {}
    with open(teamfile_path.resolve(), 'r') as f:
        data=yaml.safe_load(f)
        fantasquadre_dict = {id: dict(name=data[id]['name'], row=data[id]['excel_row'], col=data[id]['excel_col']) for id in data}

    # Parse the rosters from the excel file
    excelfile_path = HERE_PATH / 'data' / args.stagione / 'rose' / f'{args.file}.xlsx'
    rosters = Rosters(excelfile_path.resolve())

    rosters_dict = {}
    for id, data in fantasquadre_dict.items():
        rosters_dict[id] = rosters.list(data['row'], data['col'])

    # Create output directories structure
    outdir_path = OUTPUT_PATH / args.stagione / 'mercati' / args.file / 'rose'
    outdir_path.mkdir(parents=True, exist_ok=True)

    # Write roster html files
    for id in fantasquadre_dict:
        htmlfile_path = OUTPUT_PATH / args.stagione / 'mercati' / args.file / 'rose' / f'{id}.html'
        with open(htmlfile_path.resolve(), 'w') as out_f:
            templates_path = HERE_PATH / 'templates'
            templateLoader = jinja2.FileSystemLoader(templates_path.resolve())
            templateEnv = jinja2.Environment(loader=templateLoader)
            template = templateEnv.get_template('roster.html')

            title = fantasquadre_dict[id]['name']
            permalink = f'/{args.stagione}/mercati/{args.file}/rose/{id}'
            site = dict(baseurl="{{site.baseurl}}") # because {{site.baseurl}} should not be substituted by jinja but Jekyll
            outputText = template.render(title=title, permalink=permalink, calciatori=rosters_dict[id], site=site)

            out_f.write(outputText)
