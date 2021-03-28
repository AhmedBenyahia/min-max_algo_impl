import time


class Game:
    def __init__(self):
        self.initialize_game()


    def initialize_game(self):
        self.current_state = [(7, 0)]

        # Player P1 always plays first
        self.player_turn = 'P1'

    def draw_board(self):
        for p in self.current_state:
            print("(%d, %d)" % p, end="->")
        print()

    # Determines if the made move is a legal move
    def is_valid(self, n, a, b):
        return a + b == n

    # Checks if the game has ended and returns the winner in each case
    def is_end(self):
        a, b = self.current_state[-1]
        if a != b: return None
        a = ['P2', 'P1'][len(self.current_state) % 2]
        return a

    # Player 'P2' is max, in this case AI
    def max(self, alpha, beta):

        # Possible values for maxv are:
        # -1 - loss
        # 1  - win

        # We're initially setting it to -2 as worse than the worst case:
        maxv = -2

        a = None
        b = None

        result = self.is_end()

        # If the game came to an end, the function needs to return
        # the evaluation function of the end. That can be:
        # -1 - loss
        # 1  - win
        if result == 'P1':
            return -1, self.current_state[-1][0], self.current_state[-1][1]
        elif result == 'P2':
            return 1, self.current_state[-1][0], self.current_state[-1][1]

        # Get the current number to be divided
        n = self.current_state[-1][0]

        # Test all the game tree branches
        # All possible division for the chosen number
        for i in range(1, n//2+1):
            # 'P2' makes a move and calls Min
            # That's one branch of the game tree.
            self.current_state.append((max(n - i, i), min(n - i, i)))
            m, min_a, min_b = self.min(alpha, beta)
            # Fixing the maxv value if needed
            if m > maxv:
                a, b = (max(n - i, i), min(n - i, i))
                maxv = m

            # # Next two ifs in Max and Min are the only difference between regular algorithm and minimax
            # if maxv >= beta:
            #     return maxv, a, b
            #
            # if maxv > alpha:
            #     alpha = maxv

            # Setting back the field to empty
            self.current_state.pop()
        return maxv, a, b

    # Player 'P1' is min, in this case Player
    def min(self, alpha, beta):

        # Possible values for mixv are:
        # -1 - win
        # 1  - loss

        # We're initially setting it to -2 as worse than the worst case:
        minv = 2

        a = None
        b = None

        result = self.is_end()

        # If the game came to an end, the function needs to return
        # the evaluation function of the end. That can be:
        # -1 - win
        # 1  - loss
        if result == 'P1':
            return -1,  self.current_state[-1][0], self.current_state[-1][1]
        elif result == 'P2':
            return 1, self.current_state[-1][0], self.current_state[-1][1]

        # Get the current number to be divided, It's the max last value entered
        n = self.current_state[-1][0]

        # Test all the game tree branches
        # All possible division for the chosen number
        for i in range(1, n//2+1):
            # 'P1' makes a move and calls Max
            # That's one branch of the game tree.
            self.current_state.append((max(n - i, i), min(n - i, i)))
            m, min_a, min_b = self.max(alpha, beta)
            # Fixing the minv value if needed
            if m < minv:
                minv = m
                a, b = (max(n - i, i), min(n - i, i))
            # Setting back the field to empty
            self.current_state.pop()

            # # Next two ifs in Max and Min are the only difference between regular algorithm and minimax
            # if minv <= alpha:
            #     return minv, a, b
            #
            # if minv < beta:
            #     beta = minv

        return minv, a, b

    def play(self):
        while True:
            self.draw_board()
            self.result = self.is_end()

            # Printing the appropriate message if the game has ended
            if self.result is not None:
                if self.result == 'P1':
                    print('The winner is P1!')
                elif self.result == 'P2':
                    print('The winner is P2!')

                self.initialize_game()
                return

            # If it's player's turn
            if self.player_turn == 'P1':

                while True:

                    start = time.time()
                    m, a, b = self.min(-2, 2)
                    end = time.time()
                    print('Evaluation time: {}s'.format(round(end - start, 7)))
                    print('Recommended move: X = {}, Y = {}'.format(a, b))

                    a = int(input('a: '))
                    b = int(input('b: '))

                    s = (a, b)

                    # Get the current number to be divided, It's the max last value entered
                    n = self.current_state[-1][0]

                    if self.is_valid(n, a, b):
                        self.current_state.append((max(s), min(s)))
                        self.player_turn = 'P2'
                        break
                    else:
                        print('The move is not valid! Try again.')

            # If it's AI's turn
            else:
                (m, a, b) = self.max(-2, 2)
                s = (a, b)
                self.current_state.append((max(s), min(s)))
                self.player_turn = 'P1'