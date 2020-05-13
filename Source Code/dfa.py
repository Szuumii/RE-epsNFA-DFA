#Basic DFA State
class DFA_State:
    def __init__(self, name):
        self.nfa_states = []
        self.transitions_table = {}
        self.name = name
        self.is_final = False

#Class representing DFA
class DFA:
    def __init__(self):
        self.states = []

    def check_state(self,given_states):
        for state in self.states:
            if set(given_states) == set(state.nfa_states):
                return state
        return None

    def walk_dfa(self, word):
        self.current_state = self.states[0]
        for letter in word:
            if letter in self.current_state.transitions_table.keys():
                self.current_state = self.current_state.transitions_table[letter]
            else:
                return False

        if self.current_state.is_final:
            return True
        else:
            return False

    def show_dfa(self):
        self.pretty_print(self.states[0])

    def pretty_print(self,dfa_state):
        
        
        if dfa_state.is_final is True:
            print("\nState: " + dfa_state.name + " is final state!")
            print("NFA States: ",end="")
            for elem in dfa_state.nfa_states:
                print(elem.name, end=" ")
            print("\nTransition table ",end="")
            for elem in dfa_state.transitions_table.keys():
                print(elem + ":", dfa_state.transitions_table[elem].name, end=" ")
            print("\n")
            return
        
        print("\nState: " + dfa_state.name)
        print("NFA States: ",end="")
        for elem in dfa_state.nfa_states:
            print(elem.name, end=" ")
        print("\nTransition table ",end="")
        for elem in dfa_state.transitions_table.keys():
            print(elem + ":", dfa_state.transitions_table[elem].name, end=" ")

        print("\n")
        
        for elem in dfa_state.transitions_table.keys():
            self.pretty_print(dfa_state.transitions_table[elem])
        

#Class constructing DFA
class DFA_Constructor:
    def __init__(self):
        self.state_count = 0
        self.alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

    def construct_state(self):
        self.state_count += 1
        return DFA_State('DFA_s' + str(self.state_count))

    def eps_closure(self, states):
        retv = []
        retv.extend(states)
        for state in retv:
            new_states = state.epsilon_closure
            retv.extend(new_states)
        return retv


    def move(self,states,letter):
        retv = []
        for state in states:
            if state.transitions_table.get(letter) is not None:
                retv.append(state.transitions_table[letter])
        return retv

    def construct_dfa(self,nfa):
        retvDFA = DFA()
        s1 = self.construct_state()
        s1.nfa_states = self.eps_closure([nfa.start])
        retvDFA.states.append(s1)
        for state in retvDFA.states:
            for letter in self.alphabet:
                move_states = self.move(state.nfa_states,letter)
                if not move_states:
                    continue

                new_set_of_nfa_states = self.eps_closure(move_states)
                exisiting_state = retvDFA.check_state(new_set_of_nfa_states)
                
                if exisiting_state is None:
                    new_dfa_state = self.construct_state()
                    new_dfa_state.nfa_states = new_set_of_nfa_states
                    if nfa.end in new_set_of_nfa_states:
                        new_dfa_state.is_final = True
                    retvDFA.states.append(new_dfa_state)
                    state.transitions_table[letter] = new_dfa_state
                    continue
                else:
                    state.transitions_table[letter] = exisiting_state  


        return retvDFA  
