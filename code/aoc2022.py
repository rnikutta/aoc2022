import math
import re
from collections import deque
import numpy as np

import anytree
from anytree import AnyNode, RenderTree

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


def day07ab(inp='../inputs/d07a.dat'):

    # read input, construct tree
    root = AnyNode(id='root')
    
    with open(inp,'r') as f:
        for line in f:
            line = line.strip()
            print(line)
            if line == '$ cd /':
                node = root

            elif line == '$ ls' or line.startswith('dir '):
                pass

            elif line[0] in ('0','1','2','3','4','5','6','7','8','9'):
                size, fname = line.split(' ')
                size = int(size)
                leaf = AnyNode(id=fname,size=size,parent=node)

            elif line == '$ cd ..':
                node = node.parent
                
            elif line.startswith('$ cd'):
                d = line.split(' ')[2]
                node = AnyNode(id=d,parent=node)
                
    # puzzle A: find all dirs with each under 100,000 size

    # find all nodes that are dirs
    dirs = anytree.search.findall(root, filter_=lambda node: not hasattr(node,"size"))

    dirsizes = {}
    for d in dirs:
        files = anytree.search.findall(d, filter_=lambda node: hasattr(node,"size"))
        dirsizes[d.id] = sum([f.size for f in files])
    
    # for each dir node, find all nodes that are files; aggregate their sizes
    resultA = sum([v for k,v in dirsizes.items() if v <= 100000])


    # puzzle B
    total_space = 70000000
    needed_space = 30000000
    used_space = dirsizes["root"]
    unused_space = total_space - used_space
    needed_diff = needed_space - unused_space

    candidates = [v for v in dirsizes.values() if v >= needed_diff]
    resultB = min(candidates)

    return root, dirs, resultA, resultB


def day08ab(inp='../inputs/d08a_test.dat'):
    with open(inp,'r') as f:
        lines = f.readlines()


    nx, ny = len(lines), len(lines[0].strip())
    a = np.zeros((nx,ny),dtype=int)

    for j in range(len(lines)):
        a[j,:] = [int(_) for _ in lines[j].strip()]


    # puzzle A
    nouter = nx*2 + (ny-2)*2
    ninner = 0

    # brute force loop over all x,y
    for ix in range(1,nx-1):
        for iy in range(1,ny-1):
            thistree = a[ix,iy]
            
            # look left
            if (max(a[:ix,iy]) < thistree) or\
               (max(a[ix+1:,iy]) < thistree) or\
               (max(a[ix,:iy]) < thistree) or\
               (max(a[ix,iy+1:]) < thistree):
                ninner += 1
                next


    # puzzle B
    def get_scenic_score(ix_,iy_):
        thistree = a[ix,iy]
        
        # look up
        ntrees = []

        def along_los(los):
            lostrees = 0
            for e in los:
                if e < thistree:
                    lostrees += 1
                elif e >= thistree:
                    lostrees += 1
                    break

            return lostrees

        los = a[ix-1::-1,iy] # look up, starting and including the current location
        ntrees.append(along_los(los))

        los = a[ix+1:,iy] # look down
        ntrees.append(along_los(los))

        los = a[ix,iy-1::-1] # look left
        ntrees.append(along_los(los))

        los = a[ix,iy+1:] # look right
        ntrees.append(along_los(los))

#        print("ntrees:", ntrees)
#        print("ix_,iy_,thistree,losu,ntrees:",ix_,iy_,thistree,los,ntrees)
#        print()
        
        return np.product(ntrees)

    
    scenic_scores = np.zeros((nx,ny),dtype=int)
    for ix in range(1,nx-1):
        for iy in range(1,ny-1):
            scenic_scores[ix,iy] = get_scenic_score(ix,iy)
        
    return a, nouter, ninner, nouter+ninner, scenic_scores, np.max(scenic_scores)


