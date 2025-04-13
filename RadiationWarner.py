import requests, json, os, datetime, pprint

ApiUrl = "https://www.imis.bfs.de/ogc/opendata/ows?service=WFS&version=1.1.0&request=GetFeature&typeName=opendata:odlinfo_odl_1h_latest&outputFormat=application/json"

#Daten herunterladen
def GetData():
    Data = requests.get(url=ApiUrl)
    if Data.status_code == 200:
        print("Daten erfolgreich heruntergeladen")
    else:
        print("Fehler beim herunterladen der Daten")
    return Data


#Daten extrahieren und zur Verwendung bereitstellen, außerdem werden sie in eine Text-Datei geschrieben
def PreprocessData():
    RawData = GetData().json()
    if str(RawData)[0] == "{":
        print("Daten OK!")
    else:
        print("Datenfehler: " + str(RawData)[0])
        exit()
    Pfadname = os.path.dirname(__file__)
    Date = datetime.datetime.now().strftime(" %d%m %H%M")
    FormattedJsonData = json.dumps(RawData, indent=4, ensure_ascii=False)
    try: 
        File = open(Pfadname + "/Files/RadiationData" + Date + ".txt", "x")
        File.write(str(FormattedJsonData))
    except FileExistsError:
        print("Datei schon vorhanden, fahre ohne Speicherung fort.")
    return RawData


#Json Daten auswerten und Höchsten Wert aller Stationen erfassen + Weitere Stationsdaten
def ProcessData(RawData):
    HighestValue = 0
    for entry in RawData["features"]:
        feature = entry["properties"]
        Value = feature["value"]
        #print(Value)
        if Value != None and Value > HighestValue:
            HighestValue = Value
            HighestValueStation = feature["id" and "name"]
            HighestValueStationData = entry
    return HighestValue, HighestValueStation, HighestValueStationData
            

ProcessedData = ProcessData(PreprocessData())
HighestValue = ProcessedData[0]
HighestValueStation = ProcessedData[1]
HighestValueStationData = pprint.pformat(ProcessedData[2])

Ausgabe = str("\nHöchster Wert: " + str(HighestValue) + "µSv/h | 0.08-0.40 Beträgt der normale Bereich" + "\n" + "\nStationsname und Nummer: " + str(HighestValueStation) + "\n" + "Komplette Daten der Station: " + str(HighestValueStationData))
print(Ausgabe)

if HighestValue > 0.4:
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    # E-Mail-Server-Einstellungen
    smtp_server = ""
    smtp_port = 587
    smtp_user = ""
    smtp_password = ""

    # E-Mail-Inhalte
    sender_email = ""
    receiver_email = ""
    subject = "!WARNING! Radiation above Threshold !WARNING!"
    body = str(Ausgabe + "\nWebsite Überprüfen für weitere Informationen: https://odlinfo.bfs.de/ODL/DE/themen/wo-stehen-die-sonden/karte/karte_node.html")

    # E-Mail-Nachricht erstellen
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    # Verbindung zum E-Mail-Server herstellen und E-Mail senden
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # Verbindung verschlüsseln
        server.login(smtp_user, smtp_password)  # Anmeldung
        server.send_message(message)  # E-Mail senden

    print("\nE-Mail Versandt!")

else:
    print("\nWerte im grünen Bereich")
