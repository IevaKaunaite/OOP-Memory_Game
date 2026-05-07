Atminties žaidimas (,,Memory game") – OOP Kursinis darbas

Įvadas
Kas yra ši programa?
Ši programa yra grafinis atminties žaidimas (,,Memory Game”), sukurtas naudojant Python programavimo kalbą ir tkinter biblioteką grafiniam žaidimo atvaizdavimui. Žaidimo tikslas – atrasti visas sutampančias kortelių poras. Lentelėje (4×4 matricoje) išdėstomos 16 kortelių, už kurių paslėpti skaičiai. Po vieną kortelę atverdamas žaidėjas pamato skaičių, ir verčia sekančia kortelę – jei skaičiai (kortelių reikšmės) sutampa, kortelės lieka atverstos, jei ne – jos ,,užsiverčia”.
Kaip paleisti programą?
Kompiuteryje turėti įdiegtą python programavimo kalbos kompiliatorių (pvz. VS Code). Paleisti Main.py kodą. Arba, per terminalą:
cd kelias/iki/jūsų/aplanko
py main.py

Kaip naudotis programa?
1.	Paleidus programą, atsidaro 4×4 lentelė su 16 paslėptų kortelių (rodomos kaip *).
2.	Spustelėjus bet kurią kortelę, ji parodo savo reikšmę – kažkokį skaičių (nuo 0 iki 7)
3.	Spustelėkite antrą kortelę – jei reikšmės sutampa, abi kortelės lieka atverstos, jei ne – jos užvertamos atgal.
4.	Žaidimas pasibaigia tada, kada surandamos visos sutampančios (skaičiais) kortelių reikšmės
5.	Žaidimo pabaigoje rodomas pranešimas su atliktų ėjimų skaičiumi.

Analizė
1. Keturi OOP principai
1.1 Abstrakcija (Abstraction)
Programoje naudojama abstrakti bazinė klasė BazineKortele, kuri apibrėžia bendrą kortelės sąsają – metodą gauti_reiksme().  
from abc import ABC, abstractmethod

class BazineKortele(ABC):
    @abstractmethod
    def gauti_reiksme(self):
        pass
        
1.2 Enkapsuliacija (Encapsulation)
Klasėje Kortele kortelės reikšmė saugoma privačiame lauke __reiksme.
class Kortele(BazineKortele):
    def __init__(self, reiksme):
        self.__reiksme = reiksme  # privatus laukas
        self.atversta = False
        self.sutapusi = False
    def gauti_reiksme(self):
        return self.__reiksme   # pasiekiama tik per metodą
    def vaizduoti(self):
        return str(self.__reiksme) if (self.atversta or self.sutapusi) else "*"
        
1.3 Paveldimumas (Inheritance)
Kortele paveldi iš abstrakčios klasės BazineKortele ir įgyvendina reikiamą metodą gauti_reiksme().
class Kortele(BazineKortele):
    def gauti_reiksme(self):
        return self.__reiksme
        
1.4 Polimorfizmas (Polymorphism)
Polimorfizmas leidžia skirtingoms klasėms turėti tą patį metodo pavadinimą, tačiau skirtingą elgesį. gauti_reiksme() metodas yra apibrėžtas abstrakčioje klasėje, o kiekviena paveldinčioji klasė gali jį įgyvendinti skirtingai.
# Abstrakti klasė apibrėžia sąsają:
class BazineKortele(ABC):
    @abstractmethod
    def gauti_reiksme(self):
        pass

class Kortele(BazineKortele):
    def gauti_reiksme(self):
        return self.__reiksme

2. Projektavimo šablonas – Singleton
class RezultatuValdiklis:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.failas = "scores.json"
        return cls._instance
Kodėl Singleton, o ne kiti šablonai? Rezultatų valdikliui Singleton yra tinkamiausias, nes reikia vieno centralizuoto taško rašymui į failą. Factory šablonas būtų per daug sudėtingas šiam atvejui, o Prototype – nereikalingas, nes nekuriame kopijų.

3. Kompozicija ir agregacija
Programoje naudojama kompozicija – Zaidimas klasė kuria ir valdo Kortele objektus bei RezultatuValdiklis objektą. Jie egzistuoja tik kaip Zaidimas dalis.
class Zaidimas:
    def __init__(self, langas):
        self.rezultatai = RezultatuValdiklis()          # kompozicija
        self.korteles = [Kortele(s) for s in skaiciai]  # kompozicija
        self.mygtukai = []

4. Rašymas į failą ir skaitymas iš failo
Programa naudoja JSON formatą rezultatams saugoti. Kiekvieno sėkmingo žaidimo pabaigoje ėjimų skaičius pridedamas prie scores.json failo.
def issaugoti(self, ejimai):
    try:
        with open(self.failas, "r") as f:
            duomenys = json.load(f)   # nuskaitomi esami duomenys
    except FileNotFoundError:
        duomenys = []                 # jei failo nėra – pradedamas naujas sąrašas

    duomenys.append(ejimai)

    with open(self.failas, "w") as f:
        json.dump(duomenys, f)        # įrašomi atnaujinti duomenys
Naudojamas try/except blokas apsaugo nuo klaidos, jei failas dar neegzistuoja.

5. Testavimas
Testuojamos Kortele ir RezultatuValdiklis klasės.
class TestKortele(unittest.TestCase):

    def test_reiksme(self):
        k = Kortele(5)
        self.assertEqual(k.gauti_reiksme(), 5)

    def test_atvertimas(self):
        k = Kortele(3)
        k.atversti()
        self.assertTrue(k.atversta)

    def test_uzvertimas(self):
        k = Kortele(3)
        k.atversti()
        k.uzversti()
        self.assertFalse(k.atversta)

    def test_vaizdavimas_paslepta(self):
        k = Kortele(7)
        self.assertEqual(k.vaizduoti(), "*")

class TestSingleton(unittest.TestCase):

    def test_singleton(self):
        a = RezultatuValdiklis()
        b = RezultatuValdiklis()
        self.assertIs(a, b)
Testai apima: kortelės reikšmės gavimą, atvertimą, užvertimą, vaizdavimą paslėptoje būsenoje bei Singleton šablono teisingumą.

Rezultatai ir išvados
Rezultatai
•	Sėkmingai sukurtas veikiantis grafinis atminties žaidimas su 4×4 kortelių lenta, naudojant Python tkinter biblioteką.
•	Įgyvendinti visi keturi OOP principai: abstrakcija, enkapsuliacija, paveldimumas ir polimorfizmas.
•	Pritaikytas Singleton projektavimo šablonas rezultatų valdymui, užtikrinantis vieną centralizuotą rašymo į failą tašką.
•	Realizuota kompozicija tarp Zaidimas, Kortele ir RezultatuValdiklis klasių.
•	Vidinė programa padengta vienetų testais, kurie sėkmingai patikrina pagrindinį funkcionalumą.

Išvados
Šio kursinio darbo metu sukurtas pilnai veikiantis atminties žaidimas, demonstruojantis visus pagrindinius objektinio programavimo principus. Programa aiškiai parodo, kaip abstrakcija, enkapsuliacija, paveldimumas ir polimorfizmas gali būti taikomi realiame projekte. Singleton šablonas efektyviai išsprendė rezultatų saugojimo problemą. Programos kodas atitinka PEP8 stilistikos reikalavimus, o svarbiausia funkcionalumas yra padengtas automatiniais testais.

Galimi plėtiniai ateityje:
•	Pridėti skirtingus sunkumo lygius.
•	Rodyti geriausių rezultatų sąrašą iš scores.json tiesiai programos lange.
•	Pridėti laikmačio funkciją, matuojančią žaidimo trukmę.
•	Pakeisti skaičius paveikslėliais ar simboliais, padarant žaidimą vizualiai patrauklesnį.


