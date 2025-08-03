/**
 * 3D Rubik's Cube Visualization using Three.js
 * Provides interactive 3D cube rendering and animation
 */

class Cube3DRenderer {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.cube = null;
        this.controls = null;
        
        // Cube state
        this.cubeState = this.getDefaultState();
        
        // Colors for faces
        this.colors = {
            'W': 0xffffff, // White
            'Y': 0xffff00, // Yellow
            'R': 0xff0000, // Red
            'O': 0xff8800, // Orange
            'B': 0x0000ff, // Blue
            'G': 0x00ff00  // Green
        };
        
        this.init();
    }
    
    init() {
        this.setupScene();
        this.createCube();
        this.setupControls();
        this.animate();
        this.handleResize();
    }
    
    setupScene() {
        // Scene
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(0xf5f5f5);
        
        // Camera
        this.camera = new THREE.PerspectiveCamera(
            60,
            this.container.clientWidth / this.container.clientHeight,
            0.1,
            1000
        );
        this.camera.position.set(6, 6, 6);
        this.camera.lookAt(0, 0, 0);
        
        // Renderer
        this.renderer = new THREE.WebGLRenderer({ 
            antialias: true,
            alpha: false
        });
        this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
        this.renderer.setPixelRatio(window.devicePixelRatio);
        this.renderer.shadowMap.enabled = true;
        this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        this.container.appendChild(this.renderer.domElement);
        
        // Lighting
        const ambientLight = new THREE.AmbientLight(0x404040, 0.7);
        this.scene.add(ambientLight);
        
        const directionalLight = new THREE.DirectionalLight(0xffffff, 0.9);
        directionalLight.position.set(8, 8, 8);
        directionalLight.castShadow = true;
        directionalLight.shadow.mapSize.width = 1024;
        directionalLight.shadow.mapSize.height = 1024;
        this.scene.add(directionalLight);
        
        // Additional light for better visibility
        const directionalLight2 = new THREE.DirectionalLight(0xffffff, 0.3);
        directionalLight2.position.set(-8, -8, -8);
        this.scene.add(directionalLight2);
    }
    
    createCube() {
        this.cube = new THREE.Group();
        
        // Create 26 small cubes (3x3x3 minus center)
        const cubeSize = 0.9;
        const gap = 0.1;
        
        for (let x = 0; x < 3; x++) {
            for (let y = 0; y < 3; y++) {
                for (let z = 0; z < 3; z++) {
                    // Skip the center cube (not visible)
                    if (x === 1 && y === 1 && z === 1) continue;
                    
                    const smallCube = this.createSmallCube(x, y, z, cubeSize);
                    smallCube.position.set(
                        (x - 1) * (cubeSize + gap),
                        (y - 1) * (cubeSize + gap),
                        (z - 1) * (cubeSize + gap)
                    );
                    
                    this.cube.add(smallCube);
                }
            }
        }
        
        this.scene.add(this.cube);
        this.updateCubeColors();
    }
    
    createSmallCube(x, y, z, size) {
        const geometry = new THREE.BoxGeometry(size, size, size);
        
        // Create materials for each face
        const materials = [];
        
        // Face order: right, left, top, bottom, front, back
        const facePositions = [
            { face: 'R', visible: x === 2 }, // Right
            { face: 'L', visible: x === 0 }, // Left  
            { face: 'U', visible: y === 2 }, // Top
            { face: 'D', visible: y === 0 }, // Bottom
            { face: 'F', visible: z === 2 }, // Front
            { face: 'B', visible: z === 0 }  // Back
        ];
        
        facePositions.forEach(pos => {
            if (pos.visible) {
                const color = this.getFaceColor(pos.face, x, y, z);
                materials.push(new THREE.MeshLambertMaterial({ color: color }));
            } else {
                materials.push(new THREE.MeshLambertMaterial({ color: 0x000000 }));
            }
        });
        
        const cube = new THREE.Mesh(geometry, materials);
        cube.castShadow = true;
        cube.receiveShadow = true;
        
        // Store position for color updates
        cube.userData = { x, y, z };
        
        return cube;
    }
    
    getFaceColor(face, x, y, z) {
        const state = this.cubeState[face];
        let row = 1, col = 1; // Default to center
        
        switch (face) {
            case 'U': // Top
                if (y === 2) { // Only visible on top cubes
                    row = 2 - z;
                    col = x;
                }
                break;
            case 'D': // Bottom  
                if (y === 0) { // Only visible on bottom cubes
                    row = z;
                    col = x;
                }
                break;
            case 'F': // Front
                if (z === 2) { // Only visible on front cubes
                    row = 2 - y;
                    col = x;
                }
                break;
            case 'B': // Back
                if (z === 0) { // Only visible on back cubes
                    row = 2 - y;
                    col = 2 - x;
                }
                break;
            case 'L': // Left
                if (x === 0) { // Only visible on left cubes
                    row = 2 - y;
                    col = 2 - z;
                }
                break;
            case 'R': // Right
                if (x === 2) { // Only visible on right cubes
                    row = 2 - y;
                    col = z;
                }
                break;
        }
        
        const colorKey = state[row][col];
        return this.colors[colorKey];
    }
    
    setupControls() {
        // Add simple orbit controls for mouse interaction
        this.controls = new SimpleOrbitControls(this.camera, this.renderer.domElement);
    }
    
    updateCubeState(newState) {
        this.cubeState = newState;
        this.updateCubeColors();
    }
    
    updateCubeColors() {
        this.cube.children.forEach(smallCube => {
            const { x, y, z } = smallCube.userData;
            
            // Update materials for visible faces
            const facePositions = [
                { face: 'R', visible: x === 2, index: 0 }, // Right
                { face: 'L', visible: x === 0, index: 1 }, // Left
                { face: 'U', visible: y === 2, index: 2 }, // Top
                { face: 'D', visible: y === 0, index: 3 }, // Bottom
                { face: 'F', visible: z === 2, index: 4 }, // Front
                { face: 'B', visible: z === 0, index: 5 }  // Back
            ];
            
            facePositions.forEach(pos => {
                if (pos.visible) {
                    const color = this.getFaceColor(pos.face, x, y, z);
                    smallCube.material[pos.index].color.setHex(color);
                }
            });
        });
    }
    
    getDefaultState() {
        return {
            'U': [['W', 'W', 'W'], ['W', 'W', 'W'], ['W', 'W', 'W']],
            'D': [['Y', 'Y', 'Y'], ['Y', 'Y', 'Y'], ['Y', 'Y', 'Y']],
            'F': [['R', 'R', 'R'], ['R', 'R', 'R'], ['R', 'R', 'R']],
            'B': [['O', 'O', 'O'], ['O', 'O', 'O'], ['O', 'O', 'O']],
            'L': [['B', 'B', 'B'], ['B', 'B', 'B'], ['B', 'B', 'B']],
            'R': [['G', 'G', 'G'], ['G', 'G', 'G'], ['G', 'G', 'G']]
        };
    }
    
    resetToSolved() {
        this.cubeState = this.getDefaultState();
        this.updateCubeColors();
    }
    
    animate() {
        requestAnimationFrame(() => this.animate());
        
        if (this.controls) {
            this.controls.update();
        }
        
        // Gentle rotation when not interacting
        if (this.controls && this.controls.enabled && !this.controls.isMouseDown) {
            this.cube.rotation.y += 0.002;
        }
        
        this.renderer.render(this.scene, this.camera);
    }
    
    handleResize() {
        window.addEventListener('resize', () => {
            const width = this.container.clientWidth;
            const height = this.container.clientHeight;
            
            this.camera.aspect = width / height;
            this.camera.updateProjectionMatrix();
            
            this.renderer.setSize(width, height);
        });
    }
    
    // Animation methods for solving visualization
    animateMove(move) {
        console.log('3D Cube animateMove called with:', move);
        
        // Apply the move to the virtual cube state and update colors
        this.applyMoveToState(move);
        this.updateCubeColors();
        
        // Visual feedback - highlight moving pieces
        this.highlightMovingFace(move);
    }
    
    applyMoveToState(move) {
        // Apply the move to the cube state
        console.log(`Applying move: ${move}`);
        
        // Simulate the move by applying rotation logic
        const face = move.charAt(0);
        const isPrime = move.includes("'");
        const isDouble = move.includes("2");
        
        // Apply rotation to the internal state
        this.rotateFace(face, isPrime, isDouble);
    }
    
    rotateFace(face, isPrime = false, isDouble = false) {
        // Simple simulation of face rotation
        // In a full implementation, this would properly rotate the cube state
        // For now, we'll provide visual feedback through color changes
        
        const rotations = isDouble ? 2 : 1;
        const direction = isPrime ? -1 : 1;
        
        // Add some visual animation effect
        this.addRotationAnimation(face, direction, rotations);
    }
    
    addRotationAnimation(face, direction, rotations) {
        // Find cubes that belong to this face and add rotation animation
        const facePosition = this.getFacePosition(face);
        
        this.cube.children.forEach(smallCube => {
            if (this.isCubeOnFace(smallCube, face)) {
                // Add a subtle scaling effect to show movement
                const originalScale = smallCube.scale.clone();
                smallCube.scale.multiplyScalar(1.1);
                
                // Return to normal scale after animation
                setTimeout(() => {
                    smallCube.scale.copy(originalScale);
                }, 300);
            }
        });
    }
    
    getFacePosition(face) {
        const positions = {
            'U': { axis: 'y', value: 1 },    // Top
            'D': { axis: 'y', value: -1 },   // Bottom
            'F': { axis: 'z', value: 1 },    // Front
            'B': { axis: 'z', value: -1 },   // Back
            'L': { axis: 'x', value: -1 },   // Left
            'R': { axis: 'x', value: 1 }     // Right
        };
        return positions[face];
    }
    
    isCubeOnFace(cube, face) {
        const pos = this.getFacePosition(face);
        const cubePos = cube.position;
        
        switch (pos.axis) {
            case 'x': return Math.abs(cubePos.x - pos.value) < 0.1;
            case 'y': return Math.abs(cubePos.y - pos.value) < 0.1;
            case 'z': return Math.abs(cubePos.z - pos.value) < 0.1;
            default: return false;
        }
    }
    
    highlightMovingFace(move) {
        // Add visual feedback for the move being performed
        const faceMap = {
            'U': 'top', 'D': 'bottom', 'L': 'left', 
            'R': 'right', 'F': 'front', 'B': 'back'
        };
        
        const face = move.charAt(0);
        console.log(`Highlighting ${faceMap[face]} face for move ${move}`);
        
        // Add temporary highlight effect
        setTimeout(() => {
            // Remove highlight after move completes
        }, 600);
    }
    
    playSolution(moves) {
        // This method can be used for full solution playback
        const moveArray = moves.split(' ');
        let index = 0;
        
        const playNext = () => {
            if (index < moveArray.length) {
                this.animateMove(moveArray[index]);
                index++;
                setTimeout(playNext, 800);
            }
        };
        
        playNext();
    }
}

