#!/usr/bin/python
# .+
#
# .context    : Algebra
# .title      : Quaternion Algebra
# .kind	      : python source
# .author     : Marco Abrate
# .site	      : Torino - Italy
# .creation   :	10-Mar-2012
# .copyright  :	(c) 2011 Marco Abrate
# .license    : GNU General Public License
#
# qmath is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# qmath is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with qmath. If not, see <http://www.gnu.org/licenses/>.
#
# .-


# import required modules

import math, cmath
import numpy as np
import scipy

## module information
## qmath - a Python module to manipulate quaternions

__author__ = 'Marco Abrate <abrate.m@gmail.com>'
__license__ = '>= GPL v3'
__version__ = '0.3.0'


class AlgebraicError(Exception):
  "Algebraic error exception"
  def __init__(self, value):
    self.value = value

  def __str__(self):
    return repr(self.value)

class quaternion:
    "Quaternion algebra"
    
    def __init__(self, q, vector = None, matrix = np.identity(3)):
        """
        Initializes the quaternion.
        The following types can be converted to quaternion:
        - Numbers (real or complex);
        - lists or numpy arrays of the components with respect to 1,i,j and k; 
        - strings of the form 'a+bi+cj+dk';
        - pairs (rotation angle, axis of rotation);
        - lists whose components are Euler angles;
        - 3X3 orthogonal matrices representing rotations

        >>> import qmathcore
        >>> qmathcore.quaternion([1,2,3,4])
        (1.0+2.0i+3.0j+4.0k)
        >>> qmathcore.quaternion(np.array([1,2,3,4]))
        (1.0+2.0i+3.0j+4.0k)
        >>> qmathcore.quaternion(1)
        (1.0)
        >>> qmathcore.quaternion(1+1j)
        (1.0+1.0i)
        >>> qmathcore.quaternion('1+1i+3j-2k')
        (1.0+1.0i+3.0j-2.0k)
        >>> q = qmathcore.quaternion('2j')
        >>> q.__class__ == quaternion
        True
        """
        self.matrix = matrix
        if q.__class__ == quaternion:
            self.q = q.q

        elif q.__class__ == hurwitz:
            self.q = np.array([0.,0.,0.,0.])
            for i in range(4):
                self.q[i] = 1.0 * q[i]

        elif type(q) == type(np.array([])) and q.shape == (3, 3):
            self.euler = MatrixToEuler(q)
            self.q = EulerToQuaternion(self.euler)
            
        elif type(q) == list or type(q) == type(np.array([])):
            if len(q) == 4:
                self.q = 1.0 * np.array(q)
            elif len(q) == 3:
                self.q = EulerToQuaternion(q)
                
            else:
                pass
            
        elif (type(q) == int or type(q) == float or type(q) == type(1.0 * np.array([1])[0])) and vector == None:
            self.q = 1.0 * np.array([q,0.,0.,0.])
            
        elif type(q) == complex:
            self.q = 1.0 * np.array([q.real,q.imag,0,0])
        
        elif type(q) == str:
            self.q = StringToQuaternion(q).q

        elif vector:
            try:
                self.q = RotationToQuaternion(q, vector)
            except:
                pass
    
        else:
            pass
          
        if matrix.shape == (3,3) and abs(matrix - matrix.transpose()).sum() == 0:

            if (matrix - np.identity(3)).__abs__().sum() == 0:
                self.prod_tensor = np.array([[[1, 0, 0, 0],
                                              [0,-1, 0, 0],
                                              [0, 0,-1, 0],
                                              [0, 0, 0,-1]],
                                             [[0, 1, 0, 0],
                                              [1, 0, 0, 0],
                                              [0, 0, 0, 1],
                                              [0, 0,-1, 0]],
                                             [[0, 0, 1, 0],
                                              [0, 0, 0,-1],
                                              [1, 0, 0, 0],
                                              [0, 1, 0, 0]],
                                             [[0, 0, 0, 1],
                                              [0, 0, 1, 0],
                                              [0,-1, 0, 0],
                                              [1, 0, 0, 0]]])
            else:
                self.prod_tensor = np.array([[[1, 0, 0, 0],
                                              [0,-(matrix[1,1]*matrix[2,2]-matrix[1,2]*matrix[2,1]), (matrix[1,0]*matrix[2,2]-matrix[1,2]*matrix[2,0]),-(matrix[1,0]*matrix[2,1]-matrix[1,1]*matrix[2,0])],
                                              [0, (matrix[1,0]*matrix[2,2]-matrix[1,2]*matrix[2,0]),-(matrix[0,0]*matrix[2,2]-matrix[0,2]*matrix[2,0]), (matrix[0,0]*matrix[2,1]-matrix[0,1]*matrix[2,0])],
                                              [0,-(matrix[1,0]*matrix[2,1]-matrix[1,1]*matrix[2,0]), (matrix[0,0]*matrix[2,1]-matrix[0,1]*matrix[2,0]),-(matrix[0,0]*matrix[1,1]-matrix[0,1]*matrix[1,0])]],
                                             [[0, 1, 0, 0],
                                              [1, 0, matrix[0,2],-matrix[0,1]],
                                              [0,-matrix[0,2], 0, matrix[0,0]],
                                              [0,matrix[0,1],-matrix[0,0], 0]],
                                             [[0, 0, 1, 0],
                                              [0, 0, matrix[1,2],-matrix[1,1]],
                                              [1, -matrix[1,2], 0, matrix[0,1]],
                                              [0, matrix[1,1], -matrix[0,1], 0]],
                                             [[0, 0, 0, 1],
                                              [0, 0, matrix[2,2], -matrix[1,2]],
                                              [0,-matrix[2,2], 0, matrix[0,2]],
                                              [1, matrix[1,2], -matrix[0,2], 0]]])
        else:
            raise AlgebraicError('matrix must be symmetric 3X3')
        return

    
    def __repr__(self):
        "Algebraic representation of a quaternion"
        
        try:
            self.string = ''
            self.basis = ['','i','j','k']
            if self.norm() != 0:
                for self.count in range(4):
                    if self.q[self.count] > 0:
                        self.string = self.string + '+' + str(abs(self.q[self.count])) + self.basis[self.count]
                    elif self.q[self.count] < 0:
                        self.string = self.string + '-' + str(abs(self.q[self.count])) + self.basis[self.count]
            else:
                if self.__class__ == quaternion:
                    self.string = str(0.0)
                elif self.__class__ == hurwitz:
                    self.string = str(0)

            if self.string[0] == '+':
                self.string = self.string[1:]
            return '(' + self.string + ')'
        except:
            raise RuntimeError('can not convert to quaternion')

    def _int_(self):
        """
        >>> import qmathcore
        >>> q = qmathcore.quaternion([1,2,0,0])
        >>> q
        (1.0+2.0i)
        >>> q._int_()
        (1+2i)
        """
        self.value = np.array([0,0,0,0])
        for ind in range(4):
            if int(self[ind]) == self[ind]:
                self.value[ind] = int(self[ind])
            else:
                raise RuntimeError('components are not integers')
        self.q = self.value
        return self

            
    def __getitem__(self, key):
        """
        >>> import qmathcore
        >>> a = qmathcore.quaternion('1+2i-2k')
        >>> a[1]
        2.0
        >>> import qmathcore
        >>> b = qmathcore.hurwitz([1,2,3,4])
        >>> b[1]
        2
        """
        return self.q[key]
        
    def __setitem__(self,key,value):
        """
        >>> import qmathcore
        >>> a = qmathcore.quaternion('1+2i-2k')
        >>> a[1] = 7
        >>> a
        (1.0+7.0i-2.0k)
        >>> import qmathcore
        >>> b = qmathcore.hurwitz([1,2,3,4])
        >>> b[1] = 5
        >>> b
        (1+5i+3j+4k)
        """
        self.q[key] = value
        return self
        

    def __delitem__(self,key):
        """
        >>> import qmathcore
        >>> q = qmathcore.quaternion([1,2,3,4])
        >>> del q[1]
        >>> q
        (1.0+3.0j+4.0k)
        >>> b = qmathcore.hurwitz([1,2,3,4])
        >>> del b[1]
        >>> b
        (1+3j+4k)
        """
        if 0 <= key <= 3:
            self[key] = 0
            return self
        else:
            raise RuntimeError('list index out of range')

    def __delslice__(self, n, m):
        """
        >>> import qmathcore
        >>> q = qmathcore.quaternion([1,2,3,4])
        >>> del q[1:3]
        >>> q
        (1.0)
        >>> b = qmathcore.hurwitz([1,2,3,4])
        >>> del b[1:3]
        >>> b
        (1)
        """
        if n >= 0 and m <=3:
            if n <= m:
                for self.count in range(n,m + 1):
                    del self[self.count]
            else:
                for self.count in range(m,n + 1):
                    del self[self.count]
        else:
            raise RuntimeError('quaternion index out of range')

    def __contains__(self, item):
        """
        >>> import qmathcore
        >>> q = qmathcore.quaternion('1+1i+5k')
        >>> 'j' in q
        False
        >>> 'i' in q
        True
        >>> b = qmathcore.hurwitz([1,2,3,4])
        >>> 'i' in b
        True
        """
        
        if item == 'i':
            return self.q[1] != 0
        elif item == 'j':
            return self.q[2] != 0
        elif item == 'k':
            return self.q[3] != 0
        else:
            return False

    def __or__(self,other):
        """
        >>> import qmathcore
        >>> qmathcore.quaternion(1)|3
        ((1.0), 3)
        >>> qmathcore.hurwitz('2j')|3
        ((2j), 3)
        """
        return (self, other)

    def __lt__(self, other):
        """
        >>> import qmathcore
        >>> a = qmathcore.quaternion('1i')
        >>> a < 0
        Traceback (most recent call last):
        TypeError: no ordering relation is defined for quaternion numbers
        """
        raise RuntimeError('no ordering relation is defined for quaternion numbers')

    def __le__(self, other):
        """
        >>> import qmathcore
        >>> a = qmathcore.quaternion('1i')
        >>> a <= 0
        Traceback (most recent call last):
        TypeError: no ordering relation is defined for quaternion numbers
        """
        raise RuntimeError('no ordering relation is defined for quaternion numbers')
    
    def __eq__(self, other):
        """
        >>> import qmathcore
        >>> q = qmathcore.quaternion('1+1k')
        >>> q == 0
        False
        >>> q == '1+1k'
        True
        >>> q == qmathcore.quaternion([1,0,1e-15,1])|1e-9
        True
        >>> q == [1,1,1e-15,0]
        False
        >>> q = qmathcore.hurwitz('1+1k')
        >>> q == '1+1k'
        True
        """
        if type(other) == tuple:
            try:
                return self.equal(other[0],other[1])
            except:
                raise RuntimeError(str(self) + ' and ' + str(other[0]) + ' can not be compared')
        else:
            return self.equal(other)
    
    def __ne__(self, other):
        """
        >>> import qmathcore
        >>> q = qmathcore.quaternion('1+1k')
        >>> q != 0
        True
        >>> q != '1+1k'
        False
        """
        return not self == other

    def __gt__(self, other):
        """
        >>> import qmathcore
        >>> a = qmathcore.quaternion('1i')
        >>> a > 0
        Traceback (most recent call last):
        TypeError: no ordering relation is defined for quaternion numbers
        """
        raise RuntimeError('no ordering relation is defined for quaternion numbers')
    
    def __ge__(self, other):
        """
        >>> import qmathcore
        >>> a = qmathcore.quaternion('1i')
        >>> a >= 0
        Traceback (most recent call last):
        TypeError: no ordering relation is defined for quaternion numbers
        """
        raise RuntimeError('no ordering relation is defined for quaternion numbers')

    def __iadd__(self, other):
        """
        >>> import qmathcore
        >>> q = qmathcore.quaternion([1,2,0,3])
        >>> q += qmathcore.quaternion([2,1,3,0])
        >>> q
        (3.0+3.0i+3.0j+3.0k)
        >>> q = qmathcore.hurwitz([1,2,0,3])
        >>> q += qmathcore.hurwitz([2,1,3,0])
        >>> q
        (3+3i+3j+3k)
        """
        self.other = quaternion(other)
        return self.__class__(self.q + self.other.q)
        
    def __isub__(self, other):
        """
        >>> import qmathcore
        >>> q = qmathcore.quaternion([1,2,0,3])
        >>> q -= qmathcore.quaternion([2,1,3,0])
        >>> q
        (-1.0+1.0i-3.0j+3.0k)
        >>> q = qmathcore.hurwitz([1,2,0,3])
        >>> q -= qmathcore.hurwitz([2,1,3,0])
        >>> q
        (-1+1i-3j+3k)
        """
        self.other = quaternion(other)
        self += - self.other
        return self

    def __imul__(self, other):
        """
        >>> import qmathcore
        >>> a = qmathcore.quaternion([1,2,3,4])
        >>> b = qmathcore.quaternion(3-4j)
        >>> a *= b
        >>> a
        (11.0+2.0i-7.0j+24.0k)
        >>> a = qmathcore.hurwitz([1,2,3,4])
        >>> b = qmathcore.hurwitz(3-4j)
        >>> a *= b
        >>> a
        (11+2i-7j+24k)
        >>> a = qmathcore.quaternion([0,0,0,1], matrix = np.array([[-1,0,0],[0,1,0],[0,0,-1]]))
        >>> b = qmathcore.quaternion([0,0,0,1], matrix = np.array([[-1,0,0],[0,1,0],[0,0,-1]]))
        >>> a *= b
        >>> a
        (1.0)
        >>> a = qmathcore.quaternion([0,-1,0,-1], matrix = np.array([[-1,0,0],[0,1,0],[0,0,-1]]))
        >>> b = qmathcore.quaternion([0,0,2,0], matrix = np.array([[-1,0,0],[0,1,0],[0,0,-1]]))
        >>> a *= b
        >>> a
        (-2.0i+2.0k)
        """
        self.p = quaternion(other)
        try:
            self.vect = np.dot(np.dot(np.array([self.q[0],self.q[1],self.q[2],self.q[3]]),self.prod_tensor),np.array([self.p.q[0],self.p.q[1],self.p.q[2],self.p.q[3]]))
            return self.__class__(self.vect, matrix = self.matrix)
            
        except:
            return self.__class__(other,matrix=self.matrix)

    def __itruediv__(self, other):
        """
        Right multiplication by the inverse of p, if p is invertible

        >>> import qmathcore
        >>> a = qmathcore.quaternion([1,2,3,4])
        >>> b = qmathcore.quaternion(3-4j)
        >>> a /= b
        >>> a
        (-0.2+0.4i+1.0j)
        >>> a /= qmathcore.quaternion(0)
        Traceback (most recent call last):
        AlgebraicError: '(0.0) is not invertible'
        >>> a = qmathcore.hurwitz([1,2,3,4])
        >>> b = qmathcore.hurwitz(3-4j)
        >>> a /= b
        Traceback (most recent call last):
        AlgebraicError: '(3-4i) is not invertible as Hurwitz quaternion'
        """
        if self.__class__ == hurwitz:
            self.p = hurwitz(other)
            try:
                return self * self.p.inverse()
            except:
                raise RuntimeError(str(hurwitz(other)) + ' is not invertible as Hurwitz quaternion')

        else:
            self.p = quaternion(other)
            try:
                return self * self.p.inverse()
            except:
                raise RuntimeError(str(quaternion(other)) + ' is not invertible')

    def __imod__(self, other):
        """
        module reduction, if self is a hurwitz quaternion

        >>> import qmathcore
        >>> a = qmathcore.hurwitz([10,23,3,4])
        >>> a %= 3
        >>> a
        (1+2i+1k)
        >>> a = qmathcore.quaternion([10,23,3,4])
        >>> a %= 3
        Traceback (most recent call last):
        AlgebraicError: '(10.0+23.0i+3.0j+4.0k) is not a Hurwitz quaternion'
        """
        if type(other) == int:
            if self.__class__ == hurwitz:
                for self.count in range(4):
                    self[self.count] = self[self.count] % other
                return self
            else:
                raise RuntimeError(str(self) + ' is not a Hurwitz quaternion')
        else:
            raise RuntimeError(str(other) + ' is not integer')

    def __add__(self, other):
        "Quaternion addiction"
        """
        >>> import qmathcore
        >>> qmathcore.quaternion([1,2,0,3]) + qmathcore.quaternion([2,1,3,0])
        (3.0+3.0i+3.0j+3.0k)
        >>> qmathcore.hurwitz([1,2,0,3]) + qmathcore.hurwitz([2,1,3,0])
        (3+3i+3j+3k)
        """
        self += other
        return self


    def __sub__(self,other):
        "Quaternion subtraction"
        """
        >>> import qmathcore
        >>> qmathcore.quaternion([1,2,0,3]) - qmathcore.quaternion([2,1,3,0])
        (-1.0+1.0i-3.0j+3.0k)
        >>> qmathcore.hurwitz([1,2,0,3]) - qmathcore.hurwitz([2,1,3,0])
        (-1+1i-3j+3k)
        """
        self -= other
        return self

    def __mul__(self, other):
        """
        Quaternion right multiplication by p:
        i**2 = j**2 = k**2 = -1, i*j = k

        >>> import qmathcore
        >>> a = qmathcore.quaternion([1,2,3,4])
        >>> b = qmathcore.quaternion(3-4j)
        >>> a * b
        (11.0+2.0i-7.0j+24.0k)
        >>> a = qmathcore.hurwitz([1,2,3,4])
        >>> b = qmathcore.hurwitz(3-4j)
        >>> a * b
        (11+2i-7j+24k)
        >>> a = qmathcore.quaternion([0,0,0,1], matrix = np.array([[-1,0,0],[0,1,0],[0,0,-1]]))
        >>> b = qmathcore.quaternion([0,0,0,1], matrix = np.array([[-1,0,0],[0,1,0],[0,0,-1]]))
        >>> a * b
        (1.0)
        >>> a = qmathcore.quaternion([0,-1,0,-1], matrix = np.array([[-1,0,0],[0,1,0],[0,0,-1]]))
        >>> b = qmathcore.quaternion([0,0,2,0], matrix = np.array([[-1,0,0],[0,1,0],[0,0,-1]]))
        >>> a * b
        (-2.0i+2.0k)
        """
        self *= other
        return self
    
    def __truediv__(self, other):
        """
        Right multiplication by the inverse of p, if p is invertible

        >>> import qmathcore
        >>> a = qmathcore.quaternion([1,2,3,4])
        >>> b = qmathcore.quaternion(3-4j)
        >>> a / b
        (-0.2+0.4i+1.0j)
        >>> a / qmathcore.quaternion(0)
        Traceback (most recent call last):
        AlgebraicError: '(0.0) is not invertible'
        >>> a = qmathcore.hurwitz([1,2,3,4])
        >>> b = qmathcore.hurwitz(3-4j)
        >>> a / b
        Traceback (most recent call last):
        AlgebraicError: '(3-4i) is not invertible as Hurwitz quaternion'
        """
        self /= other
        return self 

    def __mod__(self, other):
        """
        >>> import qmathcore
        >>> a = qmathcore.hurwitz([10,23,3,4])
        >>> a % 3
        (1+2i+1k)
        >>> a = qmathcore.quaternion([10,23,3,4])
        >>> a % 3
        Traceback (most recent call last):
        AlgebraicError: '(10.0+23.0i+3.0j+4.0k) is not a Hurwitz quaternion'
        """
        self %= other
        return self
        
    def __rmul__(self, other):
        """
        Quaternion left multiplication by p.

        >>> import qmathcore
        >>> a = qmathcore.quaternion([1,2,3,4])
        >>> b = qmathcore.quaternion(3-4j)
        >>> a.__rmul__(b)
        (11.0+2.0i+25.0j)
        >>> 3 * a
        (3.0+6.0i+9.0j+12.0k)
        >>> a = qmathcore.hurwitz([1,2,3,4])
        >>> 3 * a
        (3+6i+9j+12k)
        """
        return self.__class__(other) * self

    def __rtruediv__(self, other):
        """
        Left multiplication by the inverse of p, if p is invertible
        >>> import qmathcore
        >>> a = qmathcore.quaternion([1,2,3,4])
        >>> b = qmathcore.quaternion(3-4j)
        >>> a.__rtruediv__(b)
        (-0.2+0.4i-0.28j+0.96k)
        """
        return self.__class__(other).inverse() * self
        
    def __neg__(self):
        """
        >>> import qmathcore
        >>> a = qmathcore.quaternion([1,2,3,4])
        >>> -a
        (-1.0-2.0i-3.0j-4.0k)
        >>> a = qmathcore.hurwitz([1,2,3,4])
        >>> -a
        (-1-2i-3j-4k)
        """
        return self.__class__(-1 * self)
    
    def __pow__(self,exponent, modulo = None):
        """
        Returns the integer power of a quaternion.
        If the basis is invertible exponent can be negative.
        Modular reduction is performed for Hurwitz quaternions
        (if self is a Hamilton quaternion, modulo is ignored)

        >>> import qmathcore
        >>> base = qmathcore.quaternion('1+1i+2j-2k')
        >>> base ** 3.0
        (-26.0-6.0i-12.0j+12.0k)
        >>> base ** (-2)
        (-0.08-0.02i-0.04j+0.04k)
        >>> qmathcore.quaternion([-5,1,0,1]) ** (1.0/3)
        (1.0+1.0i+1.0k)
        >>> qmathcore.quaternion([-5,1,0,1]) ** (2.0/3)
        (-1.0+2.0i+2.0k)
        >>> qmathcore.quaternion('1.0+1.0i+1.0k') ** 2
        (-1.0+2.0i+2.0k)
        >>> qmathcore.hurwitz('1+1i+1k') ** 2
        (-1+2i+2k)
        >>> pow(qmathcore.hurwitz('1+1i+1k'),2,3)
        (2+2i+2k)
        >>> a = qmathcore.quaternion([0,-1,0,-1], matrix = np.array([[-1,0,0],[0,1,0],[0,0,-1]]))
        >>> a ** 3
        (2.0i+2.0k)
        >>> a ** 4
        (4.0)
        """
        if self.__class__ == quaternion:
            if int(exponent) == exponent:
                self.e = int(exponent)
                if self.e > 0:
                    self.u = quaternion(self.q)
                    self.pow = quaternion(1)
                    while self.e > 0:
                        if self.e % 2 == 1:
                            self.pow = self.pow * self.u
                        self.u = self.u * self.u
                        self.e = self.e / 2
                    return self.pow
                elif self.e == 0:
                    self.pow = quaternion(1)
                    return self.pow
                else:
                    try:
                        self.pow = self.inverse() ** (-exponent)
                        return self.pow
                    except:
                        raise RuntimeError(str(self) + ' is not invertible')

            elif math.floor(2 * exponent) == 2 * exponent:
                return self ** int(math.floor(exponent)) * self.sqrt()

            elif math.floor(3 * exponent) == 3 * exponent:
                if int(math.floor(3 * exponent)) % 3 == 1:
                    return self ** int(math.floor(exponent)) * self.croot()
                elif int(math.floor(3 * exponent)) % 3 == 2:
                    return self ** int(math.floor(exponent)) * (self.croot()) ** 2
                          
            else:
                raise RuntimeError('a quaternion power can be computed only for integer powers or half of an integer')
        else:
            if int(exponent) == exponent and exponent >= 0:
                if modulo:
                    return hurwitz(quaternion(self) ** exponent) % modulo

                else:
                    return hurwitz(quaternion(self) ** exponent)
            else:
                raise RuntimeError('a quaternion power can be computed only for integer powers for hurwitz quaternions')

    def __abs__(self):
        """
        Returns the modulus of the quaternion
        >>> import qmathcore
        >>> a = qmathcore.quaternion([0,0,-3,4])
        >>> abs(a)
        5.0
        >>> a = qmathcore.hurwitz([0,0,-3,4])
        >>> abs(a)
        5.0
        """
        
        self.abs = math.sqrt(self.norm())
        return self.abs

    def equal(self, other, tolerance = 0):
        """
        Quarternion equality with arbitrary tolerance
        >>> import qmathcore
        >>> a = qmathcore.quaternion([1,1,1e-15,0])
        >>> b = qmathcore.quaternion(1+1j)
        >>> a.equal(b,1e-9)
        True
        >>> a.equal(b)
        False
        """
        for self.count in range(4):
            if abs(self.q[self.count] - quaternion(other).q[self.count]) <= tolerance:
                pass
            else:
                return False
        return True

           
    def value(self):
        try:
            return self.q
        except:
            raise RuntimeError(str(self.__class__(q)) + ' is not a quaternion')

    def real(self):
        """
        Returns the real part of the quaternion
        >>> import qmathcore
        >>> a = qmathcore.quaternion([1,2,3,4])
        >>> a.real()
        (1.0)
        >>> a = qmathcore.hurwitz([1,2,3,4])
        >>> a.real()
        (1)
        """
        return self.__class__(dot(self,[1,0,0,0]))

    def imag(self):
        """
        Returns the imaginary part of the quaternion
        >>> import qmathcore
        >>> a = qmathcore.quaternion([1,2,3,4])
        >>> a.imag()
        (2.0i+3.0j+4.0k)
        >>> a = qmathcore.hurwitz([1,2,3,4])
        >>> a.imag()
        (2i+3j+4k)
        """
        return self - self.real()      

    def trace(self):
        """
        Returns the trace of the quaternion
        >>> import qmathcore
        >>> a = qmathcore.quaternion([1,2,3,4])
        >>> a.trace()
        2.0
        >>> a = qmathcore.hurwitz([1,2,3,4])
        >>> a.trace()
        2
        """
        return 2 * self.q[0]
        
    def conj(self):
        """
        Returns the conjugate of the quaternion
        >>> import qmathcore
        >>> a = qmathcore.quaternion([1,2,3,4])
        >>> a.conj()
        (1.0-2.0i-3.0j-4.0k)
        >>> a = qmathcore.hurwitz([1,2,3,4])
        >>> a.conj()
        (1-2i-3j-4k)
        """
        return self.real() - self.imag()

    def norm(self):
        """
        Returns the norm of the quaternion (the square of the modulus)
        >>> import qmathcore
        >>> a = qmathcore.quaternion([1,2,3,4])
        >>> a.norm()
        30.0
        >>> a = qmathcore.hurwitz([1,2,3,4])
        >>> a.norm()
        30
        """
        return np.dot(np.dot(np.array([self.q[0],self.q[1],self.q[2],self.q[3]]),self.prod_tensor[0]),np.array([self.q[0],-self.q[1],-self.q[2],-self.q[3]]))

    def delta(self):
        """
        >>> import qmathcore
        >>> a = qmathcore.quaternion([1,2,3,4])
        >>> a.delta()
        -29.0
        >>> a = qmathcore.hurwitz([1,2,3,4])
        >>> a.delta()
        -29
        """
        return self.q[0] ** 2 - self.norm()
        

    def inverse(self,modulo = None):
        """
        Quaternionic inverse, if it exists
        Modular inversion is performed for Hurwitz quaternions
        (if self is a Hamilton quaternion, modulo is ignored).
        There is no control on the primality of modulo.
        >>> import qmathcore
        >>> a = qmathcore.quaternion([2,-2,-4,-1])
        >>> a.inverse()
        (0.08+0.08i+0.16j+0.04k)
        >>> b = qmathcore.hurwitz([0,-2,-2,0])
        >>> b.inverse(13)
        (10i+10j)
        >>> zero = qmathcore.quaternion(0)
        >>> zero.inverse()
        Traceback (most recent call last):
        AlgebraicError: '(0.0) is not invertible'
        >>> a = qmathcore.hurwitz('1+1j')
        >>> a.inverse()
        Traceback (most recent call last):
        TypeError: components are not integers
        """
        if self == 0:
            raise RuntimeError(str(self) + ' is not invertible')
        elif modulo and self.__class__ == hurwitz:
            return (self.conj() * pow(int(self.norm()), modulo - 2, modulo)) % modulo

        else:
            return self.__class__(self.conj() * (1 / float(self.norm())))
            
    def unitary(self):
        """
        Returns the normalized quaternion.
        >>> import qmathcore
        >>> a = qmathcore.quaternion('1+1i+1j-1k')
        >>> a.unitary()
        (0.5+0.5i+0.5j-0.5k)
        >>> zero = qmathcore.quaternion(0)
        >>> zero.unitary()
        Traceback (most recent call last):
        AlgebraicError: '(0.0) has no direction'
        >>> a = qmathcore.hurwitz('1+1j')
        >>> a.unitary()
        Traceback (most recent call last):
        TypeError: components are not integers
        """
        if self != 0:
            return self / abs(self)
        else:
            raise RuntimeError(str(self.__class__(self)) + ' has no direction')

    def sqrt(self):
        """
        Computes the square root of a quaternion.
        If q has only two roots, the one with positive trace is given.
        If this method returns r, also -r is a root.
        >>> import qmathcore
        >>> qmathcore.quaternion([3,5,0,-4]).sqrt()
        (2.24399953341+1.11408222808i-0.891265782468k)
        """
        self.nu = math.sqrt(self.norm())
        self.tau = math.sqrt(2 * self.nu + self.trace())
        if self.tau != 0:
            self.solution = (self.q + np.array([self.nu,0,0,0])) / self.tau
            return self.__class__(self.solution)
        else:
            return str(self) + ' has infinitely many square roots:\n every (a i+b j+c k) such that\n a ** 2 + b ** 2 + c ** 2 = ' + str(self.nu)

    def croot(self):
        """
        Computes the cube root of a quaternion.
        >>> import qmathcore
        >>> qmathcore.quaternion([-5,1,0,1]).croot()
        (1.0+1.0i+1.0k)
        """
        self.nu = math.pow(self.norm(), 1.0/3)
        self.tau = (self.q[0] + cmath.sqrt(self.delta())).__pow__(1.0/3) + (self.q[0] - cmath.sqrt(self.delta())).__pow__(1.0/3)
        if self.tau ** 2 - self.nu != 0:
            self.solution = (self.q + np.array([self.nu * self.tau,0,0,0])) / (self.tau ** 2 - self.nu)
            return self.__class__(self.solution)
        else:
            return str(self) + ' has infinitely many cubic roots'

    def QuaternionToRotation(self):
        """
        Converts the quaternion, if unitary, into a rotation matrix
        >>> import qmathcore
        >>> q = qmathcore.quaternion(3-4j)
        >>> q.QuaternionToRotation()
        Traceback (most recent call last):
        AlgebraicError: 'the quaternion must be unitary'
        >>> M = q.unitary().QuaternionToRotation()
        >>> M
        array([[ 1.  , -0.  ,  0.  ],
               [ 0.  , -0.28,  0.96],
               [-0.  , -0.96, -0.28]])
        >>> qmathcore.quaternion(M).equal(q.unitary(),1e-12)
        True
        """
        if quaternion(self.norm()) == quaternion(1.0)|1e-9:
            return np.array([[self.q[0] ** 2 + self.q[1] ** 2 - self.q[2] ** 2 - self.q[3] ** 2, 2 * (self.q[1] * self.q[2] - self.q[0] * self.q[3]), 2 * (self.q[0] * self.q[2] + self.q[1] * self.q[3]) ],
                             [2 * (self.q[1] * self.q[2] + self.q[0] * self.q[3]), self.q[0] ** 2 - self.q[1] ** 2 + self.q[2] ** 2 - self.q[3] ** 2, 2 * (self.q[3] * self.q[2] - self.q[0] * self.q[1])],
                             [2 * (self.q[1] * self.q[3] - self.q[0] * self.q[2]), 2 * (self.q[1] * self.q[0] + self.q[2] * self.q[3]), self.q[0] ** 2 - self.q[1] ** 2 - self.q[2] ** 2 + self.q[3] ** 2]]) / self.__abs__()
        else:
            raise RuntimeError('the quaternion must be unitary')


