import json
import yaml

# Read map from ID to Fantasquadra name
id2fantasquadra = {}
with open('../../_data/fantasquadre.yml', 'r') as f:
    data=yaml.safe_load(f)
    id2fantasquadra = {d['id']: d['name'] for d in data.values()}


class Giornata():
    def __init__(self, filename):
        self.filename = filename
        self.partite = {}   # keys: 1, 2, 3, ... values: {codice_fg: , risultato: }
                            # keys: 1, 2, 3, ... vaules: {id_partita: , modulo: , punti: , mod_difesa: , calciatori: []}
        self.read_json(self.filename)

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
                    tmp_squadra['modulo'] = squadra['m']
                    tmp_squadra['punti'] = squadra['t']
                    tmp_squadra['mod_difesa'] = squadra['ap'][2]

                    tmp_squadra['calciatori'] = []

                    calciatori = squadra['pl']
                    for calciatore in calciatori:
                        c = self.parse_calciatore(calciatore)
                        tmp_squadra['calciatori'].append(c)

                    self.partite[id_partita][field] = tmp_squadra
    
    
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
        calciatore['rigori_sbaliati'] = bonus_list[5]
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

    def genera_riepilogo_giornata(self):
        with open('../../stagioni/2022-2023/giornate/1/1.html', 'w') as f:
            f.write('---\n')
            f.write('layout: giornata_22_23\n')
            f.write('title: Giornata 1\n')
            f.write('permalink: /2022-2023/giornate/1\n')
            f.write('---\n\n')
            f.write('<h1>Risultati</h1>\n')
            f.write('<table>\n')
            f.write('  {% for item in site.data.stagione_2022_2023.giornata_1 %}\n')
            f.write('    <tr>\n')
            f.write('      <td>{{ item.home }}</td>\n')
            f.write('      <td>{{ item.score }}</td>\n')
            f.write('      <td>{{ item.away }}</td>\n')
            f.write('    <tr>\n')
            f.write('  {% endfor %}\n')
            f.write('</table>\n')

        with open('../../_data/stagione_2022_2023/giornata_1.csv', 'w') as f:
            f.write('id,home,score,away\n')
            for i, partita in self.partite.items():
                id_squadra_casa = partita['home']['id_squadra']
                nome_squadra_casa = id2fantasquadra[id_squadra_casa]
                id_squadra_trasferta = partita['away']['id_squadra']
                nome_squadra_trasferta = id2fantasquadra[id_squadra_trasferta]
                risultato = partita['risultato']

                nome_squadra_casa, nome_squadra_trasferta, risultato = self.get_title(i)
                f.write(f'{i},{nome_squadra_casa},{risultato},{nome_squadra_trasferta}\n')


    def genera_partita(self, id_partita):
        nome_squadra_casa, nome_squadra_trasferta, risultato = self.get_title(id_partita)
        title = f'{nome_squadra_casa} ({risultato}) {nome_squadra_trasferta}'

        with open(f'../../stagioni/2022-2023/giornate/1/partite/{id_partita}.html', 'w') as f:
            f.write('---\n')
            f.write('layout: partita_22_23\n')
            f.write(f'title: {title}\n')
            f.write(f'permalink: /2022-2023/giornate/1/partite/{id_partita}\n')
            f.write('---\n\n')

            # Titolari
            f.write('<h1>Titolari</h1>\n')
            f.write('<table>\n')
            f.write('  <tr>\n')
            f.write('    <th>Nome</th>\n')
            f.write('    <th>Voto</th>\n')
            f.write('    <th>FV</th>\n')
            f.write('    <th> -- </th>\n')
            f.write('    <th>Nome</th>\n')
            f.write('    <th>Voto</th>\n')
            f.write('    <th>FV</th>\n')
            f.write('  </tr>\n')
            # todo
            f.write('</table>\n')

            # Panchina

            # Tribuna


if __name__ == "__main__":
    giornata = Giornata('../data/giornata1.json')
    giornata.genera_riepilogo_giornata()
    for i in range(1,6):
        giornata.genera_partita(i)