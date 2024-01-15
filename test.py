import sys
sys.path.insert(0,'src')
from mtvs.main import MainImpl



def main():
    """Entry point for the application script"""
    a=5
    main = MainImpl()
    sys.argv = ['missingTvShow', 'sync']
    print(sys.argv[1:])
    main.getArguments(sys.argv[1:])
    #main.getArguments(['sync'])


if __name__ == "__main__":
    main()