class hurwitz(quaternion):
    "Quaternion algebra over integers"
    
    def __init__(self, att, matrix=np.identity(3)):
        """
        Initializes the quaternion.
        The following types can be converted to quaternion:
        - integers;
        - lists or numpy arrays of the (integers) components with respect to 1,i,j and k; 
        - strings of the form 'a+bi+cj+dk';

        >>> import qmathcore
        >>> qmathcore.hurwitz([1,2,3,4])
        (1+2i+3j+4k)
        >>> qmathcore.hurwitz(np.array([1,2,3,4]))
        (1+2i+3j+4k)
        >>> qmathcore.hurwitz(1)
        (1)
        >>> qmathcore.hurwitz(1+1j)
        (1+1i)
        >>> qmathcore.hurwitz('1+1i+3j-2k')
        (1+1i+3j-2k)
        >>> q = qmathcore.hurwitz('2j')
        >>> qmathcore.quaternion(q)
        (2.0j)
        """
        self.matrix = matrix
        self.q = quaternion(att, matrix = matrix)._int_()
        self.prod_tensor = self.q.prod_tensor


        
def real(quat):
    """
    >>> import qmathcore
    >>> qmathcore.real(1+3j)
    (1.0)
    >>> qmathcore.real(qmathcore.hurwitz('1+3j-2k'))
    (1)
    """
    if quat.__class__ == hurwitz:
        return quat.real()
    else:
        q = quaternion(quat)
        return q.real()

