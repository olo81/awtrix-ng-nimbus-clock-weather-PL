# NimbusPL 🕒🌦️🚨

**Rozbudowany zegar dla AWTRIX NG / AWTRIX Light na matrycy 52×16 (np. Ulanzi TC002).**

Fork popularnej aplikacji **Nimbus** — godzina, kalendarz z animowaną kartką, **25 stanów pogody Open-Meteo** z animacjami, **PM2.5** z progiem alarmowym, **ciśnienie atmosferyczne**, porywy wiatru, faza księżyca, odczyty z pokoju (MQTT / czujnik), opcjonalne dane z **Airly** lub **MQTT** oraz **ostrzeżenia Meteoalarm (IMGW)** (w wersji PL z automatycznym wykrywaniem powiatu).

Dostępne wersje językowe: **PL**, **EN**, **DE**, **ES**, **PT** — każda z menu i opisami we własnym języku; wszystkie mają Meteoalarm (wersje obcojęzyczne bez lokalizacji TERYT — pokazują najwyższy aktywny alert z całej Polski).

*A feature-packed clock for AWTRIX NG / AWTRIX Light on a 52×16 matrix (e.g. Ulanzi TC002). A fork of the popular Nimbus app with a tear-off calendar, all 25 Open-Meteo WMO weather states with pixel icons and animations, PM2.5 air quality, atmospheric pressure, wind gusts, moon phase, room readings (MQTT / sensor), optional Airly or MQTT data sources and Meteoalarm (IMGW) weather warnings (county-level in the Polish version). Available in PL, EN, DE, ES and PT, each with its own menu and descriptions.*

---

## ✨ Najważniejsze funkcje / Key features

- 🎨 **Trzy tarcze zegara**: `kartka` (kalendarz z efektem zrywania kartki), `pierścień` (obracający się sekundnik), `duży` (pełna szerokość).
- 🌦️ **Pogoda w pełnej rozdzielczości** — wszystkie 25 kodów WMO Open-Meteo z własnymi ikonkami, animowanymi opadami i opisami w Twoim języku (fioletowy opis pod ikonką, przewijany gdy długi). Dla marznących opadów — animacja **postaci w czerwonej kurtce, która wchodzi, ślizga się, przewraca, wstaje i wychodzi z ekranu** 🧊.
- 🌬️ **Porywy wiatru** — czerwono-biała powiewająca flaga + prędkość (pojawia się dopiero powyżej ustawionego progu).
- 🍃 **PM2.5** — kafelek w kolorze poziomu (zielony → żółty → pomarańczowy → czerwony → fioletowy → granatowy), pokazywany dopiero od ustawionego progu (domyślnie 30 µg/m³). Dane domyślnie z Open-Meteo, opcjonalnie z **Airly** lub **MQTT**.
- ⛅ **Ciśnienie z biometem** — wartość i `hPa` w kolorze wpływu na samopoczucie: 🟢 zielony (korzystny), 🟡 żółty (umiarkowany), 🔴 czerwony (bardzo niekorzystny) — na podstawie wartości i jej zmiany z 24 h.
- 📡 **Airly / MQTT** — temperatura i PM2.5 mogą nadpisywać dane Open-Meteo (priorytet: **MQTT > Airly > Open-Meteo**); częstotliwość Airly ustawialna (domyślnie 15 min — optymalne dla darmowego konta).
- 🌙 **Faza księżyca** — ikona z terminatorem na czarnym tle.
- 🌅 **Długość dnia** — nowa tarcza z dużą godziną, fioletową długością dnia (np. `6:25 h`) i szarym 1-pikselowym paskiem 24 h (od północy do północy) z żółtym odcinkiem wschód–zachód słońca; jako panel karuzeli na pozostałych tarczach (fioletowa wartość na dole ekranu, przełącznik + suwak czasu).
- 🚨 **Meteoalarm (IMGW)** — ostrzeżenia pogodowe z czasem zagrożenia, przejmujące karuzelę co kilka minut (osobna częstotliwość przed i w trakcie zagrożenia). Wersja **PL**: powiat wyznaczany automatycznie ze współrzędnych (lub ręcznie po TERYT). Wersje **EN/DE/ES/PT**: bez TERYT — najwyższy aktywny alert z całej Polski.
- 🎛️ **Karuzela 11 paneli z numerami** — każdy panel ma własny przełącznik, a kolejność ustalasz wpisując numery po przecinku w polu `Kolejność (numery)`.
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
| 🇵🇱 Polski | [nimbus-tc002-PL.ax](https://raw.githubusercontent.com/olo81/awtrix-ng-nimbus-clock-weather-PL/main/dist/nimbus-tc002-PL.ax) | ✅ powiat |
| 🇬🇧 English | [nimbus-tc002-en.ax](https://raw.githubusercontent.com/olo81/awtrix-ng-nimbus-clock-weather-PL/main/dist/nimbus-tc002-en.ax) | ✅ kraj |
| 🇩🇪 Deutsch | [nimbus-tc002-de.ax](https://raw.githubusercontent.com/olo81/awtrix-ng-nimbus-clock-weather-PL/main/dist/nimbus-tc002-de.ax) | ✅ kraj |
| 🇪🇸 Español | [nimbus-tc002-es.ax](https://raw.githubusercontent.com/olo81/awtrix-ng-nimbus-clock-weather-PL/main/dist/nimbus-tc002-es.ax) | ✅ kraj |
| 🇵🇹 Português | [nimbus-tc002-pt.ax](https://raw.githubusercontent.com/olo81/awtrix-ng-nimbus-clock-weather-PL/main/dist/nimbus-tc002-pt.ax) | ✅ kraj |

W ustawieniach aplikacji podaj szerokość i długość geograficzną (`Lat`, `Lon`) — służą pogodzie, PM2.5, ciśnieniu, Airly i (w wersji PL) automatycznemu powiatowi meteoalarmu. Aby korzystać z ostrzeżeń, włącz **`9. Meteoalarm`** w zakładce *Karuzela*. Chcesz danych z Airly? Wpisz `Klucz API Airly` (api.airly.eu) w grupie *Pogoda i Powietrze*.

## ⚙️ Najważniejsze ustawienia

- **Karuzela**: przełączniki paneli `1. Pogoda` … `11. Długość dnia`, pole `Kolejność (numery)` (np. `1,2,3,4,5,6,7,8,9,10,11`), czasy paneli (w tym `Czas długości dnia`), `Próg porywów wiatru`, `Próg PM2.5`.
- **Pogoda i Powietrze**: współrzędne, `TERYT powiatu` (tylko PL; puste = automatycznie), `Włącz Meteoalarm`, częstotliwości komunikatu przed i w trakcie zagrożenia, `Klucz API Airly`, `Częstotliwość Airly`, `MQTT: Temperatura zewnętrzna`, `MQTT: PM2.5`.
- **Pokój**: tematy MQTT temperatury i wilgotności (np. Home Assistant).
- **Tryb nocny**: automatyczne godziny, jasność, wstrzymanie rotacji.

## 👤 Autorzy

- **AkdM** — oryginalny Nimbus dla AWTRIX.
- **olo81** — polska lokalizacja, meteoalarm IMGW, PM2.5, porywy wiatru, księżyc, ciśnienie z biometem, długość dnia, Airly/MQTT, wersje językowe i pozostałe rozszerzenia.

Projekt open-source (MIT), repozytorium: [github.com/olo81/awtrix-ng-nimbus-clock-weather-PL](https://github.com/olo81/awtrix-ng-nimbus-clock-weather-PL)
