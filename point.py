class Point:
    def __init__(self, *args):
        if len(args) == 2:
            self.x, self.y = map(float, args)
        elif len(args) == 3:
            self.x, self.y, self.z = map(float, args)
        else:
            raise ValueError("A point can only be in 2D or 3D space.")

    def __str__(self):
        if hasattr(self, 'z'):
            return '({}, {}, {})'.format(self.x, self.y, self.z)
        else:
            return '({}, {})'.format(self.x, self.y)