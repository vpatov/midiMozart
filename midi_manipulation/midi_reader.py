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
import sys
format = None
numTracks = None
division = None
meta = dict()
tracks = []



def toInt(n):
    if type(n) == bytes:
        return int.from_bytes(n, byteorder='big')
    else:
        return int(n)



def readChunk(f):
    try:
        byte = f.read(4)

        if (byte == b'MThd'):
            readHeader(f)
        elif (byte == b'MTrk'):
            readTrack(f)
        else:
            try:
                length = f.read(4)
                length = toInt(length)

                ignore = f.read(length)
                return length
            except:
                print ("Improperly formatted file. Exiting...")
                sys.exit(1)

    except:
        print("Improperly formatted chunk")

def readHeader(f):
    try:
        headerLength = toInt(f.read(4))
        assert(headerLength == 6)

        format = toInt(f.read(2))
        numTracks = toInt(f.read(2))
        division = toInt(f.read(2))

        print("format:",format)
        print("numTracks:",numTracks)
        print("division:",division)

        return headerLength


    except:
        print("Improperly formatted header. Exiting...")
        sys.exit(1)



def readTrack(f):
    try:
        chunkLength = toInt(f.read(4))
        bytesRead = 0

        trackNotes = []
        trackDeltas = []
        trackVolumes = []

        currentTrack = f.read(chunkLength)
        print(currentTrack)

        ####currentTrack contains everything after the file header, and the MTrkl + 4bytes of length.
        ####write code that will properly process midi events and meta events.
        ####meta events include stuff like copyright information, instrument selection.
        ###midi events include actual notes, as well as channel adjustments and what not

        return bytesRead
        pass

    except:
        print("Improperly formatted chunk. Exiting...")
        sys.exit(1)


def readEvent(f):
    try:
        pass
    except:
        print("Improperly formatted chunk. Exiting...")
        sys.exit(1)

def main():
    f = open('midi/input1.mid', 'rb')
    while(readChunk(f) != 0):
        readChunk(f)

main()