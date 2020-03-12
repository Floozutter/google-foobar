import heapq
from functools import total_ordering

# Global constants.
CLEAR = 0
WALL = 1
DIRECTIONS = (
    ( 0,  1),  # RIGHT
    (-1,  0),  # UP
    ( 0, -1),  # LEFT
    ( 1,  0)   # DOWN
)
STATE2ICON = {
    CLEAR : " ",
    WALL  : "#",
}


# Classes for maze solving.
@total_ordering
class Cell:
    """
    Represents a single cell in a BunnyMap.
    Provides methods and properties for A*.
    """
    def __init__(self, state, row, col, h):
        """Initializes a Cell."""
        self.state = state
        self.row = row
        self.col = col
        self.heuristic = h  # Estimated cost to ending Cell.
        self.gap = None     # Cost from the starting Cell.
        self.parent = None  # Adjacent Cell closest to the starting Cell.
    def get_coord(self):
        """Returns the Cell's coordinates as a Tuple."""
        return self.row, self.col
    def get_fullcost(self):
        """Returns the estimated sum cost from the start to the end."""
        if self.gap is not None:
            return self.heuristic + self.gap
        return None
    def set_parent(self, parent):
        """
        Sets an adjacent Cell as this Cell's parent.
        Updates this Cell's gap (cost from the start Cell).
        """
        self.gap = parent.gap + 1
        self.parent = parent
    def __eq__(self, other):
        """Equality comparison function for priority queue ordering."""
        return self.get_fullcost() == other.get_fullcost()
    def __lt__(self, other):
        """Less than comparison function for priority queue ordering."""
        return self.get_fullcost() < other.get_fullcost()
    def __str__(self):
        """Returns an icon representing the state of the Cell."""
        return STATE2ICON[self.state]
    def __repr__(self):
        """Returns a string representation for debugging purposes."""
        return (
            f"Cell('{STATE2ICON[self.state]}', "
            f"({self.row}, {self.col}), "
            f"h={self.heuristic}, g={self.gap}, f={self.get_fullcost()})"
        )

class BunnyMap:
    """
    Represents a map of a location in Lambda's space station.
    Provides methods for solving the maze using the A* search algorithm.
    """
    def __init__(self, mat):
        """Initializes a BunnyMap from a List of Lists of states."""
        # Set map dimensions.
        self.height = len(mat)
        self.width  = len(mat[0])
        # Populate map with cells.
        self.cells = [
            [
                Cell(value, i, j, abs(self.height-i) + abs(self.width-j))
                for j, value in enumerate(row)
            ]
            for i, row in enumerate(mat)
        ]
    def __str__(self):
        """Returns a string representation of the BunnyMap."""
        out = ""
        out += "@" * (self.width+2) + "\n"
        for row in self.cells:
            out += "@"
            for cell in row:
                out += str(cell)
            out += "@\n"
        out += "@" * (self.width+2) + "\n"
        return out
    def solstr(self):
        """Returns a string representation, with a solution path."""
        path = set(self.aStarPath())
        out = ""
        out += "@" * (self.width+2) + "\n"
        for row in self.cells:
            out += "@"
            for cell in row:
                if cell.get_coord() in path:
                    out += "!"
                else:
                    out += str(cell)
            out += "@\n"
        out += "@" * (self.width+2) + "\n"
        return out
    def get_cell(self, row, col):
        """Returns a reference to the Cell at the given coordinate."""
        if (0 <= row < self.height) and (0 <= col < self.width):
            return self.cells[row][col]
        return None
    def adjacent_cells(self, row, col):
        """Returns every valid Cell adjacent to the given coordinate."""
        maybecells = [self.get_cell(row+i, col+j) for i, j in DIRECTIONS]
        return [cell for cell in maybecells if cell is not None]
    def aStarPath(self):
        """
        Runs the A* search algorithm over the BunnyMap.
        Returns a path (list of coordinates) from the start to the end.
        """
        solved = False
        # Set start and end cells.
        start = self.get_cell(0, 0)
        end   = self.get_cell(self.height-1, self.width-1)
        # Set start's gap distance to 0.
        start.gap = 0
        # Initialize the open and closed structures.
        openQueue = [start]  # min-heap priority queue
        closedSet = set()
        # Start consuming openQueue.
        while openQueue:
            # Take the cell with the lowest fullcost.
            cell = heapq.heappop(openQueue)
            closedSet.add(cell.get_coord())
            # Check if end reached.
            if cell.get_coord() == end.get_coord():
                solved = True
                break
            # Iterate over adjacent cells.
            for adj in self.adjacent_cells(cell.row, cell.col):
                if adj.get_coord() not in closedSet and adj.state == CLEAR:
                    # Check whether adj has never been visited.
                    if adj not in openQueue:
                        adj.set_parent(cell)
                        heapq.heappush(openQueue, adj)
                    else:  # adj has been visited before.
                        # Check if current cell is a better parent.
                        if adj.gap > cell.gap + 1:
                            adj.set_parent(cell)
        # Check if solution exists.
        if not solved:
            return None
        # From end, trace parents to get the path back.
        path = []
        cell = end
        while not (cell.get_coord() == start.get_coord()):
            path.append(cell.get_coord())
            cell = cell.parent
        path.append(cell.get_coord())
        return path[::-1]
    def shortest_pathlength(self):
        """Returns the length of the shortest path from start to end."""
        path = self.aStarPath()
        if path is not None:
            return len(path)
        return None


# Solution function.
def solution(mat):
    """Returns the shortest path length by A*ing over every possible map."""
    pathlengths = []
    # Iterate over every single possible map. (Each is missing one wall.)
    wall_coords = []
    for i, row in enumerate(mat):
        for j, value in enumerate(row):
            if value == WALL:
                wall_coords.append( (i, j) )
    dewalled_mat = [list(row) for row in mat]
    for i, j in wall_coords:
        dewalled_mat[i][j] = CLEAR
        pathlengths.append(BunnyMap(dewalled_mat).shortest_pathlength())
        dewalled_mat[i][j] = WALL
    return min(filter(lambda l: l is not None, pathlengths))


# Tests.
if __name__ == "__main__":
    a = [[0, 1, 1, 0], [0, 0, 0, 1], [1, 1, 0, 0], [1, 1, 1, 0]]
    b = [
        [0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1],
        [0, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0]
    ]
    aMap = BunnyMap(a)
    bMap = BunnyMap(b)

    # Test A.
    print("A:")
    print(aMap)
    print(aMap.solstr())
    print(solution(a))  # Distinct from the solution string above.

    print("\n")
    # Test B.
    print("B:")
    print(bMap)
    print(bMap.solstr())
    print(solution(b))  # Also distinct.
    
