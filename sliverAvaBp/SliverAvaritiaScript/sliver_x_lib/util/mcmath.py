import math
import copy

utility = __builtins__['__import__']('utility')
def Clamp(x, minVal, maxVal):
    return min(max(x, minVal), maxVal)


class Vector3(object):

    def __init__(self, *args):
        if len(args) == 0:
            self._x = 0
            self._y = 0
            self._z = 0
        elif len(args) == 1:
            vecTuple = args[0]
            if isinstance(vecTuple, tuple) and len(vecTuple) == 3:
                for arg in vecTuple:
                    if not isinstance(arg, (int, float)):
                        raise ValueError('Init Vector3 Failed!!! Need int or float!!!')

                self._x = vecTuple[0]
                self._y = vecTuple[1]
                self._z = vecTuple[2]
            else:
                raise ValueError('Init Vector3 Failed!!! Need Vector3(1, 2, 3) or Vector((1, 2, 3)))')
        elif len(args) == 3:
            for arg in args:
                if not isinstance(arg, (int, float)):
                    raise ValueError('Init Vector3 Failed!!! Need int or float!!!')

            self._x = args[0]
            self._y = args[1]
            self._z = args[2]
        else:
            raise ValueError('Init Vector3 Failed!!! Need Vector3(1, 2, 3) or Vector((1, 2, 3)))')

    @staticmethod
    def One():
        return Vector3(1.0, 1.0, 1.0)

    @staticmethod
    def Up():
        return Vector3(0.0, 1.0, 0.0)

    @staticmethod
    def Down():
        return Vector3(0.0, -1.0, 0.0)

    @staticmethod
    def Left():
        return Vector3(-1.0, 0.0, 0.0)

    @staticmethod
    def Right():
        return Vector3(1.0, 0.0, 0.0)

    @staticmethod
    def Forward():
        return Vector3(0.0, 0.0, 1.0)

    @staticmethod
    def Backward():
        return Vector3(0.0, 0.0, -1.0)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def z(self):
        return self._z

    def Normalized(self):
        len = self.Length()
        if len > 0.0001:
            invLen = 1.0 / len
            return Vector3(self._x * invLen, self._y * invLen, self._z * invLen)
        else:
            return Vector3()

    def Length(self):
        return math.sqrt(self.LengthSquared())

    def LengthSquared(self):
        return self._x * self._x + self._y * self._y + self._z * self._z

    def ToTuple(self):
        return (self._x, self._y, self._z)

    def Normalize(self):
        len = self.Length()
        if len > 0.0001:
            invLen = 1.0 / len
            self._x = self._x * invLen
            self._y = self._y * invLen
            self._z = self._z * invLen
        else:
            self._x = 0
            self._y = 0
            self._z = 0

    def Set(self, x = 0.0, y = 0.0, z = 0.0):
        self._x = x
        self._y = y
        self._z = z

    @staticmethod
    def Dot(a, b):
        return a.x * b.x + a.y * b.y + a.z * b.z

    @staticmethod
    def Cross(a, b):
        return Vector3(a.y * b.z - a.z * b.y, a.z * b.x - a.x * b.z, a.x * b.y - a.y * b.x)

    def __neg__(self):
        return Vector3(-self._x, -self._y, -self._z)

    def __pos__(self):
        return Vector3(self._x, self._y, self._z)

    def __add__(self, other):
        """ Returns the vector addition of self and other """
        if isinstance(other, Vector3):
            return Vector3(self._x + other.x, self._y + other.y, self._z + other.z)
        if isinstance(other, (int, float)):
            return Vector3(self._x + other, self._y + other, self._z + other)
        raise TypeError("unsupported operand type for : 'Vector3' and {0}".format(type(other)))

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        """ Returns the vector difference of self and other """
        if isinstance(other, Vector3):
            return Vector3(self._x - other.x, self._y - other.y, self._z - other.z)
        if isinstance(other, (int, float)):
            return Vector3(self._x - other, self._y - other, self._z - other)
        raise TypeError("unsupported operand type for : 'Vector3' and {0}".format(type(other)))

    def __rsub__(self, other):
        return -self + other

    def __mul__(self, other):
        if isinstance(other, Vector3):
            return Vector3.Dot(self, other)
        if isinstance(other, (int, float)):
            return Vector3(self._x * other, self._y * other, self._z * other)
        raise TypeError("unsupported operand type for : 'Vector3' and {0}".format(type(other)))

    def __rmul__(self, other):
        return self * other

    def __div__(self, other):
        if isinstance(other, (int, float)):
            return Vector3(self._x / other, self._y / other, self._z / other)
        raise TypeError("unsupported operand type for : 'Vector3' and {0}".format(type(other)))

    def __eq__(self, other):
        if not isinstance(other, Vector3):
            return False
        return self._x == other.x and self._y == other.y and self._z == other.z

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return '(' + str(self._x) + ', ' + str(self._y) + ', ' + str(self._z) + ')'

    def __str__(self):
        return '(' + str(self._x) + ', ' + str(self._y) + ', ' + str(self._z) + ')'

    def __getitem__(self, i):
        if i == 0:
            return self._x
        if i == 1:
            return self._y
        if i == 2:
            return self._z
        raise IndexError('vector3 index out of range')


