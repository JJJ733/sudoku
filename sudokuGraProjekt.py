import tkinter as tk
from tkinter import messagebox
import random
class GraSudoku:
    def __init__(self, rozmiar, procentWypelnienia, trybSortowania):
        self.rozmiar = rozmiar
        self.procentWypelnienia = procentWypelnienia
        self.trybSortowania = trybSortowania
        self.tablica = [[0] * rozmiar for _ in range(rozmiar)]
    def generowanieTablicy(self):
        wypelnioneKomorki = int(self.rozmiar * self.rozmiar * self.procentWypelnienia / 100)
        if self.procentWypelnienia == 0:
            return
        self.rozwiazTablice()
        pusteKomorki = self.rozmiar * self.rozmiar - wypelnioneKomorki
        indeksy = list(range(self.rozmiar * self.rozmiar))
        random.shuffle(indeksy)
        for i in range(pusteKomorki):
            index = indeksy[i]
            wiersze = index // self.rozmiar
            kolumny = index % self.rozmiar
            self.tablica[wiersze][kolumny] = 0
    def sprawdzaniePrawidlowegoRuchu(self, wiersze, kolumny, wartosc):
        if wartosc == 0:
            return True
        for i in range(self.rozmiar):
            if (self.tablica[wiersze][i] == wartosc and i != kolumny) or (self.tablica[i][kolumny] == wartosc and i != wiersze):
                return False
        rozmiarSiatki = int(self.rozmiar ** 0.5)
        wierszeSiatki = wiersze // rozmiarSiatki
        kolumnySiatki = kolumny // rozmiarSiatki
        for i in range(wierszeSiatki * rozmiarSiatki, (wierszeSiatki + 1) * rozmiarSiatki):
            for j in range(kolumnySiatki * rozmiarSiatki, (kolumnySiatki + 1) * rozmiarSiatki):
                if self.tablica[i][j] == wartosc and not (i == wiersze and j == kolumny):
                    return False
        return True
    def rozwiazTablice(self):
        for wiersze in range(self.rozmiar):
            for kolumny in range(self.rozmiar):
                if self.tablica[wiersze][kolumny] == 0:
                    for wartosc in random.sample(range(1, self.rozmiar + 1), self.rozmiar):
                        if self.sprawdzaniePrawidlowegoRuchu(wiersze, kolumny, wartosc):
                            self.tablica[wiersze][kolumny] = wartosc
                            if self.rozwiazTablice():
                                return True
                            self.tablica[wiersze][kolumny] = 0
                    return False
        return True
