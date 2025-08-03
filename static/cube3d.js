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
        this.scene.background = new THREE.Color(0xf0f0f0);
        
        // Camera
        this.camera = new THREE.PerspectiveCamera(
            75,
            this.container.clientWidth / this.container.clientHeight,
            0.1,
            1000
        );
        this.camera.position.set(5, 5, 5);
        this.camera.lookAt(0, 0, 0);
        
        // Renderer
        this.renderer = new THREE.WebGLRenderer({ antialias: true });
        this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
        this.renderer.shadowMap.enabled = true;
        this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        this.container.appendChild(this.renderer.domElement);
        
        // Lighting
        const ambientLight = new THREE.AmbientLight(0x404040, 0.6);
        this.scene.add(ambientLight);
        
        const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
        directionalLight.position.set(10, 10, 5);
        directionalLight.castShadow = true;
        this.scene.add(directionalLight);
    }
    
    createCube() {
        this.cube = new THREE.Group();
        
        // Create 27 small cubes (3x3x3)
        const cubeSize = 0.95;
        const gap = 0.05;
        
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
        let row, col;
        
        switch (face) {
            case 'U': // Top
                row = 2 - z;
                col = x;
                break;
            case 'D': // Bottom  
                row = z;
                col = x;
                break;
            case 'F': // Front
                row = 2 - y;
                col = x;
                break;
            case 'B': // Back
                row = 2 - y;
                col = 2 - x;
                break;
            case 'L': // Left
                row = 2 - y;
                col = 2 - z;
                break;
            case 'R': // Right
                row = 2 - y;
                col = z;
                break;
        }
        
        const colorKey = state[row][col];
        return this.colors[colorKey];
    }
    
    setupControls() {
        // Add OrbitControls for mouse interaction
        this.controls = new THREE.OrbitControls(this.camera, this.renderer.domElement);
        this.controls.enableDamping = true;
        this.controls.dampingFactor = 0.05;
        this.controls.enableZoom = true;
        this.controls.enablePan = false;
        this.controls.maxDistance = 15;
        this.controls.minDistance = 3;
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
        if (!this.controls.enabled || (!this.controls._state === THREE.OrbitControls.STATE.NONE)) {
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
        // This would animate individual face rotations
        // Implementation would depend on the specific move
        console.log(`Animating move: ${move}`);
    }
    
    playSolution(moves) {
        // Animate the entire solution sequence
        const moveArray = moves.split(' ');
        let index = 0;
        
        const playNext = () => {
            if (index < moveArray.length) {
                this.animateMove(moveArray[index]);
                index++;
                setTimeout(playNext, 500); // 500ms between moves
            }
        };
        
        playNext();
    }
}

// Three.js OrbitControls (simplified version)
THREE.OrbitControls = function(camera, domElement) {
    this.camera = camera;
    this.domElement = domElement;
    this.enabled = true;
    this.enableDamping = false;
    this.dampingFactor = 0.25;
    this.enableZoom = true;
    this.enablePan = true;
    this.maxDistance = Infinity;
    this.minDistance = 0;
    
    const scope = this;
    let isMouseDown = false;
    let mouseX = 0, mouseY = 0;
    let lastMouseX = 0, lastMouseY = 0;
    
    this.update = function() {
        // Simple damping
        if (this.enableDamping) {
            // Apply damping to rotation
        }
    };
    
    function onMouseDown(event) {
        if (!scope.enabled) return;
        isMouseDown = true;
        lastMouseX = event.clientX;
        lastMouseY = event.clientY;
    }
    
    function onMouseMove(event) {
        if (!scope.enabled || !isMouseDown) return;
        
        mouseX = event.clientX;
        mouseY = event.clientY;
        
        const deltaX = mouseX - lastMouseX;
        const deltaY = mouseY - lastMouseY;
        
        // Rotate camera around the cube
        const spherical = new THREE.Spherical();
        spherical.setFromVector3(scope.camera.position);
        
        spherical.theta -= deltaX * 0.01;
        spherical.phi += deltaY * 0.01;
        
        spherical.phi = Math.max(0.1, Math.min(Math.PI - 0.1, spherical.phi));
        
        scope.camera.position.setFromSpherical(spherical);
        scope.camera.lookAt(0, 0, 0);
        
        lastMouseX = mouseX;
        lastMouseY = mouseY;
    }
    
    function onMouseUp() {
        isMouseDown = false;
    }
    
    function onWheel(event) {
        if (!scope.enabled || !scope.enableZoom) return;
        
        const scale = Math.pow(0.95, event.deltaY * 0.01);
        scope.camera.position.multiplyScalar(scale);
        
        const distance = scope.camera.position.length();
        if (distance > scope.maxDistance) {
            scope.camera.position.normalize().multiplyScalar(scope.maxDistance);
        }
        if (distance < scope.minDistance) {
            scope.camera.position.normalize().multiplyScalar(scope.minDistance);
        }
    }
    
    this.domElement.addEventListener('mousedown', onMouseDown);
    this.domElement.addEventListener('mousemove', onMouseMove);
    this.domElement.addEventListener('mouseup', onMouseUp);
    this.domElement.addEventListener('wheel', onWheel);
};