# Nimbus Clock Weather – Polska Wersja (AWTRIX Light / Awtrix NG)

[![AWTRIX](https://img.shields.io/badge/AWTRIX-Berry%20App-blue.svg)](https://bluebeards.org/awtrix/)
[![Version](https://img.shields.io/badge/version-2.2%20PL-brightgreen.svg)]()

Zmodyfikowana i w pełni spolszczona wersja aplikacji **Nimbus** dla zegarów małych matryc LED sterowanych systemem **AWTRIX Light / Awtrix NG**. 

Aplikacja wyświetla zegar (w kilku wariantach tarcz), kalendarz, rozbudowaną pogodę z serwisu Open-Meteo, odczyty temperatury oraz wilgotności w pomieszczeniu (z czujników lokalnych lub MQTT), a także oferuje automatyczny tryb nocny i efekty przejść.

---

## 🚀 Co nowego w wersji 2.2 PL (Zmiany w forku)

### 1. 🇵🇱 Pełne spolszczenie panelu WWW
- Spolszczone wszystkie nazwy opcji, grupy ustawień, podpowiedzi (`help`) oraz listy wyboru (`select`) w panelu konfiguracyjnym AWTRIX.
- Domyślny język opisów pogodowych ustawiony na **Polski**.

### 2. 🌤️ Rozszerzona obsługa pogody (10 stanów z Open-Meteo)
- Rozbudowano parser i silnik renderowania ikonek z 7 do **10 dokładnych stanów pogodowych** WMO:
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
- Dodano dedykowane polskie opisy oraz dopasowane animacje pikselowe dla mżawki, ulewy i śnieżycy.

### 3. 🧹 Efekt "Wycieraczki" (Czyszczenie matrycy co 5 min)
- Dodano płynny efekt czyszczący – czarny pas o szerokości 8 pikseli przesuwający się z prawej do lewej strony ekranu dokładnie co 5 minut (`minute() % 5 == 0`).
- Efekt trwa 800 ms, odświeża diody LED i redukuje ryzyko utrwalania powidoków (burn-in), nadając zegarowi unikalny styl retro-skanera.
- Mżliwość włączenia/wyłączenia w sekcji **Wyświetlacz** w panelu konfiguracyjnym.

### 4. 🛠️ Poprawki stabilności i parsera Berry
- Wyeliminowano błędy parsera Berry (`syntax_error`) przy parsowaniu odpowiedzi JSON z Open-Meteo poprzez zmianę dekodowania cudzysłowów w wyrażeniach regularnych `re.search`.
- Zachowano pełną wsteczną kompatybilność z angielskimi kluczami konfiguracji.

---

## ⚙️ Instrukcja instalacji

1. Pobierz plik `Nimbus-Clock-Weather.ax` z najnowszego wydania lub bezpośrednio z tego repozytorium.
2. Otwórz panel panel zarządzania przeglądarki Twojego zegara AWTRIX (adres IP zegara w sieci lokalnej).
3. Przejdź do zakładki **Files** / **App Store** lub wejdź przez FTP/Samba do pamięci zegara.
4. Wgraj plik `Nimbus-Clock-Weather.ax` do katalogu aplikacji (`/apps/` lub bezpośrednio przez edytor plików w panelu).
5. Zrestartuj zegar lub przeładuj aplikacje.
6. W ustawieniach aplikacji wprowadź współrzędne geograficzne (Szerokość `Lat` i Długość `Lon`) swojej miejscowości dla celów prognozy pogody.

---

## 🎛️ Przegląd opcji konfiguracji

| Grupa | Opcja | Opis |
| :--- | :--- | :--- |
| **Wyświetlacz** | `Efekt wycieraczki` | Włącza czyszczenie matrycy czarnym pasem co 5 minut |
| **Czas** | `Zegar 24-godzinny`, `Zero wiodące`, `Dwukropek`, `Kolor`, `Tarcza` | Wybór formatu czasu, stylu dwukropka oraz tarczy (kartka, pierścień, klapka, duży) |
| **Kalendarz** | `Nagłówek`, `Tekst`, `Tło`, `Animacja`, `Format daty` | Wygląd i animacja zrywania kartki kalendarza |
| **Pasek tygodnia**| `Pasek tygodnia`, `Tydzień od poniedziałku`, `Kolory dni` | Pasek z 7 kropkami na dole matrycy wskazujący aktualny dzień tygodnia |
| **Karuzela** | `Panele`, `Czas daty`, `Czas paneli`, `Przejście` | Wybór wyświetlanych paneli (`date`, `temp`, `weather`, `room`, `humidity`) i animacji przełączania |
| **Pogoda** | `Lat`, `Lon`, `Odświeżanie`, `Opisy pogody`, `Własne opisy` | Konfiguracja lokalizacji Open-Meteo oraz języka opisów |
| **Pokój** | `MQTT Topics`, `Kolory` | Odczyt temperatury i wilgotności z własnych tematów MQTT lub wbudowanego czujnika |
| **Tryb nocny** | `Automatyczny tryb nocny`, `Godziny`, `Jasność nocna` | Wyciszenie rotacji paneli i obniżenie jasności w wyznaczonych godzinach |

---

## 👤 Autorzy & Podziękowania

- **AkdM** – Autor oryginalnej aplikacji [Nimbus (v2.0)](https://bluebeards.org/awtrix/) w sklepie AWTRIX Hub.
- **olo81** – Modyfikacja, polska lokalizacja, poprawki parsera oraz wdrożenie efektu wycieraczki (v2.2 PL).

---

## 📜 Licencja

Oprogramowanie udostępniane na zasadach open-source, zgodnie z pierwotną licencją projektu Nimbus dla systemu AWTRIX Light / Awtrix NG.