def imag(quat):
    """
    >>> import qmathcore
    >>> qmathcore.imag([1,2,3,4])
    (2.0i+3.0j+4.0k)
    >>> qmathcore.imag(qmathcore.hurwitz('1+3j-2k'))
    (3j-2k)
    """
    if quat.__class__ == hurwitz:
        return quat.imag()
    else:
        q = quaternion(quat)
        return q.imag()      

def trace(quat):
    """
    >>> import qmathcore
    >>> qmathcore.trace([1,2,3,4])
    2.0
    >>> qmathcore.trace(qmathcore.hurwitz('1+3j-2k'))
    2
    """
    if quat.__class__ == hurwitz:
        return quat.trace()
    else:
        q = quaternion(quat)
        return q.trace()
        
def conj(quat):
    """
    >>> import qmathcore
    >>> qmathcore.conj([1,2,3,4])
    (1.0-2.0i-3.0j-4.0k)
    >>> qmathcore.conj(qmathcore.hurwitz('1+3j-2k'))
    (1-3j+2k)
    """
    if quat.__class__ == hurwitz:
        return quat.conj()
    else:
        q = quaternion(quat)
        return q.conj()

def norm(quat):
    """
    >>> import qmathcore
    >>> qmathcore.norm([1,2,3,4])
    30.0
    >>> qmathcore.norm(qmathcore.hurwitz('1+3j-2k'))
    14
    """
    if quat.__class__ == hurwitz:
        return quat.norm()
    else:
        q = quaternion(quat)
        return q.norm()

