#!/usr/bin/env python3
"""
Rubik's Cube Solver - Command Line Interface
A Python application that implements an algorithm to solve a standard 3x3 Rubik's Cube from any scrambled state.
"""

import sys
from cube import RubiksCube
from solver import CubeSolver

def print_banner():
    """Print application banner"""
    print("=" * 60)
    print("           RUBIK'S CUBE SOLVER")
    print("    Solving 3x3 Rubik's Cube from any scrambled state")
    print("=" * 60)
    print()

def print_moves_notation():
    """Print the standard move notation"""
    print("Standard Move Notation:")
    print("U - Up face clockwise        U' - Up face counter-clockwise")
    print("D - Down face clockwise      D' - Down face counter-clockwise") 
    print("R - Right face clockwise     R' - Right face counter-clockwise")
    print("L - Left face clockwise      L' - Left face counter-clockwise")
    print("F - Front face clockwise     F' - Front face counter-clockwise")
    print("B - Back face clockwise      B' - Back face counter-clockwise")
    print()

def demonstrate_solver():
    """Demonstrate the cube solver with examples"""
    print("DEMONSTRATION: Solving scrambled cubes")
    print("-" * 40)
    
    # Example scrambles to demonstrate
    scrambles = [
        "R U R' F R F'",
        "R U R' U R U2 R'",
        "F R U' R' U' R U R' F'",
        "R U R' U' R' F R2 U' R' U' R U R' F'"
    ]
    
    solver = CubeSolver()
    
    for i, scramble in enumerate(scrambles, 1):
        print(f"\nExample {i}: Scramble = {scramble}")
        print("-" * 30)
        
        # Create solved cube and apply scramble
        cube = RubiksCube()
        cube.apply_moves(scramble)
        
        print("Scrambled state:")
        cube.display()
        
        # Solve the cube
        solution = solver.solve(cube)
        
        print(f"\nSolution ({len(solution.split())} moves): {solution}")
        
        # Verify solution
        cube.apply_moves(solution)
        if cube.is_solved():
            print("✓ Cube successfully solved!")
        else:
            print("✗ Solution verification failed!")
        
        print("-" * 30)

def interactive_mode():
    """Interactive mode for user input"""
    print("\nINTERACTIVE MODE")
    print("Enter your scramble sequence (or 'quit' to exit):")
    print("Example: R U R' F R F'")
    print()
    
    solver = CubeSolver()
    
    while True:
        try:
            scramble = input("Scramble > ").strip()
            
            if scramble.lower() in ['quit', 'exit', 'q']:
                break
                
            if not scramble:
                continue
                
            # Create solved cube and apply scramble
            cube = RubiksCube()
            print(f"\nApplying scramble: {scramble}")
            
            try:
                cube.apply_moves(scramble)
            except ValueError as e:
                print(f"Error: {e}")
                continue
                
            print("\nScrambled cube state:")
            cube.display()
            
            print("\nSolving...")
            solution = solver.solve(cube)
            
            print(f"\nSolution ({len(solution.split())} moves):")
            print(solution)
            
            # Verify solution
            cube.apply_moves(solution)
            if cube.is_solved():
                print("✓ Solution verified successfully!")
            else:
                print("✗ Solution verification failed!")
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")
    
    print("\nGoodbye!")

def main():
    """Main application entry point"""
    print_banner()
    
    if len(sys.argv) > 1:
        # Command line mode with scramble argument
        scramble = ' '.join(sys.argv[1:])
        print(f"Solving scramble: {scramble}")
        print()
        
        solver = CubeSolver()
        cube = RubiksCube()
        
        try:
            cube.apply_moves(scramble)
            print("Scrambled state:")
            cube.display()
            
            solution = solver.solve(cube)
            print(f"\nSolution ({len(solution.split())} moves): {solution}")
            
            # Verify solution
            cube.apply_moves(solution)
            if cube.is_solved():
                print("✓ Cube successfully solved!")
            else:
                print("✗ Solution verification failed!")
                
        except ValueError as e:
            print(f"Error: {e}")
            
    else:
        # Auto-start web interface for replit environment
        print("\nStarting web interface...")
        print("Open http://localhost:5000 in your browser")
        try:
            from app import app
            app.run(host='0.0.0.0', port=5000, debug=False)
        except ImportError:
            print("Error: Flask not available for web interface")
            print("\nFalling back to interactive mode...")
            print_moves_notation()
            interactive_mode()

if __name__ == "__main__":
    main()
