from tkinter import *
from modele import *

class VueSame:
    '''Gère la vue du jeu Same.
    '''

    def __init__(self, same):
        '''Construit la fenêtre principale de l'application et
        tous les composants de la vue.
        VueSame, ModeleSame -> VueSame
        '''

        self.__same = same

        fen = Tk()
        fen.title("SameGame")
        fen['bg'] = "#DDCDFE"

        self.__images = initialise_images()
        self.__images_noires = initialise_images_noires()
        images_interf = initialise_images_interf()

        # Cases
        grille = Frame(fen)
        self.__les_btns = []
        for l in range(same.nblig()):
            lig = []
            for c in range(same.nbcol()):
                lig.append(Button(grille, image=self.__images[self.__same.couleur(l, c)],
                                  command=self.cree_ctrl_btn(l,c), bg="#DDCDFE"))
                lig[-1].bind("<Enter>", self.cree_ctrl_noir(l,c))
                lig[-1].bind("<Leave>", self.cree_ctrl_blanc)
                lig[-1].grid(row=l, column=c)
            self.__les_btns.append(lig)

        grille.grid()
        
        # Interfaces
        interf = Frame(fen, bg="#DDCDFE")

        lbl_bois = Label(interf, image=images_interf['bois'])
        
        self.__lbl_score = Label(interf, text="Score : _",
                          width=18, height=3, bg="#DDCDFE")
        btn_nouveau = Button(interf, text="Nouveau", command=self.nouvelle_partie,
                             width=14, bg="#DDCDFE")
        btn_quit = Button(interf, text="Au revoir",command=fen.destroy, width=14,
                          bg="#DDCDFE")

        #lbl_bois
        self.__lbl_score.pack()
        btn_nouveau.pack()
        btn_quit.pack()

        interf.grid(row=0, column=1, pady=2)
        
        fen.mainloop()

    def redessine(self):
        '''Met à jour la vue en fonction du modèle du jeu.
        VueSame (modif) -> None
        '''

        for l in range(len(self.__les_btns)):
            for c in range(len(self.__les_btns[l])):
                self.__les_btns[l][c]['image'] = self.__images[self.__same.couleur(l, c)]

                if self.__same.composante(l,c) == 0:
                    self.__les_btns[l][c]['relief'] = "flat"
                else:
                    self.__les_btns[l][c]['relief'] = "raised"

    def nouvelle_partie(self):
        '''Demande au modèle de réinitialiser une partie, puis met à jour la vue.
        VueSame (modif) -> None
        '''

        self.__same.nouvelle_partie()
        self.maj_score()
        self.redessine()

    def cree_ctrl_btn(self, i, j):
        '''Renvoie une fonction spécifique à un bouton en (i, j).
        VueSame (modif), int, int -> fonction()
        '''

        def controleur_btn():
            '''Supprime la bille du bouton.
            None -> None
            '''

            if self.__same.supprime_composante(self.__same.composante(i,j)):
                self.redessine()
            self.maj_score()

        return controleur_btn

    def maj_score(self):
        '''Met à jour le score dans le label.
        VueSame (modif) -> None
        '''

        self.__lbl_score["text"] = "Score : " + str(self.__same.score())

    def cree_ctrl_noir(self, i, j):
        '''Renvoie une fonction mettant en avant un bouton.
        VueSame, int, int -> function()
        '''

        def ctrl_noir(event):
            '''Met en avant un bouton d'une composante spécifique.
            event -> None
            '''

            compo = self.__same.composante(i, j)
            
            for l in range(self.__same.nblig()):
                for c in range(self.__same.nbcol()):
                    act_compo = self.__same.composante(l, c)
                    if  act_compo == compo and act_compo != 0:
                        self.__les_btns[l][c]["image"] = self.__images_noires[self.__same.couleur(l,c)]

        return ctrl_noir

    def cree_ctrl_blanc(self, event):
        '''Redessine les boutons.
        VueSame, event -> None
        '''

        self.redessine()

# Fin de la classe VueSame.

def initialise_images():
    '''Renvoie la liste de toutes les images.
    None -> list(PhotoImage)
    '''

    images = []
    for i in range(8):
        images.append(PhotoImage(file="./img/sphere" + str(i+1) + ".gif"))
    images.append(PhotoImage(file="./img/spherevide.gif"))

    return images

def initialise_images_noires():
    '''Renvoie la liste de toutes les images noires.
    None -> list(PhotoImage)
    '''

    images = []
    for i in range(8):
        images.append(PhotoImage(file="./img/sphere" + str(i+1) + "black.gif"))

    return images

def initialise_images_interf():
    ''''''

    images = {}
    images['bois'] = PhotoImage(file="./img/bois.gif")

    return images

# Script principal

if __name__ == "__main__":
    # Création du modèle
    same = ModeleSame()
    # Création de la vue qui crée les contrôleurs
    # et lance la boucle d'écoute des évts.
    vue = VueSame(same)
