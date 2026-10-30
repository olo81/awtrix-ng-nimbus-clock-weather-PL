# Nimbus Clock Weather – Polska Wersja (AWTRIX Light / Awtrix NG)

<p align="center">
  <img src="docs/NimbusPL.gif" alt="Nimbus Clock Weather PL Demo" width="400">
</p>

**Nimbus Clock Weather PL** to rozbudowany, w pełni spolszczony fork aplikacji Nimbus przeznaczony dla zegarów z małą matrycą LED (52x16) sterowanych oprogramowaniem **AWTRIX Light** lub **Awtrix NG**.

Aplikacja płynnie łączy wyświetlanie czasu i kalendarza z zaawansowaną prognozą pogoda z Open-Meteo, stężeniem pyłów zawieszonych **PM2.5**, odczytami temperatury/wilgotności w pomieszczeniu oraz serią dynamicznych efektów wizualnych.

---

## 🎨 Tarcze Zegara (Style Wyglądu)

Aplikacja pozwala na wybór jednego z czterech unikalnych wariantów tarczy zegara w ustawieniach:

| Tarcza | Nazwa w opcjach | Opis |
| :---: | :---: | :--- |
| <img src="docs/sheet.gif" alt="Kartka" width="120"> | `kartka` | Klasyczna kartka z kalendarza z możliwością animowanego "zrywania" po pojawieniu się zegara oraz o północy. |
| <img src="docs/ring.gif" alt="Pierścień" width="120"> | `pierścień` | Nowoczesna tarcza cyfrowa otoczona płynnym, obracającym się pierścieniem sekundnika. |
| <img src="docs/flap.gif" alt="Klapka" width="120"> | `klapka` | Stylizowany zegar z animowanym efektem opadających klapek (split-flap) przy zmianie minut. |
| <img src="docs/big.gif" alt="Duży" width="120"> | `duży` | Duże, wyraźne cyfry na pełnej wysokości matrycy z u dołu przewijanym tekstem i datą. |

---

## 🌟 Główne Funkcje i Modyfikacje (v2.3.3 PL)

### 1. 🍃 Jakość Powietrza PM2.5 (Open-Meteo Air Quality)
* **Brak potrzeby posiadania czujnika zewnętrznego** – dane o stężeniu pyłów PM2.5 pobierane są automatycznie z darmowego API Open-Meteo na podstawie współrzędnych geograficznych (`Lat`, `Lon`).
* **Czytelny układ wizualny:**
  * Po lewej stronie: Biały napis **PM**.
  * Po prawej stronie: Boks z kolorowym tłem oraz wycentrowaną, pogrubioną wartością stężenia.
* **Dynamiczne kolorowanie tła wg norm czystości powietrza:**
  * 🟢 **Zielony** ($\le 12\,\mu\text{g/m}^3$) – Powietrze dobre
  * 🟡 **Żółty** ($13 - 35\,\mu\text{g/m}^3$) – Powietrze umiarkowane
  * 🟠 **Pomarańczowy** ($36 - 55\,\mu\text{g/m}^3$) – Powietrze niezdrowe dla grup wrażliwych
  * 🔴 **Czerwony** ($> 55\,\mu\text{g/m}^3$) – Powietrze bardzo złej jakości

### 2. 🌤️ Rozbudowana Prognoza Pogody (10 Stanów WMO)
* Pobieranie danych pogodowych z serwisu **Open-Meteo Forecast API**.
* Pełny zakres 10 dokładnych stanów pogodowych z dedykowanymi pikselowymi animacjami:
  `Słonecznie`, `Zachmurzenie`, `Chmury`, `Mgła`, `Mżawka`, `Deszcz`, `Ulewa`, `Śnieg`, `Śnieżyca`, `Burza`.

### 3. 🧹 Efekt "Wycieraczki" (Ochrona Matrycy LED)
* Co dokładnie 5 minut przez ekran przesuwa się płynny, czarny pas czyszczący (czas trwania: 800 ms).
* Efekt odświeża diody LED, zapobiega powstawaniu powidoków (*burn-in*) i nadaje urządzeniu unikalny styl retro-skanera.

