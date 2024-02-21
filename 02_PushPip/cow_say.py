import argparse

parser = argparse.ArgumentParser()

parser.add_argument("message", nargs="?", type=str)

parser.add_argument("-e", "--eye_string",  dest="eyes", type=str, default="oo")
parser.add_argument("-f", "--cowfile",  dest="cow", type=str, default="default")
parser.add_argument("-l", action="store_true")
parser.add_argument("-n", dest="wrap_text", action="store_true")
parser.add_argument("-T", "--tongue_string", dest="tongue", type=str, default="  ")
parser.add_argument("-W", "--column", dest="width", type=str)
parser.add_argument("-b", action="store_true")
parser.add_argument("-d", action="store_true")
parser.add_argument("-g", action="store_true")
parser.add_argument("-p", action="store_true")
parser.add_argument("-s", action="store_true")
parser.add_argument("-t", action="store_true")
parser.add_argument("-w", action="store_true")
parser.add_argument("-y", action="store_true")

args = parser.parse_args()
print(args)