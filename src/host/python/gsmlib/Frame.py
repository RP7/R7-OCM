import FB,SB,NB,DB
class Frame:
	pass

class FFrame(Frame):
	__field__ = [FB]+[NB]*7

class SFrame(Frame):
	__field__ = [SB]+[NB]*7

class NFrame(Frame):
	__field__ = [NB]*8

class IFrame(Frame):
	__field__ = [DB]+[NB]*7

