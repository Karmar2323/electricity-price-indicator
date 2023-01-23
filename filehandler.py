import random
class FileHandler:

    def __init__(self) -> None:
        pass


    def generate_filename(self, filename) -> str:
        name_prefix = "rnd"
        for a in filename:
            name_prefix += str(random.randrange(9))
        return name_prefix + filename

    # save to file TODO error handling
    # if save fails, try once other file name
    def save_data_file(self, data, filename = "../data.txt", get_new_name = True) -> None:
        try:
            response_file = open(filename, "w")
            response_file.write(data)
            response_file.write("\n")
            response_file.close()
            print("Data saved to " + filename)
        except:
            print("File write error: " + filename)
            if (get_new_name):
                new_file = self.generate_filename(self, filename)
                self.save_data_file(self, data, new_file, False)


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
