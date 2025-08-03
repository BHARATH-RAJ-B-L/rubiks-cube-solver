"""
Rubik's Cube Solver Algorithm
Implements a layer-by-layer solving approach for any scrambled 3x3 Rubik's Cube.
"""

from cube import RubiksCube
from typing import List, Dict, Tuple, Optional
import copy

class CubeSolver:
    """
    Implements a layer-by-layer solving algorithm for 3x3 Rubik's Cube.
    Uses a simplified version of the beginner's method with optimized algorithms.
    """
    
    def __init__(self):
        """Initialize the solver with algorithm patterns"""
        # White cross algorithms (F2L preparation)
        self.white_cross_patterns = {
            'edge_flip': "F R U R' U' F'",
            'edge_position': "R U R' F R F'"
        }
        
        # White corners algorithms
        self.white_corner_patterns = {
            'right_hand': "R U R' U' R U R'",
            'left_hand': "L' U' L U L' U' L",
            'corner_flip': "R U R' U' R U R' U' R U R'"
        }
        
        # Middle layer algorithms
        self.middle_layer_patterns = {
            'right_insert': "U R U' R' U' F' U F",
            'left_insert': "U' L' U L U F U' F'"
        }
        
        # Yellow cross algorithms (OLL)
        self.yellow_cross_patterns = {
            'line': "F R U R' U' F'",
            'L_shape': "F U R U' R' F'",
            'dot': "F R U R' U' F' U F R U R' U' F'"
        }
        
        # Yellow corners algorithms (OLL)
        self.yellow_corner_patterns = {
            'sune': "R U R' U R U2 R'",
            'antisune': "R U2 R' U' R U' R'",
            'pi': "R U2 R2 U' R2 U' R2 U2 R",
            'h': "R U R' U R U' R' U R U2 R'"
        }
        
        # PLL algorithms
        self.pll_patterns = {
            'adjacent_swap': "R U R' F' R U R' U' R' F R2 U' R'",
            'diagonal_swap': "F R U' R' U' R U R' F' R U R' U' R' F R F'",
            'clockwise_cycle': "R' F R' B2 R F' R' B2 R2",
            'counterclockwise_cycle': "R2 B2 R F R' B2 R F' R"
        }
    
    def solve(self, cube: RubiksCube) -> str:
        """
        Solve the Rubik's cube from any scrambled state.
        Returns the solution as a string of moves.
        """
        if cube.is_solved():
            return ""
        
        solution_moves = []
        working_cube = cube.copy()
        
        # Step 1: Solve white cross (bottom layer edges)
        cross_moves = self._solve_white_cross(working_cube)
        solution_moves.extend(cross_moves)
        
        # Step 2: Solve white corners (complete bottom layer)
        corner_moves = self._solve_white_corners(working_cube)
        solution_moves.extend(corner_moves)
        
        # Step 3: Solve middle layer edges
        middle_moves = self._solve_middle_layer(working_cube)
        solution_moves.extend(middle_moves)
        
        # Step 4: Solve yellow cross (top layer edges orientation)
        yellow_cross_moves = self._solve_yellow_cross(working_cube)
        solution_moves.extend(yellow_cross_moves)
        
        # Step 5: Solve yellow corners orientation
        yellow_corners_moves = self._solve_yellow_corners(working_cube)
        solution_moves.extend(yellow_corners_moves)
        
        # Step 6: Permute last layer (PLL)
        pll_moves = self._solve_pll(working_cube)
        solution_moves.extend(pll_moves)
        
        return " ".join(solution_moves)
    
    def _solve_white_cross(self, cube: RubiksCube) -> List[str]:
        """Solve the white cross on the bottom (D face)"""
        moves = []
        max_attempts = 50
        
        for attempt in range(max_attempts):
            if self._is_white_cross_solved(cube):
                break
                
            # Simple approach: get white edge pieces to bottom
            for face in ['F', 'R', 'B', 'L']:
                face_idx = cube.FACES.index(face)
                
                # Check if white edge is on top and needs to come down
                if cube.faces['U'][1][0] == 0:  # White on top-left edge
                    moves.extend(['L', 'F', 'L\''])
                    cube.apply_moves('L F L\'')
                elif cube.faces['U'][0][1] == 0:  # White on top-front edge
                    moves.extend(['F', 'F'])
                    cube.apply_moves('F F')
                elif cube.faces['U'][1][2] == 0:  # White on top-right edge
                    moves.extend(['R\'', 'F', 'R'])
                    cube.apply_moves('R\' F R')
                elif cube.faces['U'][2][1] == 0:  # White on top-back edge
                    moves.extend(['U'])
                    cube.apply_moves('U')
                
                # Rotate to check next position
                moves.append('U')
                cube.apply_move('U')
        
        return moves
    
    def _is_white_cross_solved(self, cube: RubiksCube) -> bool:
        """Check if white cross is solved on bottom face"""
        return (cube.faces['D'][0][1] == 0 and  # Top edge
                cube.faces['D'][1][0] == 0 and  # Left edge
                cube.faces['D'][1][2] == 0 and  # Right edge
                cube.faces['D'][2][1] == 0)     # Bottom edge
    
    def _solve_white_corners(self, cube: RubiksCube) -> List[str]:
        """Solve white corners to complete the first layer"""
        moves = []
        max_attempts = 50
        
        for attempt in range(max_attempts):
            if self._is_first_layer_solved(cube):
                break
            
            # Find white corner pieces and position them
            corner_positions = [(0,0), (0,2), (2,0), (2,2)]  # Corner positions on U face
            
            for pos in corner_positions:
                row, col = pos
                if cube.faces['U'][row][col] == 0:  # Found white corner on top
                    # Apply right-hand algorithm to move it down
                    algorithm = self.white_corner_patterns['right_hand']
                    moves.extend(algorithm.split())
                    cube.apply_moves(algorithm)
                    break
            else:
                # No white corner on top, rotate top face
                moves.append('U')
                cube.apply_move('U')
        
        return moves
    
    def _is_first_layer_solved(self, cube: RubiksCube) -> bool:
        """Check if the entire first layer (white face) is solved"""
        return bool(np.all(cube.faces['D'] == 0))
    
    def _solve_middle_layer(self, cube: RubiksCube) -> List[str]:
        """Solve the middle layer edges"""
        moves = []
        max_attempts = 100
        
        for attempt in range(max_attempts):
            if self._is_middle_layer_solved(cube):
                break
            
            # Look for edge pieces on top that belong in middle layer
            edge_positions = [(0,1), (1,0), (1,2), (2,1)]  # Edge positions on U face
            
            for pos in edge_positions:
                row, col = pos
                if cube.faces['U'][row][col] != 1:  # Not yellow, belongs in middle
                    # Apply appropriate insertion algorithm
                    if col == 2:  # Right edge
                        algorithm = self.middle_layer_patterns['right_insert']
                    else:  # Left edge  
                        algorithm = self.middle_layer_patterns['left_insert']
                    
                    moves.extend(algorithm.split())
                    cube.apply_moves(algorithm)
                    break
            else:
                # Rotate top to find more pieces
                moves.append('U')
                cube.apply_move('U')
        
        return moves
    
    def _is_middle_layer_solved(self, cube: RubiksCube) -> bool:
        """Check if middle layer is solved"""
        # Simplified check - middle edges in correct colors
        middle_positions = [(1,0), (1,2)]  # Left and right middle edges
        for face in ['F', 'R', 'B', 'L']:
            face_idx = cube.FACES.index(face)
            for pos in middle_positions:
                row, col = pos
                if cube.faces[face][row][col] == 1:  # Yellow in middle layer
                    return False
        return True
    
    def _solve_yellow_cross(self, cube: RubiksCube) -> List[str]:
        """Create yellow cross on top face"""
        moves = []
        max_attempts = 20
        
        for attempt in range(max_attempts):
            if self._is_yellow_cross_formed(cube):
                break
            
            # Check current yellow cross pattern
            yellow_pattern = self._get_yellow_cross_pattern(cube)
            
            if yellow_pattern == 'dot':
                algorithm = self.yellow_cross_patterns['dot']
            elif yellow_pattern == 'line':
                algorithm = self.yellow_cross_patterns['line']
            elif yellow_pattern == 'L':
                algorithm = self.yellow_cross_patterns['L_shape']
            else:
                algorithm = self.yellow_cross_patterns['line']  # Default
            
            moves.extend(algorithm.split())
            cube.apply_moves(algorithm)
        
        return moves
    
    def _is_yellow_cross_formed(self, cube: RubiksCube) -> bool:
        """Check if yellow cross is formed on top face"""
        return (cube.faces['U'][0][1] == 1 and  # Top edge
                cube.faces['U'][1][0] == 1 and  # Left edge
                cube.faces['U'][1][2] == 1 and  # Right edge
                cube.faces['U'][2][1] == 1)     # Bottom edge
    
    def _get_yellow_cross_pattern(self, cube: RubiksCube) -> str:
        """Identify the current yellow cross pattern"""
        edges = [cube.faces['U'][0][1], cube.faces['U'][1][0], 
                cube.faces['U'][1][2], cube.faces['U'][2][1]]
        yellow_count = sum(1 for edge in edges if edge == 1)
        
        if yellow_count == 0:
            return 'dot'
        elif yellow_count == 2:
            # Check if line or L-shape
            if (cube.faces['U'][0][1] == 1 and cube.faces['U'][2][1] == 1) or \
               (cube.faces['U'][1][0] == 1 and cube.faces['U'][1][2] == 1):
                return 'line'
            else:
                return 'L'
        else:
            return 'cross'
    
    def _solve_yellow_corners(self, cube: RubiksCube) -> List[str]:
        """Orient yellow corners on top face"""
        moves = []
        max_attempts = 50
        
        for attempt in range(max_attempts):
            if self._is_top_face_yellow(cube):
                break
            
            # Apply Sune algorithm or variants
            corner_pattern = self._get_yellow_corner_pattern(cube)
            
            if corner_pattern in self.yellow_corner_patterns:
                algorithm = self.yellow_corner_patterns[corner_pattern]
            else:
                algorithm = self.yellow_corner_patterns['sune']  # Default
            
            moves.extend(algorithm.split())
            cube.apply_moves(algorithm)
        
        return moves
    
    def _is_top_face_yellow(self, cube: RubiksCube) -> bool:
        """Check if entire top face is yellow"""
        return bool(np.all(cube.faces['U'] == 1))
    
    def _get_yellow_corner_pattern(self, cube: RubiksCube) -> str:
        """Identify yellow corner pattern for OLL"""
        corners = [cube.faces['U'][0][0], cube.faces['U'][0][2],
                  cube.faces['U'][2][0], cube.faces['U'][2][2]]
        yellow_corners = sum(1 for corner in corners if corner == 1)
        
        if yellow_corners == 1:
            return 'sune'
        elif yellow_corners == 2:
            return 'antisune'
        else:
            return 'pi'
    
    def _solve_pll(self, cube: RubiksCube) -> List[str]:
        """Permute last layer (position pieces correctly)"""
        moves = []
        max_attempts = 50
        
        for attempt in range(max_attempts):
            if cube.is_solved():
                break
            
            # Check if corners need swapping
            if not self._are_corners_positioned(cube):
                algorithm = self.pll_patterns['adjacent_swap']
                moves.extend(algorithm.split())
                cube.apply_moves(algorithm)
            
            # Check if edges need swapping  
            elif not self._are_edges_positioned(cube):
                algorithm = self.pll_patterns['clockwise_cycle']
                moves.extend(algorithm.split())
                cube.apply_moves(algorithm)
            
            else:
                # Just rotate top face to align
                moves.append('U')
                cube.apply_move('U')
        
        return moves
    
    def _are_corners_positioned(self, cube: RubiksCube) -> bool:
        """Check if last layer corners are in correct positions"""
        # Simplified check - look for matching corner colors
        for face in ['F', 'R', 'B', 'L']:
            face_idx = cube.FACES.index(face)
            if (cube.faces[face][0][0] == face_idx and 
                cube.faces[face][0][2] == face_idx):
                continue
            else:
                return False
        return True
    
    def _are_edges_positioned(self, cube: RubiksCube) -> bool:
        """Check if last layer edges are in correct positions"""
        # Simplified check - look for matching edge colors
        for face in ['F', 'R', 'B', 'L']:
            face_idx = cube.FACES.index(face)
            if cube.faces[face][0][1] == face_idx:
                continue
            else:
                return False
        return True

# Import numpy for array operations
import numpy as np
