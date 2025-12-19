# Network Protocol Verification using Formal Languages and Automata

## Project Overview

This project demonstrates the practical application of **Formal Languages and Automata Theory** in verifying network protocols. Specifically, it implements a **Finite State Machine (FSM)** to model and verify the **TCP 3-way handshake protocol**.

### Key Features

- **Deterministic Finite Automaton (DFA)** implementation for TCP protocol
- **Animated State Transition Diagrams** with real-time updates
- **Packet Flow Visualization** showing client-server communication
- **Interactive Protocol Verification** with step-by-step execution
- **Web-based Interface** with smooth animations and visual feedback

---

## Theoretical Background

### Formal Languages and Automata

**Formal Language Theory** provides mathematical models for describing patterns and sequences. In network protocols:

- **Alphabet (Σ)**: Set of valid packet types {LISTEN, SYN, SYN-ACK, ACK}
- **Language (L)**: Set of valid packet sequences that constitute a proper protocol
- **Automaton**: Mathematical model that accepts or rejects sequences based on protocol rules

### Finite State Machine (FSM)

An FSM is defined as a 5-tuple: **M = (Q, Σ, δ, q₀, F)**

Where:
- **Q**: Finite set of states = {CLOSED, LISTEN, SYN_SENT, SYN_RECEIVED, ESTABLISHED, ERROR}
- **Σ**: Input alphabet = {LISTEN, SYN, SYN-ACK, ACK}
- **δ**: Transition function Q × Σ → Q
- **q₀**: Initial state = CLOSED
- **F**: Set of accepting states = {ESTABLISHED}

### TCP 3-Way Handshake

The TCP connection establishment uses a 3-way handshake:

```
Client                    Server
  |                         |
  |         SYN            |
  |----------------------->|  (Server: LISTEN → SYN_RECEIVED)
  |                         |
  |       SYN-ACK          |
  |<-----------------------|  (Client: SYN_SENT → ESTABLISHED)
  |                         |
  |         ACK            |
  |----------------------->|  (Server: SYN_RECEIVED → ESTABLISHED)
  |                         |
  |    Connection Established
```

#### Valid Server-Side Sequence:
```
CLOSED → LISTEN → SYN_RECEIVED → ESTABLISHED
Inputs: LISTEN, SYN, ACK
```

#### Valid Client-Side Sequence:
```
CLOSED → SYN_SENT → ESTABLISHED
Inputs: SYN, SYN-ACK
```

---

## Project Structure

```
TOC/
├── venv/                    # Python virtual environment
├── templates/
│   └── index.html          # Frontend with animations
├── automata.py             # FSM implementation
├── server.py               # Flask backend server
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

---

## Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser (Chrome, Firefox, Edge)

### Installation Steps

1. **Navigate to project directory**:
   ```bash
   cd "c:\Users\Vishwanath B\Desktop\TOC"
   ```

2. **Activate virtual environment**:

   **Windows (Command Prompt)**:
   ```bash
   venv\Scripts\activate
   ```

   **Windows (PowerShell)**:
   ```powershell
   venv\Scripts\Activate.ps1
   ```

   **Linux/Mac**:
   ```bash
   source venv/bin/activate
   ```

3. **Install dependencies** (already done, but if needed):
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the server**:
   ```bash
   python server.py
   ```

5. **Open your browser**:
   Navigate to `http://localhost:5000`

---

## Usage Guide

### Web Interface

The application features three main sections:

#### 1. FSM State Transition Diagram
- **Visual representation** of all states and transitions
- **Color-coded states**:
  - 🟢 Green: Initial state (CLOSED)
  - 🔵 Blue: Accepting state (ESTABLISHED)
  - 🔴 Red: Error state
  - 🟡 Yellow with red border: Current active state
- **Animated transitions** showing state changes in real-time
- **Pulsing effect** on current state for emphasis

#### 2. Protocol Verification Controls
- **Input field**: Enter comma-separated packet sequence
- **Verify button**: Execute full verification with animation
- **Reset button**: Reset FSM to initial state
- **Step Mode**: Execute sequence step-by-step with delays
- **Example sequences**: Pre-loaded valid and invalid examples

#### 3. Packet Flow Animation
- **Visual representation** of client-server communication
- **Animated packets** moving between client and server
- **Color-coded packets**:
  - Purple: Valid packets
  - Red: Invalid packets

### Example Sequences

#### Valid Sequences ✅

1. **Server-side handshake**:
   ```
   LISTEN, SYN, ACK
   ```

