class Gene:
    def __init__(self):
        self.variables = {}
        self.variables_descriptor = {}

    @classmethod
    def like(cls, other_gene):
        gene = cls()
        gene.variables_descriptor = other_gene.variables_descriptor

        for name in gene.variables_descriptor:
            gene.variables[name] = 0

        return gene

    def __repr__(self):
        string = ""

        for name in self.variables:
            string += name + " (" + str(self.variables_descriptor[name]) + "): " + str(self.get_value(name))

        return string

    #	def add_integer(self, name, size):
    #		self.variables[name] = 0
    #		self.variables_descriptor[name] = ("integer", size)

    def add_fixed(self, name, size, precision):
        self.variables[name] = 0
        self.variables_descriptor[name] = ("fixed", size, precision)

    #	def add_char(self, name):
    #		self.variables[name] = 0
    #		self.variables_descriptor[name] = ("char", 8)

    #	def add_string(self, name, size):
    #		self.variables[name] = 0
    #		self.variables_descriptor[name] = ("string", 8 * size)

    def set_bits(self, name, bits):
        self.variables[name] = bits

    def set_value(self, name, value):
        type = self.variables_descriptor[name][0]

        if (type == "fixed"):
            self._set_fixed(name, value)

    def _set_fixed(self, name, value):
        (_, size, precision) = self.variables_descriptor[name]

        is_negative = (value < 0)
        value = abs(value)

        mask = (1 << (size - 1)) - 1  # e.g. 0111 1111 1111 1111 para size = 16
        bit_value = int(value * (1 << precision)) & mask

        if (is_negative):
            bit_value |= (1 << (size - 1))

        self.variables[name] = bit_value

    def get_value(self, name):
        type = self.variables_descriptor[name][0]

        if (type == "fixed"):
            return self._get_fixed(name)

    def _get_fixed(self, name):
        bit_value = self.variables[name]
        (_, size, precision) = self.variables_descriptor[name]

        mask = (1 << (size - 1)) - 1  # e.g. 0111 1111 1111 1111 para size = 16
        value = (bit_value & mask) / (1 << precision)

        if get_bit(bit_value, size - 1) == 1:
            value *= -1

        return value

    def get_variable_max(self, name):
        return 2 ** self.variables_descriptor[name][1]

    def get_variable_size(self, name):
        return self.variables_descriptor[name][1]


def get_bit(gene, bit):
    return (gene & (1 << bit)) >> bit


def print_bits(x):
    for y in range(gene_size):
        print(get_bit(x, y), end="")

    print("\n")
