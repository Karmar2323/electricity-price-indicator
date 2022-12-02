class FileHandler:

    def __init__(self) -> None:
        pass


    # save to file TODO error handling
    def save_data_file(self, data, filename = "../data.txt") -> None:
        try:
            response_file = open(filename, "w")
            response_file.write(data)
            response_file.write("\n")
            response_file.close()
            print("Data saved to " + filename)
        except:
            print("File write error")


    # read from file
    def read_file(self, filename) -> str | None:
        content = ""
        try:
            file = open(filename, "r")
            content = file.read()
        except:
            print ("File open error")
            return None
        return content