def delta(quat):
    """
    >>> import qmathcore
    >>> qmathcore.delta([1,2,3,4])
    -29.0
    """
    if quat.__class__ == hurwitz:
        return quat.delta()
    else:
        q = quaternion(quat)
        return q.delta()

def inverse(quat,modulo = None):
    """
    >>> import qmathcore
    >>> qmathcore.inverse([2,-2,-4,-1])
    (0.08+0.08i+0.16j+0.04k)
    """
    if quat.__class__ == hurwitz:
        return quat.inverse(modulo)
    else:
        q = quaternion(quat)
        return q.inverse(modulo)
            
def unitary(quat):
    """
    >>> import qmathcore
    >>> qmathcore.unitary('1+1i+1j-1k')
    (0.5+0.5i+0.5j-0.5k)
    """ 
    if quat.__class__ == hurwitz:
        return quat.unitary()
    else:
        q = quaternion(quat)
        return q.unitary()

def sqrt(quat):
    """
    >>> import qmathcore
    >>> qmathcore.sqrt([3,5,0,-4])
    (2.24399953341+1.11408222808i-0.891265782468k)
    """
    if quat.__class__ == hurwitz:
        return quat.sqrt()
    else:
        q = quaternion(quat)
        return q.sqrt()

def croot(quat):
    """
    >>> import qmathcore
    >>> qmathcore.croot([-5,1,0,1])
    (1.0+1.0i+1.0k)
    """
    if quat.__class__ == hurwitz:
        return quat.croot()
    else:
        q = quaternion(quat)
        return q.croot()

