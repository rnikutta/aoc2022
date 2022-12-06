import math
import re
from collections import deque
import numpy as np

def day01a(inp='../inputs/01a.dat'):

    d = {}
    k = 0
    s = 0
    
    with open(inp,'r') as f:
        for line in f:
            line = line.strip()
            if line == '':
                d[k] = s
                s = 0
                k += 1
            else:
                print(line)
                s += int(line)

    return d, max(d.values())


def day01b(d):
    """Input d is the result dict d from day01a()."""
    
    sumtop3 = np.sort(list(d.values()))[-3:].sum()
    return sumtop3


def day02a(inp='../inputs/d02a.dat'):

    # read input
    they, me = [], []
    with open(inp,'r') as f:
        for line in f:
            t,m = line.strip().split(' ')
            they.append(t)
            me.append(m)


    map_they = {'A':'rock', 'B':'paper', 'C':'scissors'}
    map_me =   {'X':'rock', 'Y':'paper', 'Z':'scissors'}

    map_value = {'rock':1, 'paper':2, 'scissors':3}

    map_win = {'lose':0, 'draw':3, 'win':6}

    def get_wins(t,m):
        if t == m:
            return 'draw'
        elif t == 'rock':
            if m == 'paper':
                return 'win'
            elif m == 'scissors':
                return 'lose'
        elif t == 'paper':
            if m == 'rock':
                return 'lose'
            elif m == 'scissors':
                return 'win'
        elif t == 'scissors':
            if m == 'rock':
                return 'win'
            elif m == 'paper':
                return 'lose'
        
    total = 0
    for j in range(len(they)):
        t = map_they[they[j]]
        m = map_me[me[j]]
        points_win = map_win[get_wins(t,m)]
        points_choice = map_value[m]
        total += points_win
        total += points_choice
    
    return they, me, total


def day02b(inp='../inputs/d02a.dat'):

    # read input
    they, me = [], []
    with open(inp,'r') as f:
        for line in f:
            t,m = line.strip().split(' ')
            they.append(t)
            me.append(m)

    they = np.array(they,dtype='U10')
    me = np.array(me,dtype='U10')

    they[they=='A'] = 'rock'
    they[they=='B'] = 'paper'
    they[they=='C'] = 'scissors'

    me[me=='X'] = 'lose'
    me[me=='Y'] = 'draw'
    me[me=='Z'] = 'win'

    outcomes = {'rock_draw':'rock',
                'rock_win':'paper',
                'rock_lose':'scissors',
                'paper_draw':'paper',
                'paper_win':'scissors',
                'paper_lose':'rock',
                'scissors_draw':'scissors',
                'scissors_win':'rock',
                'scissors_lose':'paper'}

    map_value = {'rock':1, 'paper':2, 'scissors':3}
    map_win = {'lose':0, 'draw':3, 'win':6}

    total = 0
    for j in range(len(me)):
        t = they[j]
        outcome = me[j]
        mychoice = outcomes[t+'_'+outcome]
        points = map_value[mychoice] + map_win[outcome]
        total += points
    
    return they, me, total


def day03a(inp='../inputs/d03a_test.dat'):

    items = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    contents = []

    # read input
    with open(inp,'r') as f:
        for line in f:
            line = line.strip()
            n = len(line)
            if n % 2 != 0:
                raise(Exception, "Number of items not even!")

            c1 = line[:n//2]
            c2 = line[n//2:]

            contents.append((c1,c2))


    priority_sum = 0
    for (c1,c2) in contents:
        inter = set(c1).intersection(set(c2))
        if len(inter) > 1:
            raise(Exception,"More than one common item type")

        item = inter.pop()
        priority = items.find(item) + 1
        priority_sum += priority

    return contents, priority_sum


def day03b(inp='../inputs/d03a_test.dat'):

    items = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    contents = []

    # read input
    with open(inp,'r') as f:
        lines = f.readlines()

    lines = np.array([line.strip() for line in lines])
    groups = np.array_split(lines, math.ceil(lines.size/3))

    priority_sum = 0
    for g in groups:
        inter = set(g[0]).intersection(set(g[1])).intersection(set(g[2]))
        if len(inter) > 1:
            raise(Exception,"More than one common item type")

        item = inter.pop()
        priority = items.find(item) + 1
        priority_sum += priority
    
    return lines, priority_sum
        

def day04a(inp='../inputs/d04a_test.dat'):

    # read input
    sections = []
    with open(inp,'r') as f:
        for line in f:
            line = line.strip().replace('-',',')
            values = [int(_) for _ in line.split(',')]
            sections.append(values)

    ncontained = 0
    for pair in sections:
        if ((pair[0] <= pair[2]) and (pair[1] >= pair[3])) or \
           ((pair[0] >= pair[2]) and (pair[1] <= pair[3])):
           ncontained += 1

    return sections, ncontained


def day04b(inp='../inputs/d04a_test.dat'):

    # read input
    sections = []
    with open(inp,'r') as f:
        for line in f:
            line = line.strip().replace('-',',')
            values = [int(_) for _ in line.split(',')]
            sections.append(values)

    ncontained = 0
    for pair in sections:
        if ((pair[2] >= pair[0]) and (pair[2] <= pair[1])) or \
           ((pair[0] >= pair[2]) and (pair[0] <= pair[3])):
           ncontained += 1

    return sections, ncontained


def day05ab(nlines=3,inp='../inputs/d05a_test.dat',cargolifter=9000):
    
    def readinp(inp,nlines):

        # stack
        lines = []
        with open(inp,'r') as f:
            for j in range(nlines):
                line = f.readline().rstrip('\n')
                lines.append(line)

        # remove brackets
        lines = [_.replace('[','') for _ in lines]
        lines = [_.replace(']','') for _ in lines]

        # sub '-' for empty position
        lines = [_.replace('    ',' - ').replace(' ','') for _ in lines]

        # create stacks
        n = len(lines[0])
        stacks = {}
        for j in range(n):
            stack = ''.join([_[j] for _ in lines])
            stack = stack.replace('-','')
            stacks[j+1] = stack
        
        # operations
        ops = []
        pattern = re.compile('move (\d+) from (\d+) to (\d+)')
        with open(inp,'r') as f:
            for op in f:
                if op.startswith('move'):
                    res = pattern.findall(op)
                    print(res)
                    ops.append([int(_) for _ in res[0]])
                
        return lines, stacks, ops

    lines, stacks, ops = readinp(inp,nlines)


    # perform all ops
    for op in ops:
        number, source, target = op
        source_stack = stacks[source]
        target_stack = stacks[target]

        cargo = source_stack[:number]
        source_stack = source_stack[number:]

        if cargolifter == 9000:
            target_stack = cargo[::-1] + target_stack
        elif cargolifter == 9001:
            target_stack = cargo + target_stack
            
        stacks[source] = source_stack
        stacks[target] = target_stack

    final = ''.join([_[0] for _ in stacks.values()])
    print(final)
    
    return lines, stacks, ops, final


def day06a(inp='../inputs/d06a.dat',nchars=4):
    
    with open(inp,'r') as f:
        s = f.readline().strip()

    buf = deque(maxlen=nchars)
    counter = 0
    for c in s:
        buf.append(c)
        counter += 1
        if len(set(buf)) == nchars:
            print(buf, counter)
            break

    return counter

