from data_manager.data import Data


class ManagerProgram:
    """
    This class manges the two parts of the program
    1. initialization: load all data from path.
    2. run: in infinite loop, get input from user and treat the input.
    """

    def __init__(self, path):
        self.__data = Data(path)

    def initialization(self):
        print("Loading the files and preparing the system...")
        self.__data.insert_data()
        print("The system is ready. ")

    def run(self):
        while True:
            # get sentence prefix from user and print the best k completions
            user_input = input("Enter your text: ")
            last_input = user_input
            while user_input != "#":
                best_completions = self.__data.get_best_k_completion(last_input)
                for i, complete in enumerate(best_completions):
                    print("{}. {}".format(i+1, complete))
                if not len(best_completions):
                    print("No results found.")
                    user_input = "#"
                else:
                    user_input = input(last_input)
                    last_input += user_input

