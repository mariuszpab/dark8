import json
import os
import random

OUTPUT_PATH = r"C:\DARK8_MARK01\dataset_intents.jsonl"

INTENTS = {
    # ===== PLIKI I FOLDERY =====
    "WRITE_FILE": [
        "zapisz plik {file}",
        "utwórz nowy plik {file}",
        "stwórz plik {file} w {path}",
        "zapisz dane do pliku {file}",
        "utwórz dokument {file} w katalogu {path}",
    ],
    "READ_FILE": [
        "odczytaj zawartość pliku {file}",
        "pokaż co jest w pliku {file}",
        "wyświetl treść pliku {file}",
        "otwórz plik {file}",
        "pokaż zawartość pliku {file} w {path}",
    ],
    "APPEND_FILE": [
        "dopisz tekst do pliku {file}",
        "dodaj linijkę do pliku {file}",
        "uzupełnij plik {file} o nowy wpis",
        "dopisz dane do pliku {file}",
        "dodaj wpis do pliku {file}",
    ],
    "DELETE_FILE": [
        "usuń plik {file}",
        "skasuj plik {file}",
        "wywal plik {file}",
        "usuń dokument {file}",
        "skasuj dokument {file} z {path}",
    ],
    "MAKE_DIR": [
        "stwórz folder {name}",
        "utwórz katalog {name}",
        "zrób nowy folder {name} w {path}",
        "dodaj katalog o nazwie {name}",
        "utwórz nowy katalog {name} w {path}",
    ],
    "DELETE_DIR": [
        "usuń folder {name}",
        "skasuj katalog {name}",
        "wywal folder {name} z {path}",
        "usuń katalog {name} z {path}",
        "skasuj folder {name}",
    ],
    "LIST_DIR": [
        "pokaż listę plików w {path}",
        "wyświetl zawartość katalogu {path}",
        "co jest w folderze {path}",
        "pokaż pliki w folderze {path}",
        "wyświetl pliki w katalogu {path}",
    ],
    "MOVE_FILE": [
        "przenieś plik {file} do {path}",
        "przesuń plik {file} do folderu {path}",
        "przenieś {file} z bieżącego katalogu do {path}",
        "przenieś dokument {file} do {path}",
        "przesuń plik {file} do katalogu {path}",
    ],
    "COPY_FILE": [
        "skopiuj plik {file} do {path}",
        "zrób kopię pliku {file} w {path}",
        "skopiuj {file} do folderu {path}",
        "utwórz kopię {file} w katalogu {path}",
        "skopiuj dokument {file} do {path}",
    ],
    "RENAME_FILE": [
        "zmień nazwę pliku {file} na {file2}",
        "przemianuj plik {file} na {file2}",
        "zmień nazwę {file} na {file2}",
        "nazwij ponownie plik {file} jako {file2}",
        "zmień nazwę dokumentu {file} na {file2}",
    ],
    "SEARCH_FILE": [
        "wyszukaj plik {file}",
        "znajdź plik {file} w {path}",
        "poszukaj pliku {file}",
        "znajdź dokument {file} w katalogu {path}",
        "wyszukaj {file} na dysku",
    ],
    # ===== APLIKACJE =====
    "RUN_APP": [
        "uruchom {app}",
        "włącz {app}",
        "otwórz {app}",
        "odpal {app}",
        "startuj {app}",
    ],
    "CLOSE_APP": [
        "zamknij {app}",
        "wyłącz {app}",
        "zakończ {app}",
        "zamknij aplikację {app}",
        "zakończ program {app}",
    ],
    "INSTALL_APP": [
        "zainstaluj {app}",
        "pobierz i zainstaluj {app}",
        "zainstaluj program {app}",
        "zainstaluj aplikację {app}",
        "ściągnij i zainstaluj {app}",
    ],
    "UNINSTALL_APP": [
        "odinstaluj {app}",
        "usuń program {app}",
        "wywal aplikację {app}",
        "odinstaluj aplikację {app}",
        "usuń {app} z systemu",
    ],
    "UPDATE_APP": [
        "zaktualizuj {app}",
        "sprawdź aktualizacje dla {app}",
        "zainstaluj update dla {app}",
        "zaktualizuj aplikację {app} do najnowszej wersji",
        "wykonaj update programu {app}",
    ],
    "CHECK_APP": [
        "sprawdź czy {app} jest zainstalowany",
        "czy mam zainstalowany {app}",
        "czy {app} jest dostępny",
        "sprawdź obecność {app} w systemie",
        "czy program {app} jest zainstalowany",
    ],
    "KILL_PROCESS": [
        "zabij proces {proc}",
        "zakończ proces {proc}",
        "wyłącz proces {proc}",
        "zabij {proc}",
        "zakończ działanie procesu {proc}",
    ],
    "LIST_PROCESSES": [
        "pokaż listę procesów",
        "wyświetl uruchomione procesy",
        "jakie procesy teraz działają",
        "pokaż wszystkie procesy",
        "wyświetl procesy systemowe",
    ],
    "PROCESS_INFO": [
        "pokaż szczegóły procesu {proc}",
        "pokaż informacje o procesie {proc}",
        "jakie parametry ma proces {proc}",
        "pokaż status procesu {proc}",
        "wyświetl dane o procesie {proc}",
    ],
    "RUN_AS_ADMIN": [
        "uruchom {app} jako administrator",
        "odpal {app} z uprawnieniami administratora",
        "włącz {app} jako admin",
        "startuj {app} jako administrator",
        "uruchom program {app} z uprawnieniami admina",
    ],
    # ===== SYSTEM =====
    "SHUTDOWN": [
        "wyłącz komputer",
        "zamknij system",
        "wyłącz system",
        "zrób shutdown",
        "wyłącz maszynę",
    ],
    "RESTART": [
        "zrestartuj komputer",
        "uruchom ponownie system",
        "zrób restart",
        "zresetuj komputer",
        "uruchom ponownie maszynę",
    ],
    "LOGOUT": [
        "wyloguj użytkownika",
        "wyloguj mnie",
        "wyloguj z systemu",
        "zakończ sesję użytkownika",
        "wyloguj aktualnego użytkownika",
    ],
    "LOCK_SYSTEM": [
        "zablokuj komputer",
        "zablokuj ekran",
        "zablokuj system",
        "przejdź do ekranu blokady",
        "zablokuj sesję",
    ],
    "SLEEP_MODE": [
        "uśpij komputer",
        "przełącz w tryb uśpienia",
        "uśpij system",
        "przełącz maszynę w sleep",
        "wejdź w tryb uśpienia",
    ],
    "HIBERNATE": [
        "zahibernuj komputer",
        "przełącz w tryb hibernacji",
        "zahibernuj system",
        "wejdź w hibernację",
        "przełącz maszynę w hibernację",
    ],
    "SYSTEM_INFO": [
        "pokaż informacje o systemie",
        "pokaż szczegóły systemu",
        "jaką mam wersję systemu",
        "pokaż parametry systemu",
        "wyświetl informacje o systemie operacyjnym",
    ],
    "OPEN_SETTINGS": [
        "otwórz ustawienia systemu",
        "pokaż ustawienia",
        "wejdź w ustawienia",
        "otwórz panel ustawień",
        "uruchom ustawienia systemowe",
    ],
    "CHANGE_SETTING": [
        "zmień ustawienia systemu",
        "zmień konfigurację {setting}",
        "przełącz opcję {setting}",
        "zmień parametr {setting}",
        "skonfiguruj {setting}",
    ],
    "CLEAR_CACHE": [
        "wyczyść cache systemu",
        "usuń pliki tymczasowe",
        "wyczyść pamięć podręczną",
        "posprzątaj pliki tymczasowe",
        "wyczyść śmieci systemowe",
    ],
    # ===== SIEĆ =====
    "CHECK_CONNECTION": [
        "sprawdź połączenie z internetem",
        "czy mam internet",
        "sprawdź czy jest dostęp do sieci",
        "czy jestem online",
        "sprawdź status połączenia sieciowego",
    ],
    "GET_IP": [
        "pokaż mój adres IP",
        "jaki mam adres IP",
        "pokaż IP",
        "pokaż adres sieciowy",
        "pokaż IP tego komputera",
    ],
    "SET_WIFI": [
        "połącz z siecią WiFi {ssid}",
        "połącz z wifi {ssid}",
        "zaloguj do sieci {ssid}",
        "połącz się z {ssid}",
        "ustaw połączenie z wifi {ssid}",
    ],
    "DISCONNECT_WIFI": [
        "rozłącz wifi",
        "odłącz się od sieci bezprzewodowej",
        "wyłącz połączenie wifi",
        "rozłącz z siecią {ssid}",
        "przerwij połączenie wifi",
    ],
    "PING_HOST": [
        "spinguj {host}",
        "wykonaj ping na {host}",
        "sprawdź ping do {host}",
        "sprawdź opóźnienie do {host}",
        "ping {host}",
    ],
    "DOWNLOAD_FILE": [
        "pobierz plik z {url}",
        "ściągnij plik z {url}",
        "zapisz plik z {url} do {path}",
        "pobierz dane z {url}",
        "ściągnij zawartość z {url}",
    ],
    "UPLOAD_FILE": [
        "wyślij plik {file} na {url}",
        "uploaduj {file} do {url}",
        "prześlij plik {file} na serwer {url}",
        "wyślij {file} na {url}",
        "zrób upload pliku {file} do {url}",
    ],
    "NETWORK_INFO": [
        "pokaż informacje o sieci",
        "pokaż konfigurację sieci",
        "jakie mam ustawienia sieciowe",
        "pokaż szczegóły połączenia sieciowego",
        "wyświetl parametry sieci",
    ],
    # ===== USŁUGI =====
    "START_SERVICE": [
        "uruchom usługę {service}",
        "włącz usługę {service}",
        "startuj usługę {service}",
        "włącz serwis {service}",
        "uruchom serwis {service}",
    ],
    "STOP_SERVICE": [
        "zatrzymaj usługę {service}",
        "wyłącz usługę {service}",
        "stopnij usługę {service}",
        "zatrzymaj serwis {service}",
        "wyłącz serwis {service}",
    ],
    "RESTART_SERVICE": [
        "zrestartuj usługę {service}",
        "uruchom ponownie usługę {service}",
        "zrób restart usługi {service}",
        "restartuj serwis {service}",
        "uruchom ponownie serwis {service}",
    ],
    "CHECK_SERVICE": [
        "sprawdź status usługi {service}",
        "czy usługa {service} działa",
        "pokaż stan usługi {service}",
        "czy serwis {service} jest uruchomiony",
        "sprawdź czy {service} jest aktywna",
    ],
    "LIST_SERVICES": [
        "pokaż listę usług",
        "wyświetl wszystkie usługi",
        "jakie usługi są uruchomione",
        "pokaż usługi systemowe",
        "wyświetl serwisy systemowe",
    ],
    # ===== LOGI =====
    "LOG": [
        "zapisz log systemowy",
        "dodaj wpis do logu",
        "zanotuj zdarzenie w logu",
        "zapisz informację do logu",
        "dodaj log operacji",
    ],
    "READ_LOG": [
        "pokaż log systemowy",
        "wyświetl logi",
        "pokaż ostatnie wpisy w logu",
        "pokaż dziennik zdarzeń",
        "wyświetl log operacji",
    ],
}

