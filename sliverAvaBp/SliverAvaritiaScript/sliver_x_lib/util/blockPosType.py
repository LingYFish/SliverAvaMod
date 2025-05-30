class BlockPos:
    """
    A utility class for handling block positions and directional offsets.
    """
    DIRECTION_DOWN = (0, -1, 0)
    DIRECTION_UP = (0, 1, 0)
    DIRECTION_NORTH = (0, 0, -1)
    DIRECTION_SOUTH = (0, 0, 1)
    DIRECTION_WEST = (-1, 0, 0)
    DIRECTION_EAST = (1, 0, 0)
    DIRECTIONS = (DIRECTION_DOWN, DIRECTION_UP, DIRECTION_NORTH, DIRECTION_SOUTH, DIRECTION_WEST, DIRECTION_EAST)

    @classmethod
    def offset(cls, position, direction, distance):
        """
        Calculate the new position by applying the given direction and distance to the current position.

        :param position: The current position (x, y, z).
        :type position: (int, int, int)
        :param direction: The direction to move (dx, dy, dz).
        :type direction: (int, int, int)
        :param distance: The distance to move in the given direction.
        :type distance: int
        :return: The new position after applying the offset.
        :rtype: (int, int, int)
        """
        x = position[0] + direction[0] * distance
        y = position[1] + direction[1] * distance
        z = position[2] + direction[2] * distance
        return x, y, z

    @classmethod
    def move_down(cls, position, distance):
        """
        Move the position downward by the given distance.

        :param position: The current position (x, y, z).
        :type position: (int, int, int)
        :param distance: The distance to move downward.
        :type distance: int
        :return: The new position after moving down.
        :rtype: (int, int, int)
        """
        return cls.offset(position, cls.DIRECTION_DOWN, distance)

    @classmethod
    def move_up(cls, position, distance):
        """
        Move the position upward by the given distance.

        :param position: The current position (x, y, z).
        :type position: (int, int, int)
        :param distance: The distance to move upward.
        :type distance: int
        :return: The new position after moving up.
        :rtype: (int, int, int)
        """
        return cls.offset(position, cls.DIRECTION_UP, distance)

    @classmethod
    def move_north(cls, position, distance):
        """
        Move the position northward by the given distance.

        :param position: The current position (x, y, z).
        :type position: (int, int, int)
        :param distance: The distance to move northward.
        :type distance: int
        :return: The new position after moving north.
        :rtype: (int, int, int)
        """
        return cls.offset(position, cls.DIRECTION_NORTH, distance)

    @classmethod
    def move_south(cls, position, distance):
        """
        Move the position southward by the given distance.

        :param position: The current position (x, y, z).
        :type position: (int, int, int)
        :param distance: The distance to move southward.
        :type distance: int
        :return: The new position after moving south.
        :rtype: (int, int, int)
        """
        return cls.offset(position, cls.DIRECTION_SOUTH, distance)

    @classmethod
    def move_west(cls, position, distance):
        """
        Move the position westward by the given distance.

        :param position: The current position (x, y, z).
        :type position: (int, int, int)
        :param distance: The distance to move westward.
        :type distance: int
        :return: The new position after moving west.
        :rtype: (int, int, int)
        """
        return cls.offset(position, cls.DIRECTION_WEST, distance)

    @classmethod
    def move_east(cls, position, distance):
        """
        Move the position eastward by the given distance.

        :param position: The current position (x, y, z).
        :type position: (int, int, int)
        :param distance: The distance to move eastward.
        :type distance: int
        :return: The new position after moving east.
        :rtype: (int, int, int)
        """
        return cls.offset(position, cls.DIRECTION_EAST, distance)

    @classmethod
    def move_next(cls, position, side):
        """
        Move the position to the next block in the specified direction.

        :param position: The current position (x, y, z).
        :type position: (int, int, int)
        :param side: The direction to move (0=down, 1=up, 2=north, 3=south, 4=west, 5=east).
        :type side: int
        :return: The new position after moving to the next block.
        :rtype: (int, int, int)
        """
        return cls.offset(position, cls.DIRECTIONS[side], 1)

    @classmethod
    def move_last(cls, position, side):
        """
        Move the position to the previous block in the specified direction.

        :param position: The current position (x, y, z).
        :type position: (int, int, int)
        :param side: The direction to move (0=down, 1=up, 2=north, 3=south, 4=west, 5=east).
        :type side: int
        :return: The new position after moving to the previous block.
        :rtype: (int, int, int)
        """
        return cls.offset(position, cls.DIRECTIONS[side], -1)