import sys
sys.path.insert(0,'src')
from mtvs.main import MainImpl



def main():
    """Entry point for the application script"""
    main = MainImpl()
    sys.argv = ['missingTvShow', 'sync']
    main.getArguments(sys.argv[1:])


if __name__ == "__main__":
    main()