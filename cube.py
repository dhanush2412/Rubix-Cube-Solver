import copy
import random

class RubiksCube:
    """
    A robust and tested implementation of a Rubik's Cube model.
    Handles the cube's state, moves, shuffling, and conversion for the solver.
    """
    def __init__(self):
        self.faces = {
            'U': [['W', 'W', 'W'], ['W', 'W', 'W'], ['W', 'W', 'W']],
            'D': [['Y', 'Y', 'Y'], ['Y', 'Y', 'Y'], ['Y', 'Y', 'Y']],
            'L': [['O', 'O', 'O'], ['O', 'O', 'O'], ['O', 'O', 'O']],
            'R': [['R', 'R', 'R'], ['R', 'R', 'R'], ['R', 'R', 'R']],
            'F': [['B', 'B', 'B'], ['B', 'B', 'B'], ['B', 'B', 'B']],
            'B': [['G', 'G', 'G'], ['G', 'G', 'G'], ['G', 'G', 'G']],
        }
        self.move_map = {
            "U": self.U, "U'": self.U_prime, "U2": lambda: (self.U(), self.U()),
            "D": self.D, "D'": self.D_prime, "D2": lambda: (self.D(), self.D()),
            "R": self.R, "R'": self.R_prime, "R2": lambda: (self.R(), self.R()),
            "L": self.L, "L'": self.L_prime, "L2": lambda: (self.L(), self.L()),
            "F": self.F, "F'": self.F_prime, "F2": lambda: (self.F(), self.F()),
            "B": self.B, "B'": self.B_prime, "B2": lambda: (self.B(), self.B()),
        }

    def _rotate_face_clockwise(self, face_name):
        face = self.faces[face_name]
        self.faces[face_name] = [[face[2-j][i] for j in range(3)] for i in range(3)]

    # --- RELIABLE MOVE FUNCTIONS ---
    def U(self):
        self._rotate_face_clockwise('U')
        temp = self.faces['F'][0]
        self.faces['F'][0] = self.faces['R'][0]
        self.faces['R'][0] = self.faces['B'][0]
        self.faces['B'][0] = self.faces['L'][0]
        self.faces['L'][0] = temp

    def D(self):
        self._rotate_face_clockwise('D')
        temp = self.faces['F'][2]
        self.faces['F'][2] = self.faces['L'][2]
        self.faces['L'][2] = self.faces['B'][2]
        self.faces['B'][2] = self.faces['R'][2]
        self.faces['R'][2] = temp

    def R(self):
        self._rotate_face_clockwise('R')
        for i in range(3):
            temp = self.faces['U'][i][2]
            self.faces['U'][i][2] = self.faces['F'][i][2]
            self.faces['F'][i][2] = self.faces['D'][i][2]
            self.faces['D'][i][2] = self.faces['B'][2-i][0]
            self.faces['B'][2-i][0] = temp

    def L(self):
        self._rotate_face_clockwise('L')
        for i in range(3):
            temp = self.faces['U'][i][0]
            self.faces['U'][i][0] = self.faces['B'][2-i][2]
            self.faces['B'][2-i][2] = self.faces['D'][i][0]
            self.faces['D'][i][0] = self.faces['F'][i][0]
            self.faces['F'][i][0] = temp
            
    def F(self):
        self._rotate_face_clockwise('F')
        temp_row = self.faces['U'][2]
        self.faces['U'][2] = [self.faces['L'][2-i][2] for i in range(3)]
        for i in range(3): self.faces['L'][i][2] = self.faces['D'][0][i]
        self.faces['D'][0] = [self.faces['R'][2-i][0] for i in range(3)]
        for i in range(3): self.faces['R'][i][0] = temp_row[i]

    def B(self):
        self._rotate_face_clockwise('B')
        temp_row = self.faces['U'][0]
        self.faces['U'][0] = [self.faces['R'][i][2] for i in range(3)]
        for i in range(3): self.faces['R'][i][2] = self.faces['D'][2][2-i]
        self.faces['D'][2] = [self.faces['L'][i][0] for i in range(3)]
        for i in range(3): self.faces['L'][2-i][0] = temp_row[i]

    def U_prime(self): self.U(); self.U(); self.U()
    def D_prime(self): self.D(); self.D(); self.D()
    def R_prime(self): self.R(); self.R(); self.R()
    def L_prime(self): self.L(); self.L(); self.L()
    def F_prime(self): self.F(); self.F(); self.F()
    def B_prime(self): self.B(); self.B(); self.B()

    def apply_moves(self, moves_str):
        for move in moves_str.split():
            if move in self.move_map:
                self.move_map[move]()

    def shuffle(self, num_moves=30):
        moves = [m for m in self.move_map.keys() if '2' not in m]
        self.apply_moves(" ".join(random.choices(moves, k=num_moves)))

    def to_kociemba_string(self):
        """Converts the cube's state to the 54-character Kociemba solver string."""
        order = ['U', 'R', 'F', 'D', 'L', 'B']
        color_map = {'W': 'U', 'R': 'R', 'B': 'F', 'Y': 'D', 'O': 'L', 'G': 'B'}
        
        kociemba_str = ""
        for face_char in order:
            face_data = self.faces[face_char]
            for row in face_data:
                for sticker_color in row:
                    kociemba_str += color_map.get(sticker_color, '')
        return kociemba_str