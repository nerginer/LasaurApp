
import os, sys, subprocess, shutil
import argparse


argparser = argparse.ArgumentParser(description='Compile Cython code.', prog='make_cython')
argparser.add_argument('-u', '--undo', dest='undo', action='store_true',
                       default=False, help='undo cython module')
args = argparser.parse_args()

ret = 0

OBJECTS  = ["backend/filereaders/path_optimizers", "backend/filereaders/kdtree"]

if args.undo:
    for obj in OBJECTS:
        # del .so
        f = '%s.so' % (obj)
        if os.path.isfile(f):
            os.remove(f)

        # restore any possible python module
        f_src = '%s_.py' % (obj)
        f_dst = '%s.py' % (obj)
        if os.path.isfile(f_src):
            shutil.move(f_src, f_dst)


else:
    for obj in OBJECTS:
        # .pyx to .c
        command = 'cython %s.pyx' % obj
        ret += subprocess.call(command, shell=True)

        # .c to .o
        command = 'gcc -c -fPIC -I/usr/include/python2.7/ %s.c -o %s.o' % (obj, obj)
        ret += subprocess.call(command, shell=True)

        # .o to .so
        command = 'gcc -shared %s.o -o %s.so' % (obj, obj)
        ret += subprocess.call(command, shell=True)

        # del .c
        f = '%s.c' % (obj)
        if os.path.isfile(f):
            os.remove(f)

        # del .o
        f = '%s.o' % (obj)
        if os.path.isfile(f):
            os.remove(f)

        # move any possible python module
        f_src = '%s.py' % (obj)
        f_dst = '%s_.py' % (obj)
        if os.path.isfile(f_src):
            shutil.move(f_src, f_dst)

        # del .pyc
        f = '%s.pyc' % (obj)
        if os.path.isfile(f):
            os.remove(f)

print "done!"