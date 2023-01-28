from functools import lru_cache

def levenshtein_distance(a, b):
    '''
    This function will calculate the levenshtein distance between two input
    strings a and b
    
    params:
        a (String) : The first string you want to compare
        b (String) : The second string you want to compare
        
    returns:
        This function will return the distnace between string a and b.
        
    example:
        a = 'stamp'
        b = 'stomp'
        lev_dist(a,b)
        >> 1.0
    '''
    
    @lru_cache(None)  # for memorization
    def min_dist(s1, s2):

        if s1 == len(a) or s2 == len(b):
            return len(a) - s1 + len(b) - s2

        # no change required
        if a[s1] == b[s2]:
            return min_dist(s1 + 1, s2 + 1)

        return 1 + min(
            min_dist(s1, s2 + 1),      # insert character
            min_dist(s1 + 1, s2),      # delete character
            min_dist(s1 + 1, s2 + 1),  # replace character
        )

    return min_dist(0, 0)

# looping throught the symbol tables to find the closest string to name 
def find_closest_to_string(name,context,global_symbol_Table,Built_in_identifiers):
    all_identifire_defined = list(context.symbol_table.symbols.keys()) + list(global_symbol_Table.symbols.keys())
    for identifier in Built_in_identifiers:
        while identifier in all_identifire_defined:
            all_identifire_defined.remove(identifier)
    
    if len(all_identifire_defined) < 1 :
        return None
    return min(all_identifire_defined,key= lambda key: levenshtein_distance(name,key))