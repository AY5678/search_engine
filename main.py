#main.py

from content_generator import content_generator

def main():
    """
    Main function for running the terminal interaction and interface
    """

    #Don't mind the name, I just named it contenter since it grabs content
    contenter = content_generator()

    #Create the generator
    generator = contenter.generate_next_content()

    for i in range(5):
        print(next(generator))



#Safety check
if __name__ == "__main__":
    main()