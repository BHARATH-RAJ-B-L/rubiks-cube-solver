"""
Flask Web Application for Rubik's Cube Solver
Provides a web interface to demonstrate the cube solving algorithm.
"""

try:
    from flask import Flask, render_template, request, jsonify
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False
    print("Flask not available. Web interface disabled.")

from cube import RubiksCube
from solver import CubeSolver
from solver_kociemba import KociembaSolver
import json
import time

if FLASK_AVAILABLE:
    app = Flask(__name__)
    
    @app.route('/')
    def index():
        """Main page with cube solver interface"""
        return render_template('index.html')
    
    @app.route('/solve', methods=['POST'])
    def solve_cube():
        """API endpoint to solve a scrambled cube"""
        try:
            data = request.get_json()
            scramble = data.get('scramble', '').strip()
            algorithm = data.get('algorithm', 'kociemba').lower()
            
            if not scramble:
                return jsonify({'error': 'No scramble provided'}), 400
            
            # Create cube and apply scramble
            cube = RubiksCube()
            cube.apply_moves(scramble)
            
            # Choose solver based on algorithm
            if algorithm == 'kociemba':
                solver = KociembaSolver()
                solution, stats = solver.solve(cube)
                
                if 'error' in stats:
                    return jsonify({'error': stats['error']}), 400
                
                # Verify solution
                is_solved = solver.verify_solution(cube, solution)
                
                response_data = {
                    'solution': solution,
                    'move_count': stats.get('moves', 0),
                    'solve_time': stats.get('time', 0),
                    'verified': is_solved,
                    'scramble': scramble,
                    'algorithm': stats.get('algorithm', 'Kociemba'),
                    'description': stats.get('description', ''),
                    'optimal': stats.get('optimal', True)
                }
            else:
                # Fallback to layer-by-layer solver
                solver = CubeSolver()
                start_time = time.time()
                solution = solver.solve(cube)
                solve_time = time.time() - start_time
                
                # Verify solution
                cube.apply_moves(solution)
                is_solved = cube.is_solved()
                
                response_data = {
                    'solution': solution,
                    'move_count': len(solution.split()) if solution else 0,
                    'solve_time': round(solve_time, 3),
                    'verified': is_solved,
                    'scramble': scramble,
                    'algorithm': 'Layer-by-Layer',
                    'description': 'Beginner method approach',
                    'optimal': False
                }
            
            # Get cube faces for visualization (reset to scrambled state)
            visualization_cube = RubiksCube()
            visualization_cube.apply_moves(scramble)
            
            cube_visualization = {}
            for face in visualization_cube.FACES:
                cube_visualization[face] = [[visualization_cube.COLORS[cell] for cell in row] 
                                          for row in visualization_cube.faces[face]]
            
            response_data['cube_state'] = cube_visualization
            return jsonify(response_data)
            
        except ValueError as e:
            return jsonify({'error': f'Invalid scramble: {str(e)}'}), 400
        except Exception as e:
            return jsonify({'error': f'Solving error: {str(e)}'}), 500
    
    @app.route('/scramble', methods=['POST'])
    def generate_scramble():
        """Generate a random scramble sequence"""
        import random
        
        moves = ['U', 'U\'', 'U2', 'D', 'D\'', 'D2', 
                'R', 'R\'', 'R2', 'L', 'L\'', 'L2',
                'F', 'F\'', 'F2', 'B', 'B\'', 'B2']
        
        # Generate 20 random moves
        scramble_moves = []
        last_face = ''
        
        for _ in range(20):
            # Avoid consecutive moves on same face
            available_moves = [m for m in moves if m[0] != last_face]
            move = random.choice(available_moves)
            scramble_moves.append(move)
            last_face = move[0]
        
        scramble = ' '.join(scramble_moves)
        
        # Create cube state visualization
        cube = RubiksCube()
        cube.apply_moves(scramble)
        
        cube_visualization = {}
        for face in cube.FACES:
            cube_visualization[face] = [[cube.COLORS[cell] for cell in row] 
                                      for row in cube.faces[face]]
        
        return jsonify({
            'scramble': scramble,
            'cube_state': cube_visualization
        })
    
    @app.route('/validate', methods=['POST'])
    def validate_moves():
        """Validate a sequence of moves"""
        try:
            data = request.get_json()
            moves = data.get('moves', '').strip()
            
            if not moves:
                return jsonify({'valid': True, 'message': 'Empty move sequence'})
            
            # Try to apply moves to a cube
            cube = RubiksCube()
            cube.apply_moves(moves)
            
            return jsonify({
                'valid': True,
                'message': 'Valid move sequence',
                'move_count': len(moves.split())
            })
            
        except ValueError as e:
            return jsonify({
                'valid': False,
                'message': f'Invalid moves: {str(e)}'
            })
        except Exception as e:
            return jsonify({
                'valid': False,
                'message': f'Error: {str(e)}'
            })
    
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('index.html'), 404
    
    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({'error': 'Internal server error'}), 500

else:
    # Create dummy app if Flask not available
    class DummyApp:
        def run(self, **kwargs):
            print("Flask not available. Cannot start web interface.")
    
    app = DummyApp()

if __name__ == '__main__':
    if FLASK_AVAILABLE:
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        print("Flask not available. Please install Flask to use web interface.")
