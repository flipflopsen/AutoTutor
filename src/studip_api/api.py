def process_files(data, pattern):

    files = []

    illegal_files = []


    for file_data in data:

        file = create_abgabe(file_data)

        match = re.search(pattern, file.name)


        if match:
            files.append(file)

        else:
            illegal_files.append(file)

    return files, illegal_files


def create_abgabe(file_data):

    return Abgabe(file_data['id'], file_data['name'], file_data['user_id'], file_data['chdate'])


def keep_latest_version(files):

    file_by_id = {}

    for file in files:

        file_by_id[file.file_id] = file


    unique_ids = file_by_id.keys()

    file_by_id = {}


    for file in files:

        temp_array = file_by_id[file.file_id]

        temp_array.append(file)

        file_by_id[file.file_id] = temp_array


    newest_files = []


    for file_id in unique_ids:

        file_by_id[file_id].sort(key=get_date, reverse=True)

        newest_files.append(file_by_id[file_id][0])


    return sorted(newest_files, key=lambda abgabe: abgabe.name, reverse=True)


def process_falsche_abgaben(gen_falsche_abgaben, illegal_files, username, password, target_dir):

    if gen_falsche_abgaben:

        illegal_user_ids = list(set(file.user_id for file in illegal_files))

        emails = create_email_list(illegal_user_ids, username, password)

        count = len(emails)


        if emails:

            file_path = os.path.join(target_dir, 'falscheAbgaben.txt')

            with open(file_path, "w") as file:

                file.write(emails)

            print(f"Die Falschen-Abgaben-Datei wurde erfolgreich gespeichert. Es haben insgesamt {count} Personen eine falsche Datei hochgeladen.")

        else:

            print("Die Falschen-Abgaben-Datei wird nicht erzeugt. Es haben keine Personen eine falsche Datei hochgeladen.")


def process_download(files_to_download, api_url, username, password, target_dir):

    all_files = [file for sublist in files_to_download for file in sublist]


    if all_files:

        tutor_number = get_tutor_number(files_to_download)

        print(f"Du bekommst heute den {tutor_number}. Teil. Es gibt die Teile 0 bis 7")


        for tutor_files in files_to_download[tutor_number]:

            download_files(api_url, tutor_files, username, password, target_dir)


        print("Alle Dateien wurden erfolgreich heruntergeladen.")

    else:

        print("Es gibt keine Dateien zum Runterladen.")


def get_tutor_number(files_to_download):

    # Implement the logic to get the tutor number
    pass


def download_files(api_url, files, username, password, target_dir):

    for file in files:

        team = extract_team_name(file.name)

        download_request = requests.get(f'{api_url}file/{file.file_id}/download', auth=HTTPBasicAuth(username, password))


        if download_request.status_code == 200:

            teams = save_team(team, teams)

            file_path = os.path.join(target_dir, file.name)

            with open(file_path, "wb") as downloaded_file:

                downloaded_file.write(download_request.content)

        else:

            print(f"Fehler beim Herunterladen der Datei {file.file_id}. Statuscode: {download_request.status_code}")


        request = requests.get(api_url+'/user/'+file.user_id, auth=HTTPBasicAuth(username, password))


        if request.status_code == 200:

            email_list[team] = request.json()['email']


def save_team(team, teams):

    return f"{teams}\n{team};" if teams else f"{team};"


def process_email_list(files, username, password, target_dir, blattnummer):

    email_list = create_email_list(files, username, password)

    file_path = os.path.join(target_dir, f'mailList_{blattnummer}.txt')


    with open(file_path, "w") as file:

        email_list_string = "\n".join([f'{key}: {value}' for key, value in email_list.items()])

        file.write(email_list_string)


    print(f"Die E-Mail-Liste für die Rückgabe wurde erfolgreich erstellt.")


def process_score_file(files, target_dir, tutor_buchstabe, blattnummer):

    teams = create_score_file(files)

    file_path = os.path.join(target_dir, f'score_{tutor_buchstabe}_{blattnummer}.csv')


    with open(file_path, "w") as file:

        file.write(teams)


    print(f"Die score.csv-Datei wurde erfolgreich erstellt.")

def process_and_write_file(blattnummer, files_to_download, tutor_buchstabe, target_dir):

    tutoren = "ADFIBJGC"

    file_path = os.path.join(target_dir, f'Verteilung_UE{blattnummer}.txt')


    with open(file_path, "w") as file:

        for buchstabe in tutoren:

            number = tuturBuchstabeInNummer[buchstabe]

            tutor_number = tutorNumberPicker[blattnummer][number]

            files = files_to_download[tutor_number]

            file.write(f"Korrekturen für Tutor {buchstabe} - [TutorBuchstabe: {tutor_number} - Anzahl: {len(files)}]\n")


            for abgabe in files:

                team_name = extract_team_name(abgabe.name)

                file.write(f"{team_name}\n")


            file.write('\n')


        file.write(f"Es gibt insgesamt {len(all_files)} Teams. Hier sind die Datei- und Teamnamen:\n")

        count = 1


        for abgabe in all_files:

            file.write(f"{count}: {abgabe.name} - {extract_team_name(abgabe.name)}\n")

            count += 1


    print(f"Die Verteilungs-Datei wurde erfolgreich erstellt.")



def send_studip_file_retrieval_request(api_url, folder, blattnummer, numberOfTutors, tutorNumber, tutorBuchstabe, genFalscheAbgaben, targetDir, username, password, pattern, tuturBuchstabeInNummer, tutorNumberPicker):

    response = requests.get(f'{api_url}/folder/{folder[blattnummer]}/files?limit=500', auth=HTTPBasicAuth(username, password))


    if response.status_code == 200:

        data = response.json()['collection']

        files, illegal_files = process_files(data, pattern)

        files = keep_latest_version(files)

        process_falsche_abgaben(genFalscheAbgaben, illegal_files, username, password, targetDir)

        files_to_download = split_list(files)

        process_download(files_to_download, api_url, username, password, targetDir)

        process_email_list(files, username, password, targetDir, blattnummer)

        process_score_file(files, targetDir, tutorBuchstabe, blattnummer)
        process_and_write_file(blattnummer, files_to_download, tutorBuchstabe, targetDir)

    else:

        print(f"Fehler bei der Anfrage: {response.status_code}")

        print(response.text)