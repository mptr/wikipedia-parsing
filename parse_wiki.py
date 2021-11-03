from xml.sax import make_parser
import sys, bz2
from classes.PageHandler import PageHandler

parser = make_parser()
parser.setContentHandler(PageHandler())
if(sys.argv[1].endswith(".bz2")):
    with bz2.open(sys.argv[1], "rb") as f:
        # Decompress data from file
        parser.parse(f)
else:
    parser.parse(sys.argv[1])

