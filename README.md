<p align="center">
  <img src="docs/icons/NimbusPL.gif" alt="Nimbus Clock Weather PL Demo" width="400"/>
</p>

<h1 align="center">Nimbus Clock Weather PL</h1>
<h3 align="center">Aplikacja zegara, pogody i jakości powietrza dla AWTRIX Light / Awtrix NG</h3>

<p align="center">
  <a href="https://bluebeards.org/awtrix/"><img src="https://img.shields.io/badge/AWTRIX-Berry%20App-blue.svg" alt="AWTRIX"></a>
  <img src="https://img.shields.io/badge/wersja-2.3.3%20PL-brightgreen.svg" alt="Version"> Polish Language Support">
</p>

---

**Nimbus Clock Weather PL** to rozbudowany, w pełni spolszczony fork aplikacji Nimbus przeznaczony dla zegarów z małą matrycą LED (52x16) sterowanych oprogramowaniem **AWTRIX Light** lub **Awtrix NG**.

Aplikacja płynnie łączy wyświetlanie czasu i kalendarza z zaawansowaną prognozą pogody, stężeniem pyłów zawieszonych **PM2.5**, temperaturą i wilgotnością w pomieszczeniu oraz serią automatycznych efektów wizualnych.

---

## 🌟 Główne Funkcje i Modyfikacje (v2.3.3 PL)

### 1. 🍃 Jakość Powietrza PM2.5 (Open-Meteo Air Quality)
- **Brak potrzeby posiadania czujnika zewnętrznego** – dane o stężeniu pyłów PM2.5 pobierane są automatycznie na podstawie współrzędnych geograficznych (`Lat`, `Lon`).
- **Dedykowany układ wizualny:**
  - Po lewej stronie: Czytelny, biały napis **PM**.
  - Po prawej stronie: Boks z kolorowym tłem oraz wycentrowaną, pogrubioną wartością stężenia.
- **Dynamiczne kolorowanie tła wg norm czystości powietrza:**
  - 🟢 **Zielony** ($\le 12\,\mu\text{g/m}^3$) – Powietrze dobre
  - 🟡 **Żółty** ($13 - 35\,\mu\text{g/m}^3$) – Powietrze umiarkowane
  - 🟠 **Pomarańczowy** ($36 - 55\,\mu\text{g/m}^3$) – Powietrze niezdrowe dla grup wrażliwych
  - 🔴 **Czerwony** ($> 55\,\mu\text{g/m}^3$) – Powietrze bardzo złej jakości

### 2. 🌤️ Rozbudowana Prognoza Pogody (10 Stanów WMO)
- Pobieranie danych pogodowych z serwisu **Open-Meteo Forecast API**.
- Pełny zakres 10 dokładnych stanów pogodowych i dedykowanych animowanych ikonek:
  `Słonecznie`, `Zachmurzenie`, `Chmury`, `Mgła`, `Mżawka`, `Deszcz`, `Ulewa`, `Śnieg`, `Śnieżyca`, `Burza`.

### 3. 🧹 Efekt "Wycieraczki" (Ochrona Matrycy LED)
- Co dokładnie 5 minut przez matrycę od prawej do lewej strony przesuwa się czarny pas czyszczący (czas trwania: 800 ms).
- Efekt niweluje ryzyko utrwalania powidoków (*burn-in*) na diodach LED oraz nadaje zegarowi dynamiczny styl retro.
- Opcję można łatwo włączyć lub wyłączyć w panelu konfiguracyjnym.

### 4. 🇵🇱 Pełna Lokalizacja i Poprawka Parsowania
- Spolszczone nazwy opcji, podpowiedzi (`help`), opisy paneli oraz listy wyboru (`select`) w panelu przeglądarkowym AWTRIX.
- Zoptymalizowany parser wyrażeń regularnych Berry (`re.search`) odporny na błędy składniowe JSON.

---

## ⚙️ Instrukcja Instalacji

1. Pobierz plik [`Nimbus-Clock-Weather.ax`](./Nimbus-Clock-Weather.ax) z repozytorium.
2. Otwórz panel zarządzania zegarem AWTRIX w przeglądarce internetowej (podając adres IP zegara w sieci lokalnej).
3. Przejdź do zakładki **Files** / **Apps** (lub połącz się przez FTP/Samba).
4. Wgraj plik `Nimbus-Clock-Weather.ax` do katalogu aplikacji (`/apps/`).
5. Zrestartuj zegar lub przeładuj aplikacje.
6. W panelu ustawień aplikacji podaj szerokość (`Lat`) i długość (`Lon`) swojej miejscowości.

---

## 🎛️ Konfiguracja i Opcje Karuzeli

W sekcji **Karuzela** w polu **Panele** możesz zdefiniować własną kolejność wyświetlanych informacji (rozdzielając nazwy przecinkami):

```text
date, temp, weather, room, humidity, pm25
```

| Nazwa panela | Opis wyświetlanej informacji |
| :--- | :--- |
| `date` | Kartka kalendarza / Data |
| `temp` | Temperatura na zewnątrz (Open-Meteo) |
| `weather` | Ikonka pogody oraz animowany opis stanu |
| `pm25` | Jakość powietrza PM2.5 w kolorowym boksie |
| `room` | Temperatura w pomieszczeniu (MQTT / Czujnik lokalny) |
| `humidity` | Wilgotność w pomieszczeniu (MQTT / Czujnik lokalny) |

---

## 📋 Tabela Parametrów w Panelu WWW

| Grupa | Parametr | Opis |
| :--- | :--- | :--- |
| **Wyświetlacz** | `Efekt wycieraczki` | Włącza automatyczne czyszczenie matrycy pasem co 5 minut |
| **Czas** | `Zegar 24-godzinny`, `Zero wiodące`, `Dwukropek`, `Kolor`, `Tarcza` | Wybór formatu czasu, stylu dwukropka i stylu tarczy (`kartka`, `pierścień`, `klapka`, `duży`) |
| **Kalendarz** | `Nagłówek`, `Tekst`, `Tło`, `Animacja`, `Format daty` | Kolorystyka i opcje zrywania kartki kalendarza |
| **Pasek tygodnia** | `Pasek tygodnia`, `Tydzień od poniedziałku`, `Kolory dni` | Kropkowy wskaźnik dnia tygodnia na dole matrycy |
| **Karuzela** | `Panele`, `Czas daty`, `Czas paneli`, `Przejście` | Wybór widocznych paneli, czasów trwania oraz efektu przejścia |
| **Pogoda i Powietrze** | `Lat`, `Lon`, `Odświeżanie`, `Opisy pogody`, `Własne opisy` | Lokalizacja geograficzna dla Open-Meteo oraz języki opisów |
| **Pokój** | `MQTT Topics`, `Kolory` | Tematy MQTT do pobierania temperatury/wilgotności z Home Assistant |
| **Tryb nocny** | `Automatyczny tryb nocny`, `Godziny`, `Jasność nocna` | Wyciszenie rotacji i zmniejszenie jasności diod w wybranych godzinach |

---

## 👤 Autorzy & Podziękowania

- **AkdM** – Autor oryginalnej aplikacji [Nimbus (v2.0)](https://bluebeards.org/awtrix/) w sklepie AWTRIX Hub.
- **olo81** – Modyfikacja, polska lokalizacja, integracja PM2.5 z Open-Meteo Air Quality, efekt wycieraczki oraz poprawki wydajności.

---

## 📜 Licencja

Projekt udostępniany na zasadach open-source, zgodnie z pierwotną licencją projektu Nimbus dla AWTRIX Light.
