# RadiationWarnerGermany
Dieses kleine Script lädt über die API des BFS (Bundesamt für Strahlenschutz) die Daten jeder verfügbaren Messstelle herunter und filtert die Messstelle mit dem höchsten Wert heraus. Liegt dieser Wert über einer bestimmten Schwelle, versendet das Script über den angegebenen E-Mail Server/Account eine E-Mail an die gewünschte Zieladresse. 
Es ist perfekt geeignet, um auf einem Homeserver o.ä. in einem Cronjob ausgeführt zu werden.

Nutzen: Durch ein stündliches ausführen des Scripts, wird man bei einem dramatischen Anstieg der Strahlungswerte in Deutschland direkt per E-Mail benachrichtigt und kann sich selbst ein Bild von der Lage machen. Somit kann dies für ein ruhiges Gewissen sorgen, da man nicht selbst die Website im Auge zu behalten braucht, wenn man Interesse daran hat, frühstmöglich über einen gefährlichen Anstieg der Strahlung informiert zu werden. 

Cronjob Intervall: Es ist völlig ausreichend und empfohlen, diese Script maximal 1x pro Stunde auszuführen, einfach aus dem Grund, da auch nur einmal pro Stunde die Daten vom BFS aktualisiert werden und kein unnötiger Traffic die Server belasten soll. Aus diesem Grund ist es auch ratsam, die Zeit anzupassen, zu welcher das Script ausgeführt wird, dh. das man es vielleicht nicht am Beginn der Stunde bei Minute 0 ausführt, sondern vielmehr eine leicht andere Zeit angibt, z.B. 5 oder 10 Minuten nach Stundenbeginn. Auch dies soll einfach dazu beitragen, die Last für die Server so gering wie möglich zu halten, selbst wenn dieses oder ein ähnliches Script von vielen Anwendern genutzt wird. 
Ein Beispiel Cronjob, welcher bei einem Debian Server mit dem Befehl ```crontab -e``` in die sich öffnende Datei eingetragen werden kann ist: 

```20 * * * * sudo python RadiationWarner.py```. Vorrausgesetzt es sind alle nötigen Pakete: requests, json, os, datetime, pprint installiert. 

Konfiguration: Im Script selbst sollten noch einige Anpassungen vorgenommen werden, welche den Versandt von E-Mails betrifft. 
Zunächst sollte der smtp Server angegeben werden, welcher zum versenden genutzt werden soll. Diese Adresse lässt sich beim E-Mail Provider herausfinden. 
Dann sollte entsprechend der richtige Port angegeben werden, falls dieser vom standard Port abweicht.
Nun werden die Account Daten des Sendenden Accounts eingetragen, die E-Mail Adresse und darunter das Passwort. 

Aufgrund der Tatsache, dass keine 2FA integriert ist und das Passwort im Klartext gespeichert ist, IST ES DRINGEND EMPFOHLEN EINEN NUR ZU DIESEM ZWECK ERSTELLTEN E-MAIL ACCOUNT ZU VERWENDEN UND EIN LANGES KOMPLEXES PASSWORT ZU NUTZEN.

Danach sind noch die E-Mail Header Daten anzugeben, bestehend aus Absender Adresse (Dieselbe, welche als User des Sendenden Accounts angegeben wurde) und die Empfänger Adresse(n).

Es wird keine Haftung für Schäden übernommen, welche durch die Verwendung dieses Scripts entstehen könnten.
