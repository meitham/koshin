import lib2to3.main
from . import fixes

def main():
    raise SystemExit(lib2to3.main.main(fixes.__name__))

if __name__ == '__main__':
    main()
