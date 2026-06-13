from helper import greet
from utils.math import add

def main():
    print("=== Hello Kaido Package ===")
    
    greet("Kaido")
    print("2 + 3 =", add(2, 3))

if __name__ == "__main__":
    main()