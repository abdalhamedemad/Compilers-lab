import os
import json
from graphviz import Digraph
import re

class State:
    def __init__(self, label=None):
        self.state_id = None
        self.is_terminating = False
        self.next_states = {}

class NFA:
    def __init__(self):
        self.states = {}
        self.initial_state = None
        self.regex = None

    def disjunction(self,initial_state, r_index, regex, states, last_s_index):
        n_begin_s_index = last_s_index + 1
        n_last_s_index = n_begin_s_index
        n_prev_state = n_begin_s_index
        # r_index from element after '|'
        while r_index < len(regex):
                # print("")
            if regex[r_index] == '(':
                # print("(r)")
                # extract the regex in the bracket
                num_of_brackets = 1
                rgx_inside = ""
                l = r_index +1
                while num_of_brackets != 0:
                    if regex[l] == '(':
                        num_of_brackets +=1
                    elif regex[l] == ')':
                        num_of_brackets -=1
                    if num_of_brackets != 0:
                        rgx_inside += regex[l]
                    l+=1
                    # r_index +=1
                # print(rgx_inside)

                i,last_s_r,f,r_prev_el =self.solve_recursive_grouping(initial_state,r_index,rgx_inside,states,n_last_s_index)
                # new initial state
                new_state = State()
                new_state.state_id = n_begin_s_index
                new_state.is_terminating = False
                new_state.next_states.update( {'ε404' : r_prev_el} )
                states[n_begin_s_index] = new_state

                n_begin_s_index = last_s_r
                n_last_s_index =n_begin_s_index
                # print(r_index)
                n_prev_state = r_prev_el
                r_index =  r_index + len(rgx_inside) + 2
            elif regex[r_index] == '|':
                # print("or")
                return r_index,n_last_s_index,0
                # call or function
            elif regex[r_index] == '*':
                self.zero_or_more(states,n_begin_s_index,n_prev_state)

                n_begin_s_index =n_begin_s_index+1
                r_index +=1
                n_last_s_index = n_begin_s_index

            elif regex[r_index] == '+':
                self.one_or_more(states,n_begin_s_index,n_prev_state)

                n_begin_s_index =n_begin_s_index+1
                r_index +=1
                n_last_s_index = n_begin_s_index
            elif regex[r_index] == '?':

                self.zero_or_one(states,n_begin_s_index,n_prev_state)
                n_begin_s_index =n_begin_s_index+1
                r_index +=1
                n_last_s_index = n_begin_s_index
            elif regex[r_index] == '[':
                # print("[")
                self.ranges(regex,r_index,n_begin_s_index,states)

                n_prev_state = n_begin_s_index
                n_begin_s_index =n_begin_s_index+1
                r_index =  r_index + len(rgx_inside) + 2
                n_last_s_index = n_begin_s_index
            else:
                new_state = State()
                new_state.state_id = n_begin_s_index
                new_state.is_terminating = False
                #
                if (regex[r_index] == '.'):
                    new_state.next_states.update( {'ε010' : n_begin_s_index +1} )
                else:
                    new_state.next_states.update( {regex[r_index] : n_begin_s_index +1} )
                states[n_begin_s_index] = new_state
                n_prev_state = n_begin_s_index
                n_begin_s_index =n_begin_s_index+1
                r_index +=1
                n_last_s_index = n_begin_s_index

        finish =1
        return -1,n_last_s_index,finish

    def save_json(self,states,initial_state):
        state_data = {
        "startingState": "S" + str(initial_state),
        # "states": {}
        }

        for state_id, state_obj in states.items():
            state_info = {
                # "state_id": state_obj.state_id,
                "isTerminatingState": state_obj.is_terminating,
                # "Transitions": {}
            }

            if not state_obj.is_terminating:
                for transition, next_state_id in state_obj.next_states.items():
                    state_info[transition] = "S" + str(next_state_id)
            # else:
                # remove the transitions key if the state is terminating
                # state_info.pop("Transitions")

            state_data["S" + str(state_obj.state_id)] = state_info

        # Writing to JSON file
        with open("states.json", "w") as json_file:
            json.dump(state_data, json_file, indent=4)
    def solve_recursive_grouping(self,initial_state, r_index, regex, states, last_s_index):
        new_state2 = State()
        new_state2.state_id = last_s_index+1
        new_state2.is_terminating = False
        states[last_s_index+1] = new_state2
        # last_s_index -> end_state

        n_begin_s_index = last_s_index + 1
        n_last_s_index = n_begin_s_index
        n_prev_state = n_begin_s_index
        n_prev_state_r = n_begin_s_index
        r_index =0
        while r_index < len(regex):

            if regex[r_index] == '(':
                # print("(r)")
                # extract the regex in the bracket
                num_of_brackets = 1
                rgx_inside = ""
                l = r_index +1
                while num_of_brackets != 0:
                    if regex[l] == '(':
                        num_of_brackets +=1
                    elif regex[l] == ')':
                        num_of_brackets -=1
                    if num_of_brackets != 0:
                        rgx_inside += regex[l]
                    l+=1
                    # r_index +=1
                # print(rgx_inside)

                # call thompsons_construction function
                # solve_recursive_grouping(rgx_inside)
                i,last_s_r,f,r_prev_el =self.solve_recursive_grouping(initial_state,r_index,rgx_inside,states,n_last_s_index)
                # new initial state
                new_state = State()
                new_state.state_id = n_begin_s_index
                new_state.is_terminating = False
                new_state.next_states.update( {'ε654' : r_prev_el} )
                states[n_begin_s_index] = new_state

                n_begin_s_index = last_s_r
                n_last_s_index =n_begin_s_index
                # print(r_index)
                n_prev_state = r_prev_el
                r_index =  r_index + len(rgx_inside) + 2

            elif regex[r_index] == '|':
                begin_disjunction = n_last_s_index + 1

                r_index,d_last_s_index, finish = self.disjunction(initial_state, r_index+1, regex, states, n_last_s_index)

                # print("orr",begin_disjunction,d_last_s_index)
                # new initial state
                new_state = State()
                new_state.state_id = d_last_s_index + 1
                new_state.is_terminating = False
                new_state.next_states.update( {'ε144' : n_prev_state_r} )
                new_state.next_states.update( {'ε2775' : begin_disjunction  } )
                states[d_last_s_index + 1] = new_state
                #new end state
                new_state = State()
                new_state.state_id = d_last_s_index + 2
                new_state.is_terminating = False
                states[d_last_s_index + 2] = new_state

                # new
                new_state = State()
                new_state.state_id = n_last_s_index
                new_state.is_terminating = False
                new_state.next_states.update( {'ε456' : d_last_s_index + 2} )
                states[n_last_s_index] = new_state

                # new
                # states[d_last_s_index].next_states.update( {'e' : d_last_s_index + 2} )
                new_state = State()
                new_state.state_id = d_last_s_index
                new_state.is_terminating = False
                new_state.next_states.update( {'ε325' : d_last_s_index + 2} )
                states[d_last_s_index] = new_state

                n_last_s_index = d_last_s_index + 2
                # initial_state = d_last_s_index + 1
                n_prev_state = d_last_s_index + 1
                n_begin_s_index = d_last_s_index + 2
                n_prev_state_r = d_last_s_index + 1



                if finish == 1:
                    r_index = len(regex)
                # call or function
            elif regex[r_index] == '*':
                self.zero_or_more(states,n_begin_s_index,n_prev_state)

                n_begin_s_index =n_begin_s_index+1
                r_index +=1
                n_last_s_index = n_begin_s_index
            elif regex[r_index] == '+':
                self.one_or_more(states,n_begin_s_index,n_prev_state)

                n_begin_s_index =n_begin_s_index+1
                r_index +=1
                n_last_s_index = n_begin_s_index
            elif regex[r_index] == '?':
                self.zero_or_one(states,n_begin_s_index,n_prev_state)

                n_begin_s_index =n_begin_s_index+1
                r_index +=1
                n_last_s_index = n_begin_s_index
            elif regex[r_index] == '[':
                rgx_inside = self.ranges(regex,r_index,n_begin_s_index,states)

                n_prev_state = n_begin_s_index
                n_begin_s_index =n_begin_s_index+1
                r_index =  r_index + len(rgx_inside) + 2
                n_last_s_index = n_begin_s_index
            else:
                # print("ppp",regex[r_index],n_begin_s_index,regex[r_index +1])
                new_state = State()
                new_state.state_id = n_begin_s_index
                new_state.is_terminating = False
                #
                if (regex[r_index] == '.'):
                    new_state.next_states.update( {'ε4578' : n_begin_s_index +1} )
                else :
                    new_state.next_states.update( {regex[r_index] : n_begin_s_index +1} )
                states[n_begin_s_index] = new_state
                n_prev_state = n_begin_s_index
                n_begin_s_index =n_begin_s_index+1
                r_index +=1
                n_last_s_index = n_begin_s_index

        finish =1
        return -1,n_last_s_index,finish,n_prev_state_r
    def ranges(self,regex,r_index,begin_s_index,states):
        num_of_brackets = 1
        rgx_inside = ""
        l = r_index +1
        while num_of_brackets != 0:
            if regex[l] == '[':
                num_of_brackets +=1
            elif regex[l] == ']':
                num_of_brackets -=1
            if num_of_brackets != 0:
                rgx_inside += regex[l]
            l+=1
            # r_index +=1
        # print(rgx_inside)
        # new initial state
        new_state = State()
        new_state.state_id = begin_s_index
        new_state.is_terminating = False
        new_state.next_states.update( {'['+rgx_inside +']' : begin_s_index +1} )
        states[begin_s_index] = new_state
        return rgx_inside
    def zero_or_one(self,states,begin_s_index,prev_state):
        new_state = State()
        new_state.state_id = begin_s_index
        new_state.is_terminating = False
        new_state.next_states.update( {'ε41' : begin_s_index +1} )
        # in case of more will go back to the prev state
        # new_state.next_states.update( {'e2' : prev_state} )
        states[begin_s_index] = new_state
        # for zero will go to next state with e moves
        states[prev_state].next_states.update( {'ε33' : begin_s_index +1} )
    def one_or_more(self,states,begin_s_index,prev_state):
        # print("")
        # print("")
        # zero or more
        new_state = State()
        new_state.state_id = begin_s_index
        new_state.is_terminating = False
        new_state.next_states.update( {'ε15' : begin_s_index +1} )
        # in case of more will go back to the prev state
        new_state.next_states.update( {'ε27' : prev_state} )
        states[begin_s_index] = new_state
        # for zero will go to next state with e moves
        # states[prev_state].next_states.update( {'e' : begin_s_index +1} )
    def zero_or_more(self,states,begin_s_index,prev_state):
        new_state = State()
        new_state.state_id = begin_s_index
        new_state.is_terminating = False
        new_state.next_states.update( {'ε10' : begin_s_index +1} )
        # in case of more will go back to the prev state
        new_state.next_states.update( {'ε20' : prev_state} )
        states[begin_s_index] = new_state
        # for zero will go to next state with e moves
        states[prev_state].next_states.update( {'ε100' : begin_s_index +1} )
    def thompsons_construction(self,regex):
        r_index = 0
        states = {}
        s_0 = State()
        s_0.state_id =0
        s_0.is_terminating =False
        states.update({0:s_0})
        # point to the first state
        begin_s_index = 0
        # point to the last state
        last_s_index = 0
        # point to the initial state (starting state)
        initial_state = 0
        # previous element that will used in case of repetition
        prev_state = 0
        while r_index < len(regex):
            if regex[r_index] == '(':
                # print("(n)")
                # extract rgx in the bracket
                # begin_grouping = last_s_index + 1
                # print(regex[begin_grouping],"s" + str(begin_grouping))
                # extract the regex in the bracket
                num_of_brackets = 1
                rgx_inside = ""
                l = r_index +1
                while num_of_brackets != 0:
                    if regex[l] == '(':
                        num_of_brackets +=1
                    elif regex[l] == ')':
                        num_of_brackets -=1
                    if num_of_brackets != 0:
                        rgx_inside += regex[l]
                    l+=1
                    # r_index +=1
                # print(rgx_inside)

                # call thompsons_construction function
                i,n_last_s_index_r,f,n_prev_state_r = self.solve_recursive_grouping(initial_state,r_index,rgx_inside,states,last_s_index)
                # new initial state
                new_state = State()
                new_state.state_id = last_s_index
                new_state.is_terminating = False
                new_state.next_states.update( {'ε7' : n_prev_state_r} )
                states[last_s_index] = new_state

                last_s_index = n_last_s_index_r
                begin_s_index = last_s_index
                r_index =  r_index + len(rgx_inside) + 2
                # print(r_index)
                prev_state = n_prev_state_r

            elif regex[r_index] == '|':
                # print("or")
                # call or function
                begin_disjunction = last_s_index + 1
                r_index,d_last_s_index, finish = self.disjunction(initial_state, r_index+1, regex, states, last_s_index)
                # new initial state
                new_state = State()
                new_state.state_id = d_last_s_index + 1
                new_state.is_terminating = False
                new_state.next_states.update( {'ε144' : begin_disjunction} )
                new_state.next_states.update( {'ε277' : initial_state  } )
                states[d_last_s_index + 1] = new_state
                #new end state
                new_state = State()
                new_state.state_id = d_last_s_index + 2
                new_state.is_terminating = False
                states[d_last_s_index + 2] = new_state

                # new
                new_state = State()
                new_state.state_id = last_s_index
                new_state.is_terminating = False
                new_state.next_states.update( {'ε789' : d_last_s_index + 2} )
                states[last_s_index] = new_state

                # new
                # states[d_last_s_index].next_states.update( {'e' : d_last_s_index + 2} )
                new_state = State()
                new_state.state_id = d_last_s_index
                new_state.is_terminating = False
                new_state.next_states.update( {'ε684' : d_last_s_index + 2} )
                states[d_last_s_index] = new_state

                last_s_index = d_last_s_index + 2
                initial_state = d_last_s_index + 1
                prev_state = d_last_s_index + 1
                begin_s_index = d_last_s_index + 2



                if finish == 1:
                    r_index = len(regex)
            elif regex[r_index] == '*':
                self.zero_or_more(states,begin_s_index,prev_state)

                begin_s_index =begin_s_index+1
                r_index +=1
                last_s_index = begin_s_index

            elif regex[r_index] == '+':
                self.one_or_more(states,begin_s_index,prev_state)

                begin_s_index =begin_s_index+1
                r_index +=1
                last_s_index = begin_s_index

            elif regex[r_index] == '?':
                self.zero_or_one(states,begin_s_index,prev_state)

                begin_s_index =begin_s_index+1
                r_index +=1
                last_s_index = begin_s_index

            elif regex[r_index] == '[':

                rgx_inside = self.ranges(regex,r_index,begin_s_index,states)
                # update the indices
                prev_state = begin_s_index
                begin_s_index =begin_s_index+1
                r_index =  r_index + len(rgx_inside) + 2
                last_s_index = begin_s_index
            else:
                new_state = State()
                new_state.state_id = begin_s_index
                new_state.is_terminating = False
                if (regex[r_index] == '.'):
                    new_state.next_states.update( {'ε78' : begin_s_index +1} )
                else:
                    new_state.next_states.update( {regex[r_index] : begin_s_index +1} )
                states[begin_s_index] = new_state

                prev_state = begin_s_index
                begin_s_index =begin_s_index+1
                r_index +=1
                last_s_index = begin_s_index
        # print loop and print the states
        # print each state and its transitions like json

        new_state = State()
        new_state.state_id = last_s_index
        new_state.is_terminating = True
        states[last_s_index] = new_state


        # self.print_states(states,initial_state)
        self.save_json(states,initial_state)


        return 0
    def print_states(self,states,initial_state):
        print("{ \"startingState\": \"S"+str(initial_state)+"\",")
        #  sort states according to their state_id

        states = dict(sorted(states.items()))
        for state in states:
            print("  S"+str(states[state].state_id) + ": {")
            print("isTerminatingState: " + str(states[state].is_terminating) + ",")
            if states[state].is_terminating:
                print("}")
            else:
                print("Transitions: {")
                for transition in states[state].next_states:
                    print(transition + ": " + "S" + str(states[state].next_states[transition]) + ",")
                print("}")
                print("}")
        print("}")
    def draw_graph2(self):
        # "C:\Program Files\Graphviz\bin\dot.exe" run this command in the terminal to install graphviz
        # ! "C:\Program Files\Graphviz\bin\dot.exe"
        os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin/'
        # Load state machine definition from JSON file
        with open("states.json", "r") as json_file:
            state_machine_definition = json.load(json_file)
        #  want to set direction to left to right


        # Initialize the Digraph object
        dot = Digraph()

        # Set the direction of the graph
        dot.attr(rankdir="LR")

        # Add states to the graph
        for state_id, state_info in state_machine_definition["states"].items():
            label = f"{state_id}"
            if state_info['isTerminatingState']:
                dot.node(state_id, label=label, shape="doublecircle")
            else:
                dot.node(state_id, label=label)

        # Add transitions to the graph
        for state_id, state_info in state_machine_definition["states"].items():
            for event, next_state_id in state_info["Transitions"].items():
                dot.edge(state_id, next_state_id, label=event)

        # Save the graph to a file
        dot.render("state_machine_graph", format="png", cleanup=True)
    def draw_graph(self):

        # Add Graphviz bin directory to PATH
        os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin/'

        # Load state machine definition from JSON file
        with open("states.json", "r") as json_file:
            state_machine_definition = json.load(json_file)

        # Initialize the Digraph object
        dot = Digraph()

        # Set the direction of the graph (left to right)
        dot.attr(rankdir="LR")

        # Add states to the graph
        for state_id, state_info in state_machine_definition.items():
            label = f"{state_id}"
            if state_id == state_machine_definition["startingState"]:
                # dot.node(state_id, label=label, shape="doublecircle")
                print("")
            elif isinstance(state_info, dict) and not state_info.get('isTerminatingState', False):
                dot.node(state_id, label=label)
            elif isinstance(state_info, dict):
                dot.node(state_id, label=label, shape="doublecircle")

        # Add transitions to the graph
        for state_id, state_info in state_machine_definition.items():
            if state_id != "startingState" and isinstance(state_info, dict):
                for action, next_state_id in state_info.items():
                    if action != "isTerminatingState":
                        dot.edge(state_id, next_state_id, label=action)

        # Add arrow to the starting state
        dot.attr('edge',dir="forward")
        dot.edge('', state_machine_definition["startingState"], label='')

        # Save the graph to a file
        dot.render("state_machine_graph", format="png", cleanup=True)
    def validate_rounded_braces(self,string):
        stack = []
        for char in string:
            if char == '(':
                stack.append(char)
            elif char == ')':
                if not stack:
                    return False
                stack.pop()
        return not stack  # If the stack is empty, braces are balanced
    def validate_square_braces(self,string):
        stack = []
        for char in string:
            if char == '[':
                stack.append(char)
            elif char == ']':
                if not stack:
                    return False
                stack.pop()
        return not stack
    def validate_regex(self,regex):
        disallowed_pattern = r'[\{\}]'  # Pattern to disallow
        if re.search(disallowed_pattern, regex):
            return False
        allowed_chars_pattern = r'[\(\)a-zA-Z\[\]*?|+.0-9-]'
        return bool(re.match(allowed_chars_pattern, regex)) and self.validate_rounded_braces(regex) and self.validate_square_braces(regex)


    def expand_range(self,pattern):
        expanded = []
        expanded_pattern = ''
        i = 0
        while i < len(pattern):
            if pattern[i] == '[':
                expanded_pattern += '('
                i += 1
                while pattern[i] != ']':
                    if pattern[i + 1] == '-' and i + 2 < len(pattern) and ord(pattern[i]) < ord(pattern[i + 2]):
                        expanded.extend(chr(c) for c in range(ord(pattern[i]), ord(pattern[i + 2]) + 1))
                        i += 2
                    else:
                        expanded.append(pattern[i])
                    i += 1
                expanded_pattern += '|'.join(expanded)
                expanded_pattern += ')'
                expanded = []
            else:
                expanded_pattern += pattern[i]
            i += 1
        return expanded_pattern

def main():
    regex = input("Enter a regular expression: ")
    # trim space
    regex = regex.replace(" ", "")
    nfa = NFA()
    if nfa.validate_regex(regex):
        print("Valid regex")
        rr = nfa.expand_range(regex)
        # print(rr)
        nfa.thompsons_construction(rr)
        nfa.draw_graph()
    else :
        print("Invalid regex")
        print("Please enter a valid regex")


if __name__ == "__main__":
    main()
#((A)((A)*))
