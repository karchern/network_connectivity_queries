import difflib

def find_closest_match(query, correct_words):
    # Use get_close_matches to find the closest match
    closest_matches = difflib.get_close_matches(query, correct_words, n=1)
    # Return the closest match if found, otherwise return None
    return closest_matches[0] if closest_matches else None