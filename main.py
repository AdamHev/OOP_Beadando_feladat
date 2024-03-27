from abc import ABC, abstractmethod
from datetime import date, datetime

# Absztrakt Szoba osztály
class Szoba(ABC):
    def __init__(self, ar, szobaszam):
        self.ar = ar
        self.szobaszam = szobaszam

    @abstractmethod
    def leiras(self):
        pass

class EgyagyasSzoba(Szoba):
    def __init__(self, ar, szobaszam):
        super().__init__(ar, szobaszam)
        self.minibar = True

    def leiras(self):
        return f"Egyágyas szoba, szobaszám: {self.szobaszam}, ár: {self.ar} Ft, minibár: {'van' if self.minibar else 'nincs'}"

class KetagyasSzoba(Szoba):
    def __init__(self, ar, szobaszam):
        super().__init__(ar, szobaszam)
        self.erkely = True

    def leiras(self):
        return f"Kétágyas szoba, szobaszám: {self.szobaszam}, ár: {self.ar} Ft, erkély: {'van' if self.erkely else 'nincs'}"

# Foglalás osztály
class Foglalas:
    def __init__(self, szoba, foglalo_neve, datum):
        self.szoba = szoba
        self.foglalo_neve = foglalo_neve
        self.datum = datum

    def foglalas_leirasa(self):
        return f"Foglalás: {self.foglalo_neve}, Szobaszám: {self.szoba.szobaszam}, Dátum: {self.datum}"

# Szalloda osztály a szobák és foglalások kezelésére
class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []
        self.foglalasok = []

    def szoba_hozzaadasa(self, szoba):
        if isinstance(szoba, Szoba):
            self.szobak.append(szoba)
        else:
            raise ValueError("Csak Szoba típusú objektumok adhatók hozzá.")

    def szoba_foglalasa(self, szobaszam, foglalo_neve, datum):
        szoba = next((sz for sz in self.szobak if sz.szobaszam == szobaszam), None)
        if szoba is None:
            raise ValueError("A megadott szobaszám nem található a szállodában.")
        if any(foglalas.szoba.szobaszam == szobaszam and foglalas.datum == datum for foglalas in self.foglalasok):
            raise ValueError("A szoba már foglalt erre a dátumra.")
        self.foglalasok.append(Foglalas(szoba, foglalo_neve, datum))
        return szoba.ar

    def foglalas_lemondasa(self, szobaszam, foglalo_neve, datum):
        for i, foglalas in enumerate(self.foglalasok):
            if foglalas.szoba.szobaszam == szobaszam and foglalas.foglalo_neve == foglalo_neve and foglalas.datum == datum:
                del self.foglalasok[i]
                return True
        return False

    def foglalasok_kiirasa(self):
        if not self.foglalasok:
            print("Nincsenek foglalások.")
            return
        print(f"{self.nev} szálloda foglalásai:")
        for foglalas in self.foglalasok:
            print(foglalas.foglalas_leirasa())

def parse_date(input_str):
    formats = ['%Y-%m-%d', '%Y %m %d', '%Y/%m/%d']  # You can add more formats
    for fmt in formats:
        try:
            return date(*map(int, input_str.replace('-', ' ').replace('/', ' ').split()))
        except ValueError:
            continue  # Try the next format
    return None  # If no format matched

def felhasznaloi_interfesz():
    szalloda = Szalloda('Hotel Trasylvania')
    szalloda.szoba_hozzaadasa(EgyagyasSzoba(15000, 101))
    szalloda.szoba_hozzaadasa(KetagyasSzoba(20000, 102))
    szalloda.szoba_hozzaadasa(EgyagyasSzoba(25000, 103))
    szalloda.szoba_foglalasa(101, "Arany János", datetime.strptime("2024-05-08", "%Y-%m-%d").date())
    szalloda.szoba_foglalasa(102, "Kosztolányi Dezső", datetime.strptime("2024-06-08", "%Y-%m-%d").date())
    szalloda.szoba_foglalasa(101, "Franz Kafka", datetime.strptime("2024-09-10", "%Y-%m-%d").date())
    szalloda.szoba_foglalasa(103, "Albert Camus", datetime.strptime("2024-06-07", "%Y-%m-%d").date())
    szalloda.szoba_foglalasa(101, "Adam", datetime.strptime("2024-05-09", "%Y-%m-%d").date())

    while True:
        print("\nVálasszon az alábbi opciók közül:")
        print("1: Szoba foglalása")
        print("2: Foglalás lemondása")
        print("3: Foglalások listázása")
        print("4: Kilépés")
        valasztas = input("Adja meg a választott opciót (1-4): ")

        if valasztas == '1':
            szobaszam = int(input("Adja meg a szobaszámot: "))
            nev = input("Adja meg a foglaló nevét: ")
            raw_date = input("Adja meg a dátumot (pl.: 2024-05-08, 2024 05 08): ")
            parsed_date = parse_date(raw_date)
            print(type(parsed_date), parsed_date)
            if parsed_date:
                try:
                    ar = szalloda.szoba_foglalasa(szobaszam, nev, parsed_date)
                    print(f"A foglalás sikeres. Az ára: {ar} Ft.")
                except ValueError as e:  # Kifejezetten ValueError kivételeket kezel
                    print(f"Hiba: {e}")

            else:
                print("Hibás dátumformátum. Kérem, próbálja újra.")

        elif valasztas == '2':
            szobaszam = int(input("Adja meg a szobaszámot, amelyikből a foglalást le szeretné mondani: "))
            nev = input("Adja meg a foglaló nevét: ")
            raw_date = input("Adja meg a lemondás dátumát (pl.: 2024-05-08, 2024 05 08): ")
            parsed_date = parse_date(raw_date)
            if parsed_date:
                if szalloda.foglalas_lemondasa(szobaszam, nev, parsed_date):
                    print("A foglalás sikeresen lemondva.")
                else:
                    print("Nem sikerült a foglalást lemondani.")
            else:
                print("Hibás dátumformátum. Kérem, próbálja újra.")

        elif valasztas == '3':
            szalloda.foglalasok_kiirasa()

        elif valasztas == '4':
            print("Kilépés...")
            break
        else:
            print("Érvénytelen opció, kérem próbálja újra.")

# Fő program indítása
felhasznaloi_interfesz()