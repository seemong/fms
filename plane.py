class Plane:
    """
    Plane reifies the position and orientation of the plane. It provides
    the viewpoint
    """
    def __init__(self):
        self._eye = None
        self._lookAt = None
        self._up = None
        
    def get_eye(self):
        return self._eye
        
    def set_eye(self, eye):
        self._eye = eye

    def get_lookAt(self):
        return self._lookAt
        
    def set_lookAt(self, lookAt):
        self._lookAt = lookAt
        
    def get_up(self):
        return self._up
        
    def set_up(self, up):
        self._up = up
        
        
