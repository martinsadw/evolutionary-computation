class SingletonPrint:
    class __SingletonPrint:
        def __init__(self):
            pass

    __instance = None
    __out = []

    def __init__(self):
        if not SingletonPrint.__instance:
            SingletonPrint.__instance = SingletonPrint.__SingletonPrint()

    def add_string(self, text):
        self.__out.append(text)

    def out(self):
        for text in self.__out:
            print(text, end='')

    def free(self):
        self.__out.clear()
