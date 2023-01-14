import sys
from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(base_dir) + '\\hope')
sys.path.append(str(base_dir))

from hope import *

__all__ = ['Parser','Token','Tokenizer','run','IllegalCharError','InvalidSyntaxErorr','Indexerror','RunTimeError','ExpectedCharError','Function']  + ['List','String','Number']