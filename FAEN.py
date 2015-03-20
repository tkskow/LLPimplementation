import sys


initialbase = []
atomicbase = []
actionbase = []


class Atomic:
	def __init__(self,string,affine=False,persisten=False, addative=[]):
		self.name = string
		self.affine = affine
		self.persisten = persisten
		self.addative = addative

   	def __key(self):
   		return self.name

	def __eq__(x, y):
		return x.name == y.name

	def __hash__(self):
		return hash(self.__key())
	def __repr__(self):
		return self.name

class Actions:
	def __init__(self,name,string,affine=False,persisten=False, addative=[]):
		self.name = name
		self.needs = set([])
		self.result = set([])
		self.affine = affine
		self.persisten = persisten
		self.addative = addative
		s2 = string.split("=")

		s3 = s2[1].split("-o")
		try:
			s4 = s3[0].split("*")
		except Exception, e:
			s4 = s3[0]
		
		try:
			s5 = s3[1].split("*")
		except Exception, e:
			s5 = s3[1]

		for i in s4:
			isAtom = False
			for x in atomicbase:
				if i == x.name:
					self.needs.add(x)
					isAtom = True
			if not isAtom:
				print "This type is not Atomic: " + i
				sys.exit(0)

		for i in s5:
			isAtom = False
			affine = False
			persisten = False
			if i[0] == "!":
				persisten = True
				i = i[1:len(i)]
			elif i[0] == "@":	
				affine = True
				i = i[1:len(i)]

			for x in atomicbase:
				if i == x.name:
					x.persisten = persisten
					x.affine = affine
					self.result.add(x)
					isAtom = True

			if not isAtom:
				print "This type is not Atomic: " + i
				sys.exit(0)

	def __repr__(self):
		return self.name
results = []
def find_path(query, atoms, action, actions, lastatoms, sequence = []):
	myNextActions = []

	if atoms == lastatoms:
		return None
	if (query in atoms):
		results.append(sequence)
		return sequence
	for action in actions:
		if (action.needs.issubset(atoms)):
			myNextActions.append(action)

	for action in myNextActions:

		atoms1 = atoms.difference(action.needs)
		atoms1 = atoms.union(action.result)
		if (action not in sequence):
			sequence.append(action)
			find_path(query, atoms1, action, actions, atoms, sequence)

	return None






def solver(query,atoms,actions,sequence=[],pop=None):
	query = Atomic(query)

	for action in actions:
		if action.needs.issubset(atoms):
			print find_path(query, atoms, action, actions, [action])
	return results


def parse(file=sys.argv[1]):
	f = filter(lambda line:line.strip(), open(file))

	extension = file.split(".")[-1]

	if extension != "llp":
		print "Wrong file extension. Bye bye"
		sys.exit(0)

	for (linenumber, line) in enumerate(f):

		line = line.replace(" ","").replace(".","").replace("{","").replace("}","").strip()
		s = line.split(":")

		if s[0] == "init":
			temp = s[1].split("=")
			temp = temp[1].split("*")

			for i in temp:
				persisten = False
				affine = False
				addative = []
				if i[0] == "!":
					persisten = True
					i = i[1:len(i)]
				elif i[0] == "@":	
					affine = True
					i = i[1:len(i)]
				if "&" in i:
					i = i.replace("(","").replace(")","")
					for x in i.split("&"):
						addative.append(x)

				if len(addative) > 0:
					for y in addative:
						for x in atomicbase:
							if y == x.name:
								x.persisten = persisten
								x.affine = affine
								initialbase.append(x)

						for x in actionbase:
							if y == x.name:
								x.persisten = persisten
								x.affine = affine
								for l in addative:
									if l == y:
										pass
									else:
										x.addative.append(l)
								initialbase.append(x)
				
				else:
					for x in atomicbase:
						if i == x.name:
							x.persisten = persisten
							x.affine = affine
							x.addative = addative
							initialbase.append(x)

					for x in actionbase:
						if i == x.name:
							x.persisten = persisten
							x.affine = affine
							x.addative = addative
							initialbase.append(x)


		elif "=" in s[1]:
			actionbase.append(Actions(s[0],s[1]))
		
		else:
			atomicbase.append(Atomic(s[0]))






if __name__ == '__main__':
	parse()

	availableAtoms = set([])
	availableActions = set([])
	result = []
	for x in initialbase:
		if x in atomicbase:
			availableAtoms.add(x)
		else:
			availableActions.add(x)

	temp =solver("emmaIsDead",availableAtoms,availableActions)
	#temp = solver("emmaCharlesMarried", availableAtoms, availableActions)

	if len(temp) == 0:
		print "could not find a solution: "

	else:
		print "========\nThe solution is:"
		print len(temp)
		for i in temp:
			print i
