class Abgabe:
    def __init__(self, id, name, userID, date):
        self.id = id
        self.name = name
        self.userID = userID
        self.date = date

    def __repr__(self):
        return repr(self.name)

    def get_file_extension(self):
        return os.path.splitext(self.name)

    def get_name_id(self):
        return extract_team_name(self.name)

    def equals(self, abgabe) -> bool:
        if self.userID == abgabe.userID and self.name != abgabe.name:
            return True
        else:
            return False