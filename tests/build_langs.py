"""Builds the language variants of NimbusPL from the multi-language template.

Reads tests/nimbus-template.ax (the multi-language template that ships all six
weather description lists and the Meteoalarm/TERYT machinery) and writes:

  dist/nimbus-tc002-PL.ax  - Polish UI, only Polish descriptions, Meteoalarm (IMGW)
  dist/nimbus-tc002-en.ax  - English UI, Meteoalarm without TERYT
  dist/nimbus-tc002-de.ax  - German UI, Meteoalarm without TERYT
  dist/nimbus-tc002-es.ax  - Spanish UI, Meteoalarm without TERYT
  dist/nimbus-tc002-pt.ax  - Portuguese UI, Meteoalarm without TERYT

The non-Polish variants keep Meteoalarm but drop the TERYT county localization
(the county table and the materyt option): they show the highest-level warning
from the whole-country IMGW feed.

The template is the source of truth for the shared code; after editing it run
this script to regenerate all five dist files.

Usage: python3 tests/build_langs.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "tests" / "nimbus-template.ax"
VERSION = "2.11.0"
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
        "room": "POKÓJ",
        "night": "CZYSTE NIEBO",
        "descs": ["SŁONECZNIE", "PRZEWAŻNIE BEZCHMURNIE", "PRZELOTNE ZACHMURZENIE", "ZACHMURZENIE",
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
            '# @config face select "Tarcza zegara" options=kartka,pierścień,duży,długośćdnia default=kartka group="Czas"',
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
            '# @config rpan bool "6. Temperatura w pokoju" default=true group="Karuzela" help="Numer 6 w polu kolejności"',
            '# @config hpan bool "7. Wilgotność w pokoju" default=true group="Karuzela" help="Numer 7 w polu kolejności"',
            '# @config moon bool "8. Faza księżyca" default=true group="Karuzela" help="Numer 8 w polu kolejności"',
            '# @config ppan bool "10. Ciśnienie" default=true group="Karuzela" help="Numer 10 w polu kolejności"',
            '# @config dlpan bool "11. Długość dnia" default=true group="Karuzela" help="Numer 11 w polu kolejności"',
            '# @config dldur slider "Czas długości dnia" default=5 min=1 max=60 unit=s group="Karuzela" help="Jak długo wyświetlać panel długości dnia\"',
            '# @config meteoalarm_enabled bool "9. Meteoalarm" default=false group="Karuzela" help="Numer 9 w polu kolejności"',
            '# @config order text "Kolejność (numery)" default="" group="Karuzela" help="Numery paneli po przecinku, np. 1,2,3,4,5,6,7,8,9,10,11. Puste = kolejność domyślna"',
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
            '# @config ttopic text "MQTT: Temperatura zewnętrzna" default="" group="Pogoda i Powietrze" help="Nadpisuje dane z Open-Meteo/Airly. Puste = automatycznie"',
            '# @config pmtopic text "MQTT: PM2.5" default="" group="Pogoda i Powietrze" help="Nadpisuje dane z Open-Meteo/Airly. Puste = automatycznie"',
            '# @config airlykey text "Klucz API Airly" default="" group="Pogoda i Powietrze" help="Opcjonalny. Podany: temperatura i PM2.5 z Airly zamiast Open-Meteo"',
            '# @config airlyref slider "Częstotliwość Airly" default=15 min=5 max=120 unit=min group="Pogoda i Powietrze" help="Jak często pobierać dane Airly. 15 minut jest optymalne dla darmowego konta"',
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
        "desc": "Clock with calendar, weather, PM2.5 air quality, room values and Meteoalarm weather warnings",
        "hub": "",
        "meteo": False,
        "week3": "SUNMONTUEWEDTHUFRISAT",
        "week6": ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"],
        "months3": "JANFEBMARAPRMAYJUNJULAUGSEPOCTNOVDEC",
        "moon": ["NEW", "CRESCENT", "1ST QUARTER", "GIBBOUS", "FULL", "GIBBOUS", "3RD QUARTER", "CRESCENT"],
        "room": "ROOM",
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
            '# @config face select "Clock face" options=sheet,ring,big,daylight default=sheet group="Time"',
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
            '# @config rpan bool "6. Room temperature" default=true group="Carousel" help="Number 6 in the order field"',
            '# @config hpan bool "7. Room humidity" default=true group="Carousel" help="Number 7 in the order field"',
            '# @config moon bool "8. Moon phase" default=true group="Carousel" help="Number 8 in the order field"',
            '# @config ppan bool "10. Pressure" default=true group="Carousel" help="Number 10 in the order field"',
            '# @config dlpan bool "11. Day length" default=true group="Carousel" help="Number 11 in the order field"',
            '# @config dldur slider "Day length duration" default=5 min=1 max=60 unit=s group="Carousel" help="How long the day length panel is shown\"',
            '# @config meteoalarm_enabled bool "9. Meteoalarm" default=false group="Carousel" help="Number 9 in the order field"',
            '# @config order text "Order (numbers)" default="" group="Carousel" help="Panel numbers separated by commas, e.g. 1,2,3,4,5,6,7,8,9,10,11. Empty = default order"',
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
            '# @config ttopic text "MQTT: Outside temperature" default="" group="Weather & Air" help="Overrides Open-Meteo/Airly. Empty = automatic"',
            '# @config pmtopic text "MQTT: PM2.5" default="" group="Weather & Air" help="Overrides Open-Meteo/Airly. Empty = automatic"',
            '# @config airlykey text "Airly API key" default="" group="Weather & Air" help="Optional. When set, temperature and PM2.5 come from Airly instead of Open-Meteo"',
            '# @config airlyref slider "Airly refresh" default=15 min=5 max=120 unit=min group="Weather & Air" help="How often to fetch Airly data. 15 minutes is optimal for a free Airly account"',
            '# @config maref number "Meteoalarm refresh" default=10 min=5 max=120 unit=min group="Weather & Air" help="How often to fetch the IMGW alert"',
            '# @config madur slider "Message duration" default=15 min=5 max=120 unit=s group="Weather & Air" help="How long the Meteoalarm message is shown"',
            '# @config mafreq slider "Frequency during the alert" default=10 min=1 max=240 unit=min group="Weather & Air" help="How often to show the message while the alert is active"',
            '# @config mafreqb slider "Frequency before the alert" default=60 min=1 max=240 unit=min group="Weather & Air" help="How often to show the message before the alert starts"',
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
        "desc": "Uhr mit Kalender, Wetter, PM2.5-Luftqualität, Raumwerten und Meteoalarm-Wetterwarnungen",
        "hub": "",
        "meteo": False,
        "week3": "SONMONDIEMITDONFRISAM",
        "week6": ["SON", "MON", "DIE", "MIT", "DON", "FRE", "SAM"],
        "months3": "JANFEBMRZAPRMAIJUNJULAUGSEPOKTNOVDEZ",
        "moon": ["NEUMOND", "SICHEL", "1. VIERTEL", "ZUNEHMEND", "VOLLMOND", "ABNEHMEND", "3. VIERTEL", "SICHEL"],
        "room": "RAUM",
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
            '# @config face select "Zifferblatt" options=sheet,ring,big,daylight default=sheet group="Zeit"',
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
            '# @config rpan bool "6. Raumtemperatur" default=true group="Karussell" help="Nummer 6 im Reihenfolge-Feld"',
            '# @config hpan bool "7. Raumluftfeuchte" default=true group="Karussell" help="Nummer 7 im Reihenfolge-Feld"',
            '# @config moon bool "8. Mondphase" default=true group="Karussell" help="Nummer 8 im Reihenfolge-Feld"',
            '# @config ppan bool "10. Luftdruck" default=true group="Karussell" help="Nummer 10 im Reihenfolge-Feld"',
            '# @config dlpan bool "11. Tageslänge" default=true group="Karussell" help="Nummer 11 im Reihenfolge-Feld"',
            '# @config dldur slider "Dauer der Tageslänge" default=5 min=1 max=60 unit=s group="Karussell" help="Wie lange das Tageslänge-Panel angezeigt wird\"',
            '# @config meteoalarm_enabled bool "9. Meteoalarm" default=false group="Karussell" help="Nummer 9 im Reihenfolge-Feld"',
            '# @config order text "Reihenfolge (Nummern)" default="" group="Karussell" help="Panelnummern durch Kommas getrennt, z. B. 1,2,3,4,5,6,7,8,9,10,11. Leer = Standardreihenfolge"',
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
            '# @config ttopic text "MQTT: Außentemperatur" default="" group="Wetter & Luft" help="Überschreibt Open-Meteo/Airly. Leer = automatisch"',
            '# @config pmtopic text "MQTT: PM2.5" default="" group="Wetter & Luft" help="Überschreibt Open-Meteo/Airly. Leer = automatisch"',
            '# @config airlykey text "Airly-API-Schlüssel" default="" group="Wetter & Luft" help="Optional. Wenn gesetzt, kommen Temperatur und PM2.5 von Airly statt von Open-Meteo"',
            '# @config airlyref slider "Airly-Aktualisierung" default=15 min=5 max=120 unit=min group="Wetter & Luft" help="Wie oft Airly-Daten abrufen. 15 Minuten sind optimal für ein Gratis-Konto"',
            '# @config maref number "Meteoalarm-Aktualisierung" default=10 min=5 max=120 unit=min group="Wetter & Luft" help="Wie oft der IMGW-Alarm abgerufen wird"',
            '# @config madur slider "Dauer der Meldung" default=15 min=5 max=120 unit=s group="Wetter & Luft" help="Wie lange die Meteoalarm-Meldung angezeigt wird"',
            '# @config mafreq slider "Häufigkeit während des Alarms" default=10 min=1 max=240 unit=min group="Wetter & Luft" help="Wie oft die Meldung bei aktivem Alarm angezeigt wird"',
            '# @config mafreqb slider "Häufigkeit vor dem Alarm" default=60 min=1 max=240 unit=min group="Wetter & Luft" help="Wie oft die Meldung vor Alarmbeginn angezeigt wird"',
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
        "desc": "Reloj con calendario, tiempo, calidad del aire PM2.5, valores de la habitación y avisos Meteoalarm",
        "hub": "",
        "meteo": False,
        "week3": "DOMLUNMARMIEJUEVIESAB",
        "week6": ["DOM", "LUN", "MAR", "MIE", "JUE", "VIE", "SAB"],
        "months3": "ENEFEBMARABRMAYJUNJULAGOSEPOCTNOVDIC",
        "moon": ["NUEVA", "CRECIENTE", "1ER CUARTO", "GIBOSA", "LLENA", "GIBOSA", "3ER CUARTO", "CRECIENTE"],
        "room": "HABITACIÓN",
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
            '# @config face select "Esfera del reloj" options=sheet,ring,big,daylight default=sheet group="Hora"',
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
            '# @config rpan bool "6. Temperatura de la habitación" default=true group="Carrusel" help="Número 6 en el campo de orden"',
            '# @config hpan bool "7. Humedad de la habitación" default=true group="Carrusel" help="Número 7 en el campo de orden"',
            '# @config moon bool "8. Fase lunar" default=true group="Carrusel" help="Número 8 en el campo de orden"',
            '# @config ppan bool "10. Presión" default=true group="Carrusel" help="Número 10 en el campo de orden"',
            '# @config dlpan bool "11. Duración del día" default=true group="Carrusel" help="Número 11 en el campo de orden"',
            '# @config dldur slider "Duración del panel día" default=5 min=1 max=60 unit=s group="Carrusel" help="Cuánto tiempo se muestra el panel de duración del día\"',
            '# @config meteoalarm_enabled bool "9. Meteoalarm" default=false group="Carrusel" help="Número 9 en el campo de orden"',
            '# @config order text "Orden (números)" default="" group="Carrusel" help="Números de paneles por comas, p. ej. 1,2,3,4,5,6,7,8,9,10,11. Vacío = orden predeterminado"',
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
            '# @config ttopic text "MQTT: Temperatura exterior" default="" group="Tiempo y Aire" help="Sustituye a Open-Meteo/Airly. Vacío = automático"',
            '# @config pmtopic text "MQTT: PM2.5" default="" group="Tiempo y Aire" help="Sustituye a Open-Meteo/Airly. Vacío = automático"',
            '# @config airlykey text "Clave API de Airly" default="" group="Tiempo y Aire" help="Opcional. Si se indica, temperatura y PM2.5 vienen de Airly en vez de Open-Meteo"',
            '# @config airlyref slider "Actualización de Airly" default=15 min=5 max=120 unit=min group="Tiempo y Aire" help="Cada cuántos minutos obtener datos de Airly. 15 min es lo óptimo para una cuenta gratuita"',
            '# @config maref number "Actualización de Meteoalarm" default=10 min=5 max=120 unit=min group="Tiempo y Aire" help="Cada cuántos minutos obtener la alerta IMGW"',
            '# @config madur slider "Duración del mensaje" default=15 min=5 max=120 unit=s group="Tiempo y Aire" help="Cuánto tiempo se muestra el mensaje de Meteoalarm"',
            '# @config mafreq slider "Frecuencia durante la alerta" default=10 min=1 max=240 unit=min group="Tiempo y Aire" help="Cada cuántos minutos mostrar el mensaje durante la alerta"',
            '# @config mafreqb slider "Frecuencia antes de la alerta" default=60 min=1 max=240 unit=min group="Tiempo y Aire" help="Cada cuántos minutos mostrar el mensaje antes del inicio"',
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
        "desc": "Relógio com calendário, tempo, qualidade do ar PM2.5, valores do quarto e avisos Meteoalarm",
        "hub": "",
        "meteo": False,
        "week3": "DOMSEGTERQUAQUISEXSAB",
        "week6": ["DOM", "SEG", "TER", "QUA", "QUI", "SEX", "SAB"],
        "months3": "JANFEVMARABRMAIJUNJULAGOSETOUTNOVDEZ",
        "moon": ["NOVA", "CRESCENTE", "QUARTO CRES", "GIBOSA", "CHEIA", "GIBOSA", "QUARTO MIN", "CRESCENTE"],
        "room": "QUARTO",
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
            '# @config face select "Mostrador do relógio" options=sheet,ring,big,daylight default=sheet group="Hora"',
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
            '# @config rpan bool "6. Temperatura do quarto" default=true group="Carrossel" help="Número 6 no campo de ordem"',
            '# @config hpan bool "7. Humidade do quarto" default=true group="Carrossel" help="Número 7 no campo de ordem"',
            '# @config moon bool "8. Fase da lua" default=true group="Carrossel" help="Número 8 no campo de ordem"',
            '# @config ppan bool "10. Pressão" default=true group="Carrossel" help="Número 10 no campo de ordem"',
            '# @config dlpan bool "11. Duração do dia" default=true group="Carrossel" help="Número 11 no campo de ordem"',
            '# @config dldur slider "Duração do painel do dia" default=5 min=1 max=60 unit=s group="Carrossel" help="Por quanto tempo o painel de duração do dia é mostrado\"',
            '# @config meteoalarm_enabled bool "9. Meteoalarm" default=false group="Carrossel" help="Número 9 no campo de ordem"',
            '# @config order text "Ordem (números)" default="" group="Carrossel" help="Números dos painéis por vírgulas, ex.: 1,2,3,4,5,6,7,8,9,10,11. Vazio = ordem predefinida"',
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
            '# @config ttopic text "MQTT: Temperatura exterior" default="" group="Tempo e Ar" help="Substitui o Open-Meteo/Airly. Vazio = automático"',
            '# @config pmtopic text "MQTT: PM2.5" default="" group="Tempo e Ar" help="Substitui o Open-Meteo/Airly. Vazio = automático"',
            '# @config airlykey text "Chave API da Airly" default="" group="Tempo e Ar" help="Opcional. Se indicada, temperatura e PM2.5 vêm da Airly em vez do Open-Meteo"',
            '# @config airlyref slider "Atualização da Airly" default=15 min=5 max=120 unit=min group="Tempo e Ar" help="Com que frequência obter dados da Airly. 15 min é o ideal para uma conta gratuita"',
            '# @config maref number "Atualização do Meteoalarm" default=10 min=5 max=120 unit=min group="Tempo e Ar" help="Com que frequência obter o alerta IMGW"',
            '# @config madur slider "Duração da mensagem" default=15 min=5 max=120 unit=s group="Tempo e Ar" help="Quanto tempo a mensagem do Meteoalarm é mostrada"',
            '# @config mafreq slider "Frequência durante o alerta" default=10 min=1 max=240 unit=min group="Tempo e Ar" help="Com que frequência mostrar a mensagem durante o alerta"',
            '# @config mafreqb slider "Frequência antes do alerta" default=60 min=1 max=240 unit=min group="Tempo e Ar" help="Com que frequência mostrar a mensagem antes do início"',
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
# meteoalarm without TERYT (non-Polish variants)
# ---------------------------------------------------------------------------
# The feature stays, but the county-localization (the TERYT table and the
# materyt option) is dropped: the app then shows the highest-level warning
# from the whole-country IMGW feed.

METEO_NO_TERYT = [
    ("var mt=store.get(\"materyt\")var mts=re.matchall(\"[0-9]+\",mt)self.maTeryt=size(mts)>0&&size(mts[0])==4?mts[0]:\"\" ", "self.maTeryt=\"\" "),
    ("var la=store.get(\"lat\")var lo=store.get(\"lon\")if self.maTeryt==\"\"&&(la<49||la>55||lo<14||lo>24.5)self.ma_enabled=false end ", ""),
    ("self.ma1=self.maTeryt!=\"\"?\"https://danepubliczne.imgw.pl/api/data/warningsmeteo/teryt/\"+self.maTeryt:\"https://danepubliczne.imgw.pl/api/data/warningsmeteo\"",
     "self.ma1=\"https://danepubliczne.imgw.pl/api/data/warningsmeteo\""),
]

METEO_NO_TERYT_RE = [
    # the TERYT county table
    (r"if self\.ma_enabled&&self\.maTeryt==\"\"[\s\S]*?self\.mc=nil end ", ""),
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
    # the room label on the room/humidity panels (sheet + big face)
    n_room = code.count('"POKÓJ"')
    assert n_room == 2, "room label: found %d" % n_room
    code = code.replace('"POKÓJ"', '"%s"' % lang["room"])
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
    # 3. meteoalarm without the TERYT localization for non-Polish variants
    if not lang["meteo"]:
        for old, new in METEO_NO_TERYT:
            code = sub1(code, old, new, "no-teryt strip: " + old[:40])
        for pat, new in METEO_NO_TERYT_RE:
            code = sub_re(code, pat, new, "no-teryt strip re: " + pat[:40])
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
run_scene("kartka", 8, "SK", {"warm": true})
run_scene("duży", 6, "SK2", {"warm": true})
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
            assert "imgw" in text and "materyt" in text and "maText" in text and "020123401540" in text, \
                "PL lost meteoalarm"
        else:
            for bad in ("materyt", "TERYT", "020123401540"):
                assert bad not in text, "%s still contains %s" % (tag, bad)
            for good in ("imgw", "maText", "METEOALARM", "meteoalarm_enabled", "mafreq"):
                assert good in text, "%s lost meteoalarm (%s)" % (tag, good)
        for bad in ("English", "Español", "Français", "Português", "Deutsch", "wlang"):
            assert bad not in text, "%s still contains %s" % (tag, bad)
        for good in ("airly", "pressure_msl", "hPa", "ppan"):
            assert good in text, "%s lost the %s feature" % (tag, good)
    smoke()
    print("OK")


if __name__ == "__main__":
    main()
