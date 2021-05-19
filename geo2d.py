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
from numbers import Real
from typing import List, Tuple, Union


class Vecteur:

    @dispatch(Real, Real, str)
    def __init__(self, x: Real, y: Real, nom: str):
        self.x = x
        self.y = y
        self.nom = nom

    @dispatch(Real, Real)
    def __init__(self, x: Real, y: Real):
        self.__init__(x, y, "")

    @dispatch((list, tuple))
    def __init__(self, couple: List[Real]):
        self.__init__(couple[0], couple[1], "")

    @dispatch((list, tuple), str)
    def __init__(self, couple: Union[List[Real], Tuple[Real]], nom: str):
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

    def produit_scalaire(self, vecteur: 'Vecteur') -> Real:
        """ Retourne le produit scalaire """
        return self.x * vecteur.x + self.y * vecteur.y

    def colineaire(self, vecteur: 'Vecteur') -> bool:
        """ Retourne True si les deux vecteurs sont colinéaires """
        return self.x * vecteur.y == self.y * vecteur.x

    def ortho(self, vecteur: 'Vecteur') -> bool:
        """ Retourne True si les deux vecteurs sont orthogonaux """
        return self.produit_scalaire(vecteur) == 0

    def norme(self) -> float:
        return sqrt(self.x ** 2 + self.y ** 2)

    def __mul__(self, vecteur: 'Vecteur') -> Real:
        return self.produit_scalaire(vecteur)

    def angle(self, vecteur: 'Vecteur') -> float:
        pass


class Point:
    @dispatch(Real, Real, str)
    def __init__(self, x: Real, y: Real, nom: str):
        self.x = x
        self.y = y
        self.nom = nom

    @dispatch(Real, Real)
    def __init__(self, x: Real, y: Real):
        self.__init__(x, y, "")

    @dispatch((list, tuple))
    def __init__(self, couple: List[Real]):
        self.__init__(couple[0], couple[1], "")

    @dispatch(object)
    def __init__(self, point: 'Point'):
        self.__init__(point.x, point.y, "")

    def __str__(self):
        if self.nom == "":
            return "({},{})".format(self.x, self.y)
        else:
            return "{}=({},{})".format(self.nom, self.x, self.y)

    def dx(self, point: 'Point'):
        return point.x - self.x

    def dy(self, point: 'Point'):
        return point.y - self.y

    def distance(self, point: 'Point'):
        """ Retourne la distance entre deux points """
        return sqrt(self.dx(point) ** 2 + self.dy(point) ** 2)

    def translation(self, vecteur: Vecteur):
        """ Retourne un point issue de la translation par un vecteur """
        return Point(self.x + vecteur.x, self.y + vecteur.y)

    def alignes(self, point1: 'Point', point2: 'Point'):
        point0 = Point(self)
        v1 = Vecteur(point0, point1)
        v2 = Vecteur(point1, point2)
        return v1.colineaire(v2)


class Droite:
    @dispatch(Real, Real)
    def __init__(self, a: Real, b: Real):
        self.a = a
        self.b = b

    @dispatch(Point, Point)
    def __init__(self, p1: Point, p2: Point):
        self.a = (p2.y - p1.y) / (p2.x - p1.x)
        self.b = p1.y - self.a * p1.x

    @dispatch(Vecteur, Point)
    def __init__(self, v: Vecteur, p: Point):
        self.a = v.y / v.x
        self.b = p.y - self.a * p.x

    def __str__(self) -> str:
        return f"y = {self.a}x {self.b:+}"

    def intersection(self, droite: 'Droite') -> Union[Point, None]:
        """retourne le point d'intersection entre deux droites sécantes"""
        if self.a != droite.a:
            x: Real = (self.b - droite.b) / (droite.a - self.a)
            y: Real = self.a * x + self.b
            return Point(x, y)
        return None

    def parallele(self, p: Point) -> 'Droite':
        """retourne la droite parallele à self passant par p"""
        return Droite(self.a, p.y - self.a * p.x)

    def perpendiculaire(self, p: Point) -> 'Droite':
        """retourne la droite perpendiculaire à self passant par p"""
        return Droite(-1/self.a, p.y + p.x/self.a)

    def appartient(self, p: Point, delta: float = 0.001) -> bool:
        """retourne true si p appartient à self à +-delta près"""
        return abs(p.y - self.a * p.x - self.b) <= delta

    def get_vecteur(self) -> Vecteur:
        return Vecteur(1, self.a)

    def hauteur(self, p: Point) -> ['Segment', None]:
        """retourne la hauteur à une doite sous la forme d'un segment si p n'appartient pas à self
        et None dans le cas contraire"""
        if self.appartient(p) is False:
            d: Droite = self.perpendiculaire(p)
            pi: Point = self.intersection(d)
            return Segment(pi, p)
        return None


class Segment(Droite):
    def __init__(self, p1: Point, p2: Point):
        super().__init__(p1, p2)
        self.p1 = p1
        self.p2 = p2

    def intersection(self, seg: 'Segment') -> Union[Point, None]:
        pi = super().intersection(seg)
        if pi is not None and (self.p1.x <= pi.x <= self.p2.x or self.p1.x >= pi.x >= self.p2.x):
            return pi
        return None

    def longueur(self):
        return self.p1.distance(self.p2)

    def __str__(self):
        return f"{super().__str__()} {self.p1} {self.p2}"

def main():
    print("debut")
    a = Point(0, 0, "A")
    b = Point(4, 1, "B")
    c = Point(-1, 4, "C")
    ca = Vecteur(c, a, "CA")
    cb = Vecteur(c, b, "CB")
    print(ca, cb)
    print("CA.CB =", ca * cb)
    print("cos(teta) = ", (ca * cb) / (ca.norme() * cb.norme()))
    print(cb.norme())
    s1 = Segment(Point(0, 0), Point(4, 0))
    s2 = Segment(Point(-1, 3), Point(3, 0))
    print(s1.intersection(s2))
    d = Droite(a,b)
    print(d.perpendiculaire(c))
    print(d.hauteur(c).longueur())


if __name__ == '__main__':
    main()
