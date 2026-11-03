# NimbusPL 🕒🌦️🚨

**Rozbudowany zegar dla AWTRIX NG / AWTRIX Light na matrycy 52×16 (np. Ulanzi TC002).**

Fork popularnej aplikacji **Nimbus** — godzina, kalendarz z animowaną kartką, **25 stanów pogody Open-Meteo** z animacjami, **PM2.5** z progiem alarmowym, porywy wiatru, faza księżyca, odczyty z pokoju (MQTT / czujnik) oraz — w wersji polskiej — **ostrzeżenia Meteoalarm (IMGW)** z automatycznym wykrywaniem powiatu.

Dostępne wersje językowe: **PL** (z Meteoalarmem), **EN**, **DE**, **ES**, **PT** — każda z menu i opisami we własnym języku.

*A feature-packed clock for AWTRIX NG / AWTRIX Light on a 52×16 matrix (e.g. Ulanzi TC002). A fork of the popular Nimbus app with a tear-off calendar, all 25 Open-Meteo WMO weather states with pixel icons and animations, PM2.5 air quality, wind gusts, moon phase, room readings (MQTT / sensor) and — in the Polish version — Meteoalarm (IMGW) weather warnings for your county. Available in PL, EN, DE, ES and PT, each with its own menu and descriptions.*

---

## ✨ Najważniejsze funkcje / Key features

- 🎨 **Trzy tarcze zegara**: `kartka` (kalendarz z efektem zrywania kartki), `pierścień` (obracający się sekundnik), `duży` (pełna szerokość).
- 🌦️ **Pogoda w pełnej rozdzielczości** — wszystkie 25 kodów WMO Open-Meteo z własnymi ikonkami, animowanymi opadami i opisami w Twoim języku (fioletowy opis pod ikonką, przewijany gdy długi). Dla marznących opadów — animacja **postaci w czerwonej kurtce, która wchodzi, ślizga się, przewraca, wstaje i wychodzi z ekranu** 🧊.
- 🌬️ **Porywy wiatru** — czerwono-biała powiewająca flaga + prędkość (pojawia się dopiero powyżej ustawionego progu).
- 🍃 **PM2.5** — kafelek w kolorze poziomu (zielony → żółty → pomarańczowy → czerwony → fioletowy → granatowy), pokazywany dopiero od ustawionego progu (domyślnie 30 µg/m³).
- 🌙 **Faza księżyca** — ikona z terminatorem na czarnym tle.
- 🚨 **Meteoalarm (IMGW)** *(tylko wersja PL)* — ostrzeżenia pogodowe dla **powiatu wyznaczonego automatycznie ze współrzędnych** (lub ręcznie po TERYT). Komunikat z czasem zagrożenia przejmuje karuzelę co kilka minut, z osobną częstotliwością przed i w trakcie zagrożenia.
- 🎛️ **Karuzela 9 paneli z numerami** — każdy panel ma własny przełącznik, a kolejność ustalasz wpisując numery po przecinku w polu `Kolejność (numery)`.
- 🌙 **Tryb nocny** — czerwony zegar, jasność, automatyczne godziny, MQTT.
- 🧹 **Efekt wycieraczki** — pas czyszczący matrycę co 5 minut.

## 📸 Podgląd

| Karuzela paneli | Meteoalarm (IMGW) | Faza księżyca |
| :---: | :---: | :---: |
| ![Karuzela](https://raw.githubusercontent.com/olo81/awtrix-ng-nimbus-clock-weather-PL/main/docs/demo-carousel.gif) | ![Meteoalarm](https://raw.githubusercontent.com/olo81/awtrix-ng-nimbus-clock-weather-PL/main/docs/meteoalarm.gif) | ![Księżyc](https://raw.githubusercontent.com/olo81/awtrix-ng-nimbus-clock-weather-PL/main/docs/moon.gif) |

Wszystkie stany pogody: [animacje](https://github.com/olo81/awtrix-ng-nimbus-clock-weather-PL/tree/main/docs) (weather-*.gif w repozytorium).

## 🚀 Instalacja

Wybierz wersję językową i wgraj plik do katalogu `/apps/` zegara (panel WWW → Files, lub FTP/Samba), potem zrestartuj aplikacje:

| Język | Plik | Meteoalarm |
| :--- | :--- | :---: |
| 🇵🇱 Polski | [nimbus-tc002-PL.ax](https://raw.githubusercontent.com/olo81/awtrix-ng-nimbus-clock-weather-PL/main/dist/nimbus-tc002-PL.ax) | ✅ |
| 🇬🇧 English | [nimbus-tc002-en.ax](https://raw.githubusercontent.com/olo81/awtrix-ng-nimbus-clock-weather-PL/main/dist/nimbus-tc002-en.ax) | — |
| 🇩🇪 Deutsch | [nimbus-tc002-de.ax](https://raw.githubusercontent.com/olo81/awtrix-ng-nimbus-clock-weather-PL/main/dist/nimbus-tc002-de.ax) | — |
| 🇪🇸 Español | [nimbus-tc002-es.ax](https://raw.githubusercontent.com/olo81/awtrix-ng-nimbus-clock-weather-PL/main/dist/nimbus-tc002-es.ax) | — |
| 🇵🇹 Português | [nimbus-tc002-pt.ax](https://raw.githubusercontent.com/olo81/awtrix-ng-nimbus-clock-weather-PL/main/dist/nimbus-tc002-pt.ax) | — |

W ustawieniach aplikacji podaj szerokość i długość geograficzną (`Lat`, `Lon`) — służą pogodzie, PM2.5 i (w wersji PL) automatycznemu powiatowi meteoalarmu. Aby korzystać z ostrzeżeń, włącz **`9. Meteoalarm`** w zakładce *Karuzela*.

## ⚙️ Najważniejsze ustawienia

- **Karuzela**: przełączniki paneli `1. Pogoda` … `9. Meteoalarm`, pole `Kolejność (numery)` (np. `1,2,3,4,5,6,7,8,9`), czasy paneli, `Próg porywów wiatru`, `Próg PM2.5`.
- **Pogoda i Powietrze**: współrzędne, `TERYT powiatu` (puste = automatycznie), `Włącz Meteoalarm`, częstotliwości komunikatu przed i w trakcie zagrożenia.
- **Pokój**: tematy MQTT temperatury i wilgotności (np. Home Assistant).
- **Tryb nocny**: automatyczne godziny, jasność, wstrzymanie rotacji.

## 👤 Autorzy

- **AkdM** — oryginalny Nimbus dla AWTRIX.
- **olo81** — polska lokalizacja, meteoalarm IMGW, PM2.5, porywy wiatru, księżyc, wersje językowe i pozostałe rozszerzenia.

Projekt open-source (MIT), repozytorium: [github.com/olo81/awtrix-ng-nimbus-clock-weather-PL](https://github.com/olo81/awtrix-ng-nimbus-clock-weather-PL)
