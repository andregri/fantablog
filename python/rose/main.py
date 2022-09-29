from roster import Rosters
import yaml

# Read map from ID to Fantasquadra name
id2fantasquadra = {}
with open('../../_data/fantasquadre.yml', 'r') as f:
    data=yaml.safe_load(f)
    id2fantasquadra = {d['id']: d['name'] for d in data.values()}

if __name__ == "__main__":
    rosters = Rosters('../data/rose/asta_iniziale.xlsx')

    rosters_dict = {}
    rosters_dict[4480615] = rosters.list(0,1)
    rosters_dict[4480737] = rosters.list(1,0)
    rosters_dict[4480837] = rosters.list(2,0)
    rosters_dict[4481779] = rosters.list(2,1)
    rosters_dict[4483105] = rosters.list(3,0)
    rosters_dict[4485329] = rosters.list(3,1)
    rosters_dict[5330685] = rosters.list(4,0)
    rosters_dict[5332606] = rosters.list(4,1)
    rosters_dict[5332804] = rosters.list(5,0)
    rosters_dict[9242836] = rosters.list(5,1)
