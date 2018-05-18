class Learner:
    def __init__(self, registrationCode, lowerTime, upperTime, atvref, senint, visver, seqglo, learningGoals):
        self.id = 0
        self.score = None
        self.atvref = 0
        self.senint = 0
        self.visver = 0
        self.seqglo = 0

        self.registrationCode = registrationCode
        self.lowerTime = int(lowerTime*3600)
        self.upperTime = int(upperTime*3600)

        self.learninGoals = learningGoals

        if atvref == -11 or atvref == -9:
            self.atvref = -3
        elif atvref == -7 or atvref == -5:
            self.atvref = -2
        elif atvref == -3 or atvref == -1:
            self.atvref = -1
        elif atvref == 11 or atvref == 9:
            self.atvref = 3
        elif atvref == 7 or atvref == 5:
            self.atvref = 2
        elif atvref == 3 or atvref == 1:
            self.atvref = 1

        if senint == -11 or senint == -9:
            self.senint = -3
        elif senint == -7 or senint == -5:
            self.senint = -2
        elif senint == -3 or senint == -1:
            self.senint = -1
        elif senint == 11 or senint == 9:
            self.senint = 3
        elif senint == 7 or senint == 5:
            self.senint = 2
        elif senint == 3 or senint == 1:
            self.senint = 1

        if visver == -11 or visver == -9:
            self.visver = -3
        elif visver == -7 or visver == -5:
            self.visver = -2
        elif visver == -3 or visver == -1:
            self.visver = -1
        elif visver == 11 or visver == 9:
            self.visver = 3
        elif visver == 7 or visver == 5:
            self.visver = 2
        elif visver == 3 or visver == 1:
            self.visver = 1

        if seqglo == -11 or seqglo == -9:
            self.seqglo = -3
        elif seqglo == -7 or seqglo == -5:
            self.seqglo = -2
        elif seqglo == -3 or seqglo == -1:
            self.seqglo = -1
        elif seqglo == 11 or seqglo == 9:
            self.seqglo = 3
        elif seqglo == 7 or seqglo == 5:
            self.seqglo = 2
        elif seqglo == 3 or seqglo == 1:
            self.seqglo = 1
