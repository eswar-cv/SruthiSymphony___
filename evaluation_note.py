class evaluation_note:
	def __init__(self,original,cover):
		self.original = original
		self.cover = cover
		self.note_accuracy = 0
		self.report ={}
		self.note_names = ["S", "R1", "R2/G1", "R3/G2", "G3", "M1", "M2", "P", "D1", "D2/N1", "N2", "N3","S-next", None, 'None']

	def evaluate(self):
		self.check_notes()
		self.check_raga()
		#self.check_lyric()
		return self.report

	def compare_(self,original,cover):
		i = 0
		correct = 0
		z=[]
		while i <len(original):
			try:
				x = False
				if (original[i])['note']==(cover[i])['note']:
					x=True
					correct+=1
				y =[(original[i])['note'],(cover[i])['note'],x]
				z.append(y)
				i+=1
			except IndexError:
				y =[(original[i])['note'],None,x]
				z.append(y)
				i+=1
		self.report['note']=z
		self.report["note_accuracy"]= correct/len(original)
		return self.report
	def compare(self, base, user):
		accuracies = []
		accs = {
				0: 100,
				1: 80,
				2: 50,
				3: 25,
				4: 15,
				5: 5
		}
		bases = [note['note'] for note in base]
		users = [note['note'] for note in user]
		for n1, n2 in zip(bases, users):
			p1, p2 = self.note_names.index(n1), self.note_names.index(n2)
			diff = abs(p1 - p2)
			if diff in accs:
				accuracies.append(accs[diff])
			else:
				accuracies.append(0)
		
		return {'note_accuracy': round(sum(accuracies) / len(accuracies), 2)}
	def check_notes(self, base, user):
		self.compare(base, user)
