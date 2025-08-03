# Rubik's Cube Solver

## Overview

A comprehensive Python-based Rubik's Cube solver that implements a layer-by-layer solving algorithm to solve any scrambled 3x3 Rubik's cube. The application features both a command-line interface for demonstration purposes and a Flask web interface for interactive solving. The system uses efficient numpy-based cube state representation and implements standard cubing algorithms to systematically solve the cube through multiple phases: white cross, white corners, middle layer, yellow cross, and final positioning.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Core Components

**Cube State Representation**: Uses numpy arrays to efficiently represent the cube's state, with each face stored as a 3x3 integer array where integers represent colors. This approach provides fast state manipulation and comparison operations essential for the solving algorithm.

**Layer-by-Layer Solver**: Implements a beginner's method approach broken into distinct solving phases. Each phase uses predefined algorithm patterns stored as move sequences, allowing the solver to systematically progress through the cube solution without complex lookahead algorithms.

**Move Engine**: Handles cube rotation mechanics through string-based move notation (U, R, F, etc.). The system parses move sequences and applies rotations to the cube state, supporting both clockwise and counter-clockwise rotations.

**Web Interface Architecture**: Flask-based web application with a clean separation between backend solving logic and frontend visualization. The frontend uses Bootstrap for responsive design and provides real-time feedback during solving operations.

### Frontend Architecture

**Single Page Application**: Built with vanilla JavaScript, HTML, and CSS using Bootstrap framework for responsive design. The interface provides input validation, example scrambles, and visual feedback during solving operations.

**API Communication**: Asynchronous JavaScript handles communication with the Flask backend through JSON APIs, providing smooth user experience with loading states and error handling.

### Backend Architecture

**Stateless Design**: Each solve request creates a new cube instance and solver, ensuring thread safety and preventing state conflicts between multiple users.

**Algorithm Storage**: Solving patterns are stored as string constants within the solver class, organized by solving phase (white cross, corners, middle layer, etc.).

## External Dependencies

**NumPy**: Used for efficient array operations and cube state representation. Provides fast matrix operations essential for cube state manipulation.

**Flask**: Web framework for serving the interactive interface and handling API requests. Includes template rendering and static file serving.

**Bootstrap CSS Framework**: Frontend styling and responsive design components loaded via CDN.

**Font Awesome**: Icon library for user interface elements, loaded via CDN.

No database storage is required as the application operates on temporary cube states without persistence needs.