### 4. 🇵🇱 Pełna Lokalizacja i Poprawka Parsowania
* Wszystkie grupy, opcje, podpowiedzi (`help`) oraz listy wyboru w panelu WWW zostały przetłumaczone na język polski.
* Zoptymalizowany parser Berry (`re.search`) wyeliminował błędy składniowe JSON.

---

## ⚙️ Instrukcja Instalacji

1. Pobierz plik [`Nimbus-Clock-Weather.ax`](./Nimbus-Clock-Weather.ax) z repozytorium.
2. Otwórz panel zarządzania zegarem AWTRIX w przeglądarce internetowej (adres IP zegara).
3. Przejdź do zakładki **Files** / **Apps** (lub połącz się przez FTP/Samba).
4. Wgraj plik `Nimbus-Clock-Weather.ax` do katalogu aplikacji (`/apps/`).
5. Zrestartuj zegar lub przeładuj aplikacje.
6. W panelu ustawień aplikacji podaj szerokość (`Lat`) i długość (`Lon`) swojej miejscowości.

---

## 🎛️ Konfiguracja i Opcje Karuzeli

W sekcji **Karuzela** w polu **Panele** zdefiniujesz własną kolejność wyświetlanych informacji (rozdzielając nazwy przecinkami):

```text
date, temp, weather, room, humidity, pm25
```

| Nazwa panela | Opis wyświetlanej informacji |
| :--- | :--- |
| `date` | Kartka kalendarza / Data |
| `temp` | Temperatura na zewnątrz (Open-Meteo) |
| `weather` | Ikonka pogody oraz animowany opis stanu |
| `pm25` | Jakość powietrza PM2.5 z dynamicznym tłem |
| `room` | Temperatura w pomieszczeniu (MQTT / Czujnik lokalny) |
| `humidity` | Wilgotność w pomieszczeniu (MQTT / Czujnik lokalny) |

---

## 📋 Tabela Parametrów w Panelu WWW

| Grupa | Parametr | Opis |
| :--- | :--- | :--- |
| **Wyświetlacz** | `Efekt wycieraczki` | Automatyczne czyszczenie matrycy pasem co 5 minut |
| **Czas** | `Zegar 24-godzinny`, `Zero wiodące`, `Dwukropek`, `Kolor`, `Tarcza` | Wybór formatu czasu, stylu dwukropka oraz wariantu tarczy (`kartka`, `pierścień`, `klapka`, `duży`) |
| **Kalendarz** | `Nagłówek`, `Tekst`, `Tło`, `Animacja`, `Format daty` | Kolorystyka i opcje zrywania kartki kalendarza |
| **Pasek tygodnia** | `Pasek tygodnia`, `Tydzień od poniedziałku`, `Kolory dni` | Kropkowy wskaźnik dnia tygodnia na dole matrycy |
| **Karuzela** | `Panele`, `Czas daty`, `Czas paneli`, `Przejście` | Wybór widocznych paneli, czasów trwania oraz animacji przełączania |
| **Pogoda i Powietrze** | `Lat`, `Lon`, `Odświeżanie`, `Opisy pogody`, `Własne opisy` | Współrzędne geograficzne dla Open-Meteo oraz język opisów |
| **Pokój** | `MQTT Topics`, `Kolory` | Tematy MQTT do pobierania temperatury/wilgotności z Home Assistant |
| **Tryb nocny** | `Automatyczny tryb nocny`, `Godziny`, `Jasność nocna` | Wyciszenie rotacji i zmniejszenie jasności diod w wyznaczonych godzinach |

---

## 👤 Autorzy & Podziękowania

* **AkdM** – Autor oryginalnej aplikacji [Nimbus (v2.0)](https://bluebeards.org/awtrix/) w sklepie AWTRIX Hub.
* **olo81** – Modyfikacja, polska lokalizacja, integracja PM2.5 z Open-Meteo Air Quality, efekt wycieraczki oraz poprawki wydajności.

---

## 📜 Licencja

Projekt udostępniany na zasadach open-source, zgodnie z pierwotną licencją projektu Nimbus dla AWTRIX Light.