def StringToQuaternion(string):
    """
    Converts a string into a quaternion
    """
    if string[0] == '+' or string[0] == '-':
        a = string
    else:
        a = '+' + string           
    components = ['','','','']
    count = 0
    while max(a.rfind('-'),a.rfind('+')) != -1:
        components[count]=a[max(a.rfind('-'),a.rfind('+')):]
        a = a[:max(a.rfind('-'),a.rfind('+'))]
        count = count + 1
    q = np.array([0.,0.,0.,0.])
    try:
        for component in components:
            if len(component) > 0:
                if component[len(component) - 1] == 'k':
                    q[3] = float(component[:len(component) - 1])
                elif component[len(component) - 1] == 'j':
                    q[2] = float(component[:len(component) - 1])
                elif component[len(component) - 1] == 'i':
                    q[1] = float(component[:len(component) - 1])
                else:
                    q[0] = float(component[:len(component)])
        return quaternion(q)
    except:
        raise RuntimeError(string + ' can not be converted to quaternion')

def MatrixToEuler(matrix):
    """
    Converts a 3X3 matrix into a vector having Euler angles as components
    """
    if matrix.shape == (3, 3):
        try:
            theta = math.asin(- matrix[2][0])
            if math.cos(theta) != 0:
                try:
                    psi = math.atan2(matrix[2][1] / math.cos(theta), matrix[2][2] / math.cos(theta))
                except:
                    psi = math.atan(matrix[2][1])
                try:
                    phi = math.atan2(matrix[1][0] / math.cos(theta), matrix[0][0] / math.cos(theta))
                except:
                    phi = math.atan(matrix[1][0])
            else:
                phi = theta
                psi = math.arcsin(matrix[1][1])
            return [phi, theta, psi]
        except:
            raise Runtime('the matrix is not orthogonal')
                      
