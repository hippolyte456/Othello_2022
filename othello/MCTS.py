import othello.minmax as minmax 
import random as rd 
import math

class MCTSNode(object):
    def __init__(self, game_state, nextPlayer, parent=None, move=None):
        self.game_state = game_state
        self.nextPlayer = nextPlayer
        self.parent = parent
        self.move = move # Parent's move that generated the child
        self.win_counts = 0 # anciennement {Player.black: 0, Player.white: 0,}
        self.num_rollouts = 0
        self.children = []
        self.unvisited_moves = game_state.possible_moves(nextPlayer)

    def add_random_child(self):
        index = rd.randint(0, len(self.unvisited_moves) - 1)
        new_move = self.unvisited_moves.pop(index)
        new_game_state = self.game_state.play_move(new_move[0], new_move[1], self.nextPlayer)
        new_nextPlayer = - self.nextPlayer # Nop, be carefull next player is not always -self.nextPLayer you should prefer to get the self.new_game.side
        new_node = MCTSNode(new_game_state, new_nextPlayer, self, new_move) # Be carefull if you send new_game_state like this you will modify it in the child and when you will come back the modification will stay you can undo the move to prevent this
        self.children.append(new_node)
        return new_node


    def record_win(self, winner):
        if self.nextPlayer == winner:
            self.win_counts += 1    #anciennement self.win_counts[winner] += 1 
        self.num_rollouts += 1



    def can_add_child(self):
        return len(self.unvisited_moves) > 0

    def is_terminal(self):
        return self.game_state.game_over()

    def winning_frac(self):
        return float(self.win_counts) / float(self.num_rollouts)




class MCTSAgent(): #(agent.Agent):

    '''a voir où on en a besoin'''
    def __init__(self, num_rounds, temperature):
        #agent.Agent.__init__(self)
        self.num_rounds = num_rounds
        self.temperature = temperature


    def select_move(self, game_state):
        root = MCTSNode(game_state)

        for i in range(self.num_rounds):
            node = root
            while (not node.can_add_child()) and (not node.is_terminal()):
                node = self.select_child(node)

            # Add a new child node into the tree.
            if node.can_add_child():
                node = node.add_random_child()

            # Simulate a random game from this node.
            winner = self.simulate_random_game(node.game_state) 

            # Propagate scores back up the tree.
            while node is not None:
                node.record_win(winner)
                node = node.parent

        scored_moves = [   #regarder ce que ça veut dire que ça avec le pdf dl and the game of go HHHHHH
            (child.winning_frac(), child.move, child.num_rollouts)
            for child in root.children
        ]
        scored_moves.sort(key=lambda x: x[0], reverse=True)
        for s, m, n in scored_moves[:10]:
            print('%s - %.3f (%d)' % (m, s, n))

# tag::mcts-selection[]
        # Having performed as many MCTS rounds as we have time for, we
        # now pick a move.
        best_move = None
        best_pct = -1.0
        for child in root.children:
            child_pct = child.winning_frac()
            if child_pct > best_pct:
                best_pct = child_pct
                best_move = child.move
        print('Select move %s with win pct %.3f' % (best_move, best_pct))
        return best_move
# end::mcts-selection[]

# tag::mcts-uct[]
    def select_child(self, node):
        """Select a child according to the upper confidence bound for
        trees (UCT) metric.
        """
        total_rollouts = sum(child.num_rollouts for child in node.children)
        log_rollouts = math.log(total_rollouts)

        best_score = -1
        best_child = None
        # Loop over each child.
        for child in node.children:
            # Calculate the UCT score.
            win_percentage = child.winning_frac()
            exploration_factor = math.sqrt(log_rollouts / child.num_rollouts)
            uct_score = win_percentage + self.temperature * exploration_factor
            # Check if this is the largest we've seen so far.
            if uct_score > best_score:
                best_score = uct_score
                best_child = child
        return best_child
# end::mcts-uct[]

    @staticmethod  #### à changeeeeeer ################################### et ce sera bon "
    def simulate_random_game(game):
        bots = {
            Player.black: agent.FastRandomBot(),
            Player.white: agent.FastRandomBot(),
        }
        while not game.is_over():
            bot_move = bots[game.next_player].select_move(game)
            game = game.apply_move(bot_move)
        return game.winner()