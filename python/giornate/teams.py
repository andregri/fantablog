import yaml


def name_by_id(id):
    # Read map from ID to Fantasquadra name
    id2fantasquadra = {}
    with open('../../_data/fantasquadre.yml', 'r') as f:
        data=yaml.safe_load(f)
        id2fantasquadra = {d['id']: d['name'] for d in data.values()}
    
    return id2fantasquadra[id]