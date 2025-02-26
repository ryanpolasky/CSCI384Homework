# Written by Ryan Polasky - 2/10/25

from heapq import heappush, heappop


class PuzzleState:
    def __init__(self, board, cost=0, parent=None):  # init important vars
        self.board = board
        self.blank_pos = board.index('_')
        self.cost = cost
        self.parent = parent

    def __lt__(self, other):  # need this for priority queue
        return self.cost < other.cost

    def __repr__(self):  # for logging's sake
        return "".join(self.board) + f" (Cost: {self.cost})"


def get_successors(state):  # function to find successors
    successors = []  # init empty list
    pos = state.blank_pos  # save blank spot position
    board = state.board  # get board from state

    moves = [-1, 1, -2, 2, -3, 3]  # left, right, & jumps
    for move in moves:  # for each action,
        new_pos = pos + move  # calculate new position

        if 0 <= new_pos < len(board):  # if the new position is valid,
            if abs(move) > 1:  # if the move is a jump,
                mid_pos = pos + (move // 2)  # calculate the mid-position between the original position & the move/2
                if board[mid_pos] == '_':  # if that calculated position is the blank tile, continue
                    continue

            new_board = board[:]  # clone a second board
            new_board[pos], new_board[new_pos] = new_board[new_pos], new_board[pos]  # swap the positions
            cost = abs(move)  # calculate the cost
            successors.append(PuzzleState(new_board, state.cost + cost, state))  # append the successor

    return successors  # return the list of successors


def heuristic_h1(state):  # calculate heuristic h1 (misplaced tiles)
    misplaced = 0  # assume 0 misplaced
    board = state.board
    for i in range(len(board)):  # for each tile,
        if board[i] == 'W':  # if the tile is white,
            for j in range(i + 1, len(board)):  # for each tile after the first current one,
                if board[j] == 'B':  # if the tile is black,
                    misplaced += 1  # increment misplaced
    return misplaced  # return misplaced


def heuristic_h2(state):  # calculate heuristic h2 (Manhattan distance)
    distance = 0  # assume total distance is 0
    board = state.board
    goal = ['W', 'W', 'W', 'W', 'W', '_', 'B', 'B', 'B', 'B', 'B']  # the goal configuration

    for i, tile in enumerate(board):  # for each tile in board
        if tile != '_':  # skip the blank tile
            goal_pos = goal.index(tile)  # find the goal position of the tile
            distance += abs(i % 5 - goal_pos % 5) + abs(i // 5 - goal_pos // 5)  # add the Manhattan distance
    return distance  # return calculated Manhattan distance


def is_goal_state(board):  # calculate if we're in the goal state
    seen_white = False  # assume we've seen no white tiles
    for tile in board:  # for every tile in the board,
        if tile == 'W':  # if the tile is white,
            seen_white = True  # say we've seen a white tile
        elif tile == 'B' and seen_white:  # if we see a black tile & we've already seen a white tile,
            return False  # we are not in a goal state
    return True  # otherwise, we are in a goal state


def a_star_search(initial_state, heuristic_func):  # A* search with custom heuristic
    open_set = []  # start with empty set
    heappush(open_set, (0 + heuristic_func(initial_state), initial_state))  # start with initial state

    visited = {}  # keep track of visited states
    total_nodes_added = 1  # track total nodes added
    expanded_nodes = 0  # track expanded nodes

    while open_set:  # while there's a state in the open set,
        f_score, current_state = heappop(open_set)  # get heuristic & state
        board_str = "".join(current_state.board)  # logging

        if board_str in visited and visited[board_str] <= current_state.cost:  # if visited with lower cost before,
            continue
        visited[board_str] = current_state.cost  # add to visited states

        expanded_nodes += 1  # increment expanded node count

        if is_goal_state(current_state.board):  # if goal state reached
            path = []  # init empty path
            while current_state:  # backtrack path
                path.append(current_state)  # add state
                current_state = current_state.parent  # move to parent
            path.reverse()  # reverse path for correct order

            # The requested output for heuristic h2
            print("\n=== Solution Found ===")
            print(f"Optimal solution sequence:")
            for step in path:
                print(f"    {step}")

            print(f"Optimal cost: {path[-1].cost}")
            print(f"Expanded nodes: {expanded_nodes}")
            print(f"Frontier size at goal: {len(open_set)}")
            print(f"Total nodes added to frontier: {total_nodes_added}")
            return path

        for successor in get_successors(current_state):  # for each successor,
            f_score = successor.cost + heuristic_func(successor)  # calculate heuristic
            heappush(open_set, (f_score, successor))  # push to heap
            total_nodes_added += 1  # increment total nodes

    print("No solution found.")  # print failure case
    return None


if __name__ == "__main__":
    initial = PuzzleState(list("WWWWW_BBBBB"))
    print("Running A* with h1 (misplaced tiles)...")
    a_star_search(initial, heuristic_h1)
    print("\nRunning A* with h2 (Manhattan distance)...")
    a_star_search(initial, heuristic_h2)
