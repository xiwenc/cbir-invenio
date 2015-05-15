import sys
import os

file1 = sys.argv[1]
file2 = sys.argv[2]

with open(file1, 'r') as f1:
    lines1 = [l.strip() for l in f1.readlines()]

with open(file2, 'r') as f2:
    lines2 = [l.strip() for l in f2.readlines()]

lines1_count = len(lines1)
lines2_count = len(lines2)
assert lines1_count == lines2_count

column1 = os.path.basename(file1).replace('.txt', '')
column2 = os.path.basename(file2).replace('.txt', '')

print '\\begin{tabular}{|l|l|l|}'
print '\\hline'
print '& & \\\\'
print '\\textbf{Image} & \\parbox{1.5in}{\\textbf{%s}} & \\parbox{1.5in}{\\textbf{%s}} \\\\' % (column1, column2)
print '& & \\\\'
print '\\hline'

current1 = None
current2 = None
base1 = None
for i in range(lines1_count):
    current_line = lines1[i]
    if current_line.startswith('src'):
        continue

    if 'datasets' in current_line:
        if current_line.startswith('datasets'):
            if current1 is not None:
                print '{name} & {v1} & {v2}\\\\'.format(name=base1, v1=current1, v2=current2)
            full_name1 = lines1[i].split('\t')[0]
            full_name2 = lines2[i].split('\t')[0]
            base1 = os.path.basename(full_name1)
            base2 = os.path.basename(full_name2)
            assert base1 == base2
            current1 = None
            current2 = None
        else:

            v1 = float(lines1[i].split()[2])
            v2 = float(lines2[i].split()[2])
            if current1 is None:
                current1 = v1
            else:
                current1 = (current1 + v1) / 2

            if current2 is None:
                current2 = v2
            else:
                current2 = (current2 + v2) / 2

if current1 is not None:
    print '{name} & {v1} & {v2}\\\\'.format(name=base1, v1=current1, v2=current2)
print '\\hline'
print '\\end{tabular}\n'
print '\\caption{Average similarities of \\emph{%s} and \\emph{%s}}' % (column1, column2)
