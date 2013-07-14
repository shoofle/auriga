import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-l", "--length", help="length of the initial string", type=int, default=5)
parser.add_argument("output", help="file to output to", type=argparse.FileType('w'), nargs="?", default=sys.stdout)
args = parser.parse_args()

node_marker = 'O'

class TreeNode:
	"""A binary tree node for the purpose of doing tree manipulations and generating tamari lattices. Not very pretty code."""
	def __init__(self,l,v,r):
		"""Arguments are: left node, payload, right node."""
		self.l = l
		self.v = v
		self.r = r
	def __str__(self):
		"""Return the string which would be parsed into this object."""
		if self.l is None or self.r is None: return str(self.v)
		return node_marker + str(self.l) + str(self.r)
	def pretty_string(self):
		"""Return a string suitable for a label."""
		if self.l is None or self.r is None: return str(self.v)
		return "(" + self.l.pretty_string() + "," + self.r.pretty_string() + ")"
	def rotate_left(self):
		if not leaf(self) and not leaf(self.r):
			self.l = TreeNode(self.l, None, self.r.l)
			self.r = self.r.r
	def rotate_right(self):
		if not leaf(self) and not leaf(self.l):
			self.r = TreeNode(self.l.r, None, self.r)
			self.l = self.l.l
	def clone(self):
		if leaf(self): return TreeNode(None, self.v, None)
		else: return TreeNode(self.l.clone(), self.v, self.r.clone())
	def count_nodes(self):
		if leaf(self): return 0
		else: return self.l.count_nodes() + self.r.count_nodes() + 1
	def do_on_nth_node(self, n, f):
		"""Call the second argument on the nth node in the tree, going depth first from left to right."""
		if leaf(self): return n
		remaining = self.l.do_on_nth_node(n,f)
		if remaining is 0: return 0
		if remaining is 1:
			f(self)
			return 0
		return self.r.do_on_nth_node(remaining-1,f)
	def __eq__(self, other):
		"""Comparison for sets. Just checks if the string representation is the same."""
		return str(self) == str(other)
	def __hash__(self):
		"""Much like __eq__, this is needed for using this in sets. This just hashes the string representation."""
		return hash(str(self))

def nth_node_helper(root, n, f):
	"""This is so ugly. I just want to do something on the nth node and return the transformed tree! ... But it works. Note: don't extend this script ever. It should stay in its little awful box."""
	root.do_on_nth_node(n, f)
	return root

def leaf(node):
	return node.l is None or node.r is None

def generate_children(root):
	"""Return a set of all the trees produced by rotating left at one point in the tree that is passed in."""
	# If there are n nodes in the tree, then there are at most n places to do a rotation. 
	# I didn't feel like figuring out a more direct method to generate all rotations, so I just did this:
	# Try rotating at each child node. Remove all the ones that weren't changed (that is, where it failed).
	children = set(nth_node_helper(root.clone(), i, TreeNode.rotate_left) for i in range(root.count_nodes()))
	return children - {root} # Return the children, except without the root. We don't care about the root.

def _parse(s):
	"""Parse one token of the string passed in, and return a tuple: (the tree we parsed, the remainer that wasn't parsed).
	This function recursively calls itself, to parse the whole string. """
	if s[0] is node_marker:
		first, remainder = _parse(s[1:])
		second, secondRemainder = _parse(remainder)
		return (TreeNode(first, None, second), secondRemainder)
	return (TreeNode(None, s[0], None), s[1:])
def parse(string):
	"""Parses a string, assuming the node marker in node_marker, and returns a TreeNode. 
	This is a wrapper around _parse."""
	return _parse(string)[0]


# The string we start with is just a slice of the alphabet, with length specified by the command line argument -l.
root_string = "abcdefghijklmnopqrstuvwxyz"[:args.length]
root_string = "".join( "O" + char for char in root_string )
root_string = "".join( root_string.rsplit("O", 1) )

# helper function for generating node labels
label_from_node = lambda x: "{name} [label=\"{label}\"];".format(name=str(x), label=x.pretty_string())


# Here's the root we start with!
RootOfAllEvil = parse(root_string)
#print(RootOfAllEvil)

current_generation = set()
next_generation = {RootOfAllEvil}
edges = set()
labels = set()

while len(current_generation ^ next_generation): # So long as we haven't reached stability...
	# Move to look at the next generation.
	#print("current_generation: {}, next_generation: {}".format(current_generation, next_generation))
	current_generation = next_generation 
	
	# Clear out the next generation so that we can fill it with the children of the now-current generation.
	next_generation = set()
	#print("current_generation: {}, next_generation: {}".format(current_generation, next_generation))
	
	labels = labels | set(label_from_node(parent) for parent in current_generation)
	
	for parent in current_generation:
		children = generate_children(parent)
		#print("children of {parent}: {children}".format(parent=parent, children=children))
		
		labels = labels | set(label_from_node(child) for child in children)
		edges = edges | set(str(parent) + " -> " + str(child) + ";" for child in children)
		next_generation = next_generation | children

args.output.write(u"digraph tamari {\n")
args.output.write(u"\n".join(labels) + "\n")
args.output.write(u"\n".join(edges))
args.output.write(u"\n}\n")
