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


class Actions:
	def __init__(self,name,string,affine=False,persisten=False, addative=[]):
		self.name = name
		self.needs = []
		self.result = []
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
					self.needs.append(x)
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
					self.result.append(x)
					isAtom = True

			if not isAtom:
				print "This type is not Atomic: " + i
				sys.exit(0)
			


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


def solver(query,atoms,actions,sequence=[],nest=0,pop=None):
	linear = True
	goal = True
	test = []
	tempPop = None
	tempRemove = []
	availableNext = []
	aLinearExists = 0
	copyAvailableAtoms = []

	for i in actions:
		availableNext.append(i)

	for i in atoms:
		copyAvailableAtoms.append(i)
		if not (i.affine or i.persisten):
			aLinearExists += 1
	for i in actions:
		#print " === " + i.name
		if not (i.affine or i.persisten):
			aLinearExists += 1

	for i in actions:
		if i == pop:
			continue
		
		arguments = len(i.needs)
		checker = 0 
		tempAtoms = []
		for x in i.needs:
			if x in copyAvailableAtoms:
				if not x.persisten:
					#print x.name + " : is removed"
					copyAvailableAtoms.remove(x)
					tempAtoms.append(x)
				if not (x.affine or x.persisten):
					aLinearExists += -1
				#print x.name + " is available"
				checker += 1
		#print "checker: " + str(checker) + " arguments: " + str(arguments)
		if checker == arguments:

			sequence.append(i)
			availableNext.remove(i)
			for y in i.result:

				#print "append result: " + y.name
				copyAvailableAtoms.append(y)
				if not (y.affine or y.persisten):
					aLinearExists += 1
				#print y.name + " " + str(y.affine)
				if y.name == query:
					goal = False

					if aLinearExists == 0:
						linear = False
						#print sequence
						#result.append(sequence)
						return False
					return True
					
						
						
			if i.persisten:
				availableNext.append(i)

					
			if goal:
				temp = solver(query,copyAvailableAtoms,availableNext,sequence,nest+1)
				if temp:
					goal = False
				elif temp == False:
					goal = False
					linear = False
				elif temp == None:
					break
				
			if linear or goal:
				tempPop = sequence.pop()
				for x in tempPop.result:
					try:
						copyAvailableAtoms.remove(x)
					except Exception,e:
						pass
				for x in tempPop.needs:
					if x not in copyAvailableAtoms:
						copyAvailableAtoms.append(x)
				temp = solver(query,copyAvailableAtoms,availableNext,sequence,nest+1,tempPop)
				if temp:
					goal = False
				elif temp == False:
					goal = False
					linear = False
				elif temp == None:
					break

			if not (goal or linear):				
				result.append(sequence)
				sequence = []
				break

		else:
			for x in tempAtoms:
				copyAvailableAtoms.append(x)

	







if __name__ == '__main__':
	parse()

	availableAtoms = []
	availableActions = []
	result = []
	for x in initialbase:
		if x in atomicbase:
			availableAtoms.append(x)
		else:
			availableActions.append(x)

	solver("emmaIsDead",availableAtoms,availableActions)
	#solver("emmaCharlesMarried", availableAtoms, availableActions)
	
	if len(result) == 0:
		print "could not find a solution: "

	else:
		print "========\nThe solution is:"
		for x in result[0]:
			print x.name
	