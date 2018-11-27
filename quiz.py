#import sys; print(sys.path)
from cryptography.fernet import Fernet


key = 'TluxwB3fV_GWuLkR1_BzGs1Zk90TYAuhNMZP_0q4WyM='

# Oh no! The code is going over the edge! What are you going to do?
message = b'gAAAAABb9ww4qtaHolrfH7YwDnbtgu51BciLQd4NFCNSleXbY1dRxLcZFcyA27tEj_riIc5Pxa7JS-mUyzrDZnLWsgvg1v6PAEAXqWWltB5mkH46FCkcJEiPsfH0FRPkiBu3dat6oiy67J7XFD9KOGVsrV9oKcrfZwiRkolwEqjF63zGSQK4G_SA5Rf5pQPfGYGCf6pRVE8N'

def main():
    f = Fernet(key)
    print(f.decrypt(message))


if __name__ == "__main__":
    main()
