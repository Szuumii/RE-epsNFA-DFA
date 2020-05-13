#Basic NFA state representation
class NFA_State:
    def __init__(self, name):
        self.epsilon_closure = [] # epsilon-closure
        self.transitions_table = {} # char : state
        self.name = name
        self.is_final = False

#NFA representation
class NFA:
    def __init__(self, start, end):
        self.start = start
        self.end = end # start and end states
        end.is_final = True

    def show_nfa(self):
        self.pretty_print(self.start)

    def pretty_print(self,state):
        
        if state.is_final is True:
            return

        print("\nState: ",state.name)
        if state.epsilon_closure:
            print("Epsilon closure: ", end="")
            for elem in state.epsilon_closure:
                print(elem.name, end=" ")
            print("\n")

        if state.transitions_table:
            print("Transition table: ",end="")
            for elem in state.transitions_table.keys():
                print(elem + ":",state.transitions_table[elem].name, end=" ")
            print("\n")

    
        if state.epsilon_closure:
            for elem in state.epsilon_closure:
                self.pretty_print(elem)

        if state.transitions_table:
            for elem in state.transitions_table.keys():
                self.pretty_print(state.transitions_table[elem])
    
        

#Constructs NFA form a given token list
class NFA_Constructor:
    def __init__(self):
        self.constructors = {'CHAR':self.construct_char, 'CONCAT':self.construct_concat,
                         'ALT':self.construct_union, 'STAR':self.construct_star }
        self.state_count = 0
        self.nfa_stack = []

    def construct_state(self):
        self.state_count += 1
        return NFA_State('s' + str(self.state_count))
    
    def construct_char(self, t):
        s0 = self.construct_state()
        s1 = self.construct_state()
        s0.transitions_table[t.value] = s1
        nfa = NFA(s0, s1)
        self.nfa_stack.append(nfa)
    
    def construct_concat(self, t):
        n2 = self.nfa_stack.pop()
        n1 = self.nfa_stack.pop()
        n1.end.is_final = False
        n1.end.epsilon_closure.append(n2.start)
        nfa = NFA(n1.start, n2.end)
        self.nfa_stack.append(nfa)
    
    def construct_union(self, t):
        n2 = self.nfa_stack.pop()
        n1 = self.nfa_stack.pop()
        s0 = self.construct_state()
        s0.epsilon_closure = [n1.start, n2.start]
        s3 = self.construct_state()
        n1.end.epsilon_closure.append(s3)
        n2.end.epsilon_closure.append(s3)
        n1.end.is_final = False
        n2.end.is_final = False
        nfa = NFA(s0, s3)
        self.nfa_stack.append(nfa)
    
    def construct_star(self, t):
        n1 = self.nfa_stack.pop()
        s0 = self.construct_state()
        s1 = self.construct_state()
        s0.epsilon_closure = [n1.start]
        s0.epsilon_closure.append(s1)
        n1.end.epsilon_closure.extend([s1, n1.start])
        n1.end.is_final = False
        nfa = NFA(s0, s1)
        self.nfa_stack.append(nfa)

    def construct_nfa(self, token_list):
        for t in token_list:
            self.constructors[t.name](t)
        assert len(self.nfa_stack) == 1
        return self.nfa_stack.pop()
