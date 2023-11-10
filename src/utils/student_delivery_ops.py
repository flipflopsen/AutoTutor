def split_list(lst):
    avg = len(lst) // numberOfTutors
    remainder = len(lst) % numberOfTutors
    result = [lst[i * avg + min(i, remainder):(i + 1) * avg + min(i + 1, remainder)] for i in range(numberOfTutors)]
    return result

# Extrahiert den Teamnamen aus dem Dateiname
def extract_team_name(file_name):
    match = re.match(patternTeam, file_name)
    if match:
        extracted_text = match.group(1)
        return extracted_text
    else:
        return None

def extract_team_name_from_Abgabe(abgabe):
    return abgabe.userID
    match = re.match(patternTeam, abgabe.name)
    if match:
        extracted_text = match.group(1)
        return extracted_text
    else:
        return None

def getDate(abgabe):
    return abgabe.date