def EulerToQuaternion(angles):
    """
    Converts a vector whose components are Euler angles into a quaternion
    """
    if len(angles) == 3:
        return quaternion(np.array([math.cos(angles[0] / 2.) * math.cos(angles[1] / 2.) * math.cos(angles[2] / 2.) + math.sin(angles[0] / 2.) * math.sin(angles[1] / 2.) * math.sin(angles[2] / 2.),
                                    math.cos(angles[0] / 2.) * math.cos(angles[1] / 2.) * math.sin(angles[2] / 2.) - math.sin(angles[0] / 2.) * math.sin(angles[1] / 2.) * math.cos(angles[2] / 2.),
                                    math.cos(angles[0] / 2.) * math.sin(angles[1] / 2.) * math.cos(angles[2] / 2.) + math.sin(angles[0] / 2.) * math.cos(angles[1] / 2.) * math.sin(angles[2] / 2.),
                                    math.sin(angles[0] / 2.) * math.cos(angles[1] / 2.) * math.cos(angles[2] / 2.) - math.cos(angles[0] / 2.) * math.sin(angles[1] / 2.) * math.sin(angles[2] / 2.)]))
    else:
        raise RuntimeError(str(angles) + ' can not be converted to quaternion')
    
def RotationToQuaternion(angle, vector):
    """
    Converts a pair angle-vector into a quaternion
    """
    if len(vector) == 3:
        quat = np.array([math.cos(angle/2.0), vector[0]*(math.sin(angle/2.0)), vector[1]*(math.sin(angle/2.0)), vector[2]*(math.sin(angle/2.0))])
    else:
        raise RuntimeError('the pair ' + str(angle) + str(vector) + ' can not be converted to quaternion')
    return quaternion(quat)

