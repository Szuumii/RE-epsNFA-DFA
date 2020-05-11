
#Exception class for token mismatch, invalid alphabet or invalid symbol
class ParseError(Exception):
    pass

#Atomic structute for recognizing input patameters
class Token:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        return self.name + ":" + self.value

#Scanner for returning tokens based on input regexp
class Scanner:
    def __init__(self, inp_pattern):
        self.regexpr = inp_pattern
        self.symbols = {'(':'LEFT_PAREN', ')':'RIGHT_PAREN', '*':'STAR', '|':'ALT', '\x08':'CONCAT'}
        self.current = 0
        self.length = len(self.regexpr)
       
    def get_token(self): 
        if self.current < self.length:
            c = self.regexpr[self.current]
            self.current += 1
            if c not in self.symbols.keys():
                token = Token('CHAR', c)
            else:
                token = Token(self.symbols[c], c)
            return token
        else:
            return Token('NONE', '')

    def show_pattern(self):
        print(self.regexpr)


#Creates token list from regexp placed in scanner
class Parser:
    def __init__(self, scanner):
        self.scanner = scanner
        self.token_list = []
        self.lookahead_pointer = self.scanner.get_token()
    
    def shift(self, name):
        if self.lookahead_pointer.name == name:
            self.lookahead_pointer = self.scanner.get_token()
        elif self.lookahead_pointer.name != name:
            raise ParseError

    def parse(self):
        self.check_union()
        return self.token_list
    
    def check_union(self):
        self.check_concat()
        if self.lookahead_pointer.name == 'ALT':
            t = self.lookahead_pointer
            self.shift('ALT')
            self.check_union()
            self.token_list.append(t)

    def check_concat(self):
        self.check_closure()
        if self.lookahead_pointer.value not in ')|':
            self.check_concat()
            self.token_list.append(Token('CONCAT', '\x08'))
    
    def check_closure(self):
        self.check_char()
        if self.lookahead_pointer.name in ['STAR', 'PLUS', 'QMARK']:
            self.token_list.append(self.lookahead_pointer)
            self.shift(self.lookahead_pointer.name)

    def check_char(self):
        if self.lookahead_pointer.name == 'LEFT_PAREN':
            self.shift('LEFT_PAREN')
            self.check_union()
            self.shift('RIGHT_PAREN')
        elif self.lookahead_pointer.name == 'CHAR':
            self.token_list.append(self.lookahead_pointer)
            self.shift('CHAR')

    def show_token_list(self):
        print("Token List: ", end="")
        for elem in self.token_list:
            print(elem.__str__(), end=" ")

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

    #iter print
    def iter_print(self,state):
        self.set_of_states = []
        self.set_of_states.append(state)
        for elem in self.set_of_states:
            if elem.epsilon_closure:
                print("Epsilon closure: ", end="")
                for one in elem.epsilon_closure:
                    print(one.name, end=" ")
                print("\n")

            if elem.transitions_table:
                print("Transition table: ",end="")
                for one in elem.transitions_table.keys():
                    print(one + ":",state.transitions_table[elem].name, end=" ")
                print("\n")


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



class DFA_State:
    def __init__(self, name):
        self.nfa_states = []
        self.transitions_table = {}
        self.name = name
        self.is_final = False


class DFA:
    def __init__(self):
        self.states = []

    def give_state(self,given_states):
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
                exisiting_state = retvDFA.give_state(new_set_of_nfa_states)
                
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








