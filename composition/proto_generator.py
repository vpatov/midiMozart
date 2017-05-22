"""
"MThd" 4 bytes
the literal string MThd, or in hexadecimal notation: 0x4d546864. These four characters at the start of the MIDI file indicate
that this is a MIDI file.


<header_length> 4 bytes
length of the header chunk (always 6 bytes long--the size of the next three fields which are considered the header chunk).


<format> 2 bytes
0 = single track file format
1 = multiple track file format
2 = multiple song file format (i.e., a series of type 0 files)


<n> 2 bytes
number of track chunks that follow the header chunk


<division> 2 bytes
unit of time for delta timing. If the value is positive, then it represents the
units per beat. For example, +96 would mean 96 ticks per beat. If the value
is negative, delta times are in SMPTE compatible units.

"""
import notes
import os
import struct

##HEADER BYTE CONSTANTS
HEADER_ID = b'MThd'

HEADER_LENGTH = b'\x00\x00\x00\x06'

FORMAT_0 = b'\x00\x00'
FORMAT_1 = b'\x00\x01'
FORMAT_2 = b'\x00\x02'

numTracks = 1
#NUM_TRK_CHUNKS = (numTracks).to_bytes(2, byteorder='big')
NUM_TRK_CHUNKS = struct.pack('>H',numTracks)

division = 300
#DIVISION = (division).to_bytes(2,byteorder='big')
DIVISION = struct.pack('>H',division)
##END HEADER BYTE CONSTANTS


##TRACK BYTE CONSTANTS
TRACK_ID = b'MTrk'
END_TRACK = b'\x00\xff\x2f\x00'
##END TRACK BYTE CONSTANTS

f = open("midi/sample.mid",'wb+')
f.write(b'MThd')
f.write(HEADER_LENGTH)
f.write(FORMAT_0)
f.write(NUM_TRK_CHUNKS)
f.write(DIVISION)


f.write(TRACK_ID)



##CREATE DATA. AFTER DATA IS CREATED, COUNT BYTES, WRITE LENGTH TO FILE, AND THEN WRITE DATA.
trk1 = b''

trk1 += b'\x00\xb0\x07\x7f'
##write controller #7 value = 127

trk1 += b'\x00\xff\x51\x03\x07\x53\x00'
##set tempo to 0x753

trk1 += b'\x00\xc0\x51'
#set instrument to number 81 (sawtooth lead)

#####MUSIC START

###RULE IDEAS
# 1. Add repetition by abstracting groups of notes, and giving the program a decent likelihood of repeating certain groups.
#   1a) Add on to this idea by having groups of notes that are considered transitions
# 2. Add support for a second track, that would play backing chords, and support for a third track that plays harmonies.
# 3. Music can be broken down into "sections", aech of which employ some sort of pre-defined technique
#   3a) This includes, solos, arpegios, pedal tones

####




deltas = [0,2,1,2,2,1,2,2]
# minorScale = [69,71,72,74,76,77,79,81]

minorNotes = {69,71,72,74,76,77,79,81,83,84}

minorArpegs = {(69,71,72),(72,71,69),(69,76,69,74,69,72,71,68,69)}
for note in minorNotes:
    minorNotes.discard(note)
    minorNotes.add(note)
majorNotes = {69,69,69,71,73,73,73,74,76,78,80,81}

minorArpegs = {(69,72,76),(69,72,76),(69,72,76),(69,70,71,72),(76,72,76,71,76,69),(76,75,74),(69,71,72,71,72),(69,72,76),(71,74,77),(72,76,79)}

minorGroup1 = {(69,71,72,71),(76,77,76,74),(79,79,81,76),(76,71,72,69)}

timeIntervals = {150,150,150,150,300,450,600,75}

testSet1 = {(18,19,20,25,30,30),(80,85,90,95,96,97,98,99,100,100,100,100,90,90,90,90)}

import random

tempTrack = b''
# for i in range(0,8):
#     randNotes = random.sample(testSet1,1)[0]
#     for note in randNotes:
#         tempTrack += notes.playNote(note,50 + random.randint(0,2) * 50)


tempTrack += notes.playNote(50,600)









    # randNotes = random.sample(minorArpegs,1)[0]
    # # randTime = random.sample(timeIntervals,1)[0]
    # randTime = 100
    # randNote = random.sample(minorNotes,1)[0]
    # for note in randNotes:
    #      tempTrack += notes.playNote(note,time)
    # randNote = random.sample(minorNotes,1)[0]
    # tempTrack += notes.playNote(randNote,time)

trk1 += tempTrack
#
# trk1 += notes.playNote(74,200)
# trk1 += notes.playNote(75,200)
# trk1 += notes.playNote(76,200)
# trk1 += notes.playNote(72,200)
# trk1 += notes.playNote(71,200)
# trk1 += notes.playNote(68,200)
# trk1 += notes.playNote(69,200)
# trk1 += notes.playNote(76,200)
# trk1 += notes.playNote(71,200)
# trk1 += notes.playNote(72,200)
# trk1 += notes.playNote(69,200)



# buf += b'\x00\x90\x45\x7f'
# buf += b'\x83\x00\x80\x45\x00'
# #turn on note 45 to full volume and then turn off after time
#
# buf += b'\x00\x90\x49\x7f'
# buf += b'\x83\x00\x80\x49\x00'
# #turn on note 49 to full volume
#
# buf += b'\x00\x90\x4c\x7f'
# buf += b'\x83\x00\x80\x4c\x00'
# #turn on note 52 to full volume

trk1 += b'\x83\x00\x80\x00\x00'
trk1 += END_TRACK

tracklength = len(trk1)
#trklength = (tracklength).to_bytes(4, byteorder='big')
trklength = notes.toBytes(tracklength,4)
for b in trklength:
    print ord(b),

f.write(trklength)
f.write(trk1)

for b in trk1:
    print ord(b),

f.close()
os.startfile("C:\\Users\\Vasia\\Documents\\PycharmProjects\\MidiMozart\\midi\\sample.mid")

