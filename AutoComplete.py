from data_manager.manager_program import ManagerProgram
import sys

if __name__ == '__main__':
    if len(sys.argv) != 2:
        # path is the path to the main directory
        sys.exit("Usage: AutoComplete [path]")
    else:
        main_path = sys.argv[1]
        manager_program = ManagerProgram(main_path)
        manager_program.initialization()
        manager_program.run()
