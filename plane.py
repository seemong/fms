class Plane:
    """
    Plane reifies the position and orientation of the plane. It provides
    the viewpoint
    """
    def __init__(self):
        self._position = None
        self._lookAt = None
        self._up = None
        
    def get_position(self):
        return self._position
        
    def set_position(self, position):
        self._position = position

    def get_lookAt(self):
        return self._lookAt
        
    def set_lookAt(self, lookAt):
        self._lookAt = lookAt
        
    def get_up(self):
        return self._up
        
    def set_up(self, up):
        self._up = up
        
        
