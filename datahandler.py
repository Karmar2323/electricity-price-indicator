# datahandler.py

class DataHandler:
    def __init__(self) -> None:
        pass

    def change_data(data_obj, key, new_value):
        data_obj[key] = new_value
        return

    def print_data(data, message=None):
        if message is None: 
            print("Data:\n")
            print(data)
        else:
            print(message)
            print(data)
        return