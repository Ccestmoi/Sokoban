# -*- coding: utf-8 -*-
"""
@author: Alain Plantec

Voici un skelette possible.
Vous devez programmez les classes contenues dans ce squelette.
Les fonctions et leurs paramètres ainsi que les variables contenues dans le classes
ont du sens par rapport à une version programmée pour la préparation du projet.
Votre version sera forcément différente.
Donc, vous pouvez ajouter/retirer des variables et/ou des fonctions et/ou des paramètres.

"""
try:  # import as appropriate for 2.x vs. 3.x
    import tkinter as tk
    import tkinter.messagebox as tkMessageBox
except:
    import Tkinter as tk
    import tkMessageBox

from sokobanXSBLevels import *
from enum import Enum

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
    - stockage de coordoannées x et y,
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
        " a compléter "

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
    def __init__(self):
        # la matrice d'Elem
        self.rawMatrix = []

    def appendRow(self, row):
 
    def at(self, position):
    
    def atPut(self, position, elem):
        
    def isPositionValid(self, position):

    def hasFreePlaceAt(self, position):
        return self.at(position).isFreePlace()

    def asXsbMatrix(self):
        return xsbMatrix(self.rawMatrix)
    
"""
Floor :
    Représente une case vide de la matrice
    (pas de None dans la matrice)
"""
class Floor(object):
    def __init__(self):
        None
    def isMovable(self):
        return False
    def canBeCovered(self):
        return True
    def xsbChar(self):
        return ' '
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
    def __init__(self, canvas, position):

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

    def isFreePlace(self):
        return False

"""
Wall : pour délimiter les murs
    Le déménageur ne peut pas traverser un mur.
    Un Wall est static, il est toujours déssiné en dessous :
        Le zOrder est assuré par le tag du create_image (tag='static')
        et self.canvas.tag_raise("movable","static") dans Level
"""
class Wall(object):
    def __init__(self, canvas, position):
        self =
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
    def __init__(self, canvas, wharehouse, position, onGoal):

    def getHeight(self):
        return self.height
    
    def getWidth(self):
        return self.width

    def isMovable(self):
        return True

    def canBeCovered(self):
        return False

    def moveTowards(self, direction):
 
    def xsbChar(self):
        if self.under.isFreePlace(): return '$'
        else: return '*'

    def isFreePlace(self):
        return False

    def startGoalCoveredAnimation(self):
 
    def cleanUpAnimation(self):
  
    def goalCoveredAnimation(self):

 
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
    def __init__(self, canvas, wharehouse, position, onGoal):  
         
    def getHeight(self):
        return self.height
    
    def getWidth(self):
        return self.width

    def isMoveable(self):
        return True

    def moveInCanvas(self, direction):

    """
        Retourne True si le Mover peut se déplacer dans la direction demandée.
        Le calcul necessite de voir l'élément adjacent mais aussi l'élément suivant (offset de 2)
    """
    def canMove(self, direction):

    """
        Pour le déplacement, il faut penser à déplacer éventuellemnt le Box et ensuite déplacer le Mover
    """
    def moveTowards(self, direction):

    """
        Le Mover est représenté differemment suivant la direction de déplacement
    """
    def setupImageForDirection(self, dir):

    """
        Pour le déplacement :
            - image changée en fonction de la direction
            - si on ne peut pas se déplacer dans cette direction -> abandon
            - sinon, bin le Mover est déplacé
    """
    def push(self, direction):
        self.setupImageForDirection(direction)
        if not self.canMove(direction):
            self.startImpossiblePushAnimation()
            return
        self.moveTowards(direction)

    def xsbChar(self):
        if self.under.isFreePlace(): return '@'
        else: return '+'

    def isFreePlace(self):
        return False

    def startImpossiblePushAnimation(self):

    def cleanUpAnimation(self):

    def impossiblePushAnimation(self):

"""
    Le jeux avec tout ce qu'il faut pour dessiner et stocker/gérer la matrice d'éléments
    
"""
class Level(object):
    def __init__(self, root, xsbMatrix):
        self.root = root
        self.wharehouse = WharehousePlan()

        # calcul des dimensions de la matrice
        nbrows = len(xsbMatrix)
        nbcolumns = 0

        for line in xsbMatrix:
            nbc = len(line)
            if nbc > nbcolumns:
                nbcolumns = nbc

        self.height = nbrows * 64 
        self.width = nbcolumns * 64 
 
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg="gray")
        self.canvas.pack()

        self.initWharehouseFromXsb(xsbMatrix)
        self.root.bind("<Key>", self.keypressed)

    def initWharehouseFromXsb(self,xsbMatrix):
        # legend :
        #   '#' = wall,  '$' = box, '.' = goal, '*' = box on goal, '@' = mover, '+' = mover on goal, '-' = floor, ' ' = floor

        self.canvas.tag_raise("movable","static")
         
    def keypressed(self, event):

class Sokoban(object):
    '''
    Main Level class
    '''

    def __init__(self):
        self.root = tk.Tk()
        self.root.resizable(False, False)
        self.root.title("Sokoban")
        print('Sokoban: ' + str(len(SokobanXSBLevels)) + ' levels')
        self.level = Level(self.root, SokobanXSBLevels[99])
        #self.level = Level(self.root, [
            #['-','-','$','+','$','.','-','.','.','.','.','-','-','.','.','-','-','.','-'] ])
        #self.level = Level(self.root, [ ['@'] ])
 
    def play(self):
        self.root.mainloop()


Sokoban().play()

