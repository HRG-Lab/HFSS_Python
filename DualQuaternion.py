import numpy as np
import qmathcore as qmath


class DualQuaternion(object):

    def __init__(self, r=[0,0,0,1], d=[0,0,0,0]):
        self.m_real = qmath.unitary(r)
        self.m_dual = d

    def dot( self, a, b ):
        return np.dot(a.m_real,b.m_real)

    def __mul__(self, other):
        ret = self
        ret.m_real *= other
        ret.m_dual *= other
        return ret

    def normalize(self):
        q = self
        mag = np.dot(q.m_real, q.m_real)
        q.m_real *= 1.0 / mag
        q.m_dual *= 1.0 / mag
        return q

    def __add__(self,other):
        q = self
        return DualQuaternion(q.m_real+other.m_real,q.m_dual+other.m_dual)

    """
    USE MULT FUNCTION FOR MULTIPLICATION OF DUAL QUATERNIONS
    """
    def mult(self, other):
        q = self
        return DualQuaternion(q.m_real*other.m_real,
                              q.m_dual*other.m_real + q.m_real*other.m_dual)

    def conjugate(self):
        q = self
        return DualQuaternion(qmath.conj(q.m_real),qmath.conj(q.m_dual))

    """
    getRotation RETURNS UNIT ROTATION QUATERNION
    """
    def getRotation(self):
        return self.m_real

    """
    getTranslation RETURNS TRANSLATION OF DUAL QUATERNION
    """
    def getTranslation(self):
        q = self
        t = (q.m_dual * 2.0) * qmath.conj(q.m_real)
        return t

    """
    dualQuat2Matrix RETURNS 4X4 MATRIX
    1ST 3 COLUMNS USED FOR ROTATION TRANSFORMATION
    LAST COLUMN USED FOR TRANSLATION ALONG ROTATION
    """
    def dualQuat2Matrix(self):
        q = self
        # q = DualQuaternion.normalize(q)

        M = np.identity(4)

        w = q.m_real[0]
        x = q.m_real[1]
        y = q.m_real[2]
        z = q.m_real[3]

        M[0][0] = w*w + x*x - y*y - z*z
        M[1][0] = 2*x*y + 2*w*z
        M[2][0] = 2*x*z - 2*w*y

        M[0][1] = 2*x*y - 2*w*z
        M[1][1] = w*w + y*y - x*x - z*z
        M[2][1] = 2*y*z + 2*w*x

        M[0][2] = 2*x*z + 2*w*y
        M[1][2] = 2*y*z - 2*w*x
        M[2][2] = w*w + z*z - x*x - y*y

        t = qmath.quaternion((q.m_dual*2.0))# * qmath.conj(q.m_real))
        M[0][3] = t[0]
        M[1][3] = t[1]
        M[2][3] = t[2]

        return M

    def __repr__(self):
        q = self
        return "{} {} {} {} {} {} {} {}".format(q.m_real[0],q.m_real[1],q.m_real[2],q.m_real[3],
                                                q.m_dual[0],q.m_dual[1],q.m_dual[2],q.m_dual[3])


#This function creates a dual quaternion from some 4x4 transformation matrix
def mat2DualQuat(M):
    tr = M[0][0] + M[1][1] + M[2][2]
    if tr > 0:
        S = np.sqrt(tr+1) * 2 #S = 4*qw
        qrw = 0.25 * S #np.sqrt(1 + M[0][0] + M[1][1] + M[2][2]) / 2
        qrx = (M[2][1] - M[1][2]) / S
        qry = (M[0][2] - M[2][0]) / S
        qrz = (M[1][0] - M[0][1]) / S
    elif M[0][0] > M[1][1] & M[0][0] > M[2][2]:
        S = np.sqrt(1 + M[0][0] - M[1][1] - M[2][2]) * 2 # S= 4 * qx
        qrw = (M[2][1] - M[1][2]) / S
        qrx = 0.25 * S
        qry = (M[0][1] + M[1][0]) / S
        qrz = (M[0][2] + M[2][0]) / S
    elif M[1][1] > M[2][2]:
        S = np.sqrt(1 + M[1][1] - M[0][0] - M[2][2]) * 2 #S=4*qy
        qrw = (M[0][2] - m[2][0]) / S
        qrx = (m[0][1] + m[1][0]) / S
        qry = 0.25 * S
        qrz = (M[1][2] + M[2][1]) / S
    else:
        S = np.sqrt(1 + M[2][2] - M[0][0] - M[1][1]) * 2 #S = 4*qz
        qrw = (M[1][0] - M[0][1]) / S
        qrx = (M[0][2] + M[2][0]) / S
        qry = (M[1][2] + M[2][1]) / S
        qrz = 0.25 * S

    r = qmath.quaternion([qrw, qrx, qry, qrz])

    d = qmath.quaternion([M[0][3]/2, M[1][3]/2, M[2][3]/2, M[3][3]/2])

    return DualQuaternion(r, d)
"""

r = qmath.quaternion([1, 2, 3, 4])
d = qmath.quaternion([5, 6, 7, 8])
q = DualQuaternion(r, d)
m = q.getRotation()
t = q.getTranslation()
mat = q.dualQuat2Matrix()

r1 = qmath.quaternion([9, 10, 11, 12])
d1 = qmath.quaternion([13, 14, 15, 16])
q1 = DualQuaternion(r1, d1)
m1 = q1.getRotation()
t1 = q1.getTranslation()
mat1 = q.dualQuat2Matrix()

Q = q.mult(q1)
M = Q.getRotation()
T = Q.getTranslation()
MAT = Q.dualQuat2Matrix()

MAT_test = np.matmul(mat1,mat)

#print(q)
print(m)
print(t)
print(mat)

print(m1)
print(t1)
print(mat1)

print(M)
print(T)
print(MAT)

print(MAT_test)
"""
