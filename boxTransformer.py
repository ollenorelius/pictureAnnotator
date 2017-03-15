import sys
import os

folder = sys.argv[1]

if not os.path.exists:
    print('Invalid folder!')
    quit()
try:
    f = open(folder + '/list.txt', 'r')
except:
    print('Could\'nt open file list.txt!')
    quit()

try:
    f_out = open(folder + '/list2.txt', 'w')
except:
    print('Could\'nt create outout file list2.txt!')
    quit()


for line in f:
    tokens = line.strip().split(' ')
    x1 = float(tokens[1])
    y1 = float(tokens[2])
    x2 = float(tokens[3])
    y2 = float(tokens[4])

    midx = (x1 + x2)/2
    midy = (y1 + y2)/2

    w = (x2-x1)
    h = (y2-y1)

    tokens[1] = '{0:.3f}'.format(midx)
    tokens[2] = '{0:.3f}'.format(midy)
    tokens[3] = '{0:.3f}'.format(w)
    tokens[4] = '{0:.3f}'.format(h)

    f_out.write(' '.join(tokens))
    f_out.write('\n')
