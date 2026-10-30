# Nimbus Clock Weather – Polska Wersja (AWTRIX Light / Awtrix NG)

Zmodyfikowana i w pełni spolszczona wersja aplikacji **Nimbus** dla zegarów małych matryc LED sterowanych systemem **AWTRIX Light / Awtrix NG**.

Aplikacja wyświetla zegar (w kilku wariantach tarcz), kalendarz, rozbudowaną pogodę z serwisu **Open-Meteo**, odczyty temperatury oraz wilgotności w pomieszczeniu (z czujników lokalnych lub MQTT), a także oferuje automatyczny tryb nocny i efekty przejść.

> **Grafiki poglądowe:** Zrzuty ekranu przedstawiające działanie aplikacji (tarcze `sheet`, `ring`, `flap`, `big`, tryb nocny oraz poszczególne panele) znajdują się w [oryginalnym repozytorium AkdM](https://github.com/AkdM/awtrix-ng-nimbus-clock-weather). W forku polskim wygląd paneli jest zgodny z poniższym opisem.

---

## Co nowego w tym forku (w stosunku do oryginału)

### 1. Pełne spolszczenie panelu WWW
- Spolszczone wszystkie nazwy opcji, grupy ustawień, podpowiedzi (`help`) oraz listy wyboru (`select`) w panelu konfiguracyjnym AWTRIX.
- Domyślny język opisów pogodowych ustawiony na **Polski**.

### 2. Rozszerzona obsługa pogody (10 stanów z Open-Meteo)
Rozbudowano parser i silnik renderowania ikonek z 7 do **10 dokładnych stanów pogodowych WMO**:

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

Dodano dedykowane polskie opisy oraz dopasowane animacje pikselowe dla mżawki, ulewy i śnieżycy.

### 3. Ulepszony panel jakości powietrza (PM2.5)
- Nowy wygląd panelu: napis **„PM”** umieszczony nad wartością liczbową.
- Napis „PM” oraz wartość liczbowa są **czarne**, co zapewnia czytelność na kolorowym tle.
- Tło panelu zmienia kolor w zależności od poziomu PM2.5 (zielone, żółte, pomarańczowe, czerwone).
- Panel został **zwężony do 15 pikseli**, dzięki czemu od strony godziny zachowany jest **2-pikselowy odstęp** – kolorowe tło nie nachodzi na cyfry zegara.
- Nowa opcja **`Pokaż PM2.5`** (`showpm`) w grupie „Pogoda i Powietrze” pozwala całkowicie wyłączyć ten panel z karuzeli.

### 4. Efekt „Wycieraczki” (czyszczenie matrycy co 5 min)
- Dodano płynny efekt czyszczący – czarny pas o szerokości 8 pikseli przesuwający się z prawej do lewej strony ekranu dokładnie co 5 minut (`minute() % 5 == 0`).
- Efekt trwa 800 ms, odświeża diody LED i redukuje ryzyko utrwalania powidoków (burn-in), nadając zegarowi unikalny styl retro-skanera.
- Możliwość włączenia/wyłączenia w sekcji **Wyświetlacz** w panelu konfiguracyjnym.

### 5. Poprawki stabilności i parsera Berry
- Wyeliminowano błędy parsera Berry (`syntax_error`) przy parsowaniu odpowiedzi JSON z Open-Meteo.
- Usunięto nieobsługiwane konstrukcje (`local`, `string.gmatch`, `table.insert`), zastępując je natywnymi mechanizmami Berry (`string.find`, `re.search`, pętle `while`).
- Zachowano pełną wsteczną kompatybilność z angielskimi kluczami konfiguracji.

### 6. Rezygnacja z alternatywnych źródeł PM2.5
- W trakcie prac testowano integrację z **GIOŚ** oraz **Airly**, jednak ze względu na ograniczenia (brak stacji PM2.5 w pobliżu, limity zapytań) zrezygnowano z nich.
- Ostatecznie **jedynym źródłem danych o jakości powietrza jest Open-Meteo** – nie wymaga klucza API i oferuje wystarczający limit zapytań.

---

## ⚙️ Instrukcja instalacji

1. Pobierz plik `Nimbus-Clock-Weather.ax` z najnowszego wydania lub bezpośrednio z tego repozytorium.
2. Otwórz panel zarządzania przeglądarki Twojego zegara AWTRIX (adres IP zegara w sieci lokalnej).
3. Przejdź do zakładki **Files** / **App Store** lub wejdź przez FTP/Samba do pamięci zegara.
4. Wgraj plik `Nimbus-Clock-Weather.ax` do katalogu aplikacji (`/apps/` lub bezpośrednio przez edytor plików w panelu).
5. Zrestartuj zegar lub przeładuj aplikacje.
6. W ustawieniach aplikacji wprowadź współrzędne geograficzne (Szerokość `Lat` i Długość `Lon`) swojej miejscowości dla celów prognozy pogody.

---

## 🛠️ Przegląd opcji konfiguracji

| Grupa | Opcja | Opis |
|---|---|---|
| **Wyświetlacz** | `Efekt wycieraczki` | Włącza czyszczenie matrycy czarnym pasem co 5 minut |
| **Czas** | `Zegar 24-godzinny`, `Zero wiodące`, `Dwukropek`, `Kolor`, `Tarcza` | Wybór formatu czasu, stylu dwukropka oraz tarczy (kartka, pierścień, klapka, duży) |
| **Kalendarz** | `Nagłówek`, `Tekst`, `Tło`, `Animacja`, `Format daty` | Wygląd i animacja zrywania kartki kalendarza |
| **Pasek tygodnia** | `Pasek tygodnia`, `Tydzień od poniedziałku`, `Kolory dni` | Pasek z 7 kropkami na dole matrycy wskazujący aktualny dzień tygodnia |
| **Karuzela** | `Panele`, `Czas daty`, `Czas paneli`, `Przejście` | Wybór wyświetlanych paneli (`date`, `temp`, `weather`, `room`, `humidity`, `pm25`) i animacji przełączania |
| **Pogoda i Powietrze** | `Pokaż PM2.5`, `Lat`, `Lon`, `Odświeżanie`, `Opisy pogody`, `Własne opisy` | Konfiguracja lokalizacji Open-Meteo, języka opisów oraz włączanie/wyłączanie panelu PM2.5 |
| **Pokój** | `MQTT Topics`, `Kolory` | Odczyt temperatury i wilgotności z własnych tematów MQTT lub wbudowanego czujnika |
| **Tryb nocny** | `Automatyczny tryb nocny`, `Godziny`, `Jasność nocna` | Wyciszenie rotacji paneli i obniżenie jasności w wyznaczonych godzinach |

---

## 🌐 Źródła danych

- **Pogoda i PM2.5:** [Open-Meteo](https://open-meteo.com/) – darmowe API, bez klucza, z limitem 10 000 zapytań dziennie. Dane pogodowe pochodzą z modeli numerycznych (m.in. ECMWF, ICON), a jakość powietrza z modelu CAMS (Copernicus Atmosphere Monitoring Service).
- **Grafiki i oryginalny kod:** [AkdM/awtrix-ng-nimbus-clock-weather](https://github.com/AkdM/awtrix-ng-nimbus-clock-weather) – repozytorium autora oryginalnej aplikacji Nimbus.

---

## 👥 Autorzy & Podziękowania

- **AkdM** – autor oryginalnej aplikacji [Nimbus (v2.0)](https://bluebeards.org/awtrix/) w sklepie AWTRIX Hub.
- **olo81** – modyfikacja, polska lokalizacja, poprawki parsera, wdrożenie efektu wycieraczki (v2.2 PL).
- **Społeczność AWTRIX** – za wsparcie i testy.

---

## 📄 Licencja

Oprogramowanie udostępniane na zasadach open-source, zgodnie z pierwotną licencją projektu Nimbus dla systemu AWTRIX Light / Awtrix NG.
