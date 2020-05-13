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
        self.alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
       
    def get_token(self): 
        if self.current < self.length:
            c = self.regexpr[self.current]
            self.current += 1
            if c not in self.symbols.keys():
                if c not in self.alphabet:
                    raise ParseError
                else:
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
        if self.lookahead_pointer.name in ['STAR']:
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








