# Nimbus Clock Weather – Polska Wersja z PM2.5 (AWTRIX Light / Awtrix NG)

[![AWTRIX](https://img.shields.io/badge/AWTRIX-Berry%20App-blue.svg)](https://bluebeards.org/awtrix/)
[![Version](https://img.shields.io/badge/version-2.3.3%20PL-brightgreen.svg)]()
[![License](https://img.shields.io/badge/license-MIT-green.svg)]()

<p align="center">
  <img src="docs/NimbusPL.gif" alt="Nimbus Clock Weather PL Demo" width="450">
</p>

**Nimbus Clock Weather PL** to rozbudowany, w pełni spolszczony fork popularnej aplikacji **Nimbus** przeznaczony dla zegarów z małą matrycą LED (52x16) sterowanych oprogramowaniem **AWTRIX Light** lub **Awtrix NG** (np. Ulanzi TC001 / TC002).

Aplikacja płynnie łączy wyświetlanie zegara, kalendarza, prognozy pogody z Open-Meteo, stężenia pyłów **PM2.5**, odczytów temperatury i wilgotności w pomieszczeniu oraz serii efektów wizualnych (m.in. efekt wycieraczki chroniący matrycę przed powidokami).

---

## 🎨 Tarcze Zegara (Style Wyglądu)

Aplikacja oferuje 4 unikalne warianty tarczy zegara do wyboru w panelu konfiguracyjnym:

| Podgląd | Nazwa w opcjach | Opis |
| :---: | :---: | :--- |
| <img src="docs/sheet.gif" width="160"> | `kartka` | **Klasyczna kartka z kalendarza** z opcją animowanego "zrywania" kartki po przełączeniu widoku oraz o północy. |
| <img src="docs/ring.gif" width="160"> | `pierścień` | **Nowoczesna tarcza cyfrowa** otoczona płynnie obracającym się pierścieniem sekundnika. |
| <img src="docs/flap.gif" width="160"> | `klapka` | **Stylizowany zegar klapkowy** (*split-flap*) z animowanym opadaniem cyfr przy zmianie minuty. |
| <img src="docs/big.gif" width="160"> | `duży` | **Duży zegar na pełną wysokość** matrycy z przewijanym u dołu tekstem daty i opisem pogody. |

---

## 🌟 Główne Funkcje i Modyfikacje (v2.3.3 PL)

### 1. 🍃 Jakość Powietrza PM2.5 (Open-Meteo Air Quality)
- **Bez zewnętrznych czujników** – dane o stężeniu pyłów PM2.5 pobierane są automatycznie z darmowego API Open-Meteo na podstawie podanych współrzędnych geograficznych (`Lat`, `Lon`).
- **Dedykowany układ graficzny:** po lewej stronie wyświetlany jest biały napis **PM**, a po prawej boks z kolorowym tłem i pogrubioną, czarną wartością stężenia.
- **Dynamiczne kolory wg norm jakości powietrza WHO/UE:**

| Stężenie PM2.5 | Kolor tła | Jakość powietrza |
| :--- | :---: | :--- |
| $\le 12\,\mu\text{g/m}^3$ | 🟢 **Zielony** | **Dobra** – czyste powietrze |
| $13 - 35\,\mu\text{g/m}^3$ | 🟡 **Żółty** | **Umiarkowana** – dopuszczalna jakość |
| $36 - 55\,\mu\text{g/m}^3$ | 🟠 **Pomarańczowy** | **Niezdrowa** dla grup wrażliwych |
| $> 55\,\mu\text{g/m}^3$ | 🔴 **Czerwony** | **Zła / Bardzo zła** – wysokie zanieczyszczenie |

### 2. 🌤️ Rozbudowana Pogoda (10 Stanów WMO)
- Pełna integracja z **Open-Meteo Forecast API**.
- Obsługa **10 dokładnych stanów pogodowych** wraz z animowanymi ikonkami pikselowymi:
  1. **Słonecznie** (`CLEAR`)
  2. **Zachmurzenie** (`PARTLY`)
  3. **Chmury** (`CLOUDY`)
  4. **Mgła** (`FOG`)
  5. **Mżawka** (`DRIZZLE`)
  6. **Deszcz** (`RAIN`)
  7. **Ulewa** (`HEAVY RAIN`)
  8. **Śnieg** (`SNOW`)
  9. **Śnieżyca** (`HEAVY SNOW`)
  10. **Burza** (`STORM`)

### 3. 🧹 Efekt "Wycieraczki" (Ochrona Matrycy LED)
- Co dokładnie 5 minut przez ekran przesuwa się płynny, czarny pas czyszczący (800 ms).
- Efekt odświeża diody LED, zapobiega utrwalaniu powidoków (*burn-in*) i dodaje unikalny retro akcent.

### 4. 🇵🇱 Pełne Spolszczenie i Poprawki Parsera
- 100% przetłumaczonych opcji, kategorii, opisów i podpowiedzi w panelu WWW AWTRIX.
- Poprawiony parser Berry (`re.search`) – wyeliminowano błędy `syntax_error` przy pobieraniu danych JSON.

---

## ⚙️ Instrukcja Instalacji

1. Pobierz plik [`Nimbus-Clock-Weather.ax`](./Nimbus-Clock-Weather.ax) z repozytorium.
2. Otwórz panel zarządzania zegarem AWTRIX w przeglądarce (wpisz adres IP zegara w sieci lokalnej).
3. Przejdź do zakładki **Files** / **Apps** (lub połącz się przez FTP/Samba).
4. Wgraj plik `Nimbus-Clock-Weather.ax` do katalogu `/apps/`.
5. Zrestartuj zegar lub przeładuj aplikacje.
6. W ustawieniach aplikacji wprowadź swoje współrzędne geograficzne (`Lat`, `Lon`).

---

## 🎛️ Konfiguracja Karuzeli Paneli

W sekcji **Karuzela** w polu **Panele** możesz ustalić kolejność wyświetlanych widoków (rozdzielając nazwy przecinkami):

```text
date, temp, weather, room, humidity, pm25
```

| Nazwa panela | Opis widoku |
| :--- | :--- |
| `date` | Kartka kalendarza / Data |
| `temp` | Temperatura na zewnątrz (Open-Meteo) |
| `weather` | Ikonka pogody + animowany opis stanu |
| `pm25` | Stężenie pyłu PM2.5 z dynamicznym tłem |
| `room` | Temperatura w pokoju (czujnik lokalny lub MQTT) |
| `humidity` | Wilgotność w pokoju (czujnik lokalny lub MQTT) |

---

## 📋 Tabela Wszystkich Opcji w Panelu WWW

| Grupa | Opcja | Domyślnie | Opis |
| :--- | :--- | :---: | :--- |
| **Wyświetlacz** | `Efekt wycieraczki` | `tak` | Pas czyszczący matrycę przechodzący co 5 minut |
| **Czas** | `Zegar 24-godzinny` | `tak` | Format 24h lub 12h (AM/PM) |
| | `Zero wiodące` | `tak` | Wyświetlanie godziny np. jako `08:00` zamiast `8:00` |
| | `Dwukropek` | `pulsowanie` | Tryby: `stały`, `mrugający`, `pulsowanie` |
| | `Kolor godziny` | `#FFFFFF` | Główny kolor cyfr zegara |
| | `Tarcza zegara` | `kartka` | Wybór stylu: `kartka`, `pierścień`, `klapka`, `duży` |
| **Kalendarz** | `Nagłówek`, `Tekst`, `Tło` | — | Kolorystyka kartki kalendarza |
| | `Animacja kalendarza` | `tak` | Zrywanie kartki przy przełączaniu i o północy |
| | `Format daty` | `dd.mm.yy` | Format daty na dużej tarczy (`dd.mm.yy`, `mm/dd/yy`, `yy-mm-dd`) |
| **Pasek tygodnia** | `Pasek tygodnia` | `tak` | Pasek z 7 kropkami na dole ekranu |
| | `Tydzień od poniedziałku` | `tak` | Rozpoczynanie tygodnia od Poniedziałku zamiast Niedzieli |
| **Karuzela** | `Panele` | `date,temp,weather,pm25` | Lista wyświetlanych paneli w rotacji |
| | `Czas daty`, `Czas paneli` | `10s / 3s` | Czas wyświetlania daty oraz pozostałych paneli |
| | `Przejście` | `przetarcie` | Animacja przejścia (`przetarcie`, `zanikanie`, `przejście`, `dół`, `góra`, `lewo`, `prawo`, `brak`) |
| **Pogoda i Powietrze** | `Lat`, `Lon` | — | Szerokość i długość geograficzna dla Open-Meteo |
| | `Odświeżanie` | `15 min` | Częstotliwość pobierania danych pogodowych z API |
| | `Opisy pogody` | `Polski` | Język opisów dla dużej tarczy |
| **Pokój** | `MQTT Topics` | — | Ścieżki MQTT dla temperatury i wilgotności z Home Assistant |
| **Tryb nocny** | `Automatyczny tryb nocny` | `nie` | Automatyczne przyciemnienie i wstrzymanie rotacji w wybranych godzinach |

---

## 👤 Autorzy & Podziękowania

- **AkdM** – Autor oryginalnej aplikacji [Nimbus (v2.0)](https://bluebeards.org/awtrix/) opublikowanej w AWTRIX Hub.
- **olo81** – Modyfikacja, polska lokalizacja, wdrożenie jakości powietrza PM2.5, efekt wycieraczki oraz poprawki stabilności.

---

## 📜 Licencja

Projekt udostępniany na zasadach open-source, zgodnie z pierwotną licencją projektu Nimbus dla systemu AWTRIX Light.
