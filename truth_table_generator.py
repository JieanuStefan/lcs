# - is negation, = is equivalance, & is conjunction, / is disjunction, > is implication
#  (((P>Q)/S)=T), (P&((-Q)&(-(-(Q=(-R)))))),  (((P/Q)>(-(P/Q)))&(P/(-(-Q)))), (((P&Q)/S)=(-T))

import itertools
import copy

proposition = input("Enter a proposition: ")
logical_connectives = '-=&/>'
tree = []
tree_copy = []

truth_values = {}

# Parses the given string and generates a nested list containing the expression
def create_tree(i, original):

    while i < len(proposition):
        if proposition[i] == ' ':
            i += 1
        elif proposition[i] == '(':
            new_list = []
            original.append(new_list)
            i = create_tree(i+1, new_list)
        elif proposition[i].isalpha() or logical_connectives.find(proposition[i]) != -1:
            original.append(proposition[i])
            i += 1
        elif proposition[i] == ')':
            return i + 1

    return i

# Parses the nested list and replaces each atom with it's corresponding truth value
def tree_to_truth_value(l):
    for i in range(0, len(l)):
        if type(l[i]) is str:
            if l[i].isalpha():
                l[i] = truth_values[l[i]]
        else:
            tree_to_truth_value(l[i])

# Parses the nested list and returns the truth value of the proposition
def parse_truth_value(l):   
    if isinstance(l, bool):
        return l
                
    for i in range(0, len(l)):
        if isinstance(l, bool):
            return l
        if isinstance(l[i], str):
            if logical_connectives.find(l[i]) != -1:
                if l[i] == '-':
                    l = not parse_truth_value(l[i+1])
                elif l[i] == '&':
                    l = parse_truth_value(l[i-1]) and parse_truth_value(l[i+1])
                elif l[i] == '=':
                    l = parse_truth_value(l[i-1]) == parse_truth_value(l[i+1])
                elif l[i] == '/':
                    l = parse_truth_value(l[i-1]) or parse_truth_value(l[i+1])
                elif l[i] == '>':
                    first = parse_truth_value(l[i-1])
                    second = parse_truth_value(l[i+1])
                    if (first == True and second == False):
                        l = False
                    else:
                        l = True

    return l
                    
def find_atoms(l):
    for i in range(0, len(l)):
        if type(l[i]) is str:
            if l[i].isalpha():
                truth_values[l[i]] = True
        else:
            find_atoms(l[i])


# Generate the tree
create_tree(0, tree)

# Find all the atoms in the tree
find_atoms(tree)

# Generate all truth values
values = [True, False]
values_permutations = list(itertools.product(values, repeat=len(truth_values)))
for i in range(0, len(values_permutations)):
    for j in range(0, len(truth_values)):
        truth_values[list(truth_values.keys())[j]] = values_permutations[i][j]
    # Replace the atoms with the truth values
    tree_copy = copy.deepcopy(tree)
    tree_to_truth_value(tree_copy)
    
    value = parse_truth_value(tree_copy[0])
    print (truth_values, value)


