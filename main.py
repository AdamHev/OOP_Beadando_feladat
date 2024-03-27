from abc import ABC, abstractmethod
from datetime import date, datetime

class Szoba(ABC):
    """"Szoba absztakt osztály, ahol létrehozzuk az
    Egyagyas és Ketagyas szoba származtatitt osztályokat"""
    def __init__(self, ar, szobaszam):
        self.ar = ar
        self.szobaszam = szobaszam


class EgyagyasSzoba(Szoba):
    def __init__(self, ar, szobaszam, minibar=True):
        super().__init__(ar, szobaszam)
        self.minibar = minibar


class KetagyasSzoba(Szoba):
    def __init__(self, ar, szobaszam, erkely=True):
        super().__init__(ar, szobaszam)
        self.erkely = erkely



class Foglalas:
    """Fogalalás olytály egy foglalas_leirasa függvénnyel,
    amelyik a foglalások listázásánál segít"""
    def __init__(self, szoba, foglalo_neve, datum):
        self.szoba = szoba
        self.foglalo_neve = foglalo_neve
        self.datum = datum

    def foglalas_leirasa(self):
        return f"Foglalás: {self.foglalo_neve}, Szobaszám: {self.szoba.szobaszam}, Dátum: {self.datum}"


class Szalloda:
    """Szalloda osztály, ahol a foglalásokat kezeljük:
     hozzáadás, foglalás, lemondás, foglalások kiírása."""
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []
        self.foglalasok = []

    def szoba_hozzaadasa(self, szoba):
        if isinstance(szoba, Szoba):    # Ellenőrzi, hogy példánya-e egy adott osztálynak és annak valemlyik leszármazottjának
            self.szobak.append(szoba)
        else:
            raise ValueError("Csak Szoba típusú objektumok adhatók hozzá.")

    def szoba_foglalasa(self, szobaszam, foglalo_neve, datum):
        # Először None-t állítunk be a szoba változónak.
        # Ez lesz az alapértelmezett érték, ha nem találunk megfelelő szobát.
        szoba = None

        # Bejárjuk a szálloda összes szobáját tartalmazó listát.
        for aktualis_szoba in self.szobak:
            # Ellenőrizzük, hogy az aktuális szoba szobaszáma megegyezik-e a keresettel.
            if aktualis_szoba.szobaszam == szobaszam:
                # Ha igen, akkor megtaláltuk a megfelelő szobát,
                # és beállítjuk a szoba változót az aktuális szobára.
                szoba = aktualis_szoba
                # Mivel megtaláltuk a szobát, nincs szükség további keresésre,
                # így kilépünk a ciklusból.
                break

        # Ellenőrizzük, hogy találtunk-e megfelelő szobát.
        if szoba is None:
            # Ha nem, hibaüzenetet küldünk.
            raise ValueError("A megadott szobaszám nem található a szállodában.")

        # Ellenőrizzük, hogy a szoba már foglalt-e az adott dátumra.
        for foglalas in self.foglalasok:
            if foglalas.szoba.szobaszam == szobaszam and foglalas.datum == datum:
                # Ha igen, akkor hibaüzenetet küldünk.
                raise ValueError("A szoba már foglalt erre a dátumra.")

        # Ha minden rendben, létrehozunk egy új foglalást, és hozzáadjuk a foglalások listájához.
        self.foglalasok.append(Foglalas(szoba, foglalo_neve, datum))
        return szoba.ar, szoba

    def foglalas_lemondasa(self, szobaszam, foglalo_neve, datum):
        for i, foglalas in enumerate(self.foglalasok):      # Az enumarate miatt az indexe az i-ben tárolódik
            if foglalas.szoba.szobaszam == szobaszam and foglalas.foglalo_neve == foglalo_neve and foglalas.datum == datum:
                del self.foglalasok[i]                      # Kitörli az i indexü foglalást
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
    formats = ['%Y-%m-%d', '%Y %m %d', '%Y/%m/%d']
    for fmt in formats:
        try:
            return date(*map(int, input_str.replace('-', ' ').replace('/', ' ').split()))
        except ValueError:
            continue  # Próbáld ki a következő format-et
    return None  # Ha nem találtál megfelelőt

def felhasznaloi_interfesz():
    # Rendzser feltöltése egy szálodával, három szobával, és öt foglalással
    szalloda = Szalloda('Grand Budapest Hotel')
    szalloda.szoba_hozzaadasa(EgyagyasSzoba(15000, 101))
    szalloda.szoba_hozzaadasa(KetagyasSzoba(20000, 102))
    szalloda.szoba_hozzaadasa(KetagyasSzoba(25000, 103))
    szalloda.szoba_foglalasa(101, "Kincső", datetime.strptime("2024-05-08", "%Y-%m-%d").date())
    szalloda.szoba_foglalasa(102, "Dezső", datetime.strptime("2024-06-08", "%Y-%m-%d").date())
    szalloda.szoba_foglalasa(101, "Virág", datetime.strptime("2024-09-10", "%Y-%m-%d").date())
    szalloda.szoba_foglalasa(103, "Albert", datetime.strptime("2024-06-07", "%Y-%m-%d").date())
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
            if parsed_date:
                try:
                    ar, szoba = szalloda.szoba_foglalasa(szobaszam, nev, parsed_date)
                    extra_info = ""
                    if isinstance(szoba, EgyagyasSzoba) and szoba.minibar:
                        extra_info = " és minibárral rendelkezik."
                    elif isinstance(szoba, KetagyasSzoba) and szoba.erkely:
                        extra_info = " és erkéllyel rendelkezik."
                    print(f"A foglalás sikeres. Az ára: {ar} Ft.{extra_info}")
                except ValueError as e:
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