class Sudoku:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sudoku")
        self.game = None
        self.rozmiar_var = tk.StringVar()
        self.procentWypelnienia_var = tk.StringVar()
        self.trybSortowania_var = tk.StringVar()
        self.end_label = None
        rozmiar_label = tk.Label(self.root, text="Jesli plansza ma byc wielkosci 4x4 wpisz 4, jesli 9x9 to wpisz 9:")
        rozmiar_label.pack()
        rozmiar_entry = tk.Entry(self.root, textvariable=self.rozmiar_var)
        rozmiar_entry.pack()
        procentWypelnienia_label = tk.Label(self.root, text="W ilu procentach chcesz zeby plansza byla wypelniona, wpisz sama liczbe:")
        procentWypelnienia_label.pack()
        procentWypelnienia_entry = tk.Entry(self.root, textvariable=self.procentWypelnienia_var)
        procentWypelnienia_entry.pack()
        trybSortowania_label = tk.Label(self.root, text="Tryb gry, jesli plansza ma skladac sie z cyfr wpisz cyfry jesli z liter wpisz litery:")
        trybSortowania_label.pack()
        trybSortowania_entry = tk.Entry(self.root, textvariable=self.trybSortowania_var)
        trybSortowania_entry.pack()
        generate_button = tk.Button(self.root, text="Generuj planszę", command=self.generowanieTablicy)
        generate_button.pack()
        self.canvas = tk.Canvas(self.root, width=500, height=500)
        self.canvas.pack()
        self.wartoscNaWejscie = tk.StringVar()
        self.entry = tk.Entry(self.root, textvariable=self.wartoscNaWejscie)
        self.entry.pack()
        confirm_button = tk.Button(self.root, text="Potwierdź", command=self.potwierdzWybor)
        confirm_button.pack()
    def generowanieTablicy(self):
        rozmiar = int(self.rozmiar_var.get())
        procentWypelnienia = int(self.procentWypelnienia_var.get())
        trybSortowania = self.trybSortowania_var.get()
        if rozmiar not in [4, 9] or procentWypelnienia < 0 or procentWypelnienia > 100 or trybSortowania not in ["cyfry", "litery"]:
            messagebox.showerror("Błąd", "Nieprawidłowe dane wejściowe.")
            return
        self.game = GraSudoku(rozmiar, procentWypelnienia, trybSortowania)
        self.game.generowanieTablicy()
        self.rysujTablice()
        self.canvas.bind("<Button-1>", self.naPrzycisk)
    def rysujTablice(self):
        self.canvas.delete("all")
        szerokosc = self.canvas.winfo_width()
        wysokosc = self.canvas.winfo_height()
        rozmiarKomorek = min(szerokosc, wysokosc) // self.game.rozmiar
        for wiersze in range(self.game.rozmiar):
            for kolumny in range(self.game.rozmiar):
                x1 = kolumny * rozmiarKomorek
                y1 = wiersze * rozmiarKomorek
                x2 = (kolumny + 1) * rozmiarKomorek
                y2 = (wiersze + 1) * rozmiarKomorek
                # self.canvas.create_line(x1, y1, x2, y1, width=2)  # Linie poziome
                # self.canvas.create_line(x1, y1, x1, y2, width=2)  # Linie pionowe
                WartoscKomorek = self.game.tablica[wiersze][kolumny]
                if WartoscKomorek != 0:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")
                    if self.game.trybSortowania == "cyfry":
                        self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=str(WartoscKomorek),font=("Arial", 16), fill="black")
                    else:
                        letter = chr(ord('A') + WartoscKomorek - 1)
                        self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=letter, font=("Arial", 16),fill="black")
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="lightblue", outline="black")

        rozmiarSiatki = int(self.game.rozmiar ** 0.5)
        for wiersze in range(rozmiarSiatki):
            for kolumny in range(rozmiarSiatki):
                x1 = kolumny * rozmiarKomorek * rozmiarSiatki
                y1 = wiersze * rozmiarKomorek * rozmiarSiatki
                x2 = (kolumny + 1) * rozmiarKomorek * rozmiarSiatki
                y2 = (wiersze + 1) * rozmiarKomorek * rozmiarSiatki
                self.canvas.create_line(x1, y1, x2, y1, width=2)  # Linie poziome
                self.canvas.create_line(x1, y1, x1, y2, width=2)  # Linie pionowe
    def naPrzycisk(self, event):
        if self.game is None:
            return
        szerokosc = self.canvas.winfo_width()
        wysokosc = self.canvas.winfo_height()
        rozmiarKomorek = min(szerokosc, wysokosc) // self.game.rozmiar
        kolumny = event.x // rozmiarKomorek
        wiersze = event.y // rozmiarKomorek
        if 0 <= wiersze < self.game.rozmiar and 0 <= kolumny < self.game.rozmiar:
            if self.game.tablica[wiersze][kolumny] == 0:
                self.entry.delete(0, tk.END)
                self.wartoscNaWejscie.set("")
                self.entry.focus()
                self.entry.bind("<Return>", self.potwierdzWybor)
                self.aktualnyWiersz = wiersze
                self.aktualnaKolumna = kolumny
    def potwierdzWybor(self, event=None):
        wartosc = self.wartoscNaWejscie.get()
        if self.game.trybSortowania == "litery":
            wartosc = str(-ord('A') + ord(wartosc) + 1)
        if wartosc.isdigit() and 1 <= int(wartosc) <= self.game.rozmiar and self.game.sprawdzaniePrawidlowegoRuchu(self.aktualnyWiersz,self.aktualnaKolumna,int(wartosc)):
            self.game.tablica[self.aktualnyWiersz][self.aktualnaKolumna] = int(wartosc)
            self.rysujTablice()
            self.sprawdzGre()
            self.entry.unbind("<Return>")
            self.entry.delete(0, tk.END)
    def sprawdzGre(self):
        for wiersze in range(self.game.rozmiar):
            for kolumny in range(self.game.rozmiar):
                if self.game.tablica[wiersze][kolumny] == 0 or not self.game.sprawdzaniePrawidlowegoRuchu(wiersze, kolumny, self.game.tablica[wiersze][kolumny]):
                    return
        self.end_label = tk.Label(self.root, text="Koniec")
        self.end_label.pack()
    def rozpocznij(self):
        self.root.mainloop()
if __name__ == "__main__":
    s = Sudoku()
    s.rozpocznij()