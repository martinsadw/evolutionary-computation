# TODO(andre:06-04-2018): Definir tipo gene contendo informações sobre sua representação interna
gene_bitsize = 16
gene_max = 2 ** gene_bitsize
precision_bitsize = 6

class Gene:
	def __init__(self, value, size, precision):
		self.value = value
		self.size = size
		self.precision = precision

		self.max = 2 ** self.size

	def __float__(self):
		mask = (2 ** (self.size-1)) - 1 # mask = 0111 1111 1111 1111
		num = (self.value & mask) / (2 ** self.precision)

		if self.get_bit(self.size-1) == 0:
			num *= -1

		return num

	def __str__(self):
		return str(float(self))

	def get_bit(self, bit):
		return (self.value & (1 << bit)) >> bit


def get_bit(gene, bit):
	return (gene & (1 << bit)) >> bit

def num_gene(gene):
	mask = (2 ** (gene_bitsize-1)) - 1 # mask = 0111 1111 1111 1111
	num = (gene & mask) / (2 ** precision_bitsize)

	if get_bit(gene, gene_bitsize-1) == 0:
		num *= -1

	return num

def str_gene(gene):
	return str(num_gene(gene))

def print_gene_list(gene_list):
	print("[", end="")

	for gene in gene_list:
		print("[" + str_gene(gene) + " -> " + str(fitness(gene)) + "]" + ", ", end="")

	print("]")

def print_bits(x):
	for y in range(gene_size):
		print(get_bit(x, y), end="")

	print("\n")

def fitness(x):
	x = num_gene(x)

#	return x*x - 5*x + 4

	# 85.1326727 -> -4568.23409
	return 0.0001*x**4 - 0.002*x**3 - 1.2*x**2 + 1*x + 25	

