"""
Kociemba Algorithm Solver for Rubik's Cube
Uses the two-phase Kociemba algorithm for optimal solving (typically 20 moves or less).
"""

import kociemba
from cube import RubiksCube
from typing import Optional, Tuple
import time

class KociembaSolver:
    """
    Advanced Rubik's Cube solver using the Kociemba two-phase algorithm.
    This provides much more efficient solutions than the layer-by-layer method.
    """
    
    def __init__(self):
        """Initialize the Kociemba solver"""
        self.color_to_kociemba = {
            'U': 'U',  # Up (White) -> U
            'D': 'D',  # Down (Yellow) -> D  
            'F': 'F',  # Front (Red) -> F
            'B': 'B',  # Back (Orange) -> B
            'L': 'L',  # Left (Blue) -> L
            'R': 'R'   # Right (Green) -> R
        }
        
        # Kociemba face order: U R F D L B
        self.face_order = ['U', 'R', 'F', 'D', 'L', 'B']
        
    def cube_to_kociemba_string(self, cube: RubiksCube) -> str:
        """
        Convert cube state to Kociemba string format.
        Kociemba expects a 54-character string representing the cube state.
        """
        # Map our color indices to face letters
        color_to_face = {0: 'U', 1: 'D', 2: 'F', 3: 'B', 4: 'L', 5: 'R'}
        
        kociemba_string = ""
        
        # Process faces in Kociemba order: U R F D L B
        face_mapping = {
            'U': cube.faces['U'],  # Up (White)
            'R': cube.faces['R'],  # Right (Green) 
            'F': cube.faces['F'],  # Front (Red)
            'D': cube.faces['D'],  # Down (Yellow)
            'L': cube.faces['L'],  # Left (Blue)
            'B': cube.faces['B']   # Back (Orange)
        }
        
        for face_name in self.face_order:
            face_array = face_mapping[face_name]
            for row in range(3):
                for col in range(3):
                    color_index = face_array[row][col]
                    kociemba_string += color_to_face[color_index]
        
        return kociemba_string
    
    def solve(self, cube: RubiksCube) -> Tuple[str, dict]:
        """
        Solve the cube using Kociemba algorithm.
        Returns the solution string and solving statistics.
        """
        if cube.is_solved():
            return "", {"moves": 0, "algorithm": "Already solved", "time": 0}
        
        try:
            # Convert cube to Kociemba format
            kociemba_string = self.cube_to_kociemba_string(cube)
            
            # Solve using Kociemba algorithm
            start_time = time.time()
            solution = kociemba.solve(kociemba_string)
            solve_time = time.time() - start_time
            
            if solution == "Error: Invalid cube state":
                return "", {"error": "Invalid cube state - cannot solve"}
            
            # Parse solution
            moves = solution.split() if solution else []
            
            return solution, {
                "moves": len(moves),
                "algorithm": "Kociemba Two-Phase",
                "time": round(solve_time, 3),
                "optimal": True,
                "description": "Uses God's Number algorithm (≤20 moves)"
            }
            
        except Exception as e:
            return "", {"error": f"Kociemba solver error: {str(e)}"}
    
    def verify_solution(self, cube: RubiksCube, solution: str) -> bool:
        """Verify that the solution actually solves the cube"""
        if not solution:
            return cube.is_solved()
        
        try:
            test_cube = cube.copy()
            test_cube.apply_moves(solution)
            return test_cube.is_solved()
        except Exception:
            return False
    
    def get_solve_statistics(self, solution: str) -> dict:
        """Get detailed statistics about the solution"""
        if not solution:
            return {"moves": 0, "quarter_turns": 0, "face_turns": 0}
        
        moves = solution.split()
        quarter_turns = 0
        face_turns = 0
        
        for move in moves:
            if "2" in move:
                quarter_turns += 2
            else:
                quarter_turns += 1
            face_turns += 1
        
        return {
            "moves": len(moves),
            "quarter_turns": quarter_turns,
            "face_turns": face_turns,
            "efficiency": "Optimal" if len(moves) <= 20 else "Near-optimal"
        }