import json
import yaml
import csv
import argparse
from pathlib import Path


# Read map from ID to Fantasquadra name
id2fantasquadra = {}
with open('../../_data/fantasquadre.yml', 'r') as f:
    data=yaml.safe_load(f)
    id2fantasquadra = {d['id']: d['name'] for d in data.values()}


class Giornata():
    def __init__(self, filename, filename_classifica):
        self.filename = filename
        self.partite = {}   # keys: 1, 2, 3, ... values: {codice_fg: , risultato: }
                            # keys: 1, 2, 3, ... vaules: {id_partita: , modulo: , punti: , mod_difesa: , calciatori: []}
        self.classifica = []
        
        self.read_json(self.filename)
        self.read_classifica_csv(filename_classifica)


    def read_json(self, filename):
        """
        Read json file that contains all informations about
        a specific matchday
        """
        with open(filename, 'r') as f:
            data = json.load(f)
            partite = data['data']['formazioni']

            for id_partita, partita in enumerate(partite):
                # i want id_partita to start from 1
                id_partita += 1

                self.partite[id_partita] = {}
                self.partite[id_partita]['codice_fg'] = partita['id']
                self.partite[id_partita]['risultato'] = partita['r']

                squadre = partita['sq']
                for field, squadra in zip(['home', 'away'], squadre):
                    tmp_squadra = {}
                    tmp_squadra['id_squadra'] = squadra['id']

                    moduli = squadra['m'].split(';')
                    tmp_squadra['modulo_iniziale'] = moduli[0]
                    tmp_squadra['modulo_finale']   = moduli[1]
                    
                    tmp_squadra['punti'] = squadra['t']
                    tmp_squadra['mod_difesa'] = squadra['ap'][2]
                    tmp_squadra['mod_fairplay'] = squadra['ap'][5]

                    tmp_squadra['calciatori'] = []

                    calciatori = squadra['pl']
                    for calciatore in calciatori:
                        c = self.parse_calciatore(calciatore)
                        tmp_squadra['calciatori'].append(c)

                    self.partite[id_partita][field] = tmp_squadra

    
    def read_classifica_csv(self, filename):
        """
        Read csv file that contains all informations about
        the chart of a specific matchday
        """
        with open(filename, newline='') as csvFile:
            reader = csv.DictReader(csvFile, delimiter=';')
            for row in reader:
                self.classifica.append(row)

    
    def parse_calciatore(self, data):
        # rename keys
        calciatore = {}
        calciatore['ruolo'] = data['r']
        calciatore['nome'] = data['n']
        calciatore['team'] = data['t']
        calciatore['voto'] = data['vt'] # 56 se non ha giocato
        calciatore['fantavoto'] = data['fv'] # 100 se non ha giocato

        calciatore['sostituzione'] = data['s'] # U (uscito) oppure E (entrato) nella fanta partita
        
        bonus_list = data['b']
        calciatore['ammonizioni']     = bonus_list[0]
        calciatore['espulsioni']      = bonus_list[1]
        calciatore['gol_fatti']       = bonus_list[2]
        calciatore['gol_subiti']      = bonus_list[3]
        calciatore['rigori_parati']   = bonus_list[4]
        calciatore['rigori_sbagliati'] = bonus_list[5]
        calciatore['rigori_segnati']  = bonus_list[6]
        calciatore['autogol']         = bonus_list[7]
        calciatore['porta_inviolata'] = bonus_list[10]
        calciatore['assist_bronzo']   = bonus_list[12]
        calciatore['assist_argento']  = bonus_list[13]
        calciatore['assist_oro']      = bonus_list[14]

        return calciatore


    def get_title(self, id_partita):
        id_squadra_casa = self.partite[id_partita]['home']['id_squadra']
        nome_squadra_casa = id2fantasquadra[id_squadra_casa]
        id_squadra_trasferta = self.partite[id_partita]['away']['id_squadra']
        nome_squadra_trasferta = id2fantasquadra[id_squadra_trasferta]
        risultato = self.partite[id_partita]['risultato']
        return nome_squadra_casa, nome_squadra_trasferta, risultato


    def genera_riepilogo_giornata(self, stagione, giornata):
        with open(f'../../stagioni/{stagione}/giornate/{giornata}/{giornata}.html', 'w') as f:
            f.write('---\n')
            f.write(f'layout: page\n')
            f.write(f'title: Giornata {giornata}\n')
            f.write(f'permalink: /{stagione}/giornate/{giornata}\n')
            f.write('---\n\n')

            self.genera_navigazione(file=f, is_riepilogo=True, giornata=giornata)
            
            f.write('<h1>Risultati</h1>\n')
            f.write('<table>\n')
            f.write('  {% for item in site.data.stagione_' + stagione + '.giornata_' + giornata + ' %}\n')
            f.write('    <tr>\n')
            f.write('      <td>{{ item.home }}</td>\n')
            f.write('      <td>{{ item.score }}</td>\n')
            f.write('      <td>{{ item.away }}</td>\n')
            f.write('    <tr>\n')
            f.write('  {% endfor %}\n')
            f.write('</table>\n')

            f.write('<h1>Classifica</h1>\n')
            f.write('  <table>\n')
            f.write('    <tr>\n')
            # Header row
            for header in self.classifica[0].keys():
                f.write(f'      <th>{header}</th>')
            f.write('    </tr>\n')
            # Value rows
            for row in self.classifica:
                f.write('    <tr>\n')
                for value in row.values():
                    f.write(f'      <td>{value}</td>\n')
                f.write('    </tr>\n')
            f.write('  </table>\n')

        with open(f'../../_data/stagione_{stagione}/giornata_{giornata}.csv', 'w') as f:
            f.write('id,home,score,away\n')
            for i, partita in self.partite.items():
                id_squadra_casa = partita['home']['id_squadra']
                nome_squadra_casa = id2fantasquadra[id_squadra_casa]
                id_squadra_trasferta = partita['away']['id_squadra']
                nome_squadra_trasferta = id2fantasquadra[id_squadra_trasferta]
                risultato = partita['risultato']

                nome_squadra_casa, nome_squadra_trasferta, risultato = self.get_title(i)
                f.write(f'{i},{nome_squadra_casa},{risultato},{nome_squadra_trasferta}\n')


    def genera_partita(self, stagione, giornata, id_partita):
        nome_squadra_casa, nome_squadra_trasferta, risultato = self.get_title(id_partita)
        title = f'{nome_squadra_casa} ({risultato}) {nome_squadra_trasferta}'

        with open(f'../../stagioni/{stagione}/giornate/{giornata}/partite/{id_partita}.html', 'w') as f:
            f.write('---\n')
            f.write(f'layout: page\n')
            f.write(f'title: {title}\n')
            f.write(f'permalink: /{stagione}/giornate/{giornata}/partite/{id_partita}\n')
            f.write('---\n\n')

            self.genera_navigazione(file=f, is_riepilogo=False, giornata=giornata)

            # Titolari
            f.write('<h1>Titolari</h1>\n')
            self.genera_tabella_formazioni(f, id_partita, 0, 10, aggiungi_nomi_squadre=True)

            # Panchina
            f.write('<h1>Panchina</h1>\n')
            self.genera_tabella_formazioni(f, id_partita, 11, 17, aggiungi_nomi_squadre=False)

            f.write('<table>\n')
            # MODIFICATORE DIFESA
            f.write(f'  <tr>\n')
            f.write(f'    <td>{int(self.partite[id_partita]["home"]["mod_difesa"])}</td>\n')
            f.write(f'    <td style="text-align: center" colspan="7">Modificatore difesa</td>\n')
            f.write(f'    <td>{int(self.partite[id_partita]["away"]["mod_difesa"])}</td>\n')
            f.write(f'  </tr>\n')

            # FAIRPLAY
            f.write(f'  <tr>\n')
            f.write(f'    <td>{int(self.partite[id_partita]["home"]["mod_fairplay"])}</td>\n')
            f.write(f'    <td style="text-align: center" colspan="7">Bonus fairplay</td>\n')
            f.write(f'    <td>{int(self.partite[id_partita]["away"]["mod_fairplay"])}</td>\n')
            f.write(f'  </tr>\n')

            # MODULO FINALE
            f.write(f'  <tr>\n')
            f.write(f'    <td>{self.partite[id_partita]["home"]["modulo_finale"]}</td>\n')
            f.write(f'    <td style="text-align: center" colspan="7">Modulo finale</td>\n')
            f.write(f'    <td>{self.partite[id_partita]["away"]["modulo_finale"]}</td>\n')
            f.write(f'  </tr>\n')

            # PUNTI TOTALI
            f.write(f'  <tr>\n')
            f.write(f'    <td>{self.partite[id_partita]["home"]["punti"]}</td>\n')
            f.write(f'    <td style="text-align: center" colspan="7">Punti totali</td>\n')
            f.write(f'    <td>{self.partite[id_partita]["away"]["punti"]}</td>\n')
            f.write(f'  </tr>\n')

            f.write('</table>\n')
    

    def genera_navigazione(self, file, is_riepilogo, giornata):
        if is_riepilogo:
            file.write('<a href=".">Riepilogo</a>\n')
        else:
            file.write('<a href="..">Riepilogo</a>\n')

        file.write('{% for item in site.data.stagione_2022_2023.giornata_' + str(giornata) + '%}\n')
        
        if is_riepilogo:
            file.write('  || <a href="partite/{{ item.id }}">\n')
        else:
            file.write('  || <a href="{{ item.id }}">\n')
        
        file.write('    {{ item.home }} ({{ item.score }}) {{ item.away }}\n')
        file.write('  </a>\n')
        file.write('{% endfor %}')


    def genera_tabella_formazioni(self, f, id_partita, start_index, stop_index, aggiungi_nomi_squadre=False):
        f.write('<table>\n')
        
        # Aggiungi i nomi delle squadre all'inizio della tabella
        if aggiungi_nomi_squadre:
            nomi_squadre = self.get_title(id_partita=id_partita)
            f.write(f'  <tr>\n')
            for i, field in zip(range(2), ['home', 'away']):
                modulo = self.partite[id_partita][field]["modulo_iniziale"]
                f.write(f'    <td colspan="4">{nomi_squadre[i]} ({modulo})</td>\n')
                if i == 0:
                    f.write('    <td></td>\n')
            f.write(f'  </tr>\n')

        for i in range(2):
            f.write('    <th>Nome</th>\n')
            f.write('    <th></th>\n')
            f.write('    <th>Voto</th>\n')
            f.write('    <th>FV</th>\n')
            if i == 0:
                f.write('    <th> -- </th>\n')
        f.write('  </tr>\n')
        
        for i in range(start_index, stop_index+1):
            f.write(f'  <tr>\n')
            for field in ['home', 'away']:
                calciatori = self.partite[id_partita][field]['calciatori']
                calciatore = calciatori[i]

                # RUOLO
                ruolo = calciatore["ruolo"].upper()
                if ruolo == 'P':
                    ruolo_img = f'<img src="/assets/img/ruolo_p.png" alt="P">'
                elif ruolo == 'D':
                    ruolo_img = f'<img src="/assets/img/ruolo_d.png" alt="D">'
                elif ruolo == 'C':
                    ruolo_img = f'<img src="/assets/img/ruolo_c.png" alt="C">'
                elif ruolo == 'A':
                    ruolo_img = f'<img src="/assets/img/ruolo_a.png" alt="A">'
                
                nome = calciatore["nome"]
                team = calciatore["team"].upper()
                
                # VOTO is 56 when player has not played
                voto = calciatore["voto"]
                if voto > 50:
                    voto = '-'
                
                # FANTAVOTO is 100 when player has not played
                fantavoto = calciatore["fantavoto"]
                if fantavoto == 100:
                    fantavoto = '-'

                # BONUS
                bonus = ''

                for _ in range(calciatore['ammonizioni']):
                    bonus += '<img src="/assets/img/ammonito.png" alt="Giallo">'

                for _ in range(calciatore['espulsioni']):
                    bonus += '<img src="/assets/img/espulso.png" alt="Rosso">'

                for _ in range(calciatore['gol_fatti']):
                    bonus += '<img src="/assets/img/golFatto.png" alt="Gol">'

                for _ in range(calciatore['gol_subiti']):
                    bonus += '<img src="/assets/img/golSubito.png" alt="Gol Subito">'

                for _ in range(calciatore['rigori_parati']):
                    bonus += '<img src="/assets/img/rigoreParato.png" alt="Rigore Parato">'

                for _ in range(calciatore['rigori_sbagliati']):
                    bonus += '<img src="/assets/img/rigoreSbagliato.png" alt="Rigore Sbagliato">'
                
                for _ in range(calciatore['rigori_segnati']):
                    bonus += '<img src="/assets/img/rigoreSegnato.png" alt="Rigore Segnato">'

                for _ in range(calciatore['porta_inviolata']):
                    bonus += '<img src="/assets/img/portiereImbattuto.png" alt="Portiere imbattuto">'

                for _ in range(calciatore['autogol']):
                    bonus += '<img src="/assets/img/autogol.png" alt="Autogol">'

                for _ in range(calciatore['assist_bronzo']):
                    bonus += '<img src="/assets/img/assistSoft.png" alt="Assist bronzo">'

                for _ in range(calciatore['assist_argento']):
                    bonus += '<img src="/assets/img/assist.png" alt="Assist argento">'

                for _ in range(calciatore['assist_oro']):
                    bonus += '<img src="/assets/img/assistGold.png" alt="Assist oro">'

                f.write(f'    <td><span style="display: block">{ruolo_img} {nome}</span><span style="display: block">{bonus}</span></td>\n')
                f.write(f'    <td>{team}</td>\n')
                f.write(f'    <td>{voto}</td>\n')
                f.write(f'    <td>{fantavoto}</td>\n')
                if field == 'home':
                    f.write(f'    <td></td>\n')
            f.write(f'  </tr>\n')

        f.write('</table>\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Genera i file per una giornata')
    parser.add_argument('stagione', type=str, help='stagione e.g. 2022_2023')
    parser.add_argument('giornata', type=str, help='giornata e.g. 1')
    args = parser.parse_args()

    # Crea la struttura di cartelle
    Path(f"../../stagioni/{args.stagione}/giornate/{args.giornata}/partite").mkdir(parents=True, exist_ok=True)

    giornata = Giornata(f'../data/giornata{args.giornata}.json', f'../data/Classifica_{args.giornata}.csv')
    giornata.genera_riepilogo_giornata(stagione=args.stagione, giornata=args.giornata)
    for i in range(1,6):
        giornata.genera_partita(stagione=args.stagione, giornata=args.giornata, id_partita=i)

    # Aggiorna _data/stagione_xxxx_yyyy/calendario.yml
    calendario = None
    with open(f'../../_data/stagione_{args.stagione}/calendario.yml', 'r') as f:
        calendario = yaml.safe_load(f)
        # aggiungi giornata al calendario solo se non esiste già
        if not dict(giornata=int(args.giornata)) in calendario:
            calendario.insert(int(args.giornata)-1, {'giornata': int(args.giornata)})

    with open(f'../../_data/stagione_{args.stagione}/calendario.yml', 'w') as f:
        text = yaml.safe_dump(calendario)
        f.write(text)