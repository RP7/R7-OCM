from fractions import Fraction

SymbolRate = Fraction(6500000,24)
MultiFrameC = 51
MultiFrameT = 26
MultiFrame = MultiFrameC * MultiFrameT
SupperFrame = MultiFrame * 2048

S_Slot = Fraction(625,4)
S_Frame = S_Slot*8

T_Symbol = 1/SymbolRate
T_Slot = T_Symbol * S_Slot
T_Frame = T_Symbol * S_Frame
T_MultiFrame = T_Frame * MultiFrame
T_SupperFrame = T_Frame * SupperFrame

 