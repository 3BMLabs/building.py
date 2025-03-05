from abstract.matrix import Matrix
from abstract.vector import Vector


class dimension_changer:
    """transforms geometry to a desired amount of dimensions.  for example, if you have a line from (2,3,4) to (5,6,7) and you want to make it 2d, then it will remove the last values to create
    (2,3) -> (5,6)
    multiply this dimension changer with the item you want to change the dimensions of.
    """

    def __init__(self, desired_dimensions=3):
        self.desired_dimensions = desired_dimensions

    def __mul__(self, other: Matrix | Vector):
        def get_scaled_item(row, col):
            if row == self.desired_dimensions - 1:
                get_row = other.rows - 1
            elif row < other.dimensions - 1:
                get_row = row
            else: return 0
            
            if col == self.desired_dimensions - 1:
                return other[get_row][other.cols - 1]
            elif col < other.dimensions - 1:
                return other[get_row][col]
            else:
                return 0

        if isinstance(other, Matrix):
            return Matrix(
                [
                    [
                        get_scaled_item(row, col)
                        for col in range(self.desired_dimensions)
                    ]
                    for row in range(self.desired_dimensions)
                ]
            )
        elif isinstance(other, Vector):
            other_dimensions = len(other)
            return Vector(list(other) + [0] * (self.desired_dimensions - other_dimensions) if self.desired_dimensions > other_dimensions else other[:self.desired_dimensions])
        else:
            return NotImplemented