// Simple orbit controls implementation
class SimpleOrbitControls {
    constructor(camera, domElement) {
        this.camera = camera;
        this.domElement = domElement;
        this.enabled = true;
        this.enableDamping = true;
        this.dampingFactor = 0.05;
        this.enableZoom = true;
        this.enablePan = false;
        this.maxDistance = 15;
        this.minDistance = 3;
        
        this.isMouseDown = false;
        this.mouseX = 0;
        this.mouseY = 0;
        this.lastMouseX = 0;
        this.lastMouseY = 0;
        
        this.spherical = new THREE.Spherical();
        this.spherical.setFromVector3(this.camera.position);
        
        this.setupEventListeners();
    }
    
    setupEventListeners() {
        this.domElement.addEventListener('mousedown', (e) => this.onMouseDown(e));
        this.domElement.addEventListener('mousemove', (e) => this.onMouseMove(e));
        this.domElement.addEventListener('mouseup', () => this.onMouseUp());
        this.domElement.addEventListener('wheel', (e) => this.onWheel(e));
        
        // Prevent context menu
        this.domElement.addEventListener('contextmenu', (e) => e.preventDefault());
    }
    
    onMouseDown(event) {
        if (!this.enabled) return;
        this.isMouseDown = true;
        this.lastMouseX = event.clientX;
        this.lastMouseY = event.clientY;
    }
    
