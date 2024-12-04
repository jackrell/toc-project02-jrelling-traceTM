#!/usr/bin/env python3
''' traceTM -- traces nondeterministic (and deterministic) turing machine execution'''

import sys
import csv

MAX_DEPTH = 100

# Functions
def usage(exit_status: int=0) -> None:
    ''' Print usage and exit '''
    print('Usage: traceTM_jrelling.py TMFILE STRING [OPTIONAL -m MAXDEPTH]', file=sys.stderr)
    sys.exit(exit_status)


def run_tm(start_state, string, transitions, accept_state):
    ''' runs the tm on the input string '''
    depth = 0
    start_config = [["", start_state, string], None] # second value to keep track of parent config
    tree = [[start_config]]
    
    accepted = 0
    exceeded_depth = 0

    final_config = []
    
    while 1:
        num_configs = 0
        
        new_level = []
        for config in tree[depth]:
            state = config[0][1]
            symbol = config[0][2][0]
            
            if state == accept_state:
                accepted = 1
                final_config = config[0]
                break # config was accepted
            
            # check every transition 
            for transition in transitions:
                if transition[0] == state and transition[1] == symbol:
                    new_state = transition[2]
                    new_symbol = transition[3]
                    movement = transition[4] 
                    
                    if movement == 'R':
                        new_config = [[config[0][0] + new_symbol, new_state, config[0][2][1:]], config[0]]
                        if new_config[0][2] == "":
                            new_config[0][2] = "_"
                    elif movement == 'L':
                        new_config = [[config[0][0][:-1], new_state, config[0][0][-1] + new_symbol + config[0][2][1:]], config[0]]
                    
                    new_level.append(new_config)
                    num_configs+=1
        
        if accepted:
            break
        if depth > MAX_DEPTH:
            print('Exceeded MAX_DEPTH of', MAX_DEPTH, 'and execution was stopped.')
            break
        if num_configs == 0: # rejected, no more paths
            depth += 1 # because I don't physically transition to reject state, would add another level
            print('String rejected in', depth, 'steps')
            break

        depth+=1
        tree.append(new_level)
    

    if accepted:
        print()
        print('String accepted in', depth, 'steps')
        config_print(tree, final_config)



    total_transitions = 0
    for d, level in enumerate(tree, start=1):
        # print(d) # debug
        for config in level:
            total_transitions += 1
            # print('config:', config[0], 'parent:', config[1]) # debug
    total_transitions -= 1 # for start config

    print()
    print('Depth of tree of configurations:', depth)
    print('Total number of transitions:', total_transitions)
    print('Average nondeterminism:', total_transitions/depth)
    print()
    

 
def config_print(tree, final_config):
    c = final_config
    config_list = []
    for level in tree[::-1]:
        for config in level:
            if c == config[0]:
                config_list.append(' ' + c[0] + ' ' + c[1] + ' ' + c[2][0] + ' ' + c[2][1:]) # joining together the configuration pieces
                c = config[1] # parent
    for index, item in enumerate(config_list[::-1], start=1):
        print('C' + str(index), item)





def main(arguments=sys.argv[1:]) -> None:
    ''' Reads arguments and runs the machine '''
    if len(arguments) != 2:
        if len(arguments) == 1 and arguments[0] == "-h":
            usage(0)
        elif len(arguments) == 4 and arguments[2] == "-m":
            global MAX_DEPTH
            MAX_DEPTH = int(arguments[3])
        else:
            usage(1)

    tmfile = arguments[0]
    string = arguments[1] if arguments[1].endswith('_') else arguments[1] + '_'

    # extracting information about machine
    transitions = []
    start_state, accept_state, reject_state = '', '', ''
    with open(tmfile, 'r') as f:
        csv_file = csv.reader(f)
        for i, line in enumerate(csv_file, start=1):
            if i == 1:
                print('Machine Name:', line[0])
            elif i == 2 or i == 3 or i == 4:
                continue
            elif i == 5:
                start_state = line[0]
            elif i == 6:
                accept_state = line[0]
            elif i == 7:
                reject_state = line[0]
            else:
                transitions.append(line)

    print('Input String:', string)
    # print('start:', start_state)
    # print('accept:', accept_state)
    # print('transitions:', transitions)
    
    run_tm(start_state, string, transitions, accept_state)



if __name__ == '__main__':
    main()
