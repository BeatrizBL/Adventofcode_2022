
def clean_string_list(
    l: str,
    drop_spaces: bool = True
) -> list:
    def _clean_string(s: str) -> str:
        s = s.strip() if drop_spaces else s.replace('\n', '')
        return (s if len(s)>0 else None)
    l = [(_clean_string(s) if not isinstance(s, list) else clean_string_list(s, drop_spaces=drop_spaces)) for s in l] 
    l = [s for s in l if s is not None] 
    return l if len(l)>0 else None

def read_file_into_list(
    path: str,
    split_list_char: str = None,
    drop_spaces: bool = True
) -> list:
    with open(path) as f:
        lines = f.readlines()
    if split_list_char is not None:
        cuts = [i for i, x in enumerate(lines) if x == split_list_char]
        cuts = [0] + cuts + [len(lines)]
        lines = [[s for s in lines[i:j]] for i,j in zip(cuts[:(len(cuts)-1)], cuts[1:len(cuts)])]
    return clean_string_list(lines, drop_spaces=drop_spaces)