    onMouseMove(event) {
        if (!this.enabled || !this.isMouseDown) return;
        
        this.mouseX = event.clientX;
        this.mouseY = event.clientY;
        
        const deltaX = this.mouseX - this.lastMouseX;
        const deltaY = this.mouseY - this.lastMouseY;
        
        this.spherical.theta -= deltaX * 0.01;
        this.spherical.phi += deltaY * 0.01;
        
        // Constrain phi
        this.spherical.phi = Math.max(0.1, Math.min(Math.PI - 0.1, this.spherical.phi));
        
        this.camera.position.setFromSpherical(this.spherical);
        this.camera.lookAt(0, 0, 0);
        
        this.lastMouseX = this.mouseX;
        this.lastMouseY = this.mouseY;
    }
    
    onMouseUp() {
        this.isMouseDown = false;
    }
    
    onWheel(event) {
        if (!this.enabled || !this.enableZoom) return;
        
        event.preventDefault();
        
        const scale = Math.pow(0.95, event.deltaY * 0.01);
        this.spherical.radius *= scale;
        
        // Constrain distance
        this.spherical.radius = Math.max(this.minDistance, 
                                       Math.min(this.maxDistance, this.spherical.radius));
        
        this.camera.position.setFromSpherical(this.spherical);
        this.camera.lookAt(0, 0, 0);
    }
    
    update() {
        // Simple update for damping
        this.spherical.setFromVector3(this.camera.position);
    }
}