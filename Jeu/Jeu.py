# -*- coding: utf-8 -*-
"""
@author: Alain Plantec

Voici un skelette possible.
Vous devez programmer les classes contenues dans ce squelette.
Les fonctions et leurs paramètres ainsi que les variables contenues dans le classes
ont du sens par rapport à une version programmée pour la préparation du projet.
Votre version sera forcément différente.
Donc, vous pouvez ajouter/retirer des variables et/ou des fonctions et/ou des paramètres.

"""
from debugpy.common.timestamp import current

try:  # import as appropriate for 2.x vs. 3.x
    import tkinter as tk
    import tkinter.messagebox as tkMessageBox
except:
    import Tkinter as tk
    import tkMessageBox

from sokobanXSBLevels import *
from enum import Enum
import json

"""
Direction :
    Utile pour gérer le calcul des positions pour les mouvements
"""


class Direction(Enum):
    Up = 1
    Down = 2
    Left = 3
    Right = 4


"""
Position :
    - stockage de coordonnées x et y,
    - vérification de x et y par rapport à une matrice
    - calcule de position relative à partir d'un offset (un décalage) et une direction 
"""
class Position(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return 'Position(' + str(self.x) + ',' + str(self.y) + str(')')

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    # retoune la position vers la direction #direction en tenant compte de l'offset
    #   Position(3,4).positionTowards(Direction.Right, 2) == Position(5,4)
    def positionTowards(self, direction, offset):
        if direction == Direction.Up:
            return Position(self.x, self.y - offset)
        elif direction == Direction.Down:
            return Position(self.x, self.y + offset)
        elif direction == Direction.Left:
            return Position(self.x - offset, self.y)
        elif direction == Direction.Right:
            return Position(self.x + offset, self.y)
        else:
            return Position(self.x, self.y)

    # Retourne True si les coordonnées sont valides dans le wharehouse
    def isValidInWharehouse(self, wharehouse):
        return wharehouse.isPositionValid(self)

    # Convertit le receveur en une position correspondante dans un Canvas
    def asCanvasPositionIn(self, elem):
        lx = self.getX() * elem.getWidth()
        ly = self.getY() * elem.getHeight()
        return Position(lx, ly)


"""
WharehousePlan : Plan de l'entrepot pour stocker les éléments.
    Les éléments sont stockés dans une matrice (#rawMatrix)
"""
class WharehousePlan(object):
    """Plan de l'entrepôt pour le jeu Sokoban."""

    def __init__(self, score):
        self.rawMatrix = [] # La matrice d'éléments vide
        self.mover = None  # Stocke le joueur
        self.score = score # Stocke le score

    def appendRow(self, row):
        """Ajoute une nouvelle ligne à la matrice."""
        self.rawMatrix.append(row)

    def at(self, position):
        """Retourne l'élément à la position donnée."""
        if not self.isPositionValid(position): #Gestion de l'erreur en dehors des limites
            #Affiche la position de l'erreur
            raise IndexError(f"Position invalide: {position}")
        return self.rawMatrix[position.getY()][position.getX()]

    def atPut(self, position, elem):
        """Place un élément à la position donnée."""
        if not self.isPositionValid(position): #Gestion de l'erreur en dehors des limites
            #Affiche la position de l'erreur
            raise IndexError(f"Position invalide: {position}")
        self.rawMatrix[position.getY()][position.getX()] = elem

    def isPositionValid(self, position):
        """Vérifie si une position est valide dans la matrice."""
        return (0 <= position.getY() < len(self.rawMatrix) and
                0 <= position.getX() < len(self.rawMatrix[position.getY()]))

    def setMover(self, mover):
        """Définit le joueur."""
        self.mover = mover

    def getMover(self):
        """Retourne le joueur."""
        return self.mover
        
"""
Floor :
    Représente une case vide de la matrice
    (pas de None dans la matrice)
"""
class Floor(object):
    """Initialise un sol vide"""
    def __init__(self):
        None

    def isMovable(self):
        return False

    def canBeCovered(self):
        return True

    def xsbChar(self):
        return ' '

    # Retourne True parce qu'on peut passer dessus avec une caisse et le mover (c'est la Hitbox)
    def isFreePlace(self):
        return True


"""
Goal :
    Représente une localisation à recouvrir d'un BOX (objectif du jeu).
    Le déménageur doit parvenir à couvrir toutes ces cellules à partir des caisses.
    Un Goal est static, il est toujours déssiné en dessous :
        Le zOrder est assuré par le tag du create_image (tag='static')
        et self.canvas.tag_raise("movable","static") dans Level
"""
class Goal(object):
    """Initialise un objectif"""
    def __init__(self, canvas, position):
        self.image = tk.PhotoImage(file='goal.png')
        self.canvas = canvas
        self.canvas.create_image(position.getX() * 64 + 32, position.getY() * 64 + 32, image=self.image, tags="static")

    def isMovable(self):
        return False

    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width

    def canBeCovered(self):
        return True

    def xsbChar(self):
        return '.'
    # Retourne True parce qu'on peut passer dessus avec une caisse et le mover (c'est la Hitbox)
    def isFreePlace(self):
        return True


"""
Wall : pour délimiter les murs
    Le déménageur ne peut pas traverser un mur.
    Un Wall est static, il est toujours déssiné en dessous :
        Le zOrder est assuré par le tag du create_image (tag='static')
        et self.canvas.tag_raise("movable","static") dans Level
"""
class Wall(object):
    """Initialise un mur"""
    def __init__(self, canvas, position):
        self.image = tk.PhotoImage(file='wall.png')
        self.canvas = canvas
        self.canvas.create_image(position.getX() * 64 + 32, position.getY() * 64 + 32, image=self.image, tags="static") #Crée l'image du Mur(64x64) en decalent de 32 px en X et Y (car 0,0 est au centre de l'image)

    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width

    def isMovable(self):
        return False

    def canBeCovered(self):
        return False

    def xsbChar(self):
        return '#'
    # Retourne False parce qu'on peut pas passer dessus avec une caisse ou le mover (c'est la Hitbox)
    def isFreePlace(self):
        return False


"""
Box : Caisse à déplacer par le déménageur.
    Etant donné qu'une caisse doit être déplacé, le canvas et la matrice sont necessaires pour
    reconstruire l'image et mettre en oeuvre sont déplacement (dans le canvas et dans la matrice)
    Un Box est "movable", il est toujours déssiné au dessus des objets "static" :
        Le zOrder est assuré par le tag du create_image (tag='movable')
        et self.canvas.tag_raise("movable","static") dans Level
    Un Box est représenté differemment (image différente) suivant qu'il se situe sur un emplacement marqué par un Goal ou non.
 """


class Box(object):
    """Initialise une boite"""
    def __init__(self, canvas, wharehouse, position, onGoal=False):
        self.width = 64
        self.height = 64
        self.canvas = canvas
        self.position = position
        self.wharehouse = wharehouse
        self.onGoal = onGoal
        self.image = tk.PhotoImage(file='box.png')
        self.imageId = self.canvas.create_image(
            self.position.getX() * self.width + self.width / 2,
            self.position.getY() * self.height + self.height / 2,
            image=self.image,
            tags="movable"
        )

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def isMovable(self):
        return True

    def canBeCovered(self):
        return False

    #Verifie si la prochaine position du joueur est disponible où est un mur
    def moveTowards(self, direction):
        nextPos = self.position.positionTowards(direction, 1)
        nextElement = self.wharehouse.at(nextPos)
        if nextElement is None or not nextElement.canBeCovered():
            return False
        # Mise à jour de la matrice
        # Remplacer l'ancienne instance du Mover par un Floor
        self.wharehouse.atPut(self.position, Floor())
        self.position = nextPos
        element = self.wharehouse.at(self.position)
        if isinstance(element,Goal):
            self.onGoal = True #si la boite est sur l'objectif
            self.wharehouse.score.player_score += 100 #Augmente de 100 le score du joueur
            
        # Ajoute la boite sur la position suivante
        self.wharehouse.atPut(self.position, self)

        # Mise à jour de l'état onGoal
        self.updateImage()

        # Mise à jour de l'affichage
        canvasPos = self.position.asCanvasPositionIn(self)
        self.canvas.coords(
            self.imageId,
            canvasPos.getX() + self.width / 2,
            canvasPos.getY() + self.height / 2
        )
        return True

    def updateImage(self):
        if self.onGoal: #si la boite est sur l'objectif
            self.image = tk.PhotoImage(file='boxOnTarget.png') #on change l'image
        else:
            self.image = tk.PhotoImage(file='box.png')
        self.canvas.delete(self.imageId)
        self.imageId = self.canvas.create_image(
            self.position.getX() * self.width + self.width / 2,
            self.position.getY() * self.height + self.height / 2,
            image=self.image,
            tags="movable"
        )


    def xsbChar(self):
        return '*' if self.onGoal else '$'

    def isFreePlace(self):
        return False


"""
Mover : C'est  le déménageur.
    La classe Mover met en oeuvre la logique du jeu dans #canMove et #moveTowards.
    Etant donné qu'un Mover se déplace, le canvas et la matrice sont necessaires pour
    reconstruire l'image et mettre en oeuvre sont déplacement (dans le canvas et dans la matrice)
    Un Mover est "movable", il est toujours déssiné au dessus des objets "static" :
        Le zOrder est assuré par le tag du create_image (tag='movable')
        et self.canvas.tag_raise("movable","static") dans Level
    Un Box est représenté differemment (image différente) suivant la direction de déplacement (même si le dépplacement s'avère impossible).
"""


class Mover(object):
    # Initialise le Joueur
    def __init__(self, canvas, wharehouse, position, onGoal=False):
        self.canvas = canvas
        self.wharehouse = wharehouse
        self.position = position
        self.onGoal = onGoal
        self.width = 64
        self.height = 64
        self.image = tk.PhotoImage(file='player.png')
        self.player = self.canvas.create_image(
            self.position.getX() * self.width + self.width / 2,
            self.position.getY() * self.height + self.height / 2,
            image=self.image,
            tags="movable"
        )

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def isMovable(self): #verife si les oItem sont bougable
        return True

    def canMove(self, direction): #Verifie si le chemin est libre
        nextPos = self.position.positionTowards(direction, 1)
        if not self.wharehouse.isPositionValid(nextPos):
            return False
        nextElement = self.wharehouse.at(nextPos)

        if isinstance(nextElement, (Floor, Goal)):
            return True
        elif isinstance(nextElement, Box):
            boxNextPos = nextPos.positionTowards(direction, 1)
            if not self.wharehouse.isPositionValid(boxNextPos):
                return False
            boxNextElement = self.wharehouse.at(boxNextPos)
            if isinstance(boxNextElement, (Floor, Goal)):
                return True
        return False

    def moveTowards(self, direction): #Bouge a la direction visé (Up, Down...)
        if not self.canMove(direction):
            return

        nextPos = self.position.positionTowards(direction, 1)
        nextElement = self.wharehouse.at(nextPos)

        # Mise à jour de la matrice
        self.wharehouse.atPut(self.position, Floor())

        if self.onGoal:
            self.wharehouse.atPut(self.position, Goal(self.canvas, self.position))
        else:
            self.wharehouse.atPut(self.position, Floor())

        currentElement = self.wharehouse.at(nextPos)
        if isinstance(currentElement, Goal):
            self.onGoal = True
        else:
            self.onGoal = False

        if isinstance(nextElement, Box):
            if nextElement.onGoal:
                self.onGoal = True
            nextElement.moveTowards(direction)

        self.position = nextPos
        self.wharehouse.atPut(self.position, self)

        # Mise à jour de l'affichage
        canvasPos = self.position.asCanvasPositionIn(self)
        self.canvas.coords(
            self.player,
            canvasPos.getX() + self.width / 2,
            canvasPos.getY() + self.height / 2
        )

    def setupImageForDirection(self, direction):
        if direction == Direction.Up:
            self.image = tk.PhotoImage(file='playerUp.png')
        elif direction == Direction.Down:
            self.image = tk.PhotoImage(file='playerDown.png')
        elif direction == Direction.Left:
            self.image = tk.PhotoImage(file='playerLeft.png')
        elif direction == Direction.Right:
            self.image = tk.PhotoImage(file='playerRight.png')

        self.canvas.itemconfig(self.player, image=self.image)

    def push(self, direction):
        self.setupImageForDirection(direction)
        self.moveTowards(direction)

    def xsbChar(self):
        return '+' if self.onGoal else '@'

    def isFreePlace(self):
        return False


"""
    Permet de calculer le Score du joueur en prenant en compte le nom du joueur, le score et le nombre de déplacements
"""
class Score(object):
    def __init__(self, name, player_score=0, player_deplacement=0):
        self.player_name = name
        self.player_score = player_score
        self.player_deplacement = player_deplacement

    def __str__(self):
        return f"Joueur : {self.player_name}, Score : {self.player_score}, Déplacements : {self.player_deplacement}"

    def getPlayer(self):
        return self.player_name  # Retourne le nom du joueur

    def getScore(self):
        return self.player_score  # Retourne le score du joueur

    def toFile(self, fich):
        try:
            # Tente d'ouvrir le fichier en mode lecture
            with open(fich, "r") as f:
                try:
                    data = json.load(f)  # Charge les données existantes
                except json.JSONDecodeError:
                    data = []  # Si le JSON est invalide, initialise une liste vide
        except FileNotFoundError:
            data = []  # Si le fichier n'existe pas, initialise une liste vide

        # Crée un dictionnaire du score actuel
        current_score = {
            "player_name": self.player_name,
            "player_score": self.player_score,
            "player_deplacement": self.player_deplacement
        }

        # Ajoute le score actuel à la liste des scores
        data.append(current_score)

        # Écrit la liste mise à jour dans le fichier
        with open(fich, "w") as f: #Ouvre et ferme automatiquement le fichier
            json.dump(data, f, indent=4)  #stocke les données dans le fichier, Indent pour une meilleure lisibilité,

    def fromFile(cls, fich):
        f = open(fich, "r")
        tmp = json.load(f)

        liste = []
        for d in tmp:
            # créer un livre
            tmp_var = Score(d["player_name"], d["player_score"], d["player_deplacement"])
            # l'ajouter dans la liste
            liste.append(tmp_var)
        history = Score()
        history.score = liste
        f.close()
        return history

"""
    Le jeux avec tout ce qu'il faut pour dessiner et stocker/gérer la matrice d'éléments
"""
class Level(object):
    def __init__(self, root, xsbMatrix):
        self.root = root
        self.score = Score("User")
        self.warehouse = WharehousePlan(self.score)  # Correction de l'orthographe

        # Définir la taille des tuiles
        self.tile_size = 64

        # Calcul des dimensions de la matrice
        nbrows = len(xsbMatrix)
        nbcolumns = max(len(line) for line in xsbMatrix) if xsbMatrix else 0

        self.height = nbrows * self.tile_size
        self.width = nbcolumns * self.tile_size

        # Création du canvas
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg="gray")
        self.canvas.pack()

        # Initialisation du plan de l'entrepôt à partir de la matrice
        self.initWarehouseFromXsb(xsbMatrix)

        # Liaison des touches du clavier
        self.root.bind("<Key>", self.keypressed)

        # Affichage du score
        self.score_text_id = self.canvas.create_text(10, 10, anchor='nw', 
                                                    text=f"Score : {self.score.getScore()}", 
                                                    font=("Arial", 16), fill="white")

        # Affichage du nombre de déplacements
        self.deplacements_text_id = self.canvas.create_text(10, 30, anchor='nw', 
                                                           text=f"Déplacements : {self.score.player_deplacement}", 
                                                           font=("Arial", 16), fill="white")

    def initWarehouseFromXsb(self, xsbMatrix):
        """
        Initialise le plan de l'entrepôt à partir de la matrice xsb.
        Legend :
            '#' = mur, '$' = caisse, '.' = objectif, '*' = caisse sur objectif,
            '@' = joueur, '+' = joueur sur objectif, '-' ou ' ' = sol
        """
        for y, line in enumerate(xsbMatrix):
            row = []
            for x, char in enumerate(line):
                pos = Position(x, y)
                if char == '#':
                    # Ajout d'un mur
                    wall = Wall(self.canvas, pos)
                    row.append(wall)
                elif char == '@':
                    # Ajout du joueur
                    mover = Mover(self.canvas, self.warehouse, pos, onGoal=False)
                    row.append(mover)
                    self.warehouse.setMover(mover)
                elif char == '+':
                    # Ajout du joueur sur objectif
                    mover = Mover(self.canvas, self.warehouse, pos, onGoal=True)
                    row.append(mover)
                    self.warehouse.setMover(mover)
                elif char == '$':
                    # Ajout d'une caisse
                    box = Box(self.canvas, self.warehouse, pos, onGoal=False)
                    row.append(box)
                elif char == '*':
                    # Ajout d'une caisse sur objectif
                    box = Box(self.canvas, self.warehouse, pos, onGoal=True)
                    row.append(box)
                elif char in ['.', '-', ' ']:
                    # Ajout d'un sol ou d'un objectif
                    if char == '.':
                        goal = Goal(self.canvas, pos)
                        row.append(goal)
                    else:
                        floor = Floor()
                        row.append(floor)
                else:
                    # Gestion des caractères inconnus en ajoutant un sol par défaut
                    floor = Floor()
                    row.append(floor)
            self.warehouse.appendRow(row)

    def keypressed(self, event):
        """
        Gère les événements de pression de touche pour déplacer le joueur.
        """
        mover = self.warehouse.getMover()
        if mover is None:
            return

        direction = None
        if event.keysym == 'Up':
            direction = Direction.Up
        elif event.keysym == 'Down':
            direction = Direction.Down
        elif event.keysym == 'Left':
            direction = Direction.Left
        elif event.keysym == 'Right':
            direction = Direction.Right

        if direction is not None:
            self.score.player_deplacement += 1
            mover.push(direction)
            self.update_score_display()
            self.checkWinCondition()

    def update_score_display(self):
        self.canvas.itemconfig(self.score_text_id, text=f"Score : {self.score.getScore()}")
        self.canvas.itemconfig(self.deplacements_text_id, text=f"Déplacements : {self.score.player_deplacement}")

    def checkWinCondition(self):
        """
        Vérifie si toutes les caisses sont sur les objectifs.
        """
        for row in self.warehouse.rawMatrix:
            for element in row:
                if isinstance(element, Box) and not element.onGoal:
                    return  # Au moins une caisse n'est pas sur un objectif
        print("Félicitations ! Vous avez gagné !")
        self.root.unbind("<Key>")  # Désactive les entrées clavier
        self.score.toFile("jeu.json")


class Sokoban(object):
    '''
    Main Level class
    '''

    def __init__(self):
        self.root = tk.Tk()
        self.root.resizable(False, False)
        self.root.title("Sokoban")
        print('Sokoban: ' + str(len(SokobanXSBLevels)) + ' levels')
        self.level = Level(self.root, SokobanXSBLevels[2])

    def play(self):
        self.root.mainloop()

Sokoban().play()