def day9a(inp='../inputs/d09a_test.dat'):
    with open(inp,'r') as f:
        lines = f.readlines()

    Hx, Hy = 0, 0
    Tx, Ty = 0, 0

    tvisited = [ ]
    
    for line in lines:
        op, n = line.strip().split()

        # move H
        for j in range(int(n)):
            if op == 'R':
                Hx += 1
            elif op == 'L':
                Hx -= 1
            elif op == 'U':
                Hy += 1
            elif op == 'D':
                Hy -= 1

            # update T
            if (abs(Hx-Tx)>1) or (abs(Hy-Ty)>1):
                Tx += np.sign(Hx-Tx)
                Ty += np.sign(Hy-Ty)


#            print("  ", (Tx,Ty))
            tvisited.append((Tx,Ty))
            
#        print()

    return tvisited, len(set(tvisited))


def day9b(inp='../inputs/d09a_test.dat',nknots=10):

    with open(inp,'r') as f:
        lines = f.readlines()

    pos = np.zeros((nknots,2),dtype=int)  # 10 knots, 2 positions each (x,y)
    
    tvisited = [ ]
    
    for line in lines:
        op, n = line.strip().split()

        # move H
        for j in range(int(n)):
            if op == 'R':
                pos[0,0] += 1
            elif op == 'L':
                pos[0,0] -= 1
            elif op == 'U':
                pos[0,1] += 1
            elif op == 'D':
                pos[0,1] -= 1

            # update N-1 trailing knots
            for k in range(1,nknots):
                if (abs(pos[k-1,0]-pos[k,0])>1) or (abs(pos[k-1,1]-pos[k,1])>1):
                    pos[k,0] += np.sign(pos[k-1,0]-pos[k,0])
                    pos[k,1] += np.sign(pos[k-1,1]-pos[k,1])

            tvisited.append((pos[-1,0],pos[-1,1]))

    return tvisited, len(set(tvisited))


def day10a(inp='../inputs/d10a_test.dat'):

    Xinit = 1
    X = []
    
    with open(inp,'r') as f:
        c = 0
        for line in f:
            res = line.split()
            if c == 0:
                X.append(Xinit)
            if len(res) == 1:
                X.append(X[-1])
            elif len(res) == 2:
                X += [X[-1]]
                X += [X[-1]+int(res[1])]

            c += 1

    cycles = [20,60,100,140,180,220]
    sum6 = sum([X[c-1]*c for c in cycles])
            
    return X, sum6


def day10b(inp='../inputs/d10a_test.dat'):

    crt = np.zeros(6*40,dtype=int)

    # data reading and construction of X exactly as in day10a()
    Xinit = 1
    X = []
    
    with open(inp,'r') as f:
        c = 0
        for line in f:
            res = line.split()
            if c == 0:
                X.append(Xinit)
            if len(res) == 1:
                X.append(X[-1])
            elif len(res) == 2:
                X += [X[-1]]
                X += [X[-1]+int(res[1])]

            c += 1

    # now draw on the crt screen; we realize that the crt is just a
    # 1-D array of 240 elements; reshaping into 6 rows only happens at
    # the end
    for j in range(0,len(X)-1):
        center = X[j]  # center position of the 3-wide sprite
        currentrow = j // 40  # X gives the sprite position, but only along a repeating 0..39 line; we need to introduce crt line skipping
        center = center + currentrow*40
        spritepos = list(range(center-1,center+2))

        # draw (or not) on the crt line
        if j in spritepos:
            crt[j] = 1
        else:
            crt[j] = 0
    
    # reshape single crt line to a rectangle 6x40
    crtr = crt.reshape(6,40)

    # Converts ones to # and zeros to space, print rows
    for j in range(crtr.shape[0]):
        row = "".join([str(_) for _ in crtr[j,:]])
        row = row.replace('1','#')
        row = row.replace('0',' ')
        print(row)
    
    return X, crt, crtr


    
