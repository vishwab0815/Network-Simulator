"""
Finite State Machine for TCP Protocol Verification
Implements DFA for TCP 3-way handshake validation
"""

class FiniteStateMachine:
    """
    FSM for TCP 3-way Handshake Protocol
    States: CLOSED, LISTEN, SYN_SENT, SYN_RECEIVED, ESTABLISHED
    """

    def __init__(self):
        self.states = {
            'CLOSED': 0,
            'LISTEN': 1,
            'SYN_SENT': 2,
            'SYN_RECEIVED': 3,
            'ESTABLISHED': 4,
            'ERROR': 5
        }

        # Reverse mapping for state names
        self.state_names = {v: k for k, v in self.states.items()}

        # Define transition table: (current_state, input) -> next_state
        self.transitions = {
            (self.states['CLOSED'], 'LISTEN'): self.states['LISTEN'],
            (self.states['LISTEN'], 'SYN'): self.states['SYN_RECEIVED'],
            (self.states['SYN_RECEIVED'], 'SYN-ACK'): self.states['SYN_RECEIVED'],
            (self.states['SYN_RECEIVED'], 'ACK'): self.states['ESTABLISHED'],

            # Client side transitions
            (self.states['CLOSED'], 'SYN'): self.states['SYN_SENT'],
            (self.states['SYN_SENT'], 'SYN-ACK'): self.states['ESTABLISHED'],
        }

        self.current_state = self.states['CLOSED']
        self.history = []

    def reset(self):
        """Reset FSM to initial state"""
        self.current_state = self.states['CLOSED']
        self.history = []

    def get_state_name(self, state=None):
        """Get name of current or specified state"""
        if state is None:
            state = self.current_state
        return self.state_names.get(state, 'UNKNOWN')

    def transition(self, input_symbol):
        """
        Process input and transition to next state
        Returns: (success, old_state, new_state, message)
        """
        old_state = self.current_state
        old_state_name = self.get_state_name(old_state)

        # Check if transition exists
        key = (old_state, input_symbol)
        if key in self.transitions:
            self.current_state = self.transitions[key]
            new_state_name = self.get_state_name()

            # Record history
            self.history.append({
                'input': input_symbol,
                'from_state': old_state_name,
                'to_state': new_state_name,
                'valid': True
            })

            return (True, old_state_name, new_state_name,
                    f"Valid transition: {old_state_name} -> {input_symbol} -> {new_state_name}")
        else:
            # Invalid transition
            self.current_state = self.states['ERROR']
            self.history.append({
                'input': input_symbol,
                'from_state': old_state_name,
                'to_state': 'ERROR',
                'valid': False
            })

            return (False, old_state_name, 'ERROR',
                    f"Invalid transition: No rule for {old_state_name} with input '{input_symbol}'")

    def verify_sequence(self, packet_sequence):
        """
        Verify if a sequence of packets represents a valid TCP handshake
        Returns: (is_valid, steps, final_state)
        """
        self.reset()
        steps = []

        for packet in packet_sequence:
            success, old_state, new_state, message = self.transition(packet)
            steps.append({
                'packet': packet,
                'old_state': old_state,
                'new_state': new_state,
                'valid': success,
                'message': message
            })

            if not success:
                return (False, steps, self.get_state_name())

        # Check if we reached ESTABLISHED state
        is_valid = self.current_state == self.states['ESTABLISHED']
        return (is_valid, steps, self.get_state_name())

    def get_all_transitions(self):
        """Get all valid transitions for visualization"""
        transitions = []
        for (from_state, input_sym), to_state in self.transitions.items():
            transitions.append({
                'from': self.get_state_name(from_state),
                'to': self.get_state_name(to_state),
                'label': input_sym
            })
        return transitions


class ProtocolVerifier:
    """Main protocol verification class"""

    def __init__(self):
        self.fsm = FiniteStateMachine()

    def verify_tcp_handshake(self, packets):
        """
        Verify TCP 3-way handshake
        Expected sequence: LISTEN -> SYN -> SYN-ACK -> ACK
        """
        is_valid, steps, final_state = self.fsm.verify_sequence(packets)

        return {
            'valid': is_valid,
            'steps': steps,
            'final_state': final_state,
            'message': 'Valid TCP handshake' if is_valid else 'Invalid packet sequence'
        }

    def get_transition_diagram(self):
        """Get FSM transition diagram data for visualization"""
        return {
            'states': list(self.fsm.states.keys()),
            'transitions': self.fsm.get_all_transitions(),
            'initial_state': 'CLOSED',
            'accepting_states': ['ESTABLISHED']
        }


# Example usage
if __name__ == "__main__":
    verifier = ProtocolVerifier()

    # Test valid TCP handshake (server side)
    print("Test 1: Valid TCP Handshake (Server Side)")
    valid_sequence = ['LISTEN', 'SYN', 'ACK']
    result = verifier.verify_tcp_handshake(valid_sequence)
    print(f"Valid: {result['valid']}")
    print(f"Final State: {result['final_state']}")
    for step in result['steps']:
        print(f"  {step['old_state']} --[{step['packet']}]--> {step['new_state']}")

    print("\n" + "="*50 + "\n")

    # Test invalid sequence
    print("Test 2: Invalid Sequence")
    verifier.fsm.reset()
    invalid_sequence = ['LISTEN', 'ACK', 'SYN']
    result = verifier.verify_tcp_handshake(invalid_sequence)
    print(f"Valid: {result['valid']}")
    print(f"Final State: {result['final_state']}")
    for step in result['steps']:
        print(f"  {step['old_state']} --[{step['packet']}]--> {step['new_state']}")

    print("\n" + "="*50 + "\n")

    # Get transition diagram
    print("Test 3: Transition Diagram")
    diagram = verifier.get_transition_diagram()
    print(f"States: {diagram['states']}")
    print(f"Transitions:")
    for trans in diagram['transitions']:
        print(f"  {trans['from']} --[{trans['label']}]--> {trans['to']}")
