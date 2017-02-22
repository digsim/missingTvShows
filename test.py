import sys
sys.path.insert(0,'src')
from mtvs.main import MainImpl



def main():
    """Entry point for the application script"""
    a=5
    main = MainImpl()
    main.getArguments(sys.argv[1:])


if __name__ == "__main__":
    main()