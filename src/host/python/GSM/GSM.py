symbolrate = 1625e3/6.
slotlen = 625./4
oversamplerate = 1.92e6/symbolrate
Beta = 0.3
BType = ['FB','SB','NB']

samplepreslot = slotlen*oversamplerate
samplepreframe = samplepreslot*8
samplerate = oversamplerate*symbolrate

ts = 1./samplerate
tslot = ts*samplepreslot
tframe = ts*samplepreframe

all0freq = symbolrate/4.
channelspace = 200e3