NAMES = [
    "test",
    "backup",
    "logi",
    "projekty",
    "dane",
    "temp",
    "config",
    "raporty",
    "system",
    "archiwum",
    "debug",
    "output",
    "sesje",
    "cache",
    "obrazy",
]

FILES = [
    "log.txt",
    "dane.txt",
    "raport.docx",
    "config.ini",
    "output.log",
    "backup.zip",
    "test.txt",
    "dane.csv",
    "debug.log",
    "system.log",
]

FILES2 = [
    "nowy_log.txt",
    "nowe_dane.txt",
    "raport2.docx",
    "config2.ini",
    "output2.log",
    "backup2.zip",
    "test2.txt",
    "dane2.csv",
]

APPS = [
    "Chrome",
    "Notepad",
    "VLC",
    "Spotify",
    "Discord",
    "Steam",
    "Visual Studio Code",
    "PowerShell",
    "Explorer",
    "Teams",
]

PROCS = [
    "chrome.exe",
    "explorer.exe",
    "vlc.exe",
    "spotify.exe",
    "discord.exe",
    "steam.exe",
    "code.exe",
    "powershell.exe",
    "cmd.exe",
    "teams.exe",
]

PATHS = [
    r"C:\DARK8_MARK01",
    r"C:\Users\Public",
    r"C:\Temp",
    r"C:\Windows",
    r"C:\Program Files",
    r"C:\DARK8_MARK01\logs",
    r"C:\DARK8_MARK01\data",
]