def identity():
    """
    >>> import qmath
    >>> qmath.identity()
    (1.0)
    """
    return quaternion(1)

def zero():
    """
    >>> import qmath
    >>> qmath.zero()
    (0.0)
    """
    return quaternion(0)

def dot(q1,q2):
    """
    Dot product of two quaternions
    >>> import qmathcore
    >>> a = qmathcore.quaternion('1+2i-2k')
    >>> b = qmathcore.quaternion('3-2i+8j')
    >>> qmathcore.dot(a,b)
    -1.0
    """
    Q1 = quaternion(q1)
    Q2 = quaternion(q2)
    return np.dot(Q1.q,Q2.q)

def CrossRatio(q1,q2=None,q3=None,q4=None):
    """
    Cross ratio of four quaternions
    >>> import qmath
    >>> a = qmath.quaternion([1,0,1,0])
    >>> b = qmath.quaternion([0,1,0,1])
    >>> c = qmath.quaternion([-1,0,-1,0])
    >>> d = qmath.quaternion([0,-1,0,-1])
    >>> qmath.CrossRatio(a,b,c,d)
    (2.0)
    >>> tpl = a,b,c,d
    >>> qmath.CrossRatio(tpl)
    (2.0)
    >>> qmath.CrossRatio(a,b,b,d)
    'Infinity'
    >>> qmath.CrossRatio(a,a,a,d)
    (1.0)
    >>> qmath.CrossRatio(a,b,a,b)
    (0.0)
    """
    if type(q1) == tuple:
        return CrossRatio(q1[0],q1[1],q1[2],q1[3])

    else:
        Q1 = quaternion(q1)
        Q2 = quaternion(q2)
        Q3 = quaternion(q3)
        Q4 = quaternion(q4)
        if (Q1 - Q4) * (Q2 - Q3) != 0:
            return (Q1 - Q3) * (quaternion.inverse(Q1 - Q4))*(Q2 - Q4)*(quaternion.inverse(Q2 - Q3))
        elif (Q1 - Q3) * (Q2 - Q4) != 0:
            return 'Infinity'
        else:
            return identity()
            
