"""
Flask Backend Server for Protocol Verification System
Provides REST API for automata operations and verification
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from automata import ProtocolVerifier

app = Flask(__name__)
CORS(app)

# Initialize verifier
verifier = ProtocolVerifier()

@app.route('/')
def index():
    """Serve main page"""
    return render_template('index.html')

@app.route('/api/verify', methods=['POST'])
def verify_sequence():
    """
    Verify a packet sequence
    Expected JSON: {"packets": ["LISTEN", "SYN", "ACK"]}
    """
    try:
        data = request.get_json()
        packets = data.get('packets', [])

        if not packets:
            return jsonify({'error': 'No packets provided'}), 400

        # Reset FSM before verification
        verifier.fsm.reset()

        # Verify sequence
        result = verifier.verify_tcp_handshake(packets)

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/diagram', methods=['GET'])
def get_diagram():
    """Get FSM transition diagram data"""
    try:
        diagram = verifier.get_transition_diagram()
        return jsonify(diagram)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/step', methods=['POST'])
def step_transition():
    """
    Execute single transition step
    Expected JSON: {"input": "SYN"}
    """
    try:
        data = request.get_json()
        input_symbol = data.get('input', '')

        if not input_symbol:
            return jsonify({'error': 'No input provided'}), 400

        success, old_state, new_state, message = verifier.fsm.transition(input_symbol)

        return jsonify({
            'success': success,
            'old_state': old_state,
            'new_state': new_state,
            'message': message
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reset', methods=['POST'])
def reset_fsm():
    """Reset FSM to initial state"""
    try:
        verifier.fsm.reset()
        return jsonify({
            'success': True,
            'current_state': verifier.fsm.get_state_name(),
            'message': 'FSM reset to initial state'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/examples', methods=['GET'])
def get_examples():
    """Get example packet sequences"""
    examples = {
        'valid_sequences': [
            {
                'name': 'Valid TCP Handshake (Server)',
                'packets': ['LISTEN', 'SYN', 'ACK'],
                'description': 'Server-side TCP 3-way handshake'
            },
            {
                'name': 'Valid TCP Handshake (Client)',
                'packets': ['SYN', 'SYN-ACK'],
                'description': 'Client-side TCP handshake'
            }
        ],
        'invalid_sequences': [
            {
                'name': 'Missing SYN',
                'packets': ['LISTEN', 'ACK'],
                'description': 'Skips SYN packet - invalid'
            },
            {
                'name': 'Wrong Order',
                'packets': ['ACK', 'SYN', 'LISTEN'],
                'description': 'Packets in wrong order'
            },
            {
                'name': 'Invalid Input',
                'packets': ['LISTEN', 'INVALID', 'SYN'],
                'description': 'Contains invalid packet type'
            }
        ]
    }
    return jsonify(examples)

if __name__ == '__main__':
    print("="*60)
    print("Network Protocol Verification System")
    print("Using Finite State Machines & Formal Languages")
    print("="*60)
    print("\nServer starting...")
    print("Open http://localhost:5000 in your browser")
    print("\nPress CTRL+C to stop the server")
    print("="*60)

    app.run(debug=True, host='0.0.0.0', port=5000)