HOSTS = [
    "google.com",
    "microsoft.com",
    "github.com",
    "onet.pl",
    "wp.pl",
    "localhost",
    "192.168.0.1",
    "8.8.8.8",
]

URLS = [
    "https://example.com/file.zip",
    "https://example.com/data.json",
    "https://example.com/setup.exe",
    "https://example.com/archive.tar.gz",
    "https://example.com/image.png",
]

SERVICES = [
    "Spooler",
    "W32Time",
    "Dhcp",
    "Dnscache",
    "WinDefend",
    "MpsSvc",
    "BITS",
    "EventLog",
    "LanmanServer",
    "LanmanWorkstation",
]

SETTINGS = [
    "głośność",
    "jasność ekranu",
    "tryb zasilania",
    "tapetę",
    "język systemu",
    "czas systemowy",
    "strefę czasową",
    "rozmiar czcionki",
    "tryb nocny",
    "aktualizacje automatyczne",
]

SSIDS = ["DomWiFi", "BiuroNet", "Hotspot", "Siec5G", "Router123"]


def generate_examples_for_intent(intent, templates, count):
    examples = []
    for _ in range(count):
        template = random.choice(templates)
        text = template.format(
            name=random.choice(NAMES),
            file=random.choice(FILES),
            file2=random.choice(FILES2),
            app=random.choice(APPS),
            path=random.choice(PATHS),
            host=random.choice(HOSTS),
            url=random.choice(URLS),
            service=random.choice(SERVICES),
            setting=random.choice(SETTINGS),
            ssid=random.choice(SSIDS),
            proc=random.choice(PROCS),
        )
        examples.append({"text": text, "label": intent})
    return examples


def main():
    random.seed(42)
    total = 0
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        for intent, templates in INTENTS.items():
            examples = generate_examples_for_intent(intent, templates, 80)
            for ex in examples:
                f.write(json.dumps(ex, ensure_ascii=False) + "\n")
            total += len(examples)

    print(f"Wygenerowano {total} przykładów do pliku: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
