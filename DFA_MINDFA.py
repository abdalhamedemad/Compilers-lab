from graphviz import Digraph
import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin/'
import json
class MIN_DFA:
    def __init__(self, dfa):
        # Initialize the minimized DFA states
        self.states = self.dfa2min(dfa)

    def getGroupKeys(self, group):
        # Get keys of states in a group
        keys = []
        for state in group:
            for key, value in state.items():
                keys.append(key)
        return keys

    def toDict(self):
        # Convert the minimized DFA to a dictionary
        return self.states

    def getSymbols(self, dfa):
        # Get all symbols/transitions present in the DFA
        symbols = set()
        for state in dfa.values():
            for transition in state:
                if transition not in ['isTerminatingState']:
                    symbols.add(transition)
        return symbols

    def dfa2min(self, dfa):
        # Convert DFA to minimized DFA
        states = dfa
        symbols = self.getSymbols(states)
        # Remove the starting state from DFA
        states.pop('startingState')
        # Initialize partitions
        groups = self.initializePartitions(states)
        # Refine partitions until no further splits are possible
        groups = self.refinePartitions(groups, symbols)
        # Concatenate states within each group
        newGroups = self.concatStates(groups)
        return newGroups

    def initializePartitions(self, states):
        # Initialize partitions based on accepting and non-accepting states
        accepting_states = []
        non_accepting_states = []
        for key, value in states.items():
            if value["isTerminatingState"] == True:
                accepting_states.append({key: value})
            else:
                non_accepting_states.append({key: value})
        return [accepting_states, non_accepting_states]

    def refinePartitions(self, groups, symbols):
        # Refine partitions until no further splits are possible
        split = True
        while split:
            split = False
            for i, group in enumerate(groups):
                if not group:
                    continue 
                # Get target groups for each state in the current group
                targetGroups = self.getTargetGroups(group, symbols, groups)
                # Split states if necessary and update partitions
                splitted_states = self.splitStates(group, symbols, targetGroups, groups)
                if len(splitted_states) > 0:
                    groups.insert(i+1, list(splitted_states))
                    groups[i] = [state for state in group if state not in splitted_states]
                    split = True
        return groups

    def getTargetGroups(self, group, symbols, all_groups):
        # Get target groups for each symbol transition
        targetGroups = {}
        first_state = next(iter(group))
        for key, value in first_state.items():
            for symbol in symbols:
                if symbol in value:
                    targetGroups[symbol] = [j for j, group in enumerate(all_groups) if value[symbol] in self.getGroupKeys(group)][0]
        return targetGroups

    def splitStates(self, group, symbols, targetGroups, all_groups):
        # Split states based on target groups
        splitted_states = []
        for state in group:
            outputGroups = {}
            for key, value in state.items():
                for symbol in symbols:
                    if symbol in value:
                        List = [j for j, group in enumerate(all_groups) if value[symbol] in self.getGroupKeys(group)]
                        outputGroups[symbol] = List[0]
            if outputGroups != targetGroups:
                splitted_states.append(state)
        return splitted_states

    def concatStates(self, groups):
        # Concatenate states within each group and update transitions
        hashTable = {}
        for g, group in enumerate(groups):
            for state in group:
                for key, value in state.items():
                    hashTable[key] = str(g)
        newGroups = {'startingState':0}
        groupCopy = groups.copy()
        for g, group in enumerate(groupCopy):
            for state in group:
                for key, value in state.items():
                    for symbol, next_state in value.items():
                        if next_state in hashTable:
                            value[symbol] = str(hashTable[next_state])
                            newGroups[str(g)] = value
        return newGroups
    
    def save_as_json(self, filename):
        # Save the minimized DFA as a JSON file
        with open(filename, 'w') as f:
            json.dump(self.states, f)
    def save_as_dot(self, filename):
        # Generate a DOT file representing the minimized DFA
        dot = Digraph()

        # Add the starting state
        dot.node("0", shape="circle")

        # Add the transitions
        for state, transitions in self.states.items():
            if state != "startingState":
                is_terminating = transitions.get("isTerminatingState", False)
                peripheries = 2 if is_terminating else 1
                dot.node(str(state), shape="circle", peripheries=str(peripheries))
                for symbol, next_state in transitions.items():
                    if symbol != "isTerminatingState":
                        dot.edge(str(state), str(next_state), label=str(symbol))

        # Save DOT file
        dot.render(filename, format='png', cleanup=True)

def read_nfa_json(filename):
    # Read NFA from JSON file
    with open(filename, 'r') as f:
        states = json.load(f)
    return states

def main3():
    # print(read_nfa_json("dfa_states.json"))
    minDfa = MIN_DFA(read_nfa_json("dfa_states.json"))
    minDfa.save_as_json('minimized_dfa.json')
    minDfa.save_as_dot('minimized_dfa')
    print("Minimized DFA: ", minDfa.toDict())

# if __name__ == "__main__":
#     main3()