class Quaternion(object):
    M_DEGTORAD = math.pi / 180.0
    M_RADTODEG = 1.0 / M_DEGTORAD
    NATIVE = False

    def __init__(self, *args):
        if len(args) == 0:
            self._x = 0
            self._y = 0
            self._z = 0
            self._w = 0
        elif len(args) == 1:
            vecTuple = args[0]
            if (isinstance(vecTuple, tuple) or isinstance(vecTuple, list)) and len(vecTuple) == 4:
                for arg in vecTuple:
                    if not isinstance(arg, (int, float)):
                        raise ValueError('Init Vector3 Failed!!! Need int or float!!!')

                self._x = vecTuple[0]
                self._y = vecTuple[1]
                self._z = vecTuple[2]
                self._w = vecTuple[3]
            else:
                raise ValueError('Init Vector3 Failed!!! Need Vector3(1, 2, 3) or Vector((1, 2, 3)))')
        elif len(args) == 4:
            for arg in args:
                if not isinstance(arg, (int, float)):
                    raise ValueError('Init Vector3 Failed!!! Need int or float!!!')

            self._x = args[0]
            self._y = args[1]
            self._z = args[2]
            self._w = args[3]
        else:
            raise ValueError('Init Vector3 Failed!!! Need Vector3(1, 2, 3) or Vector((1, 2, 3)))')

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def z(self):
        return self._z

    @property
    def w(self):
        return self._w

    @staticmethod
    def Euler(x = 0.0, y = 0.0, z = 0.0):
        if Quaternion.NATIVE:
            x_, y_, z_, w_ = utility.from_euler_angles([x, y, z])
        else:
            x = math.radians(x) * 0.5
            y = math.radians(y) * 0.5
            z = math.radians(z) * 0.5
            sinX = math.sin(x)
            cosX = math.cos(x)
            sinY = math.sin(y)
            cosY = math.cos(y)
            sinZ = math.sin(z)
            cosZ = math.cos(z)
            w_ = cosY * cosX * cosZ + sinY * sinX * sinZ
            x_ = cosY * sinX * cosZ + sinY * cosX * sinZ
            y_ = sinY * cosX * cosZ - cosY * sinX * sinZ
            z_ = cosY * cosX * sinZ - sinY * sinX * cosZ
        return Quaternion(x_, y_, z_, w_)

    @staticmethod
    def AngleAxis(angle = 0.0, axis = Vector3.Up()):
        s = math.sin(math.radians(angle) * 0.5)
        w = math.cos(math.radians(angle) * 0.5)
        x = axis.x * s
        y = axis.y * s
        z = axis.z * s
        return Quaternion(x, y, z, w)

    @staticmethod
    def RotationTo(start = Vector3.Up(), end = Vector3.Up()):
        v0 = start.Normalized()
        v1 = end.Normalized()
        dot = Vector3.Dot(v0, v1)
        if dot + 1 > 0.0001:
            cross = Vector3.Cross(v0, v1)
            scale = ((dot + 1) * 2) ** 0.5
            x, y, z = cross / scale
            w = 0.5 * scale
            return Quaternion(x, y, z, w)
        else:
            axis = Vector3.Cross(Vector3.Right(), v0)
            if axis.Length() < 0.0001:
                axis = Vector3.Cross(Vector3.Up(), v0)
            return Quaternion.AngleAxis(180.0, axis)

    @staticmethod
    def LookDirection(direction = Vector3.Backward(), up = Vector3.Up()):
        if direction.LengthSquared() < 0.0001:
            return Quaternion(0, 0, 0, 1)
        zAxis = -direction.Normalized()
        xAxis = Vector3.Cross(up, zAxis)
        if xAxis.LengthSquared() < 0.0001:
            return Quaternion.RotationTo(Vector3.Forward(), zAxis)
        xAxis.Normalize()
        yAxis = Vector3.Cross(zAxis, xAxis)
        rotMat = Matrix.Transpose(Matrix.Create([xAxis.ToTuple(), yAxis.ToTuple(), zAxis.ToTuple()]))
        return Quaternion(*rotMat.ToQuaternion())

    @staticmethod
    def Dot(a, b):
        return a.x * b.x + a.y * b.y + a.z * b.z + a.w * b.w

    @staticmethod
    def Cross(a, b):
        if Quaternion.NATIVE:
            data = utility.quaternion_multiply(a.wxyz(), b.wxyz())
            return Quaternion(data)
        else:
            return Quaternion(a._w * b.x + a._x * b.w + a._y * b.z - a._z * b.y, a._w * b.y + a._y * b.w + a._z * b.x - a._x * b.z, a._w * b.z + a._z * b.w + a._x * b.y - a._y * b.x, a._w * b.w - a._x * b.x - a._y * b.y - a._z * b.z)

    @staticmethod
    def Conjugate(q):
        return Quaternion(-q.x, -q.y, -q.z, q.w)

    @staticmethod
    def Inverse(q):
        return Quaternion.Conjugate(q) / Quaternion.Dot(q, q)

    @property
    def roll(self):
        x_ = self.x
        y_ = self.y
        z_ = self.z
        w_ = self.w
        check = 2.0 * (-y_ * z_ + w_ * x_)
        if check < -0.995:
            return -math.atan2(2.0 * (x_ * z_ - w_ * y_), 1.0 - 2.0 * (y_ * y_ + z_ * z_))
        elif check > 0.995:
            return math.atan2(2.0 * (x_ * z_ - w_ * y_), 1.0 - 2.0 * (y_ * y_ + z_ * z_))
        else:
            return math.atan2(2.0 * (x_ * y_ + w_ * z_), 1.0 - 2.0 * (x_ * x_ + z_ * z_))

    @property
    def pitch(self):
        check = 2.0 * (-self.y * self.z + self.w * self.x)
        if check < -0.995:
            return -0.5 * math.pi
        elif check > 0.995:
            return 0.5 * math.pi
        else:
            return math.asin(check)

    @property
    def yaw(self):
        check = 2.0 * (-self.y * self.z + self.w * self.x)
        if check < -0.995 or check > 0.995:
            return 0
        else:
            return math.atan2(2.0 * (self.x * self.z + self.w * self.y), 1.0 - 2.0 * (self.x * self.x + self.y * self.y))

    def HasRotation(self):
        return abs(self.w - 1.0) > 0.001

    def Length(self):
        return math.sqrt(self.LengthSquared())

    def LengthSquared(self):
        return self._x * self._x + self._y * self._y + self._z * self._z + self._w * self._w

    def ToTuple(self):
        return (self._x,
         self._y,
         self._z,
         self._w)

    def wxyz(self):
        return [self._w,
         self._x,
         self._y,
         self._z]

    def Normalized(self):
        len = self.Length()
        if len > 0.0001:
            invLen = 1.0 / len
            return Quaternion(self._x * invLen, self._y * invLen, self._z * invLen, self._w * invLen)
        else:
            return Quaternion(0, 0, 0, 1)

    def Normalize(self):
        len = self.Length()
        if len > 0.0001:
            invLen = 1.0 / len
            self._x *= invLen
            self._y *= invLen
            self._z *= invLen
            self._w *= invLen
        else:
            self._x *= 0
            self._y *= 0
            self._z *= 0
            self._w *= 0

    def EulerAngles(self):
        if Matrix.NATIVE:
            data = utility.euler_angles(self.wxyz())
            return Vector3(data)
        else:
            return Vector3(self.pitch, self.yaw, self.roll) * self.M_RADTODEG

    def EulerAnglesZYX(self):
        if Matrix.NATIVE:
            data = utility.euler_angles_zyx(self.wxyz())
            return Vector3(data)
        else:
            check = 2 * (self.w * self.y + self.x * self.z)
            if check < -0.995:
                x = 0
                y = -0.5 * math.pi
                z = 2 * math.atan2(self.x, self.w)
            elif check > 0.995:
                x = 0
                y = 0.5 * math.pi
                z = -2 * math.atan2(self.x, self.w)
            else:
                x = math.atan2(2 * (self.w * self.x - self.y * self.z), self.w * self.w - self.x * self.x - self.y * self.y + self.z * self.z)
                y = math.asin(2 * (self.w * self.y + self.x * self.z))
                z = math.atan2(2 * (self.w * self.z - self.x * self.y), self.w * self.w + self.x * self.x - self.y * self.y - self.z * self.z)
            return Vector3(x, y, z) * self.M_RADTODEG

    def __neg__(self):
        return Quaternion(-self._x, -self._y, -self._z, -self._w)

    def __pos__(self):
        return Quaternion(self._x, self._y, self._z, self._w)

    def __add__(self, other):
        """ Returns the vector addition of self and other """
        if isinstance(other, Quaternion):
            return Quaternion(self._x + other.x, self._y + other.y, self._z + other.z, self._w + other.w)
        if isinstance(other, (int, float)):
            return Quaternion(self._x + other, self._y + other, self._z + other, self._w + other)
        raise TypeError("unsupported operand type for : 'Quaternion' and {0}".format(type(other)))

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        """ Returns the vector difference of self and other """
        if isinstance(other, Quaternion):
            return Quaternion(self._x - other.x, self._y - other.y, self._z - other.z, self._w - other.w)
        if isinstance(other, (int, float)):
            return Quaternion(self._x - other, self._y - other, self._z - other, self._w - other)
        raise TypeError("unsupported operand type for : 'Quaternion' and {0}".format(type(other)))

    def __rsub__(self, other):
        return -self + other

    def __mul__(self, other):
        if isinstance(other, Quaternion):
            return Quaternion.Cross(self, other)
        if isinstance(other, Vector3):
            quatVector = Vector3(self.x, self.y, self.z)
            uv = Vector3.Cross(quatVector, other)
            uuv = Vector3.Cross(quatVector, uv)
            return other + (uv * self._w + uuv) * 2
        if isinstance(other, (int, float)):
            return Quaternion(self._x * other, self._y * other, self._z * other, self._w * other)
        raise TypeError("unsupported operand type for : 'Quaternion' and {0}".format(type(other)))

    def __rmul__(self, other):
        if isinstance(other, (int, float)):
            return self * other
        raise TypeError("unsupported operand type for : {0} and 'Quaternion'".format(type(other)))

    def __div__(self, other):
        if isinstance(other, (int, float)):
            return Quaternion(self._x / other, self._y / other, self._z / other, self._w)
        raise TypeError("unsupported operand type for : 'Quaternion' and {0}".format(type(other)))

    def __eq__(self, other):
        if not isinstance(other, Quaternion):
            return False
        return self._x == other.x and self._y == other.y and self._z == other.z and self._w == other.w

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return '(' + str(self._x) + ', ' + str(self._y) + ', ' + str(self._z) + ', ' + str(self._w) + ')'

    def __str__(self):
        return '(' + str(self._x) + ', ' + str(self._y) + ', ' + str(self._z) + ', ' + str(self._w) + ')'


