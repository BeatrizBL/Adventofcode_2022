
def clean_string_list(l: str) -> list:
    def _clean_string(s: str) -> str:
        return (s.strip() if len(s.strip())>0 else None)
    l = [(_clean_string(s) if not isinstance(s, list) else clean_string_list(s)) for s in l] 
    l = [s for s in l if s is not None] 
    return l if len(l)>0 else None

def read_file_into_list(
    path: str,
    split_list_char: str = None
) -> list:
    with open(path) as f:
        lines = f.readlines()
    if split_list_char is not None:
        cuts = [i for i, x in enumerate(lines) if x == split_list_char]
        cuts = [0] + cuts + [len(lines)]
        lines = [[s for s in lines[i:j]] for i,j in zip(cuts[:(len(cuts)-1)], cuts[1:len(cuts)])]
    return clean_string_list(lines)
