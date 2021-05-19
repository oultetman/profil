# -------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      pierre
#
# Created:     26/05/2018
# Copyright:   (c) pierre 2018
# Licence:     <your licence>
# -------------------------------------------------------------------------------
from math import *
from multipledispatch import dispatch
from numbers import Number
from typing import List, Tuple


class Vecteur:

    @dispatch(Number, Number, str)
    def __init__(self, x: Number, y: Number, nom: str):
        self.x = x
        self.y = y
        self.nom = nom

    @dispatch(int, int)
    def __init__(self, x: Number, y: Number):
        self.__init__(x, y, "")

    @dispatch((list, tuple))
    def __init__(self, couple: List[int]):
        self.__init__(couple[0], couple[1], "")

    @dispatch((list, tuple), str)
    def __init__(self, couple: List[Number], nom: str):
        self.__init__(couple[0], couple[1], nom)

    @dispatch(object)
    def __init__(self, vecteur: 'Vecteur'):
        self.__init__(vecteur.x, vecteur.y)

    @dispatch(object, object)
    def __init__(self, p1: 'Point', p2: 'Point'):
        x = p2.x - p1.x
        y = p2.y - p1.y
        self.__init__(x, y, "")

    @dispatch(object, object, str)
    def __init__(self, p1: 'Point', p2: 'Point', nom: str):
        x = p2.x - p1.x
        y = p2.y - p1.y
        self.__init__(x, y, nom)

    def __str__(self) -> str:
        if self.nom == "":
            return "({},{})".format(self.x, self.y)
        else:
            return "{}=({},{})".format(self.nom, self.x, self.y)

    def produitScalaire(self, vecteur: 'Vecteur') -> Number:
        """ Retourne le produit scalaire """
        return self.x * vecteur.x + self.y * vecteur.y

    def colineaire(self, vecteur: 'Vecteur') -> bool:
        """ Retourne True si les deux vecteurs sont colinéaires """
        return self.x * vecteur.y == self.y * vecteur.x

    def ortho(self, vecteur: 'Vecteur') -> bool:
        """ Retourne True si les deux vecteurs sont orthogonaux """
        return self.produitScalaire(vecteur) == 0

    def norme(self) -> float:
        return sqrt(self.x ** 2 + self.y ** 2)

    def __mul__(self, vecteur: 'Vecteur') -> Number:
        return self.produitScalaire(vecteur)

    def angle(self, vecteur: 'Vecteur') -> float:
        pass


class Point:
    @dispatch(Number, Number, str)
    def __init__(self, x: Number, y: Number, nom: str):
        self.x = x
        self.y = y
        self.nom = nom

    @dispatch(list)
    def __init__(self, couple: List[Number]):
        self.__init__(couple[0], couple[1], "")

    @dispatch(tuple)
    def __init__(self, couple: Tuple[Number]):
        self.__init__(couple[0], couple[1], "")

    @dispatch(object)
    def __init__(self, point: 'Point'):
        self.__init__(point.x, point.y, "")

    def __str__(self):
        if self.nom == "":
            return "({};{})".format(self.x, self.y)
        else:
            return "{}=({};{})".format(self.nom, self.x, self.y)

    def dx(self, point):
        return point.x - self.x

    def dy(self, point):
        return point.y - self.y

    def distance(self, point):
        """ Retourne la distance entre deux points """
        return sqrt(self.dx(point) ** 2 + self.dy(point) ** 2)

    def translation(self, vecteur):
        """ Retourne un point issue de la translation par un vecteur """
        return Point(self.x + vecteur.x, self.y + vecteur.y)

    def alignes(self, point1, point2):
        point0 = Point(self)
        v1 = Vecteur(point0, point1)
        v2 = Vecteur(point1, point2)
        return v1.colineaire(v2)


def main():
    print("debut")
    A = Point(6, 0, "A")
    B = Point(0, 8, "B")
    C = Point(2, 2, "C")
    CA = Vecteur(C, A, "CA")
    CB = Vecteur(C, B, "CB")
    print(CA, CB)
    print("CA.CB =", CA * CB)
    print("cos(teta) = ", (CA * CB) / (CA.norme() * CB.norme()))


if __name__ == '__main__':
    main()
