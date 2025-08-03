"""
Rubik's Cube State Representation and Move Engine
Implements efficient cube state representation and move simulation.
"""

import numpy as np
from typing import List, Dict, Tuple
import copy

class RubiksCube:
    """
    Represents a 3x3 Rubik's Cube state using efficient array-based representation.
    Each face is represented as a 3x3 numpy array with color indices.
    """
    
    # Color mapping: 0=White, 1=Yellow, 2=Red, 3=Orange, 4=Blue, 5=Green
    COLORS = ['W', 'Y', 'R', 'O', 'B', 'G']
    FACES = ['U', 'D', 'F', 'B', 'L', 'R']  # Up, Down, Front, Back, Left, Right
    
    def __init__(self):
        """Initialize a solved cube state"""
        # Each face is a 3x3 array, initialized to solved state
        self.faces = {}
        for i, face in enumerate(self.FACES):
            self.faces[face] = np.full((3, 3), i, dtype=int)
    
    def copy(self):
        """Create a deep copy of the cube"""
        new_cube = RubiksCube()
        for face in self.FACES:
            new_cube.faces[face] = self.faces[face].copy()
        return new_cube
    
    def is_solved(self) -> bool:
        """Check if the cube is in solved state"""
        for i, face in enumerate(self.FACES):
            if not np.all(self.faces[face] == i):
                return False
        return True
    
    def get_state_string(self) -> str:
        """Get a string representation of the cube state for hashing/comparison"""
        state = ""
        for face in self.FACES:
            state += "".join(str(x) for row in self.faces[face] for x in row)
        return state
    
    def display(self):
        """Display the cube in a readable format"""
        def face_to_string(face_array):
            return "\n".join(" ".join(self.COLORS[cell] for cell in row) for row in face_array)
        
        print("Cube State:")
        print("    Up (U)")
        for row in self.faces['U']:
            print("   ", " ".join(self.COLORS[cell] for cell in row))
        
        print("\nL(L) F(F) R(R) B(B)")
        for i in range(3):
            left = " ".join(self.COLORS[cell] for cell in self.faces['L'][i])
            front = " ".join(self.COLORS[cell] for cell in self.faces['F'][i])
            right = " ".join(self.COLORS[cell] for cell in self.faces['R'][i])
            back = " ".join(self.COLORS[cell] for cell in self.faces['B'][i])
            print(f"{left} {front} {right} {back}")
        
        print("\n   Down (D)")
        for row in self.faces['D']:
            print("   ", " ".join(self.COLORS[cell] for cell in row))
        print()
    
    def rotate_face_clockwise(self, face: str):
        """Rotate a face 90 degrees clockwise"""
        self.faces[face] = np.rot90(self.faces[face], -1)  # -1 for clockwise
    
    def rotate_face_counterclockwise(self, face: str):
        """Rotate a face 90 degrees counter-clockwise"""
        self.faces[face] = np.rot90(self.faces[face], 1)  # 1 for counter-clockwise
    
    def move_U(self):
        """Up face clockwise rotation"""
        self.rotate_face_clockwise('U')
        # Rotate adjacent edges
        temp = self.faces['F'][0].copy()
        self.faces['F'][0] = self.faces['R'][0]
        self.faces['R'][0] = self.faces['B'][0]
        self.faces['B'][0] = self.faces['L'][0]
        self.faces['L'][0] = temp
    
    def move_U_prime(self):
        """Up face counter-clockwise rotation"""
        self.rotate_face_counterclockwise('U')
        # Rotate adjacent edges in reverse
        temp = self.faces['F'][0].copy()
        self.faces['F'][0] = self.faces['L'][0]
        self.faces['L'][0] = self.faces['B'][0]
        self.faces['B'][0] = self.faces['R'][0]
        self.faces['R'][0] = temp
    
    def move_D(self):
        """Down face clockwise rotation"""
        self.rotate_face_clockwise('D')
        # Rotate adjacent edges
        temp = self.faces['F'][2].copy()
        self.faces['F'][2] = self.faces['L'][2]
        self.faces['L'][2] = self.faces['B'][2]
        self.faces['B'][2] = self.faces['R'][2]
        self.faces['R'][2] = temp
    
    def move_D_prime(self):
        """Down face counter-clockwise rotation"""
        self.rotate_face_counterclockwise('D')
        # Rotate adjacent edges in reverse
        temp = self.faces['F'][2].copy()
        self.faces['F'][2] = self.faces['R'][2]
        self.faces['R'][2] = self.faces['B'][2]
        self.faces['B'][2] = self.faces['L'][2]
        self.faces['L'][2] = temp
    
    def move_R(self):
        """Right face clockwise rotation"""
        self.rotate_face_clockwise('R')
        # Rotate adjacent edges
        temp = np.array([self.faces['U'][i][2] for i in range(3)])
        for i in range(3):
            self.faces['U'][i][2] = self.faces['F'][i][2]
            self.faces['F'][i][2] = self.faces['D'][i][2]
            self.faces['D'][i][2] = self.faces['B'][2-i][0]
            self.faces['B'][2-i][0] = temp[i]
    
    def move_R_prime(self):
        """Right face counter-clockwise rotation"""
        self.rotate_face_counterclockwise('R')
        # Rotate adjacent edges in reverse
        temp = np.array([self.faces['U'][i][2] for i in range(3)])
        for i in range(3):
            self.faces['U'][i][2] = self.faces['B'][2-i][0]
            self.faces['B'][2-i][0] = self.faces['D'][i][2]
            self.faces['D'][i][2] = self.faces['F'][i][2]
            self.faces['F'][i][2] = temp[i]
    
    def move_L(self):
        """Left face clockwise rotation"""
        self.rotate_face_clockwise('L')
        # Rotate adjacent edges
        temp = np.array([self.faces['U'][i][0] for i in range(3)])
        for i in range(3):
            self.faces['U'][i][0] = self.faces['B'][2-i][2]
            self.faces['B'][2-i][2] = self.faces['D'][i][0]
            self.faces['D'][i][0] = self.faces['F'][i][0]
            self.faces['F'][i][0] = temp[i]
    
    def move_L_prime(self):
        """Left face counter-clockwise rotation"""
        self.rotate_face_counterclockwise('L')
        # Rotate adjacent edges in reverse
        temp = np.array([self.faces['U'][i][0] for i in range(3)])
        for i in range(3):
            self.faces['U'][i][0] = self.faces['F'][i][0]
            self.faces['F'][i][0] = self.faces['D'][i][0]
            self.faces['D'][i][0] = self.faces['B'][2-i][2]
            self.faces['B'][2-i][2] = temp[i]
    
    def move_F(self):
        """Front face clockwise rotation"""
        self.rotate_face_clockwise('F')
        # Rotate adjacent edges
        temp = self.faces['U'][2].copy()
        self.faces['U'][2] = np.array([self.faces['L'][2-i][2] for i in range(3)])
        for i in range(3):
            self.faces['L'][i][2] = self.faces['D'][0][i]
        self.faces['D'][0] = np.array([self.faces['R'][2-i][0] for i in range(3)])
        for i in range(3):
            self.faces['R'][i][0] = temp[i]
    
    def move_F_prime(self):
        """Front face counter-clockwise rotation"""
        self.rotate_face_counterclockwise('F')
        # Rotate adjacent edges in reverse
        temp = self.faces['U'][2].copy()
        for i in range(3):
            self.faces['U'][2][i] = self.faces['R'][i][0]
        self.faces['R'][:, 0] = np.array([self.faces['D'][0][2-i] for i in range(3)])
        self.faces['D'][0] = np.array([self.faces['L'][i][2] for i in range(3)])
        for i in range(3):
            self.faces['L'][2-i][2] = temp[i]
    
    def move_B(self):
        """Back face clockwise rotation"""
        self.rotate_face_clockwise('B')
        # Rotate adjacent edges
        temp = self.faces['U'][0].copy()
        for i in range(3):
            self.faces['U'][0][i] = self.faces['R'][i][2]
        self.faces['R'][:, 2] = np.array([self.faces['D'][2][2-i] for i in range(3)])
        self.faces['D'][2] = np.array([self.faces['L'][i][0] for i in range(3)])
        for i in range(3):
            self.faces['L'][2-i][0] = temp[i]
    
    def move_B_prime(self):
        """Back face counter-clockwise rotation"""
        self.rotate_face_counterclockwise('B')
        # Rotate adjacent edges in reverse
        temp = self.faces['U'][0].copy()
        self.faces['U'][0] = np.array([self.faces['L'][2-i][0] for i in range(3)])
        for i in range(3):
            self.faces['L'][i][0] = self.faces['D'][2][i]
        self.faces['D'][2] = np.array([self.faces['R'][2-i][2] for i in range(3)])
        for i in range(3):
            self.faces['R'][i][2] = temp[i]
    
    def apply_move(self, move: str):
        """Apply a single move to the cube"""
        move = move.strip()
        if move == 'U':
            self.move_U()
        elif move == "U'":
            self.move_U_prime()
        elif move == 'D':
            self.move_D()
        elif move == "D'":
            self.move_D_prime()
        elif move == 'R':
            self.move_R()
        elif move == "R'":
            self.move_R_prime()
        elif move == 'L':
            self.move_L()
        elif move == "L'":
            self.move_L_prime()
        elif move == 'F':
            self.move_F()
        elif move == "F'":
            self.move_F_prime()
        elif move == 'B':
            self.move_B()
        elif move == "B'":
            self.move_B_prime()
        elif move == 'U2':
            self.move_U()
            self.move_U()
        elif move == 'D2':
            self.move_D()
            self.move_D()
        elif move == 'R2':
            self.move_R()
            self.move_R()
        elif move == 'L2':
            self.move_L()
            self.move_L()
        elif move == 'F2':
            self.move_F()
            self.move_F()
        elif move == 'B2':
            self.move_B()
            self.move_B()
        else:
            raise ValueError(f"Invalid move: {move}")
    
    def apply_moves(self, moves: str):
        """Apply a sequence of moves to the cube"""
        if not moves.strip():
            return
            
        move_list = moves.strip().split()
        for move in move_list:
            self.apply_move(move)
    
    def scramble(self, moves: str):
        """Apply scramble moves to the cube"""
        self.apply_moves(moves)
    
    def get_corner_orientation(self, corner_pos: Tuple[str, int, int]) -> int:
        """Get the orientation of a corner piece"""
        face, row, col = corner_pos
        return self.faces[face][row][col]
    
    def get_edge_orientation(self, edge_pos: Tuple[str, int, int]) -> int:
        """Get the orientation of an edge piece"""
        face, row, col = edge_pos
        return self.faces[face][row][col]
