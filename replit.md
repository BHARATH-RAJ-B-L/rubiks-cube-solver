# Rubik's Cube Solver

## Overview

A comprehensive Python-based Rubik's Cube solver that implements both the optimal Kociemba two-phase algorithm and a layer-by-layer solving algorithm to solve any scrambled 3x3 Rubik's cube. The application features both a command-line interface for demonstration purposes and a Flask web interface with both 2D net and interactive 3D cube visualization. The system uses efficient numpy-based cube state representation and provides optimal solutions typically in 20 moves or less using the Kociemba algorithm, with a fallback to the beginner-friendly layer-by-layer method.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Core Components

**Cube State Representation**: Uses numpy arrays to efficiently represent the cube's state, with each face stored as a 3x3 integer array where integers represent colors. This approach provides fast state manipulation and comparison operations essential for the solving algorithm.

**Dual Solving Algorithms**: 
- **Kociemba Solver**: Implements the two-phase Kociemba algorithm for optimal solutions (typically ≤20 moves), using the industry-standard kociemba library for professional-grade solving performance.
- **Layer-by-Layer Solver**: Implements a beginner's method approach broken into distinct solving phases for educational purposes and as a fallback option.

**Move Engine**: Handles cube rotation mechanics through string-based move notation (U, R, F, etc.). The system parses move sequences and applies rotations to the cube state, supporting both clockwise and counter-clockwise rotations.

**Web Interface Architecture**: Flask-based web application with clean separation between backend solving logic and frontend visualization. Features both 2D cube net visualization and interactive 3D cube rendering using Three.js. The frontend uses Bootstrap for responsive design and provides real-time feedback during solving operations with algorithm selection capabilities.

### Frontend Architecture

**Single Page Application**: Built with vanilla JavaScript, HTML, and CSS using Bootstrap framework for responsive design. Features dual visualization modes (2D net and 3D interactive cube using Three.js), algorithm selection, input validation, example scrambles, and comprehensive visual feedback during solving operations.

**API Communication**: Asynchronous JavaScript handles communication with the Flask backend through JSON APIs, providing smooth user experience with loading states and error handling.

### Backend Architecture

**Stateless Design**: Each solve request creates a new cube instance and solver, ensuring thread safety and preventing state conflicts between multiple users.

**Algorithm Implementation**: 
- **Kociemba Integration**: Uses the professional kociemba library for optimal two-phase algorithm implementation
- **Pattern Storage**: Layer-by-layer solving patterns stored as string constants within the solver class, organized by solving phase (white cross, corners, middle layer, etc.)

## External Dependencies

**NumPy**: Used for efficient array operations and cube state representation. Provides fast matrix operations essential for cube state manipulation.

**Kociemba**: Professional-grade library implementing the two-phase Kociemba algorithm for optimal cube solving (typically ≤20 moves).

**Flask**: Web framework for serving the interactive interface and handling API requests. Includes template rendering and static file serving.

**Three.js**: 3D graphics library for interactive cube visualization, providing real-time 3D rendering with mouse controls.

**Bootstrap CSS Framework**: Frontend styling and responsive design components loaded via CDN.

**Font Awesome**: Icon library for user interface elements, loaded via CDN.

No database storage is required as the application operates on temporary cube states without persistence needs.