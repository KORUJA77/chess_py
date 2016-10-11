# -*- coding: utf-8 -*-

"""
Class that holds state of a game.

Takes two subclasses of Player as defined
in chess_py.players.player.Player, and calls 
``generate_move(position)``
from each of the players and updates the board using 
each corresponding result.

Start game using play(), which returns the result 
(1 - white wins, 0 - black wins, 0.5 - draw)
when the game is finished.

Copyright © 2016 Aubhro Sengupta. All rights reserved.
"""

from chess_py.core.board import Board
from chess_py.core import color
from chess_py.game import game_state
from chess_py.core.algebraic.converter import make_legal
import itertools


class Game:
    def __init__(self, player_white, player_black):
        """
        Creates new game given the players.

        :type player_white: Player
        :type player_black: Player
        """
        self.player_white = player_white
        self.player_black = player_black
        self.position = Board.init_default()

    def play(self):
        """
        Starts game and returns one of 3 results . 
        Iterates between methods ``white_move()`` and
        ``black_move()`` until game ends. Each
        method calls the respective player's ``generate_move()``
        method.

        :rtype: int
        """
        colors = [lambda: self.white_move(), lambda: self.black_move()]
        colors = itertools.cycle(colors)

        while True:
            color_fn = next(colors)
            if game_state.no_moves(self.position):
                if game_state.is_checkmate(self.position, color.white):
                    return 1

                elif game_state.is_checkmate(self.position, color.black):
                    return 0

                else:
                    return 0.5

            color_fn()

    def white_move(self):
        """
        Calls the white player's ``generate_move()``
        method and updates the board with the move returned.
        """
        move = self.player_white.generate_move(self.position)
        move = make_legal(move, self.position)
        self.position.update(move)

    def black_move(self):
        """
        Calls the black player's ``generate_move()``
        method and updates the board with the move returned.
        """
        move = self.player_black.generate_move(self.position)
        move = make_legal(move, self.position)
        self.position.update(move)

    def all_possible_moves(self, input_color):
        """
        Finds all possible moves a particular player can
        play during a game. Calling this method is recommended over
        calling the ``all_possible_moves(input_color)``
        from this ``Board`` directly.
        """
        return self.position.all_possible_moves(input_color)
