import sys
import argparse
sys.path.extend(['.', '..'])

from pycparser import c_parser
from misc.selfcaller import SelfCallHiddenAdder

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='SelfCall preprocessor!')
    parser.add_argument('--file', required=True, help='Source C file for the SeflCall preprocessing')
    args = parser.parse_args()
    
    with open(args.file) as f:
        parser = c_parser.CParser()
        ast = parser.parse(f.read())
        
        v: SelfCallHiddenAdder = SelfCallHiddenAdder()
        v.visit(ast)
    