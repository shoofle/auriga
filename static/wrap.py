supported_operations = ["__add__", "__sub__", "__mul__", "__floordiv__", "__mod__", "__divmod__", "__pow__", "__lshift__", "__rshift__", "__and__", "__xor__", "__or__", "__pow__", "__div__", "__truediv__", "__div__", "__radd__", "__rsub__", "__rmul__", "__rdiv__", "__rtruediv__", "__rfloordiv__", "__rmod__", "__rdivmod__", "__rpow__", "__rlshift__", "__rrshift__", "__rand__", "__rxor__", "__ror__", "__sub__", "__rpow__", "__radd__", "__neg__", "__pos__", "__abs__", "__complex__", "__long__", "__float__", "__oct__", "__hex__", "__index__", "__len__"] 
class Wrapper(object):
	"""Wrap a value so that it will be lazy-evaluated. `wrapper.value` returns the current value (you can also use c(wrapper))."""
	def __init__(self, target, attribute=None, arguments=None):
		self.target = target
		self.attribute = attribute
		self.arguments = arguments
		if attribute is not None and arguments is not None:
			raise TypeError
	@property
	def value(self):
		if self.attribute is None and self.arguments is None:
			return self.target
		if self.attribute is not None:
			return getattr(c(self.target), self.attribute)
		if self.arguments is not None:
			return c(self.target)(*map(c, self.arguments))
	@value.setter
	def value(self, new_target):
		self.target = new_target
	def __getattr__(self, name):
		return Wrapper(self, attribute=name)
	def __call__(self, *args):
		return Wrapper(self, arguments=args)
	def __repr__(self): return str(self)
	def __str__(self):
		if self.attribute is None and self.arguments is None: 
			return "w(" + str(self.target) + ")"
		if self.attribute is not None: 
			return "w(" + str(self.target) + "." + str(self.attribute) + ")"
		if self.arguments is not None: 
			return "w(" + str(self.target) + "(" + ",".join(map(str, self.arguments)) + ")"

def pass_through(operation):
	return lambda self, *others: Wrapper(Wrapper(self, attribute=operation), arguments=others)
for operation in supported_operations:
	setattr(Wrapper, operation, pass_through(operation))

def c(g):
	"""Get the current value of a wrapper or bare variable."""
	if isinstance(g, Wrapper): return g.value
	else: return g

def wrap(v):
	"""Wrap a variable, or just return it if it's already wrapped."""
	if isinstance(v, Wrapper): return v
	else: return Wrapper(v)

if __name__ == "__main__":
	foo, bar, baz = wrap(1), wrap(2), wrap(3)
	print("foo, bar, and baz are the wrapped values 1, 2, and 3.")
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
	print("There is also a shorthand for evaluating a glomp: c(boop) => %s" % (c(boop), ))
