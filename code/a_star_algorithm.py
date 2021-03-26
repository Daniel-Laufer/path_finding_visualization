from box import Box

# added a comment here
class A_Star():

    def __init__(self) -> None:
        self.closed_set = []
        self.starting_node = None
        self.open_set = []
        self.current_node = None