def Moebius(quaternion_or_infinity, a,b=None,c=None,d=None):
    """
    The Moebius transformation of a quaternion (z)
    with parameters a,b,c and d
    >>> import qmath
    >>> a = qmath.quaternion([1,1,1,0])
    >>> b = qmath.quaternion([-2,1,0,1])
    >>> c = qmath.quaternion([1,0,0,0])
    >>> d = qmath.quaternion([0,-1,-3,-4])
    >>> z = qmath.quaternion([1,1,3,4])
    >>> qmath.Moebius(z,a,b,c,d)
    (-5.0+7.0i+7.0k)
    >>> d = - z
    >>> z = qmath.Moebius(z,a,b,c,d)
    >>> z
    'Infinity'
    >>> qmath.Moebius(z,a,b,c,d)
    (1.0+1.0i+1.0j)
    """
    if type(a) == tuple:
        return Moebius(quaternion_or_infinity,a[0],a[1],a[2],a[3])
    else:
        A = quaternion(a)
        B = quaternion(b)
        C = quaternion(c)
        D = quaternion(d)
        if A * D - B * C == 0:
            raise RuntimeError(' this is not a Moebius transformation')
        elif quaternion_or_infinity == 'Infinity':
            return A / C
        else:
            Z = quaternion(quaternion_or_infinity)
            try:
                return (A * Z + B) * quaternion.inverse(C * Z + D)
            except:
                return 'Infinity'
        
if __name__ == "__main__":
    print('*** running doctest ***')
    import doctest,qmathcore
    doctest.testmod(qmathcore)


#### END
