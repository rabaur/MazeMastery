class State:
    """
    State is a singleton class that holds the current state of the maze solver,
    e.g., the current positions of the player, the position of gems, etc. All
    functions that manipulate the state instantiate this class and modify its
    attributes. By doing so, we don't need to bind these state-changing methods
    to a single class (so no knowledge about OOP is required).
    """
    _self = None
    def __new__(cls):
        if cls._self is None:
            cls._self = super().__new__(cls)
        return cls._self

    def __init__(self):
        self.__pos = (0, 0)
    
    def get_pos(self):
        return self.__pos


if __name__ == "__main__":
    state = State()
    print(state.__pos)