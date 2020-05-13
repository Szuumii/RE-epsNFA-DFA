from parsing import Scanner, Parser,  ParseError
from nfa import  NFA_Constructor
from dfa import  DFA_Constructor, DFA


def test_1():
    regexp = "a|b*"
    my_scan = Scanner(regexp)
    my_parser = Parser(my_scan)
    my_parser.parse()
    nfa_construct = NFA_Constructor()
    my_nfa = nfa_construct.construct_nfa(my_parser.token_list)
    dfa_construct = DFA_Constructor()
    my_dfa = dfa_construct.construct_dfa(my_nfa)
    assert my_dfa.walk_dfa("ab") == False
    assert my_dfa.walk_dfa("a") == True
    assert my_dfa.walk_dfa("aa") == False
    assert my_dfa.walk_dfa("ba") == False
    assert my_dfa.walk_dfa("bbbb") == True

def test_2():
    regexp = "(ab|aa)*"
    my_scan = Scanner(regexp)
    my_parser = Parser(my_scan)
    my_parser.parse()
    nfa_construct = NFA_Constructor()
    my_nfa = nfa_construct.construct_nfa(my_parser.token_list)
    dfa_construct = DFA_Constructor()
    my_dfa = dfa_construct.construct_dfa(my_nfa)
    assert my_dfa.walk_dfa("ababab") == True
    assert my_dfa.walk_dfa("aaa") == False
    assert my_dfa.walk_dfa("a") == False
    assert my_dfa.walk_dfa("aa") == True
    assert my_dfa.walk_dfa("bb") == False

def test_3():
    regexp = "(cd*|bha)*jk"
    my_scan = Scanner(regexp)
    my_parser = Parser(my_scan)
    my_parser.parse()
    nfa_construct = NFA_Constructor()
    my_nfa = nfa_construct.construct_nfa(my_parser.token_list)
    dfa_construct = DFA_Constructor()
    my_dfa = dfa_construct.construct_dfa(my_nfa)
    assert my_dfa.walk_dfa("k") == False
    assert my_dfa.walk_dfa("mf") == False
    assert my_dfa.walk_dfa("jk") == True
    assert my_dfa.walk_dfa("e") == False
    assert my_dfa.walk_dfa("t") == False

def test_4():
    regexp = "ytut(a|g)*lk"
    my_scan = Scanner(regexp)
    my_parser = Parser(my_scan)
    my_parser.parse()
    #print(my_parser.show_token_list())
    nfa_construct = NFA_Constructor()
    my_nfa = nfa_construct.construct_nfa(my_parser.token_list)
    dfa_construct = DFA_Constructor()
    my_dfa = dfa_construct.construct_dfa(my_nfa)
    assert my_dfa.walk_dfa("a") == False
    assert my_dfa.walk_dfa("ytu") == False
    assert my_dfa.walk_dfa("ytutalk") == True

def test_5():
    
    try:
        regexp = "01('=34567)"
        my_scan = Scanner(regexp)
        my_parser = Parser(my_scan)
        my_parser.parse()
    except ParseError:
        print("test 5: Incorrect regexp")
    
    

def test_6():
    regexp = "(z*)"
    my_scan = Scanner(regexp)
    my_parser = Parser(my_scan)
    my_parser.parse()
    nfa_construct = NFA_Constructor()
    my_nfa = nfa_construct.construct_nfa(my_parser.token_list)
    dfa_construct = DFA_Constructor()
    my_dfa = dfa_construct.construct_dfa(my_nfa)
    assert my_dfa.walk_dfa("a") == False
    assert my_dfa.walk_dfa("4") == False
    assert my_dfa.walk_dfa("26546") == False
    assert my_dfa.walk_dfa("Owskemg") == False

    




test_1()
test_2()
test_3()
test_4()
test_5()
test_6()


