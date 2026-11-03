"""Builds the language variants of NimbusPL from the multi-language template.

Reads tests/nimbus-template.ax (the multi-language template that ships all six
weather description lists and the Meteoalarm/TERYT machinery) and writes:

  dist/nimbus-tc002-PL.ax  - Polish UI, only Polish descriptions, Meteoalarm (IMGW)
  dist/nimbus-tc002-en.ax  - English UI, no Meteoalarm/TERYT
  dist/nimbus-tc002-de.ax  - German UI, no Meteoalarm/TERYT
  dist/nimbus-tc002-es.ax  - Spanish UI, no Meteoalarm/TERYT
  dist/nimbus-tc002-pt.ax  - Portuguese UI, no Meteoalarm/TERYT

The non-Polish variants drop the whole Meteoalarm feature (config options, the
TERYT county table and the message rendering), because IMGW warnings cover
Poland only.

The template is the source of truth for the shared code; after editing it run
this script to regenerate all five dist files.

Usage: python3 tests/build_langs.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "tests" / "nimbus-template.ax"
VERSION = "2.9.0"
HELP_LIMIT = 96  # AWTRIX NG truncates @config help texts to 96 UTF-8 bytes


def sub1(src, old, new, what):
    """Replace exactly one occurrence; fail loudly on drift."""
    n = src.count(old)
    if n != 1:
        raise SystemExit("build_langs: expected exactly one occurrence of %r (found %d)"
                         % (what, n))
    return src.replace(old, new)


def sub_re(src, pattern, new, what):
    """Replace exactly one regex match (DOTALL); fail loudly on drift."""
    found = list(re.finditer(pattern, src, re.S))
    if len(found) != 1:
        raise SystemExit("build_langs: expected exactly one match for %s (found %d)"
                         % (what, len(found)))
    return src[:found[0].start()] + new + src[found[0].end():]


# ---------------------------------------------------------------------------
# per-language data
# ---------------------------------------------------------------------------

LANG = {
    "PL": {
        "name": "NimbusPL",
        "desc": "Zegar z kalendarzem, pogodą, jakością powietrza PM, odczytami z pomieszczenia i ostrzeżeniami meteoalarm (IMGW)",
        "hub": "# @hub aCQWh4FpWLwK 4410930662c50393922093fa3ecc7adeb28f7d014c755028b7aa4cf066b660b4\n",
        "meteo": True,
        "week3": "NIEPONWTOSROCZWPIASOB",
        "week6": ["NIEDZ", "PONIE", "WTORE", "SRODA", "CZWAR", "PIATE", "SOBOT"],
        "months3": "STYLUTMARKWIMAJCZELIPSIEWRZPAZLISGRU",
        "moon": ["NÓW", "SIERP", "I KWADRA", "GARB", "PEŁNIA", "GARB", "III KWADRA", "SIERP"],
        "night": "CZYSTE NIEBO",
        "descs": ["SŁONECZNIE", "PRZEWAŻNIE SŁONECZNIE", "PRZELOTNE ZACHMURZENIE", "ZACHMURZENIE",
                  "MGŁA", "SZADŹ", "MŻAWKA", "SILNA MŻAWKA", "MŻAWKA MARZNĄCA", "SILNA MŻAWKA MARZNĄCA",
                  "DESZCZ", "ULEWA", "DESZCZ MARZNĄCY", "SILNY DESZCZ MARZNĄCY", "ŚNIEG", "ŚNIEŻYCA",
                  "KRUPA ŚNIEŻNA", "PRZELOTNY DESZCZ", "ULEWNY PRZELOTNY DESZCZ", "PRZELOTNY ŚNIEG",
                  "SILNY PRZELOTNY ŚNIEG", "BURZA", "BURZA Z GRADEM", "BURZA Z SILNYM GRADEM"],
        "config": [
            '# @name NimbusPL',
            '# @desc Zegar z kalendarzem, pogodą, jakością powietrza PM, odczytami z pomieszczenia i ostrzeżeniami meteoalarm (IMGW)',
            '# @author AkdM / olo81',
            '# @version ' + VERSION,
            '# @display 52x16',
            '# @config sweep bool "Efekt wycieraczki (co 5 min)" default=true group="Wyświetlacz" help="Czarny pas czyszczący matrycę przechodzi z prawej do lewej co 5 minut"',
            '# @config t24 bool "Zegar 24-godzinny" default=true group="Czas"',
            '# @config tlz bool "Zero wiodące" default=true group="Czas"',
            '# @config tsep select "Dwukropek" options=stały,mrugający,pulsowanie default=pulsowanie group="Czas"',
            '# @config tcol color "Kolor godziny" default=#FFFFFF group="Czas"',
            '# @config face select "Tarcza zegara" options=kartka,pierścień,duży default=kartka group="Czas"',
            '# @config chc color "Kolor nagłówka" default=#FF0000 group="Kalendarz"',
            '# @config ctc color "Kolor tekstu" default=#000000 group="Kalendarz"',
            '# @config cbc color "Kolor tła" default=#FFFFFF group="Kalendarz"',
            '# @config canim bool "Animacja kalendarza" default=true group="Kalendarz" help="Kartka jest zrywana po pojawieniu się zegara i o północy"',
            '# @config dfmt select "Format daty" options=dd.mm.yy,mm/dd/yy,yy-mm-dd default=dd.mm.yy group="Kalendarz" help="Dla dużej tarczy"',
            '# @config wbar bool "Pasek tygodnia" default=true group="Pasek tygodnia"',
            '# @config wmon bool "Tydzień od poniedziałku" default=true group="Pasek tygodnia"',
            '# @config wtd color "Dzisiaj" default=#FFFFFF group="Pasek tygodnia"',
            '# @config wod color "Pozostałe dni robocze" default=#666666 group="Pasek tygodnia"',
            '# @config wtw color "Dzisiaj w weekend" default=#FFFFFF group="Pasek tygodnia"',
            '# @config wow color "Pozostałe dni weekendowe" default=#666666 group="Pasek tygodnia"',
            '# @config wpan bool "1. Pogoda" default=true group="Karuzela" help="Numer 1 w polu kolejności"',
            '# @config wind bool "2. Porywy wiatru" default=true group="Karuzela" help="Numer 2 w polu kolejności; pojawia się, gdy porywy przekroczą próg"',
            '# @config dpan bool "3. Data" default=true group="Karuzela" help="Numer 3 w polu kolejności"',
            '# @config tpan bool "4. Temperatura" default=true group="Karuzela" help="Numer 4 w polu kolejności"',
            '# @config showpm bool "5. PM2.5" default=true group="Karuzela" help="Numer 5 w polu kolejności"',
            '# @config rpan bool "6. Pokój" default=true group="Karuzela" help="Numer 6 w polu kolejności"',
            '# @config hpan bool "7. Wilgotność" default=true group="Karuzela" help="Numer 7 w polu kolejności"',
            '# @config moon bool "8. Faza księżyca" default=true group="Karuzela" help="Numer 8 w polu kolejności"',
            '# @config meteoalarm_enabled bool "9. Meteoalarm" default=false group="Karuzela" help="Numer 9 w polu kolejności"',
            '# @config order text "Kolejność (numery)" default="" group="Karuzela" help="Numery paneli po przecinku, np. 1,2,3,4,5,6,7,8,9. Puste = kolejność domyślna"',
            '# @config ddur slider "Czas wyświetlania daty" default=10 min=1 max=60 unit=s group="Karuzela"',
            '# @config pdur slider "Czas pozostałych paneli" default=3 min=1 max=60 unit=s group="Karuzela"',
            '# @config wdur slider "Czas panelu pogody" default=10 min=1 max=60 unit=s group="Karuzela" help="Dłuższy czas na odczytanie przewijanego opisu pogody pod ikonką"',
            '# @config wthr slider "Próg porywów wiatru" default=40 min=10 max=100 unit=km/h group="Karuzela" help="Panel wiatru pojawia się, gdy porywy przekroczą ten próg"',
            '# @config pmthr slider "Próg PM2.5" default=30 min=1 max=100 unit=ug/m3 group="Karuzela" help="Panel PM2.5 pojawia się, gdy stężenie przekroczy ten próg"',
            '# @config tran select "Przejście" options=przetarcie,zanikanie,przejście,dół,góra,lewo,prawo,brak default=przetarcie group="Karuzela"',
            '# @config lat number "Szerokość geogr. (Lat)" default=48.8566 min=-90 max=90 step=0.0001 group="Pogoda i Powietrze"',
            '# @config lon number "Długość geogr. (Lon)" default=2.3522 min=-180 max=180 step=0.0001 group="Pogoda i Powietrze"',
            '# @config wref number "Odświeżanie" default=15 min=5 max=120 unit=min group="Pogoda i Powietrze"',
            '# @config wtext text "Własne opisy" default="" group="Pogoda i Powietrze" help="Duża tarcza. Do 24 własnych opisów po przecinku, w kolejności stanów (noc ma stały opis)"',
            '# @config materyt text "TERYT powiatu" default="" group="Pogoda i Powietrze" help="4-cyfrowy TERYT (np. 1465). Puste: auto ze współrzędnych. Kody: eteryt.stat.gov.pl"',
            '# @config maref number "Odświeżanie Meteoalarmu" default=10 min=5 max=120 unit=min group="Pogoda i Powietrze" help="Co ile minut pobierać alert IMGW"',
            '# @config madur slider "Czas komunikatu" default=15 min=5 max=120 unit=s group="Pogoda i Powietrze" help="Jak długo wyświetlać komunikat meteoalarmu"',
            '# @config mafreq slider "Częstotliwość w trakcie zagrożenia" default=10 min=1 max=240 unit=min group="Pogoda i Powietrze" help="Co ile minut pokazywać komunikat w trakcie zagrożenia"',
            '# @config mafreqb slider "Częstotliwość przed zagrożeniem" default=60 min=1 max=240 unit=min group="Pogoda i Powietrze" help="Co ile minut pokazywać komunikat przed rozpoczęciem zagrożenia"',
            '# @config rtopic text "MQTT: Temperatura w pokoju" default="" group="Pokój" help="Na brokerze z ustawień AWTRIX. Puste używa czujnika zegara"',
            '# @config htopic text "MQTT: Wilgotność" default="" group="Pokój" help="Na brokerze z ustawień AWTRIX. Puste używa czujnika zegara"',
            '# @config rcol color "Kolor temperatury w pokoju" default=#FFFFFF group="Pokój"',
            '# @config hcol color "Kolor wilgotności" default=#00AAFF group="Pokój"',
            '# @config night bool "Tryb nocny" default=false group="Tryb nocny"',
            '# @config nauto bool "Automatyczny tryb nocny" default=false group="Tryb nocny" help="Pomiędzy poniższymi godzinami"',
            '# @config nfrom number "Od godziny" default=22 min=0 max=23 unit=h group="Tryb nocny"',
            '# @config nto number "Do godziny" default=7 min=0 max=23 unit=h group="Tryb nocny"',
            '# @config nbar bool "Pasek tygodnia w nocy" default=true group="Tryb nocny"',
            '# @config npause bool "Wstrzymaj rotację w nocy" default=false group="Tryb nocny"',
            '# @config nbri number "Jasność nocna" default=0 min=0 max=255 group="Tryb nocny" help="0 zachowuje jasność urządzenia; inna wartość ustawi jasność na noc"',
            '# @config ntopic text "MQTT Topic trybu nocnego" default="" group="Tryb nocny" help="Payload: on/off, true/false lub 1/0"',
        ],
    },
    "en": {
        "name": "NimbusEN",
        "desc": "Clock with calendar, weather, PM2.5 air quality and room values",
        "hub": "",
        "meteo": False,
        "week3": "SUNMONTUEWEDTHUFRISAT",
        "week6": ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"],
        "months3": "JANFEBMARAPRMAYJUNJULAUGSEPOCTNOVDEC",
        "moon": ["NEW", "CRESCENT", "1ST QUARTER", "GIBBOUS", "FULL", "GIBBOUS", "3RD QUARTER", "CRESCENT"],
        "night": "CLEAR NIGHT",
        "descs": ["CLEAR", "MOSTLY CLEAR", "PARTLY CLOUDY", "OVERCAST", "FOG", "RIME", "DRIZZLE",
                  "HEAVY DRIZZLE", "FREEZING DRIZZLE", "HEAVY FREEZING DRIZZLE", "RAIN", "HEAVY RAIN",
                  "FREEZING RAIN", "HEAVY FREEZING RAIN", "SNOW", "HEAVY SNOW", "SNOW GRAINS",
                  "RAIN SHOWERS", "HEAVY RAIN SHOWERS", "SNOW SHOWERS", "HEAVY SNOW SHOWERS",
                  "THUNDERSTORM", "HAIL STORM", "HEAVY HAIL STORM"],
        "config": [
            '# @name NimbusEN',
            '# @desc Clock with calendar, weather, PM2.5 air quality and room values',
            '# @author AkdM / olo81',
            '# @version ' + VERSION,
            '# @display 52x16',
            '# @config sweep bool "Wiper effect (every 5 min)" default=true group="Display" help="A black cleaning bar sweeps the matrix right-to-left every 5 minutes"',
            '# @config t24 bool "24-hour clock" default=true group="Time"',
            '# @config tlz bool "Leading zero" default=true group="Time"',
            '# @config tsep select "Colon" options=steady,blink,pulse default=pulse group="Time"',
            '# @config tcol color "Time color" default=#FFFFFF group="Time"',
            '# @config face select "Clock face" options=sheet,ring,big default=sheet group="Time"',
            '# @config chc color "Header color" default=#FF0000 group="Calendar"',
            '# @config ctc color "Text color" default=#000000 group="Calendar"',
            '# @config cbc color "Background color" default=#FFFFFF group="Calendar"',
            '# @config canim bool "Calendar animation" default=true group="Calendar" help="The sheet is torn off when the clock appears and at midnight"',
            '# @config dfmt select "Date format" options=dd.mm.yy,mm/dd/yy,yy-mm-dd default=dd.mm.yy group="Calendar" help="For the big face"',
            '# @config wbar bool "Week bar" default=true group="Week bar"',
            '# @config wmon bool "Week starts Monday" default=true group="Week bar"',
            '# @config wtd color "Today" default=#FFFFFF group="Week bar"',
            '# @config wod color "Other weekdays" default=#666666 group="Week bar"',
            '# @config wtw color "Today on a weekend" default=#FFFFFF group="Week bar"',
            '# @config wow color "Other weekend days" default=#666666 group="Week bar"',
            '# @config wpan bool "1. Weather" default=true group="Carousel" help="Number 1 in the order field"',
            '# @config wind bool "2. Wind gusts" default=true group="Carousel" help="Number 2 in the order field; shows when gusts exceed the threshold"',
            '# @config dpan bool "3. Date" default=true group="Carousel" help="Number 3 in the order field"',
            '# @config tpan bool "4. Temperature" default=true group="Carousel" help="Number 4 in the order field"',
            '# @config showpm bool "5. PM2.5" default=true group="Carousel" help="Number 5 in the order field"',
            '# @config rpan bool "6. Room" default=true group="Carousel" help="Number 6 in the order field"',
            '# @config hpan bool "7. Humidity" default=true group="Carousel" help="Number 7 in the order field"',
            '# @config moon bool "8. Moon phase" default=true group="Carousel" help="Number 8 in the order field"',
            '# @config order text "Order (numbers)" default="" group="Carousel" help="Panel numbers separated by commas, e.g. 1,2,3,4,5,6,7,8. Empty = default order"',
            '# @config ddur slider "Date duration" default=10 min=1 max=60 unit=s group="Carousel"',
            '# @config pdur slider "Other panels duration" default=3 min=1 max=60 unit=s group="Carousel"',
            '# @config wdur slider "Weather panel duration" default=10 min=1 max=60 unit=s group="Carousel" help="More time to read the scrolling weather description under the icon"',
            '# @config wthr slider "Wind gust threshold" default=40 min=10 max=100 unit=km/h group="Carousel" help="The wind panel appears when gusts exceed this threshold"',
            '# @config pmthr slider "PM2.5 threshold" default=30 min=1 max=100 unit=ug/m3 group="Carousel" help="The PM2.5 panel appears when the concentration exceeds this threshold"',
            '# @config tran select "Transition" options=wipe,fade,morph,down,up,left,right,none default=wipe group="Carousel"',
            '# @config lat number "Latitude" default=48.8566 min=-90 max=90 step=0.0001 group="Weather & Air"',
            '# @config lon number "Longitude" default=2.3522 min=-180 max=180 step=0.0001 group="Weather & Air"',
            '# @config wref number "Refresh" default=15 min=5 max=120 unit=min group="Weather & Air"',
            '# @config wtext text "Custom descriptions" default="" group="Weather & Air" help="Big face. Up to 24 custom descriptions, comma separated, in state order"',
            '# @config rtopic text "MQTT: Room temperature" default="" group="Room" help="On the broker set in AWTRIX settings. Empty uses the clock sensor"',
            '# @config htopic text "MQTT: Humidity" default="" group="Room" help="On the broker set in AWTRIX settings. Empty uses the clock sensor"',
            '# @config rcol color "Room temperature color" default=#FFFFFF group="Room"',
            '# @config hcol color "Humidity color" default=#00AAFF group="Room"',
            '# @config night bool "Night mode" default=false group="Night mode"',
            '# @config nauto bool "Automatic night mode" default=false group="Night mode" help="Between the hours below"',
            '# @config nfrom number "From hour" default=22 min=0 max=23 unit=h group="Night mode"',
            '# @config nto number "Until hour" default=7 min=0 max=23 unit=h group="Night mode"',
            '# @config nbar bool "Week bar at night" default=true group="Night mode"',
            '# @config npause bool "Pause rotation at night" default=false group="Night mode"',
            '# @config nbri number "Night brightness" default=0 min=0 max=255 group="Night mode" help="0 keeps the device brightness; any other value sets the night brightness"',
            '# @config ntopic text "MQTT Topic for night mode" default="" group="Night mode" help="Payload: on/off, true/false or 1/0"',
        ],
    },
    "de": {
        "name": "NimbusDE",
        "desc": "Uhr mit Kalender, Wetter, PM2.5-Luftqualität und Raumwerten",
        "hub": "",
        "meteo": False,
        "week3": "SONMONDIEMITDONFRISAM",
        "week6": ["SON", "MON", "DIE", "MIT", "DON", "FRE", "SAM"],
        "months3": "JANFEBMRZAPRMAIJUNJULAUGSEPOKTNOVDEZ",
        "moon": ["NEUMOND", "SICHEL", "1. VIERTEL", "ZUNEHMEND", "VOLLMOND", "ABNEHMEND", "3. VIERTEL", "SICHEL"],
        "night": "KLARE NACHT",
        "descs": ["KLAR", "MEIST KLAR", "HEITER", "BEDECKT", "NEBEL", "REIF", "NIESEL", "STARKER NIESEL",
                  "GEFRIERENDER NIESEL", "STARKER GEFRIERENDER NIESEL", "REGEN", "STARKREGEN",
                  "GEFRIERENDER REGEN", "STARKER GEFRIERENDER REGEN", "SCHNEE", "SCHNEESTURM",
                  "SCHNEEGRIESEL", "REGENSCHAUER", "STARKER REGENSCHAUER", "SCHNEESCHAUER",
                  "STARKER SCHNEESCHAUER", "GEWITTER", "HAGELGEWITTER", "GEWITTER MIT STARKEM HAGEL"],
        "config": [
            '# @name NimbusDE',
            '# @desc Uhr mit Kalender, Wetter, PM2.5-Luftqualität und Raumwerten',
            '# @author AkdM / olo81',
            '# @version ' + VERSION,
            '# @display 52x16',
            '# @config sweep bool "Wischereffekt (alle 5 min)" default=true group="Anzeige" help="Ein schwarzer Reinigungsbalken fährt alle 5 Minuten von rechts nach links über die Matrix"',
            '# @config t24 bool "24-Stunden-Uhr" default=true group="Zeit"',
            '# @config tlz bool "Führende Null" default=true group="Zeit"',
            '# @config tsep select "Doppelpunkt" options=steady,blink,pulse default=pulse group="Zeit"',
            '# @config tcol color "Farbe der Uhrzeit" default=#FFFFFF group="Zeit"',
            '# @config face select "Zifferblatt" options=sheet,ring,big default=sheet group="Zeit"',
            '# @config chc color "Farbe der Kopfzeile" default=#FF0000 group="Kalender"',
            '# @config ctc color "Textfarbe" default=#000000 group="Kalender"',
            '# @config cbc color "Hintergrundfarbe" default=#FFFFFF group="Kalender"',
            '# @config canim bool "Kalenderanimation" default=true group="Kalender" help="Das Blatt wird beim Erscheinen der Uhr und um Mitternacht abgerissen"',
            '# @config dfmt select "Datumsformat" options=dd.mm.yy,mm/dd/yy,yy-mm-dd default=dd.mm.yy group="Kalender" help="Für das große Zifferblatt"',
            '# @config wbar bool "Wochenleiste" default=true group="Wochenleiste"',
            '# @config wmon bool "Woche beginnt Montag" default=true group="Wochenleiste"',
            '# @config wtd color "Heute" default=#FFFFFF group="Wochenleiste"',
            '# @config wod color "Andere Werktage" default=#666666 group="Wochenleiste"',
            '# @config wtw color "Heute am Wochenende" default=#FFFFFF group="Wochenleiste"',
            '# @config wow color "Andere Wochenendtage" default=#666666 group="Wochenleiste"',
            '# @config wpan bool "1. Wetter" default=true group="Karussell" help="Nummer 1 im Reihenfolge-Feld"',
            '# @config wind bool "2. Windböen" default=true group="Karussell" help="Nummer 2 im Reihenfolge-Feld; erscheint, wenn die Böen die Schwelle überschreiten"',
            '# @config dpan bool "3. Datum" default=true group="Karussell" help="Nummer 3 im Reihenfolge-Feld"',
            '# @config tpan bool "4. Temperatur" default=true group="Karussell" help="Nummer 4 im Reihenfolge-Feld"',
            '# @config showpm bool "5. PM2.5" default=true group="Karussell" help="Nummer 5 im Reihenfolge-Feld"',
            '# @config rpan bool "6. Raum" default=true group="Karussell" help="Nummer 6 im Reihenfolge-Feld"',
            '# @config hpan bool "7. Luftfeuchte" default=true group="Karussell" help="Nummer 7 im Reihenfolge-Feld"',
            '# @config moon bool "8. Mondphase" default=true group="Karussell" help="Nummer 8 im Reihenfolge-Feld"',
            '# @config order text "Reihenfolge (Nummern)" default="" group="Karussell" help="Panelnummern durch Kommas getrennt, z. B. 1,2,3,4,5,6,7,8. Leer = Standardreihenfolge"',
            '# @config ddur slider "Dauer des Datums" default=10 min=1 max=60 unit=s group="Karussell"',
            '# @config pdur slider "Dauer der anderen Panels" default=3 min=1 max=60 unit=s group="Karussell"',
            '# @config wdur slider "Dauer des Wetter-Panels" default=10 min=1 max=60 unit=s group="Karussell" help="Mehr Zeit, um die scrollende Wetterbeschreibung unter dem Symbol zu lesen"',
            '# @config wthr slider "Schwelle für Windböen" default=40 min=10 max=100 unit=km/h group="Karussell" help="Das Wind-Panel erscheint, wenn die Böen diese Schwelle überschreiten"',
            '# @config pmthr slider "PM2.5-Schwelle" default=30 min=1 max=100 unit=ug/m3 group="Karussell" help="Das PM2.5-Panel erscheint, wenn die Konzentration diese Schwelle überschreitet"',
            '# @config tran select "Übergang" options=wipe,fade,morph,down,up,left,right,none default=wipe group="Karussell"',
            '# @config lat number "Breitengrad" default=48.8566 min=-90 max=90 step=0.0001 group="Wetter & Luft"',
            '# @config lon number "Längengrad" default=2.3522 min=-180 max=180 step=0.0001 group="Wetter & Luft"',
            '# @config wref number "Aktualisierung" default=15 min=5 max=120 unit=min group="Wetter & Luft"',
            '# @config wtext text "Eigene Beschreibungen" default="" group="Wetter & Luft" help="Großes Zifferblatt. Bis zu 24 eigene Beschreibungen, Komma-getrennt"',
            '# @config rtopic text "MQTT: Raumtemperatur" default="" group="Raum" help="Auf dem Broker aus den AWTRIX-Einstellungen. Leer nutzt den Uhr-Sensor"',
            '# @config htopic text "MQTT: Luftfeuchte" default="" group="Raum" help="Auf dem Broker aus den AWTRIX-Einstellungen. Leer nutzt den Uhr-Sensor"',
            '# @config rcol color "Farbe der Raumtemperatur" default=#FFFFFF group="Raum"',
            '# @config hcol color "Farbe der Luftfeuchte" default=#00AAFF group="Raum"',
            '# @config night bool "Nachtmodus" default=false group="Nachtmodus"',
            '# @config nauto bool "Automatischer Nachtmodus" default=false group="Nachtmodus" help="Zwischen den unten angegebenen Stunden"',
            '# @config nfrom number "Von Stunde" default=22 min=0 max=23 unit=h group="Nachtmodus"',
            '# @config nto number "Bis Stunde" default=7 min=0 max=23 unit=h group="Nachtmodus"',
            '# @config nbar bool "Wochenleiste nachts" default=true group="Nachtmodus"',
            '# @config npause bool "Rotation nachts pausieren" default=false group="Nachtmodus"',
            '# @config nbri number "Nacht-Helligkeit" default=0 min=0 max=255 group="Nachtmodus" help="0 behält die Gerätehelligkeit bei; ein anderer Wert setzt die Helligkeit für die Nacht"',
            '# @config ntopic text "MQTT-Topic für den Nachtmodus" default="" group="Nachtmodus" help="Payload: on/off, true/false oder 1/0"',
        ],
    },
    "es": {
        "name": "NimbusES",
        "desc": "Reloj con calendario, tiempo, calidad del aire PM2.5 y valores de la habitación",
        "hub": "",
        "meteo": False,
        "week3": "DOMLUNMARMIEJUEVIESAB",
        "week6": ["DOM", "LUN", "MAR", "MIE", "JUE", "VIE", "SAB"],
        "months3": "ENEFEBMARABRMAYJUNJULAGOSEPOCTNOVDIC",
        "moon": ["NUEVA", "CRECIENTE", "1ER CUARTO", "GIBOSA", "LLENA", "GIBOSA", "3ER CUARTO", "CRECIENTE"],
        "night": "NOCHE DESPEJADA",
        "descs": ["DESPEJADO", "MAYORMENTE DESPEJADO", "POCO NUBOSO", "CUBIERTO", "NIEBLA", "CENCELLADA",
                  "LLOVIZNA", "LLOVIZNA FUERTE", "LLOVIZNA HELADA", "LLOVIZNA HELADA FUERTE", "LLUVIA",
                  "LLUVIA FUERTE", "LLUVIA HELADA", "LLUVIA HELADA FUERTE", "NIEVE", "VENTISCA", "CINARRA",
                  "CHUBASCOS", "CHUBASCOS FUERTES", "CHUBASCOS DE NIEVE", "CHUBASCOS DE NIEVE FUERTES",
                  "TORMENTA", "TORMENTA CON GRANIZO", "TORMENTA CON GRANIZO FUERTE"],
        "config": [
            '# @name NimbusES',
            '# @desc Reloj con calendario, tiempo, calidad del aire PM2.5 y valores de la habitación',
            '# @author AkdM / olo81',
            '# @version ' + VERSION,
            '# @display 52x16',
            '# @config sweep bool "Efecto limpiaparabrisas (cada 5 min)" default=true group="Pantalla" help="Una barra negra de limpieza recorre la matriz de derecha a izquierda cada 5 minutos"',
            '# @config t24 bool "Reloj de 24 horas" default=true group="Hora"',
            '# @config tlz bool "Cero a la izquierda" default=true group="Hora"',
            '# @config tsep select "Dos puntos" options=steady,blink,pulse default=pulse group="Hora"',
            '# @config tcol color "Color de la hora" default=#FFFFFF group="Hora"',
            '# @config face select "Esfera del reloj" options=sheet,ring,big default=sheet group="Hora"',
            '# @config chc color "Color del encabezado" default=#FF0000 group="Calendario"',
            '# @config ctc color "Color del texto" default=#000000 group="Calendario"',
            '# @config cbc color "Color de fondo" default=#FFFFFF group="Calendario"',
            '# @config canim bool "Animación del calendario" default=true group="Calendario" help="La hoja se arranca cuando aparece el reloj y a medianoche"',
            '# @config dfmt select "Formato de fecha" options=dd.mm.yy,mm/dd/yy,yy-mm-dd default=dd.mm.yy group="Calendario" help="Para la esfera grande"',
            '# @config wbar bool "Barra semanal" default=true group="Barra semanal"',
            '# @config wmon bool "La semana empieza el lunes" default=true group="Barra semanal"',
            '# @config wtd color "Hoy" default=#FFFFFF group="Barra semanal"',
            '# @config wod color "Otros días laborables" default=#666666 group="Barra semanal"',
            '# @config wtw color "Hoy en fin de semana" default=#FFFFFF group="Barra semanal"',
            '# @config wow color "Otros días de fin de semana" default=#666666 group="Barra semanal"',
            '# @config wpan bool "1. Tiempo" default=true group="Carrusel" help="Número 1 en el campo de orden"',
            '# @config wind bool "2. Rachas de viento" default=true group="Carrusel" help="Número 2 en el campo de orden; aparece cuando las rachas superan el umbral"',
            '# @config dpan bool "3. Fecha" default=true group="Carrusel" help="Número 3 en el campo de orden"',
            '# @config tpan bool "4. Temperatura" default=true group="Carrusel" help="Número 4 en el campo de orden"',
            '# @config showpm bool "5. PM2.5" default=true group="Carrusel" help="Número 5 en el campo de orden"',
            '# @config rpan bool "6. Habitación" default=true group="Carrusel" help="Número 6 en el campo de orden"',
            '# @config hpan bool "7. Humedad" default=true group="Carrusel" help="Número 7 en el campo de orden"',
            '# @config moon bool "8. Fase lunar" default=true group="Carrusel" help="Número 8 en el campo de orden"',
            '# @config order text "Orden (números)" default="" group="Carrusel" help="Números de paneles separados por comas, p. ej. 1,2,3,4,5,6,7,8. Vacío = orden predeterminado"',
            '# @config ddur slider "Duración de la fecha" default=10 min=1 max=60 unit=s group="Carrusel"',
            '# @config pdur slider "Duración de otros paneles" default=3 min=1 max=60 unit=s group="Carrusel"',
            '# @config wdur slider "Duración del panel del tiempo" default=10 min=1 max=60 unit=s group="Carrusel" help="Más tiempo para leer la descripción deslizante del tiempo bajo el icono"',
            '# @config wthr slider "Umbral de rachas de viento" default=40 min=10 max=100 unit=km/h group="Carrusel" help="El panel de viento aparece cuando las rachas superan este umbral"',
            '# @config pmthr slider "Umbral de PM2.5" default=30 min=1 max=100 unit=ug/m3 group="Carrusel" help="El panel PM2.5 aparece cuando la concentración supera este umbral"',
            '# @config tran select "Transición" options=wipe,fade,morph,down,up,left,right,none default=wipe group="Carrusel"',
            '# @config lat number "Latitud" default=48.8566 min=-90 max=90 step=0.0001 group="Tiempo y Aire"',
            '# @config lon number "Longitud" default=2.3522 min=-180 max=180 step=0.0001 group="Tiempo y Aire"',
            '# @config wref number "Actualización" default=15 min=5 max=120 unit=min group="Tiempo y Aire"',
            '# @config wtext text "Descripciones propias" default="" group="Tiempo y Aire" help="Esfera grande. Hasta 24 descripciones propias, separadas por comas"',
            '# @config rtopic text "MQTT: Temperatura de la habitación" default="" group="Habitación" help="En el broker de los ajustes de AWTRIX. Vacío usa el sensor del reloj"',
            '# @config htopic text "MQTT: Humedad" default="" group="Habitación" help="En el broker de los ajustes de AWTRIX. Vacío usa el sensor del reloj"',
            '# @config rcol color "Color de la temperatura" default=#FFFFFF group="Habitación"',
            '# @config hcol color "Color de la humedad" default=#00AAFF group="Habitación"',
            '# @config night bool "Modo nocturno" default=false group="Modo nocturno"',
            '# @config nauto bool "Modo nocturno automático" default=false group="Modo nocturno" help="Entre las horas indicadas abajo"',
            '# @config nfrom number "Desde la hora" default=22 min=0 max=23 unit=h group="Modo nocturno"',
            '# @config nto number "Hasta la hora" default=7 min=0 max=23 unit=h group="Modo nocturno"',
            '# @config nbar bool "Barra semanal de noche" default=true group="Modo nocturno"',
            '# @config npause bool "Pausar la rotación de noche" default=false group="Modo nocturno"',
            '# @config nbri number "Brillo nocturno" default=0 min=0 max=255 group="Modo nocturno" help="0 mantiene el brillo del dispositivo; otro valor fija el brillo nocturno"',
            '# @config ntopic text "Topic MQTT del modo nocturno" default="" group="Modo nocturno" help="Payload: on/off, true/false o 1/0"',
        ],
    },
    "pt": {
        "name": "NimbusPT",
        "desc": "Relógio com calendário, tempo, qualidade do ar PM2.5 e valores do quarto",
        "hub": "",
        "meteo": False,
        "week3": "DOMSEGTERQUAQUISEXSAB",
        "week6": ["DOM", "SEG", "TER", "QUA", "QUI", "SEX", "SAB"],
        "months3": "JANFEVMARABRMAIJUNJULAGOSETOUTNOVDEZ",
        "moon": ["NOVA", "CRESCENTE", "QUARTO CRES", "GIBOSA", "CHEIA", "GIBOSA", "QUARTO MIN", "CRESCENTE"],
        "night": "NOITE LIMPA",
        "descs": ["LIMPO", "QUASE LIMPO", "NUBLADO", "ENCOBERTO", "NEVOEIRO", "SINCELO", "GAROA",
                  "GAROA FORTE", "GAROA GELADA", "GAROA GELADA FORTE", "CHUVA", "CHUVA FORTE",
                  "CHUVA CONGELANTE", "CHUVA CONGELANTE FORTE", "NEVE", "NEVASCA", "GRANIZO MIÚDO",
                  "AGUACEIROS", "AGUACEIROS FORTES", "AGUACEIROS DE NEVE", "AGUACEIROS DE NEVE FORTES",
                  "TROVOADA", "TORMENTA DE GRANIZO", "TROVOADA COM GRANIZO FORTE"],
        "config": [
            '# @name NimbusPT',
            '# @desc Relógio com calendário, tempo, qualidade do ar PM2.5 e valores do quarto',
            '# @author AkdM / olo81',
            '# @version ' + VERSION,
            '# @display 52x16',
            '# @config sweep bool "Efeito limpa-para-brisas (a cada 5 min)" default=true group="Ecrã" help="Uma barra preta de limpeza percorre a matriz da direita para a esquerda a cada 5 minutos"',
            '# @config t24 bool "Relógio de 24 horas" default=true group="Hora"',
            '# @config tlz bool "Zero à esquerda" default=true group="Hora"',
            '# @config tsep select "Dois pontos" options=steady,blink,pulse default=pulse group="Hora"',
            '# @config tcol color "Cor da hora" default=#FFFFFF group="Hora"',
            '# @config face select "Mostrador do relógio" options=sheet,ring,big default=sheet group="Hora"',
            '# @config chc color "Cor do cabeçalho" default=#FF0000 group="Calendário"',
            '# @config ctc color "Cor do texto" default=#000000 group="Calendário"',
            '# @config cbc color "Cor de fundo" default=#FFFFFF group="Calendário"',
            '# @config canim bool "Animação do calendário" default=true group="Calendário" help="A folha é arrancada quando o relógio aparece e à meia-noite"',
            '# @config dfmt select "Formato da data" options=dd.mm.yy,mm/dd/yy,yy-mm-dd default=dd.mm.yy group="Calendário" help="Para o mostrador grande"',
            '# @config wbar bool "Barra semanal" default=true group="Barra semanal"',
            '# @config wmon bool "Semana começa na segunda" default=true group="Barra semanal"',
            '# @config wtd color "Hoje" default=#FFFFFF group="Barra semanal"',
            '# @config wod color "Outros dias úteis" default=#666666 group="Barra semanal"',
            '# @config wtw color "Hoje no fim de semana" default=#FFFFFF group="Barra semanal"',
            '# @config wow color "Outros dias de fim de semana" default=#666666 group="Barra semanal"',
            '# @config wpan bool "1. Tempo" default=true group="Carrossel" help="Número 1 no campo de ordem"',
            '# @config wind bool "2. Rajadas de vento" default=true group="Carrossel" help="Número 2 no campo de ordem; aparece quando as rajadas ultrapassam o limiar"',
            '# @config dpan bool "3. Data" default=true group="Carrossel" help="Número 3 no campo de ordem"',
            '# @config tpan bool "4. Temperatura" default=true group="Carrossel" help="Número 4 no campo de ordem"',
            '# @config showpm bool "5. PM2.5" default=true group="Carrossel" help="Número 5 no campo de ordem"',
            '# @config rpan bool "6. Quarto" default=true group="Carrossel" help="Número 6 no campo de ordem"',
            '# @config hpan bool "7. Humidade" default=true group="Carrossel" help="Número 7 no campo de ordem"',
            '# @config moon bool "8. Fase da lua" default=true group="Carrossel" help="Número 8 no campo de ordem"',
            '# @config order text "Ordem (números)" default="" group="Carrossel" help="Números dos painéis separados por vírgulas, ex.: 1,2,3,4,5,6,7,8. Vazio = ordem predefinida"',
            '# @config ddur slider "Duração da data" default=10 min=1 max=60 unit=s group="Carrossel"',
            '# @config pdur slider "Duração dos outros painéis" default=3 min=1 max=60 unit=s group="Carrossel"',
            '# @config wdur slider "Duração do painel do tempo" default=10 min=1 max=60 unit=s group="Carrossel" help="Mais tempo para ler a descrição deslizante do tempo sob o ícone"',
            '# @config wthr slider "Limiar de rajadas de vento" default=40 min=10 max=100 unit=km/h group="Carrossel" help="O painel de vento aparece quando as rajadas ultrapassam este limiar"',
            '# @config pmthr slider "Limiar de PM2.5" default=30 min=1 max=100 unit=ug/m3 group="Carrossel" help="O painel PM2.5 aparece quando a concentração ultrapassa este limiar"',
            '# @config tran select "Transição" options=wipe,fade,morph,down,up,left,right,none default=wipe group="Carrossel"',
            '# @config lat number "Latitude" default=48.8566 min=-90 max=90 step=0.0001 group="Tempo e Ar"',
            '# @config lon number "Longitude" default=2.3522 min=-180 max=180 step=0.0001 group="Tempo e Ar"',
            '# @config wref number "Atualização" default=15 min=5 max=120 unit=min group="Tempo e Ar"',
            '# @config wtext text "Descrições próprias" default="" group="Tempo e Ar" help="Mostrador grande. Até 24 descrições próprias, separadas por vírgulas"',
            '# @config rtopic text "MQTT: Temperatura do quarto" default="" group="Quarto" help="No broker das definições do AWTRIX. Vazio usa o sensor do relógio"',
            '# @config htopic text "MQTT: Humidade" default="" group="Quarto" help="No broker das definições do AWTRIX. Vazio usa o sensor do relógio"',
            '# @config rcol color "Cor da temperatura do quarto" default=#FFFFFF group="Quarto"',
            '# @config hcol color "Cor da humidade" default=#00AAFF group="Quarto"',
            '# @config night bool "Modo noturno" default=false group="Modo noturno"',
            '# @config nauto bool "Modo noturno automático" default=false group="Modo noturno" help="Entre as horas abaixo"',
            '# @config nfrom number "Da hora" default=22 min=0 max=23 unit=h group="Modo noturno"',
            '# @config nto number "Até à hora" default=7 min=0 max=23 unit=h group="Modo noturno"',
            '# @config nbar bool "Barra semanal à noite" default=true group="Modo noturno"',
            '# @config npause bool "Pausar a rotação à noite" default=false group="Modo noturno"',
            '# @config nbri number "Brilho noturno" default=0 min=0 max=255 group="Modo noturno" help="0 mantém o brilho do dispositivo; outro valor define o brilho noturno"',
            '# @config ntopic text "Tópico MQTT do modo noturno" default="" group="Modo noturno" help="Payload: on/off, true/false ou 1/0"',
        ],
    },
}

ORDER = ["PL", "en", "de", "es", "pt"]

# ---------------------------------------------------------------------------
# meteoalarm removal (non-Polish variants)
# ---------------------------------------------------------------------------

METEO_STRIP = [
    # member variables
    ("var r,aq,ar,ma1,maQ,maB,ma_enabled,ma_ref_rate,maText,maLvl,maCol,mc,maFrom,maTo,maMsg,maNext,maUntil,maDur,maFreq,maFreqB,mao,wao,maTeryt,moon_on,moonp,mo,mos,wind_on,wthr,w8prev",
     "var r,aq,ar,wao,moon_on,moonp,mo,mos,wind_on,wthr,w8prev"),
    ("var pmthr,p5prev,fg,fgh,showpm,pl", "var pmthr,p5prev,fg,fgh,showpm"),
    # init
    ("self.ma_enabled=store.get(\"meteoalarm_enabled\",false)", ""),
    ("var rf=store.get(\"maref\")self.ma_ref_rate=(rf==nil?10:rf)*60 var md=store.get(\"madur\")self.maDur=(md==nil?15:md)*1000 var mf=store.get(\"mafreq\")self.maFreq=(mf==nil?10:mf)*60 var mb=store.get(\"mafreqb\")self.maFreqB=(mb==nil?60:mb)*60 ", ""),
    ("self.wao={\"mode\":\"loop\",\"speed\":40,\"direction\":\"left\",\"gap\":28}self.mao={\"mode\":\"loop\",\"speed\":40,\"direction\":\"left\",\"gap\":10}",
     "self.wao={\"mode\":\"loop\",\"speed\":40,\"direction\":\"left\",\"gap\":28}"),
    ("var mt=store.get(\"materyt\")var mts=re.matchall(\"[0-9]+\",mt)self.maTeryt=size(mts)>0&&size(mts[0])==4?mts[0]:\"\" var la=store.get(\"lat\")var lo=store.get(\"lon\")if self.maTeryt==\"\"&&(la<49||la>55||lo<14||lo>24.5)self.ma_enabled=false end ", ""),
    (" elif n==9&&self.ma_enabled a=6", ""),
    (" elif n2==9&&self.ma_enabled a=6", ""),
    ("self.pl={}self.pl[\"Ą\"]=self.v(\"./##./#.#/###/#.#/##.#\")self.pl[\"Ć\"]=self.v(\".#/.#/#.#/#/#.#/.#\")self.pl[\"Ę\"]=self.v(\"./###/#/###/#/###.#\")self.pl[\"Ł\"]=self.v(\"./#./#./##./#./###\")self.pl[\"Ń\"]=self.v(\".#/##./#.#/#.#/#.#/#.#\")self.pl[\"Ó\"]=self.v(\".#/.#/#.#/#.#/#.#/.#\")self.pl[\"Ś\"]=self.v(\".#/.##/#../.#./..#/##.\")self.pl[\"Ź\"]=self.v(\".#/###/..#/.#./#../###\")self.pl[\"Ż\"]=self.v(\".#./###/..#/.#./#../###\")", ""),
    # loop
    ("if self.maText!=nil var ns=self.mts()if self.maTo!=\"\"&&ns>=self.maTo self.maText=nil self.maMsg=\"\" self.maUntil=0 self.maNext=0 else var nw=now_ms()if self.maNext==0||nw>=self.maNext self.maUntil=nw+self.maDur self.maNext=nw+((self.maFrom==\"\"||ns>=self.maFrom)?self.maFreq*1000:self.maFreqB*1000)self.M=0 end end end ", ""),
    ("if self.d==6&&(self.maText==nil||now_ms()>=self.maUntil)self.M=0 end ", ""),
    ("var msg=self.maText!=nil&&self.maUntil>0&&now_ms()<self.maUntil var a=0 if msg var k6=self.c.find(6)if k6!=nil self.L=k6 a=6 end else ", "var a=0 "),
    ("self.L=f end if a!=self.d", "self.L=f if a!=self.d"),
    ("self.B-=1\n    self.maB-=1\n", "self.B-=1\n"),
    ("\n    if self.ma_enabled && self.maB <= 0 && !self.maQ\n        self.maQ = true\n        self.maB = self.ma_ref_rate\n        http.get(self.ma1,/o,c->self.ma_cb(o,c))\n    end\n", "\n"),
    # mok
    ("def mok(i)\n  if i==6 return false end\n", "def mok(i)\n"),
    # panel renderers
    (" elif b==6 var t6=self.maText if t6==nil return end var u6=c<1?self.b(self.maCol,c):self.maCol if self.e<2 rect_fill(d,e,15,9,u6)if self.k==nil||(self.k>=50)==self.D scroll_text(d,e+7,15,\"METEOALARM\",0x000000,self.mao)end else rect_fill(d,e,15,16,u6)if self.k==nil||(self.k>=50)==self.D scroll_text(d,e+11,15,\"METEOALARM\",0x000000,self.mao)end end ",
     " "),
    (" elif b==6 var t6=self.maMsg if t6==nil return end var t6u=self.mup(t6)var u6=a<1?self.b(self.maCol,a):self.maCol var lw=self.E(\"METEOALARM\",self.a)+2 var total=lw+1+self.ma_w(t6u)+10 var off=int(now_ms()*40/1000)%total var lx=c+52-off rect_fill(lx,11,lw,5,u6)self.l(lx+1,11,\"METEOALARM\",self.a,0x000000)self.lm(lx+lw+1,11,t6u,u6,0,52) ",
     " "),
    # draw
    ("var mv=self.maText!=nil&&l<self.maUntil ", ""),
    ("a<2&&!mv&&self.d!=2&&self.d!=8", "a<2&&self.d!=2&&self.d!=8"),
    ("if !o&&a<2&&mv scroll_text(0,15,52,self.maMsg,self.maCol,self.mao)end ", ""),
]

METEO_STRIP_RE = [
    # the TERYT county table and the IMGW URL / message state
    (r"if self\.ma_enabled&&self\.maTeryt==\"\"[\s\S]*?self\.mc=nil end ", ""),
    (r"self\.ma1=self\.maTeryt!=\"\"\?\"https://danepubliczne\.imgw\.pl/api/data/warningsmeteo/teryt/\"\+self\.maTeryt:\"https://danepubliczne\.imgw\.pl/api/data/warningsmeteo\"self\.maQ=false self\.maB=0 self\.maText=nil self\.maLvl=1 self\.maCol=0xFFC800 self\.maFrom=\"\" self\.maTo=\"\" self\.maMsg=\"\" self\.maNext=0 self\.maUntil=0 ", ""),
    # helper functions used only by the meteoalarm message
    (r"def lm\(c,f,e,h,w0,w1\)[^\n]*?return c end", ""),
    (r"def ma_w\(s\)[^\n]*?return c end", ""),
    (r"def mup\(s\)[^\n]*?return s end", ""),
    (r"def mts\(\)[\s\S]*?\nend ", ""),
    (r"def mdec\(s\)[\s\S]*?\nend ", ""),
    (r"def ma_cb\(c,g\)[\s\S]*?\nend ", ""),
]


def build_one(tag, src):
    lang = LANG[tag]
    head, sep, code = src.partition("import math")
    assert sep, "template lost its 'import math'"
    # 1. config block
    cfg = "\n".join(lang["config"]) + "\n"
    head = lang["hub"] + cfg
    # 2. single-language code strings
    code = sub1(code, 'self.aa="NIEPONWTOSROCZWPIASOB"',
                'self.aa="%s"' % lang["week3"], "weekday abbreviations")
    code = sub1(code, 'self.aa6=["NIEDZ","PONIE","WTORE","SRODA","CZWAR","PIATE","SOBOT"]',
                'self.aa6=["%s"]' % '","'.join(lang["week6"]), "big-face weekday names")
    code = sub1(code, 'self.aM=\n"STYLUTMARKWIMAJCZELIPSIEWRZPAZLISGRU"',
                'self.aM="%s"' % lang["months3"], "month abbreviations")
    code = sub1(code, 'var nm=["NÓW","SIERP","I KWADRA","GARB","PEŁNIA","GARB","III KWADRA","SIERP"][q]',
                'var nm=["%s"][q]' % '","'.join(lang["moon"]), "moon phase names")
    code = sub_re(code,
                  r'var r=\["Polski","English","Español","Français","Português","Deutsch"\]\.find\(store\.get\("wlang"\)\)var c=\[\[[\s\S]*?\]\]\[r==nil\?0:r\]',
                  'var c=["%s"]' % '","'.join(lang["descs"]),
                  "weather description lists")
    code = sub1(code,
                '["CZYSTE NIEBO","CLEAR NIGHT","NOCHE DESPEJADA","NUIT CLAIRE","NOITE LIMPA","KLARE NACHT"][r==nil?0:r]',
                '"%s"' % lang["night"], "night description")
    # 3. meteoalarm removal for non-Polish variants
    if not lang["meteo"]:
        for old, new in METEO_STRIP:
            code = sub1(code, old, new, "meteo strip: " + old[:40])
        for pat, new in METEO_STRIP_RE:
            code = sub_re(code, pat, new, "meteo strip re: " + pat[:40])
    # the TERYT table is huge and multi-line; strip it (it is gone in non-PL anyway,
    # but keep PL safe by removing it only there) - nothing to do for PL
    return head + "import math" + code


def check_help(text, tag):
    for m in re.finditer(r'help="([^"]*)"', text):
        n = len(m.group(1).encode("utf-8"))
        if n > HELP_LIMIT:
            raise SystemExit("%s: help longer than %d bytes (%d): %s"
                             % (tag, HELP_LIMIT, n, m.group(1)))


def smoke():
    """Run every variant in the GIF harness for a few seconds and check it renders."""
    import subprocess
    sys.path.insert(0, str(Path(__file__).parent))
    from gifs_local import HARNESS, build_berry
    cache = ROOT / "tests" / ".berry-cache"
    berry = build_berry(cache)
    run_dir = cache / "run"
    run_dir.mkdir(exist_ok=True)
    scenes = '''
run_scene("kartka", 8, "SK", {"meteoalarm_enabled": false, "warm": true})
run_scene("duży", 6, "SK2", {"meteoalarm_enabled": false, "warm": true})
print("DONE")
'''
    for tag in ORDER:
        fname = "nimbus-tc002-%s.ax" % ("PL" if tag == "PL" else tag)
        h = HARNESS.replace('print("DONE")', scenes)
        (run_dir / "harness.ax").write_text(h, encoding="utf-8")
        (run_dir / "nimbus-tc002.ax").write_text(
            (ROOT / "dist" / fname).read_text(encoding="utf-8"), encoding="utf-8")
        out = subprocess.run([str(berry), "harness.ax"], cwd=run_dir, check=True,
                             capture_output=True, text=True).stdout
        frames = [l for l in out.splitlines() if l.startswith("F") and len(l) == 1 + 832 * 6]
        assert frames, "%s: no frames" % tag
        assert any("ffffff" in f for f in frames), "%s: no content rendered" % tag
        print("smoke %s OK (%d frames)" % (tag, len(frames)))


def main():
    src = TEMPLATE.read_text(encoding="utf-8")
    for tag in ORDER:
        out = build_one(tag, src)
        check_help(out, tag)
        path = ROOT / "dist" / ("nimbus-tc002-%s.ax" % ("PL" if tag == "PL" else tag))
        path.write_text(out, encoding="utf-8")
        print("%s (%d bytes)" % (path.name, len(out.encode("utf-8"))))
    # sanity checks
    for tag in ORDER:
        text = (ROOT / "dist" / ("nimbus-tc002-%s.ax" % ("PL" if tag == "PL" else tag))).read_text(encoding="utf-8")
        if tag == "PL":
            assert "imgw" in text and "TERYT" in text and "maText" in text, "PL lost meteoalarm"
        else:
            for bad in ("imgw", "TERYT", "meteoalarm", "maText", "maMsg", "materyt", "maref", "mafreq"):
                assert bad not in text, "%s still contains %s" % (tag, bad)
        for bad in ("English", "Español", "Français", "Português", "Deutsch", "wlang"):
            assert bad not in text, "%s still contains %s" % (tag, bad)
    smoke()
    print("OK")


if __name__ == "__main__":
    main()
