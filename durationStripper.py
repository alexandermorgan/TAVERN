import os, sys; sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from score import Score
import pdb
import shlex, subprocess
import re
path = os.getcwd()

# **harm spine syntax reference: https://www.humdrum.org/rep/harm/index.html
filesToCheck = []  # look at 'M573_06_01a_a.krn'
problemFiles = []
for composer in os.listdir(path):
    if not os.path.isdir(composer) or composer.startswith('.'):
        continue
    composerPath = os.path.join(path, composer)

    for work in os.listdir(composerPath):
        workPath = os.path.join(composerPath, work)
        if not os.path.isdir(workPath):
            continue
        joinedPath = os.path.join(workPath, 'Joined')
        noDurPath = os.path.join(workPath, 'Stripped')
        if 'Stripped' not in os.listdir(workPath):
            os.makedirs(noDurPath)

        for file in os.listdir(joinedPath):
            if not file.endswith('.krn'):
                continue
            currFilePath = os.path.join(joinedPath, file)
            newFilePath = os.path.join(noDurPath, file)
            ### humsed version
            # _args = shlex.split(r"humsed -E 's/[0-9]\.?([iIvV]+)/\1/g' " + currFilePath)
            # with open(newFilePath, "w") as out_file:
            #     subprocess.run(args=_args, stdout=out_file)
            ### python-only version
            with open(currFilePath, 'r') as input_file:
                modified = re.sub(r'[0-9]+\.*([iIvVr]+|-|Cc|Gn|Nb|Tr|N|Lt|Fr|~|Cto)', r'\1', input_file.read())
                m1 = modified
                if 'Cc' in modified:
                    iCount = modified.count('\ti\t') + modified.count('\tib\t')
                    ICount = modified.count('\tI\t') + modified.count('\tIb\t')
                    if ICount >= iCount:
                        modified = re.sub(r'\tCc', '\tIc', modified)
                    else:
                        modified = re.sub(r'\tCc', '\tic', modified)
                    if ICount > 0 and iCount > 0:
                        filesToCheck.append((currFilePath, newFilePath))
                with open(newFilePath, "w") as out_file:
                    out_file.write(modified)
            
            try:
                piece = Score(newFilePath)
            except:
                print('Issue with this file:', currFilePath)
                problemFiles.append(file)

pfs = sorted({pf[:4] for pf in problemFiles})
print(f'{len(problemFiles)} Problem files:', *pfs, sep='\n')  # 16
print(f'{len(filesToCheck)} Files to check:', *filesToCheck, sep='\n')  # 20
pdb.set_trace()