2. **Client-side handshake**:
   ```
   SYN, SYN-ACK
   ```

#### Invalid Sequences ❌

1. **Missing SYN**:
   ```
   LISTEN, ACK
   ```

2. **Wrong order**:
   ```
   ACK, SYN, LISTEN
   ```

3. **Invalid input**:
   ```
   LISTEN, INVALID, SYN
   ```

---

## API Endpoints

The Flask backend provides the following REST API:

### `GET /`
Returns the main HTML page

### `POST /api/verify`
Verify a complete packet sequence

**Request body**:
```json
{
  "packets": ["LISTEN", "SYN", "ACK"]
}
```

**Response**:
```json
{
  "valid": true,
  "steps": [...],
  "final_state": "ESTABLISHED",
  "message": "Valid TCP handshake"
}
```

### `GET /api/diagram`
Get FSM transition diagram data

**Response**:
```json
{
  "states": ["CLOSED", "LISTEN", ...],
  "transitions": [...],
  "initial_state": "CLOSED",
  "accepting_states": ["ESTABLISHED"]
}
```

### `POST /api/step`
Execute single transition

**Request body**:
```json
{
  "input": "SYN"
}
```

**Response**:
```json
{
  "success": true,
  "old_state": "LISTEN",
  "new_state": "SYN_RECEIVED",
  "message": "Valid transition..."
}
```

### `POST /api/reset`
Reset FSM to initial state

### `GET /api/examples`
Get example sequences (valid and invalid)

---

## Technical Implementation

### FSM Implementation (`automata.py`)

The `FiniteStateMachine` class implements:

- **State representation**: Dictionary mapping state names to integers
- **Transition table**: Dictionary with (state, input) → next_state mappings
- **Transition function**: Validates and executes state transitions
- **Sequence verification**: Processes complete packet sequences
- **History tracking**: Records all transitions for visualization

### Animation Implementation

Animations are implemented using:

- **SVG graphics**: Scalable vector graphics for diagrams
- **CSS animations**: Smooth transitions and effects
- **JavaScript requestAnimationFrame**: Smooth packet movement
- **Async/await**: Sequential step animations

### Key Animation Features

1. **State transitions**: Current state pulses with color change
2. **Packet flow**: Packets move smoothly between client/server
3. **Result display**: Sequential fade-in with staggered delays
4. **Interactive feedback**: Hover effects and click responses

---

## Learning Objectives

This project demonstrates:

1. **Formal Language Theory Application**: Using DFA to model real protocols
2. **State Machine Design**: Implementing FSM with transition tables
3. **Protocol Verification**: Validating sequences against formal rules
4. **Visualization**: Representing abstract concepts graphically
5. **Full-Stack Development**: Backend logic + frontend visualization

---

## Extensions & Improvements

Potential enhancements:

1. **Additional Protocols**:
   - HTTP request/response cycles
   - DNS query resolution
   - SMTP email exchange

2. **Advanced Automata**:
   - Non-deterministic Finite Automata (NFA)
   - Pushdown Automata (PDA) for context-free protocols
   - Regular expressions for pattern matching

3. **Enhanced Visualization**:
   - Network packet capture integration
   - Real-time protocol monitoring
   - 3D state diagram visualization

4. **Formal Verification**:
   - Property checking (safety, liveness)
   - Model checking algorithms
   - Correctness proofs

---

## Troubleshooting

### Port already in use
If port 5000 is busy, modify `server.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change port
```

### Dependencies not installed
Ensure virtual environment is activated before installing:
```bash
venv\Scripts\activate
pip install -r requirements.txt
```

### Browser not showing animations
- Clear browser cache
- Try a different browser (Chrome recommended)
- Check browser console for JavaScript errors

---

## References

1. **Automata Theory**:
   - Introduction to Automata Theory, Languages, and Computation (Hopcroft, Ullman)
   - Theory of Computation (Sipser)

2. **Network Protocols**:
   - TCP/IP Illustrated (Stevens)
   - Computer Networks (Tanenbaum)

3. **Formal Methods**:
   - Principles of Model Checking (Baier, Katoen)
   - Software Specification Methods (Habrias, Frappier)

---

## License

This project is created for educational purposes.

---

## Author

Created as a demonstration of **Formal Languages and Automata** applications in **Network Protocol Verification**.

---

## Acknowledgments

- Flask framework for web backend
- SVG for scalable graphics
- Theory of Computation course materials
