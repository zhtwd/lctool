import os
import argparse
from lctool.func import lctool

def lcget():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", help="Directory for lc files",
                        type=str)
    parser.add_argument("--overwrite", help="Overwrite existed file and code", action="store_true")

    args = parser.parse_args()
    path = args.path
    overwriteflag = args.overwrite
    lc = lctool()
    tag_list = lc.get_tag_list()
    if not path:
        path = '.'
    for tag in tag_list:
        dirpath = path + '/' + tag
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
        notefile = dirpath + ('/%s_notes.txt' % tag)
        problem_list = lc.get_problem_list(tag=tag)
        with open(notefile, 'w') as nf:
            for problem in problem_list:
                print 'getting problem: ', tag, problem
                filepath = dirpath + '/' + problem
                content = lc.get_problem(problem)
                if not content:
                    continue
                if os.path.exists(filepath + '.' + 'java') and not overwriteflag:
                    print 'problem exists: ', tag, problem
                    continue
                source, _, lang = lc.get_problem_source(problem)
                filepath += '.' + lang
                with open(filepath, 'w') as f:
                    f.write('/*\n')
                    f.write(content.encode('utf-8'))
                    f.write('*/\n')
                    f.write('\n\n')
                    f.write(source.encode('utf-8'))
                nf.write('*' * 30 + problem + '\n')
                nf.write(content.encode('utf-8'))
                nf.write('\n')

def submit():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--problem_path", help="lc file for submission",
                        type=str, required=True)
    args = parser.parse_args()
    problem_path = args.problem_path
    lc = lctool()
    res = lc.submit_problem(problem_path)
    for info in res:
        print "%s: %s" % (info, res[info])
