class Glomp():
	@classmethod
	def metaize(self, op=None, *arguments):
		if op is None: 
			raise TypeError
		fixed_arguments = [g(quantity) for quantity in arguments]
		return MetaGlomp(op, *fixed_arguments)
	def __add__(self, other): return Glomp.metaize("__add__", self, other)
	def __sub__(self, other): return Glomp.metaize("__sub__", self, other)
	def __mul__(self, other): return Glomp.metaize("__mul__", self, other)
	def __div__(self, other): return Glomp.metaize("__div__", self, other)
	def __floordiv__(self, other): return Glomp.metaize("__floordiv__", self, other)
	def __mod__(self, other): return Glomp.metaize("__mod__", self, other)
	def __divmod__(self, other): return Glomp.metaize("__divmod__", self, other)
	def __pow__(self, other): return Glomp.metaize("__pow__", self, other)
	def __lshift__(self, other): return Glomp.metaize("__lshift__", self, other)
	def __rshift__(self, other): return Glomp.metaize("__rshift__", self, other)
	def __and__(self, other): return Glomp.metaize("__and__", self, other)
	def __xor__(self, other): return Glomp.metaize("__xor__", self, other)
	def __or__(self, other): return Glomp.metaize("__or__", self, other)

def v(g):
	"""Get the value of a glomp or variable."""
	if isinstance(g, Glomp):
		return g.value
	else:
		return g

def g(v):
	"""Get a glomp of a variable. If the argument is already a glomp, this returns it."""
	if isinstance(v, Glomp):
		return v
	else:
		return BasicGlomp(v)

class BasicGlomp(Glomp):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return "g(" + str(self.value) + ")"

class MetaGlomp(Glomp):
	def __init__(self, operation_name=None, *arguments):
		self.targets = arguments
		self.operation_name = operation_name
	@property
	def value(self):
		return getattr(v(self.targets[0]), self.operation_name)(*[v(i) for i in self.targets[1:]])
	@value.setter
	def value(self, new_metaglomp):
		self.operation_name = new_metaglomp.operation_name
		self.targets = new_metaglomp.targets
	def __str__(self):
		return str(self.operation_name) + ":[" + ",".join(map(str,self.targets)) + "]"

if __name__ == "__main__":
	foo, bar, baz = g(1), g(2), g(3)
	print("foo, bar, and baz are set as glomps of 1, 2, and 3.")
	boop = foo + bar*baz
	print("boop is set to foo + bar*baz: %s" % (boop, ))
	print("And we can fetch the value of that computation easily as boop.value: %s" % (boop.value, ))
	print
	print("We can change the value of foo:")
	print(">>> foo.value = 5")
	foo.value = 5
	print("And now, when we fetch the value of boop, it is adjusted accordingly:")
	print(">>> boop.value => %s" % (boop.value,))
	print
	print("There is also a shorthand for evaluating a glomp: v(boop) => %s" % (v(boop), ))
