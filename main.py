# OOP-Memory_Game
import tkinter as tk
from tkinter import messagebox
import random
import json
from abc import ABC, abstractmethod


# 1. Abstrakcija
class BazineKortele(ABC):
    @abstractmethod
    def gauti_reiksme(self):
        pass


# 2. Enkapsuliacija ir polimorfizmas
class Kortele(BazineKortele):
    def __init__(self, reiksme):
        self.__reiksme = reiksme
        self.atversta = False
        self.sutapusi = False

    def atversti(self):
        self.atversta = True

    def uzversti(self):
        self.atversta = False

    def gauti_reiksme(self):
        return self.__reiksme

    def vaizduoti(self):
        return str(self.__reiksme) if (self.atversta or self.sutapusi) else "*"


# 3. Singleton (rezultatų valdymas)
class RezultatuValdiklis:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.failas = "scores.json"
        return cls._instance

    def issaugoti(self, ejimai):
        try:
            with open(self.failas, "r") as f:
                duomenys = json.load(f)
        except FileNotFoundError:
            duomenys = []

        duomenys.append(ejimai)

        with open(self.failas, "w") as f:
            json.dump(duomenys, f)


# 4. Žaidimas
class Zaidimas:
    def __init__(self, langas):
        self.langas = langas
        self.langas.title("Atminties žaidimas")

        self.dydis = 4
        self.ejimai = 0
        self.pirma = None

        self.rezultatai = RezultatuValdiklis()

        skaiciai = list(range(self.dydis * self.dydis // 2)) * 2
        random.shuffle(skaiciai)

        self.korteles = [Kortele(s) for s in skaiciai]
        self.mygtukai = []

        self.sukurti_lenta()

    def sukurti_lenta(self):
        for i, _ in enumerate(self.korteles):
            mygtukas = tk.Button(
                self.langas,
                text="*",
                width=6,
                height=3,
                command=lambda i=i: self.paspausti(i)
            )
            mygtukas.grid(row=i // self.dydis, column=i % self.dydis)
            self.mygtukai.append(mygtukas)

    def paspausti(self, i):
        kortele = self.korteles[i]

        if kortele.atversta or kortele.sutapusi:
            return

        kortele.atversti()
        self.mygtukai[i].config(text=kortele.vaizduoti())

        if self.pirma is None:
            self.pirma = i
        else:
            self.ejimai += 1
            self.langas.after(500, self.tikrinti, self.pirma, i)
            self.pirma = None

    def tikrinti(self, i1, i2):
        if self.korteles[i1].gauti_reiksme() == self.korteles[i2].gauti_reiksme():
            self.korteles[i1].sutapusi = True
            self.korteles[i2].sutapusi = True

            if all(k.sutapusi for k in self.korteles):
                self.rezultatai.issaugoti(self.ejimai)
                messagebox.showinfo("Laimėjai!", f"Ėjimai: {self.ejimai}")

        else:
            self.korteles[i1].uzversti()
            self.korteles[i2].uzversti()

        self.atnaujinti()

    def atnaujinti(self):
        for i, k in enumerate(self.korteles):
            self.mygtukai[i].config(text=k.vaizduoti())


if __name__ == "__main__":
    langas = tk.Tk()
    Zaidimas(langas)
    langas.mainloop()
