/**
 * Rubik's Cube Solver - Frontend JavaScript
 * Handles user interactions and API communication
 */

class CubeSolverApp {
    constructor() {
        this.isLoading = false;
        this.currentScramble = '';
        this.initializeEventListeners();
        this.resetCubeVisualization();
    }

    initializeEventListeners() {
        // Main action buttons
        document.getElementById('solveBtn').addEventListener('click', () => this.solveCube());
        document.getElementById('scrambleBtn').addEventListener('click', () => this.generateScramble());
        document.getElementById('resetBtn').addEventListener('click', () => this.resetCube());
        document.getElementById('validateBtn').addEventListener('click', () => this.validateMoves());

        // Example scramble buttons
        document.querySelectorAll('.load-example').forEach(button => {
            button.addEventListener('click', (e) => {
                const scramble = e.target.getAttribute('data-scramble');
                this.loadExampleScramble(scramble);
            });
        });

        // Enter key support for scramble input
        document.getElementById('scrambleInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.solveCube();
            }
        });

        // Real-time validation on input change
        document.getElementById('scrambleInput').addEventListener('input', () => {
            this.clearValidationFeedback();
        });
    }

    async solveCube() {
        if (this.isLoading) return;

        const scrambleInput = document.getElementById('scrambleInput');
        const scramble = scrambleInput.value.trim();

        if (!scramble) {
            this.showError('Please enter a scramble sequence');
            return;
        }

        this.setLoading(true);
        this.hideSolution();

        try {
            const response = await fetch('/solve', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ scramble: scramble })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Failed to solve cube');
            }

            this.displaySolution(data);
            this.updateCubeVisualization(data.cube_state);
            this.currentScramble = scramble;

            // Add success animation
            this.addSuccessAnimation();

        } catch (error) {
            this.showError(`Error: ${error.message}`);
        } finally {
            this.setLoading(false);
        }
    }

    async generateScramble() {
        if (this.isLoading) return;

        this.setLoading(true);

        try {
            const response = await fetch('/scramble', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Failed to generate scramble');
            }

            document.getElementById('scrambleInput').value = data.scramble;
            this.updateCubeVisualization(data.cube_state);
            this.hideSolution();
            this.clearValidationFeedback();

            this.showSuccess('Random scramble generated!');

        } catch (error) {
            this.showError(`Error: ${error.message}`);
        } finally {
            this.setLoading(false);
        }
    }

    async validateMoves() {
        const scrambleInput = document.getElementById('scrambleInput');
        const moves = scrambleInput.value.trim();

        if (!moves) {
            this.showValidationFeedback('Empty move sequence', 'success');
            return;
        }

        try {
            const response = await fetch('/validate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ moves: moves })
            });

            const data = await response.json();

            if (data.valid) {
                this.showValidationFeedback(`✓ Valid sequence (${data.move_count} moves)`, 'success');
            } else {
                this.showValidationFeedback(`✗ ${data.message}`, 'error');
            }

        } catch (error) {
            this.showValidationFeedback(`✗ Validation failed: ${error.message}`, 'error');
        }
    }

    loadExampleScramble(scramble) {
        document.getElementById('scrambleInput').value = scramble;
        this.hideSolution();
        this.clearValidationFeedback();
        this.showSuccess(`Loaded example: ${scramble}`);
    }

    resetCube() {
        document.getElementById('scrambleInput').value = '';
        this.resetCubeVisualization();
        this.hideSolution();
        this.clearValidationFeedback();
        this.showSuccess('Cube reset to solved state');
    }

    displaySolution(data) {
        const solutionCard = document.getElementById('solutionCard');
        const solutionResult = document.getElementById('solutionResult');

        let html = `
            <div class="solution-stats">
                <div class="row text-center">
                    <div class="col-md-3">
                        <strong>${data.move_count}</strong><br>
                        <small class="text-muted">Moves</small>
                    </div>
                    <div class="col-md-3">
                        <strong>${data.solve_time}s</strong><br>
                        <small class="text-muted">Solve Time</small>
                    </div>
                    <div class="col-md-3">
                        <strong>${data.verified ? '✓' : '✗'}</strong><br>
                        <small class="text-muted">Verified</small>
                    </div>
                    <div class="col-md-3">
                        <strong>Layer-by-Layer</strong><br>
                        <small class="text-muted">Algorithm</small>
                    </div>
                </div>
            </div>
        `;

        if (data.solution) {
            html += `
                <div class="solution-moves">
                    <strong>Solution Sequence:</strong><br>
                    ${this.formatMoveSequence(data.solution)}
                </div>
            `;
        } else {
            html += `
                <div class="alert alert-info">
                    <i class="fas fa-info-circle me-2"></i>
                    Cube is already solved!
                </div>
            `;
        }

        html += `
            <div class="mt-3">
                <small class="text-muted">
                    <strong>Scramble:</strong> ${data.scramble}<br>
                    <strong>Status:</strong> ${data.verified ? 'Solution verified successfully' : 'Solution verification failed'}
                </small>
            </div>
        `;

        solutionResult.innerHTML = html;
        solutionCard.style.display = 'block';

        // Scroll to solution
        solutionCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    formatMoveSequence(moves) {
        return moves.split(' ').map(move => 
            `<span class="move-highlight">${move}</span>`
        ).join(' ');
    }

    updateCubeVisualization(cubeState) {
        const faces = ['U', 'D', 'F', 'B', 'L', 'R'];
        
        faces.forEach(face => {
            const faceElement = document.getElementById(`face-${face}`);
            const cells = faceElement.querySelectorAll('.cube-cell');
            
            let cellIndex = 0;
            for (let row = 0; row < 3; row++) {
                for (let col = 0; col < 3; col++) {
                    const color = cubeState[face][row][col];
                    cells[cellIndex].setAttribute('data-color', color);
                    cellIndex++;
                }
            }
        });
    }

    resetCubeVisualization() {
        const faceColors = {
            'U': 'W', // Up - White
            'D': 'Y', // Down - Yellow  
            'F': 'R', // Front - Red
            'B': 'O', // Back - Orange
            'L': 'B', // Left - Blue
            'R': 'G'  // Right - Green
        };

        Object.keys(faceColors).forEach(face => {
            const faceElement = document.getElementById(`face-${face}`);
            const cells = faceElement.querySelectorAll('.cube-cell');
            
            cells.forEach(cell => {
                cell.setAttribute('data-color', faceColors[face]);
            });
        });
    }

    setLoading(loading) {
        this.isLoading = loading;
        const loadingIndicator = document.getElementById('loadingIndicator');
        const solveBtn = document.getElementById('solveBtn');
        const scrambleBtn = document.getElementById('scrambleBtn');

        if (loading) {
            loadingIndicator.style.display = 'block';
            solveBtn.disabled = true;
            scrambleBtn.disabled = true;
            solveBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Solving...';
        } else {
            loadingIndicator.style.display = 'none';
            solveBtn.disabled = false;
            scrambleBtn.disabled = false;
            solveBtn.innerHTML = '<i class="fas fa-magic me-2"></i>Solve Cube';
        }
    }

    showValidationFeedback(message, type) {
        const feedbackElement = document.getElementById('validation-feedback');
        feedbackElement.innerHTML = `<div class="validation-${type}">${message}</div>`;
    }

    clearValidationFeedback() {
        const feedbackElement = document.getElementById('validation-feedback');
        feedbackElement.innerHTML = '';
    }

    hideSolution() {
        document.getElementById('solutionCard').style.display = 'none';
    }

    showError(message) {
        this.showToast(message, 'error');
    }

    showSuccess(message) {
        this.showToast(message, 'success');
    }

    showToast(message, type) {
        // Create toast element
        const toast = document.createElement('div');
        toast.className = `alert alert-${type === 'error' ? 'danger' : 'success'} position-fixed`;
        toast.style.cssText = `
            top: 20px;
            right: 20px;
            z-index: 9999;
            min-width: 300px;
            opacity: 0;
            transition: opacity 0.3s ease;
        `;
        
        toast.innerHTML = `
            <i class="fas fa-${type === 'error' ? 'exclamation-triangle' : 'check-circle'} me-2"></i>
            ${message}
        `;

        document.body.appendChild(toast);

        // Fade in
        setTimeout(() => {
            toast.style.opacity = '1';
        }, 100);

        // Remove after 3 seconds
        setTimeout(() => {
            toast.style.opacity = '0';
            setTimeout(() => {
                if (toast.parentNode) {
                    toast.parentNode.removeChild(toast);
                }
            }, 300);
        }, 3000);
    }

    addSuccessAnimation() {
        const cubeContainer = document.querySelector('.cube-container');
        cubeContainer.classList.add('success-animation');
        
        setTimeout(() => {
            cubeContainer.classList.remove('success-animation');
        }, 600);
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new CubeSolverApp();
});

// Add some utility functions for enhanced user experience
document.addEventListener('DOMContentLoaded', () => {
    // Add keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        if (e.ctrlKey || e.metaKey) {
            switch(e.key) {
                case 'Enter':
                    e.preventDefault();
                    document.getElementById('solveBtn').click();
                    break;
                case 'r':
                    e.preventDefault();
                    document.getElementById('scrambleBtn').click();
                    break;
                case 'Backspace':
                    e.preventDefault();
                    document.getElementById('resetBtn').click();
                    break;
            }
        }
    });

    // Add tooltips for keyboard shortcuts
    const tooltips = {
        'solveBtn': 'Ctrl+Enter to solve',
        'scrambleBtn': 'Ctrl+R to scramble',
        'resetBtn': 'Ctrl+Backspace to reset'
    };

    Object.keys(tooltips).forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            element.title = tooltips[id];
        }
    });
});
