from random import randint

class Case:
    '''Modélise une bille du jeu Same.
    '''

    def __init__(self, couleur):
        '''Initialise les attributs de la classe Case.
        Case, int -> Case
        '''

        self.__couleur = couleur
        self.__compo = -1
        
    def couleur(self):
        '''Renvoie la couleur de la bille.
        Case -> int
        '''

        return self.__couleur

    def change_couleur(self, n_couleur):
        '''Modifie la valeur de la couleur de la bille.
        Case (modif), int -> None
        '''

        self.__couleur = n_couleur
        self.__compo = -1

    def supprime(self):
        '''Enlève la bille de la case (passe la couleur à -1).
        Case (modif) -> None
        '''

        self.__couleur = -1
        self.__compo = 0
        
    def est_vide(self):
        '''Indique si la case est vide (= -1).
        Case -> bool
        '''

        return self.__couleur == -1

    def composante(self):
        '''Renvoie le numéro de la composante.
        Case -> int
        '''

        return self.__compo

    def pose_composante(self, num):
        '''Modifie le numéro de composante de la case.
        Case (modif), int -> None
        '''

        self.__compo = num

    def supprime_compo(self):
        '''Désaffecte le numéro de composante.
        Case (modif) -> None
        '''

        self.__compo = 0
        if not self.est_vide():
            self.__compo = -1

    def parcourue(self):
        '''Indique si la case a été affectée à un numéro de composante.
        Case -> bool
        '''

        return self.__compo != -1 and self.__compo != 0

# Fin de la classe Case.

class ModeleSame:
    '''Gère le modèle du jeu Same.
    '''

    def __init__(self, nblig=10, nbcol=15, nbcouleurs=3):
        '''Initialise les attributs de la classe ModeleSame.
        ModeleSame, int, int, int -> ModeleSame
        '''

        assert nblig > 0 and nbcol > 0 and 0 <= nbcouleurs <= 8

        self.__nblig = nblig
        self.__nbcol = nbcol
        self.__nbcouleurs = nbcouleurs

        self.__mat = []
        for l in range(nblig):
            lig = []
            for c in range(nbcol):
                lig.append(Case(randint(0, nbcouleurs - 1)))
            self.__mat.append(lig)
        
        self.__score = 0
        self.__nb_elts_compo = []
        self.calcule_composantes()

    def score(self):
        '''Renvoie le score.
        ModeleSame -> int
        '''

        return self.__score

    def nblig(self):
        '''Renvoie le nombre de lignes.
        ModeleSame -> int
        '''

        return self.__nblig

    def nbcol(self):
        '''Renvoie le nombre de colonnes.
        ModeleSame -> int
        '''

        return self.__nbcol

    def nbcouleurs(self):
        '''Renvoie le nombre de couleurs.
        ModeleSame -> int
        '''

        return self.__nbcouleurs

    def coords_valides(self, i, j):
        '''Indique si (i, j) sont des coordonnée valides pour le jeu.
        ModeleSame, int, int -> bool
        '''

        return 0 <= i < self.__nblig and 0 <= j < self.__nbcol

    def couleur(self, i, j):
        '''Renvoie la couleur de la bille en (i, j).
        ModeleSame, int, int -> int
        '''

        return self.__mat[i][j].couleur()

    def supprime_bille(self, i, j):
        '''Supprime la bille en (i, j).
        ModeleSame (modif), int, int -> None
        '''

        self.__mat[i][j].supprime()

    def nouvelle_partie(self):
        '''Réinitialise toutes les cases.
        ModeleCase (modif) -> None
        '''

        nouv_mat = []
        for l in range(self.__nblig):
            lig = []
            for c in range(self.__nbcol):
                lig.append(Case(randint(0, self.__nbcouleurs - 1)))
            nouv_mat.append(lig)

        self.__mat = nouv_mat
        self.__score = 0
        self.recalc_composante()

    def composante(self, i, j):
        '''Renvoie la composante de la bille en (i, j).
        ModeleSame, int, int -> int
        '''

        return self.__mat[i][j].composante()

    def calcule_composantes(self):
        '''Calcule les composantes de toutes les cases.
        ModeleSame (modif) -> None
        '''

        self.__nb_elts_compo = [0]
        
        num_compo = 1
        for i in range(self.__nblig):
            for j in range(self.__nbcol):
                if self.__mat[i][j].composante() == -1:
                    couleur = self.__mat[i][j].couleur()
                    self.__nb_elts_compo.append(self.calcule_composante_numero(i, j, num_compo, couleur))
                    num_compo += 1

    def calcule_composante_numero(self, i, j, num_compo, couleur):
        '''Calcule le nombre de case du composant numéro 'num_compo' d'une couleur.
        ModeleSame (modif), int, int, int, int -> int
        '''

        if  self.__mat[i][j].parcourue() or self.__mat[i][j].couleur() != couleur:
            return 0
        else:
            self.__mat[i][j].pose_composante(num_compo)
            adjs = [(i,j-1),(i+1,j),(i,j+1),(i-1,j)]
            num = 1
            for l,c in adjs:
                if self.coords_valides(l,c):
                    num += self.calcule_composante_numero(l, c, num_compo, couleur)
        return num

    def recalc_composante(self):
        '''Recalcule la composante des cases.
        ModeleSame (modif), int -> None
        '''

        for ligne in self.__mat:
            for case in ligne:
                case.supprime_compo()
        self.calcule_composantes()

    def supprime_composante(self, num_compo):
        '''Supprime toutes les billes de la matrice étant dans la composante num_compo.
        ModeleSame (modif), int -> None
        '''

        supprime = False

        for j in range(self.__nbcol):
            if self.__nb_elts_compo[num_compo] >= 2:
                self.supprime_composante_colonne(j, num_compo)
                supprime = True

        if supprime:
            self.__score += (self.__nb_elts_compo[num_compo] - 2)**2
            self.supprime_colonnes_vides()
            self.recalc_composante()
        
        return supprime

    def est_vide(self, i, j):
        '''Indique si la case en (i, j) est vide.
        ModeleSame, int, int -> bool
        '''

        return self.__mat[i][j].est_vide()

    def supprime_composante_colonne(self, j, num_compo):
        '''Supprime les case en colonne j de la composante num_compo.
        ModeleSame (modif), int, int -> None
        '''

        for lig in self.__mat:
            if lig[j].composante() == num_compo:
                lig[j].supprime()

        i = self.__nblig
        while i > 0:
            i -= 1
            deb = i
            while self.est_vide(i, j) and i > 0:
                i -= 1
                
            if deb != i:
                fin = self.__mat[i][j]
                self.__mat[i][j] = self.__mat[deb][j]
                self.__mat[deb][j] = fin

                i = deb

    def colonne_vide(self, j):
        '''Indique si la colonne j est vide.
        ModeleSame, int -> bool
        '''

        for lig in self.__mat:
            if not lig[j].est_vide():
                return False

        return True

    def interv_colonnes(self, j1, j2):
        '''Intervertie les colonnes j1 et j2.
        ModeleSame (modif), int, int -> None
        '''

        for lig in self.__mat:
            temp = lig[j1]
            lig[j1] = lig[j2]
            lig[j2] = temp

    def supprime_colonnes_vides(self):
        '''Décale les colonnes vides vers la droite.
        ModeleSame (modif) -> None
        '''

        j = 0
        while j < self.__nbcol:
            if self.colonne_vide(j):
                j_bis = j
                while j_bis > 0:
                    self.interv_colonnes(j_bis, j_bis - 1)
                    j_bis -= 1

            j += 1



















