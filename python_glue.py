
def merge_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z

def find_key_in_dict(keys, dict):
    for key in keys:
        if key in dict:
            return key
    return None