class Matrix(object):
    NATIVE = False

    def __init__(self, rowNum, colNum):
        self._data = None
        self._row = rowNum
        self._col = colNum
        return

    @staticmethod
    def CreateEye(rowNum):
        newMatrix = Matrix(rowNum, rowNum)
        newMatrix.Eye()
        return newMatrix

    @staticmethod
    def Create(data):
        newMatrix = Matrix(len(data), len(data[0]))
        newMatrix.SetData(data)
        return newMatrix

    @staticmethod
    def FromEulerXYZ(euler):
        cx = math.cos(euler[0] * Quaternion.M_DEGTORAD)
        sx = math.sin(euler[0] * Quaternion.M_DEGTORAD)
        cy = math.cos(euler[1] * Quaternion.M_DEGTORAD)
        sy = math.sin(euler[1] * Quaternion.M_DEGTORAD)
        cz = math.cos(euler[2] * Quaternion.M_DEGTORAD)
        sz = math.sin(euler[2] * Quaternion.M_DEGTORAD)
        mat = Matrix(4, 4)
        mat.SetData([[cy * cz,
          sx * sy * cz - cx * sz,
          cx * sy * cz + sx * sz,
          0],
         [cy * sz,
          sx * sy * sz + cx * cz,
          cx * sy * sz - sx * cz,
          0],
         [-sy,
          sx * cy,
          cx * cy,
          0],
         [0,
          0,
          0,
          1]])
        return mat

    @staticmethod
    def ToEulerXYZ(mat):
        m31 = round(mat[(2, 0)], 2)
        if m31 != 1 and m31 != -1:
            t1 = -math.asin(mat[(2, 0)])
            c1 = 1.0 / math.cos(t1)
            return (Quaternion.M_RADTODEG * math.atan2(mat[(2, 1)] * c1, mat[(2, 2)] * c1), Quaternion.M_RADTODEG * t1, Quaternion.M_RADTODEG * math.atan2(mat[(1, 0)] * c1, mat[(0, 0)] * c1))
        else:
            if m31 == -1:
                y = math.pi * 0.5
                x = Quaternion.M_RADTODEG * math.atan2(mat[(0, 1)], mat[(0, 2)])
            else:
                y = -math.pi * 0.5
                x = Quaternion.M_RADTODEG * math.atan2(-mat[(0, 1)], -mat[(0, 2)])
            return (x, y, 0)

    def Eye(self):
        raise self.row == self.col or AssertionError('numRows must equal numCols to unit Maxtrix.')
        for i in range(self.row):
            for j in range(self.col):
                self[i, j] = 1 if j == i else 0

    def SetData(self, data):
        for r in range(self.row):
            for c in range(self.col):
                self[r, c] = data[r][c]

    def SetListData(self, data):
        self._data = data

    @staticmethod
    def QuaternionToMatrix(wxyz):
        if Matrix.NATIVE:
            newMatrix = Matrix(4, 4)
            newMatrix.SetListData(utility.quaternion_to_matrix(wxyz))
            return newMatrix
        w = wxyz[0]
        x = wxyz[1]
        y = wxyz[2]
        z = wxyz[3]
        m11 = 1 - y * y * 2 - z * z * 2
        m21 = 2 * x * y + 2 * z * w
        m31 = 2 * x * z - 2 * y * w
        m12 = 2 * x * y - 2 * z * w
        m22 = 1 - x * x * 2 - z * z * 2
        m32 = 2 * z * y + 2 * x * w
        m13 = 2 * x * z + 2 * y * w
        m23 = 2 * z * y - 2 * x * w
        m33 = 1 - x * x * 2 - y * y * 2
        mat = Matrix.Create([[m11,
          m12,
          m13,
          0],
         [m21,
          m22,
          m23,
          0],
         [m31,
          m32,
          m33,
          0],
         [0,
          0,
          0,
          1]])
        return mat

    def Copy(self):
        newMatrix = Matrix(self._row, self._col)
        newMatrix.SetListData(copy.deepcopy(self._data))
        return newMatrix

    @property
    def row(self):
        return self._row

    @property
    def col(self):
        return self._col

    def __getitem__(self, ndxTuple):
        if not self._data:
            self._data = [0] * self._col * self._row
        return self._data[ndxTuple[0] * self._col + ndxTuple[1]]

    def __setitem__(self, ndxTuple, value):
        if not self._data:
            self._data = [0] * self._col * self._row
        self._data[ndxTuple[0] * self._col + ndxTuple[1]] = value

    def Transpose(self):
        newMatrix = Matrix(self.col, self.row)
        for r in range(self.row):
            for c in range(self.col):
                newMatrix[c, r] = self[r, c]

        return newMatrix

    def Inverse(self):
        if not self.row == self.col:
            raise AssertionError('numRows must equal numCols to inverse Maxtrix.')
            newMatrix = Matrix.NATIVE and Matrix(self._row, self._col)
            newMatrix.SetListData(utility.matrix4_inverse(self._data))
            return newMatrix
        A = self.Copy()
        n = self.row
        for pivot in xrange(n):
            B = Matrix(n, 1)
            B[pivot, 0] = 1.0
            if A[pivot, pivot] == 0:
                A[pivot, pivot] = 1e-09
            coef = 1.0 / A[pivot, pivot]
            if abs(coef) > 1e-32:
                for col in xrange(0, n):
                    A[(pivot, col)] *= coef

                B[(pivot, 0)] *= coef
            for row in xrange(n):
                if row == pivot:
                    continue
                coef = 1.0 * A[row, pivot]
                if abs(coef) > 1e-32:
                    for col in xrange(0, n):
                        A[(row, col)] -= coef * A[pivot, col]

                    B[(row, 0)] -= coef * B[pivot, 0]

            for row in xrange(n):
                A[row, pivot] = B[row, 0]

        return A

    def Decompose(self):
        matrix = self.Copy()
        trans = (matrix[(0, 3)], matrix[(1, 3)], matrix[(2, 3)])
        matrix[(0, 3)] = matrix[(1, 3)] = matrix[(2, 3)] = 0
        matrix[(3, 3)] = 1
        norm = 1
        count = 0
        mR = matrix.Copy()
        while count <= 100 and norm > 0.0001:
            mRnext = Matrix(4, 4)
            mRit = mR.Transpose().Inverse()
            for i in range(4):
                for j in range(4):
                    mRnext[i, j] = 0.5 * (mR[i, j] + mRit[i, j])

            norm = 0
            for i in range(3):
                n = abs(mR[i, 0] - mRnext[i, 0]) + abs(mR[i, 1] - mRnext[i, 1]) + abs(mR[i, 2] - mRnext[i, 2])
                norm = max(norm, n)

            mR = mRnext
            count += 1

        quater = mR.ToQuaternion()
        mS = mR.Inverse() * matrix
        scale = (mS[(0, 0)], mS[(1, 1)], mS[(2, 2)])
        return (trans, quater, scale)

    def DecomposeByQuaternion(self, wxyz):
        trans = (self[(0, 3)], self[(1, 3)], self[(2, 3)])
        if Matrix.NATIVE:
            scale = utility.quaternion_decomposition(self._data, wxyz)
        else:
            matrix = self.Copy()
            matrix[(0, 3)] = matrix[(1, 3)] = matrix[(2, 3)] = 0
            matrix[(3, 3)] = 1
            quatermat = Matrix.QuaternionToMatrix(wxyz)
            ms = quatermat.Inverse() * matrix
            scale = (ms[(0, 0)], ms[(1, 1)], ms[(2, 2)])
        return (trans, tuple(scale))

    def ToQuaternion(self):
        m11 = self[(0, 0)]
        m22 = self[(1, 1)]
        m33 = self[(2, 2)]
        m32 = self[(2, 1)]
        m23 = self[(1, 2)]
        m13 = self[(0, 2)]
        m31 = self[(2, 0)]
        m21 = self[(1, 0)]
        m12 = self[(0, 1)]
        if m11 + m22 + m33 + 1 > 1e-05:
            w = math.sqrt(m11 + m22 + m33 + 1) / 2
            x = (m32 - m23) / (4 * w)
            y = (m13 - m31) / (4 * w)
            z = (m21 - m12) / (4 * w)
        elif max(m11, m22, m33) == m11:
            t = math.sqrt(m11 - m22 - m33 + 1) * 2
            w = (m32 - m23) / t
            x = t / 4
            y = (m12 + m21) / t
            z = (m13 + m31) / t
        elif max(m11, m22, m33) == m22:
            t = math.sqrt(-m11 + m22 - m33 + 1) * 2
            w = (m13 - m31) / t
            x = (m12 + m21) / t
            y = t / 4
            z = (m32 + m23) / t
        else:
            t = math.sqrt(-m11 - m22 + m33 + 1) * 2
            w = (m21 - m12) / t
            x = (m13 + m31) / t
            y = (m23 + m32) / t
            z = t / 4
        return (x,
         y,
         z,
         w)

    @staticmethod
    def matrix4_multiply(lhs, rhs):
        raise lhs.col == lhs.row == rhs.col == rhs.row == 4 or AssertionError('Matrix sizes not compatible for the matrix multiply4 operation.')
        newMatrix = Matrix(lhs.row, rhs.col)
        data = utility.matrix4_multiply(lhs._data, rhs._data)
        newMatrix.SetListData(data)
        return newMatrix

    def __add__(self, rhsMatrix):
        raise rhsMatrix.row == self.row and rhsMatrix.col == self.col or AssertionError('Matrix sizes not compatible for the add operation.')
        newMatrix = Matrix(self.row, self.col)
        for r in range(self.row):
            for c in range(self.col):
                newMatrix[r, c] = self[r, c] + rhsMatrix[r, c]

        return newMatrix

    def __mul__(self, rhsMatrix):
        if not rhsMatrix.row == self.col:
            raise AssertionError('Matrix sizes not compatible for the multi operation.')
            return Matrix.NATIVE and self._row == 4 and self._col == 4 and rhsMatrix.col == 4 and Matrix.matrix4_multiply(self, rhsMatrix)
        newMatrix = Matrix(self.row, rhsMatrix.col)
        for r in range(self.row):
            for c in range(rhsMatrix.col):
                mysum = 0.0
                for k in range(self.col):
                    mysum += self[r, k] * rhsMatrix[k, c]

                newMatrix[r, c] = mysum

        return newMatrix

    def __sub__(self, rhsMatrix):
        raise rhsMatrix.row == self.row and rhsMatrix.col == self.col or AssertionError('Matrix sizes not compatible for the add operation.')
        newMatrix = Matrix(self.row, self.col)
        for r in range(self.row):
            for c in range(self.col):
                newMatrix[r, c] = self[r, c] - rhsMatrix[r, c]

        return newMatrix

    def __str__(self):
        s = '[ '
        for i in range(self.row):
            if i > 0:
                s += '\n  '
            for j in range(self.col):
                s += str(self[i, j])
                if j < self.col - 1:
                    s += ','

            if i < self.row - 1:
                s += ';'

        s += ' ]'
        return s