import json
from collections import deque
from graphviz import Digraph
import os

os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin/'

class State:
    def __init__(self, label=None):
        self.state_id = None
        self.is_terminating = False
        self.next_in_states = {}

class DFA:
    def __init__(self):
        self.in_states = {}
        self.initial_state = None
        self.regex = None

    def read_json(self, file_path):
        with open(file_path, "r") as json_file:
            state_machine_definition = json.load(json_file)
        
        # Extract in_states and initial state from the JSON data
        self.in_states = state_machine_definition  # assuming JSON structure is already in expected format
        self.initial_state = state_machine_definition["startingState"]
        # remove the initial state from the in_states
        self.in_states.pop("startingState")

    def epsilon_closure(self, states):
        epsilon_closure_set = set(states)
        stack = list(states)
        while stack:
            current_state = stack.pop()
            listt = []
            for transition in self.in_states[current_state]:
                if transition[0] == 'ε':
                    listt.append(self.in_states[current_state][transition])
            for next_state in listt:
                if next_state != []:
                    if next_state not in epsilon_closure_set:
                        epsilon_closure_set.add(next_state)
                        stack.append(next_state)
        return epsilon_closure_set

    def get_all_actions(self):
        actions = set()
        for state in self.in_states.values():
            for transition in state:
                if transition[0] not in ['ε', 'ε1', 'ε2', 'isTerminatingState']:
                    actions.update(transition)
        actions.discard('ε')  # Remove epsilon from actions
        return actions

    def get_terminating_state(self):
        terminating_states = []
        for state in self.in_states.keys():
            if self.in_states[state]["isTerminatingState"] == True:
                terminating_states.append(state)
        return terminating_states

    def check_terminating_state(self, states):
        terminating_states = self.get_terminating_state()
        for state in states:
            if state in terminating_states:
                return True
        return False

    def nfa2dfa(self):
        # Initialize the DFA states dictionary
        dfa_states = {}
        initial_epsilon_closure = self.epsilon_closure([self.initial_state])
        dfa_states["startingState"] = ' '.join(initial_epsilon_closure)
        dfa_states[' '.join(initial_epsilon_closure)] = {'isTerminatingState': False}
        # Create a queue to process the states
        state_queue = deque([tuple(initial_epsilon_closure)])

        # While there are unprocessed states in the queue
        while state_queue:
            current_state = state_queue.popleft()

            # Get all possible symbols for the NFA
            symbols = self.get_all_actions()

            # Initialize the transition dictionary for the current DFA state
            dfa_states[' '.join(current_state)]['isTerminatingState'] = False
            if self.check_terminating_state(current_state):
                dfa_states[' '.join(current_state)]["isTerminatingState"] = True

            # For each symbol, find the epsilon closure of the next state
            for symbol in symbols:
                next_states = []
                for nfa_state_label in current_state:
                    nfa_state = self.in_states[nfa_state_label]
                    transitions = []
                    transitions.append(nfa_state.get(symbol, ""))
                    if transitions[0] != "":
                        for transition in transitions:
                            transition = [transition] if isinstance(transition, str) else transition
                            next_states.extend(self.epsilon_closure(transition))
                if next_states == []:
                    continue
                next_states = list(set(next_states))  # Remove duplicates
                next_states.sort()  # Sort for consistency

                # Add the next state to the DFA if it's not already in there
                if ' '.join(next_states) not in dfa_states:
                    dfa_states[' '.join(next_states)] = {'isTerminatingState': False}
                    state_queue.append(next_states)

                # Add the transition from the current DFA state to the next DFA state
                dfa_states[' '.join(current_state)][symbol] = ' '.join(next_states)

        return dfa_states

    def visualize(self, filename='dfa_graph'):
        dfa_states = self.nfa2dfa()
        dot = Digraph()
        for state, transitions in dfa_states.items():
            if state != "startingState":
                state_label = state
                if transitions['isTerminatingState']:
                    dot.node(state_label, state_label, shape='doublecircle')
                else:
                    dot.node(state_label, state_label)
                for symbol, next_state in transitions.items():
                    if symbol == 'isTerminatingState':
                        continue
                    dot.edge(state_label, next_state, label=symbol)
        dot.render(filename, format='png', cleanup=True)

    def save_json(self, filename='dfa_states.json'):
        dfa_states = self.nfa2dfa()
        dfa_states_json = {}
        # save starting state
        dfa_states_json["startingState"] = dfa_states["startingState"]
        for state, transitions in dfa_states.items():
            if state != "startingState":
                dfa_states_json[state] = transitions

        with open(filename, 'w') as json_file:
            json.dump(dfa_states_json, json_file, indent=4)


def main():
    dfa = DFA()
    dfa.read_json("states.json")
    # print(dfa.in_states)
    # print(dfa.initial_state)
    # print("get_all_actions",dfa.get_all_actions())
    # print(nfa.epsilon_closure(["S4"]))
    # print("fff",dfa.nfa2dfa())
    dfa.visualize()
    dfa.save_json()
    # dfa_out=dfa.nfa2dfa()
    
if __name__ == "__main__":
    main()
