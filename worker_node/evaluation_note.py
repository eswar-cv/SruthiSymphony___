class evaluation_note:
  def __init__(self,original,cover):
    self.original = original
    self.cover = cover
    self.note_accuracy = 0
    self.report ={}

  def evaluate(self):
    self.check_notes()
    self.check_raga()
    #self.check_lyric()
    return self.report

  def check_raga(self):
    x=False
    original_raga = "Kalyani"
    cover_raga = "Kalyani"
    if original_raga == cover_raga:
      x = True
    self.report['raga']=[original_raga,cover_raga,x] #{Original, Cover, True/False}

  def compare(self,original,cover):
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
  def check_notes(self, base, user):
    self.compare(base, user)
