import json
import teams

class TableRow():
    def __init__(self, position, data):
        self.position = position
        self.team = teams.name_by_id(data.get('id'))
        self.played = data.get('g')
        self.won = data.get('v')
        self.draw = data.get('n')
        self.lost = data.get('pr')
        self.goals_for = data.get('gf')
        self.goals_against = data.get('gs')
        self.goal_difference = data.get('d_r')
        self.tot_points = data.get('p')
        self.tot_special_points = data.get('s_p')
        self.group = data.get('gr')


class Table():
    def __init__(self, teams_per_group, json_path):
        self.rows = []

        with open(json_path, 'r') as f:
            data = json.load(f)
            table = data['data']

            for i, row in enumerate(table):
                pos = (i % teams_per_group) + 1
                self.rows.append(TableRow(pos, row))

    def groups(self):
        return sorted(set((row.group for row in self.rows)))

    def by_group(self, group_name):
        return [row for row in self.rows if row.group == group_name]
