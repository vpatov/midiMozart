import struct

#note can either be an integer 0-127
def toBytes(num,width):
    if (width == 1):
        return struct.pack('>B',num)
    if (width == 2):
        return struct.pack('>H',num)
    if (width == 4):
        return struct.pack('>I',num)
    else:
        raise Exception("invalid width provided")


def toBytes2(num,width):
    return (num).to_bytes(width,byteorder='little')


##takes an integer as a parameter, and returns a variable length of bytes representing that value
def toVarBytes(num):
    pass

def playNote(note,time,volume = 127):
    on = b'\x00\x90'
    on += toBytes(note,1)
    on += toBytes(volume,1)
    off = encodeVarInt(time) + b'\x80'
    off += toBytes(note,1)
    off += toBytes(0,1)
    return on + off



# def intToVarField(num):
#     binNum = (bin(num)[2:])[::-1]
#     binaryString = ''
#     i = 0
#     while (i < len(binNum)):
#         if (i +1 % 8 == 0):
#             if (i == len(binNum) - 1):
#                 pass
#             pass
#         else: binaryString = binNum[i] + binaryString
#     pass



##this works correctly but it kinda sucks haha
def encodeVarInt(num):
    outputSize = 0
    output = b''
    first = 1
    if (num <= 127):
        return toBytes(num,1)

    while (num > 127):
        if (first == 1):
            output = toBytes((num & 127), 1) + output
            first = 0
        else:
            output = toBytes((num & 127) | 128,1) + output
        num >>= 7
        outputSize += 1
    output = toBytes((num & 127) | 128,1)  + output
    return output





def noteToInt(note):
    #a4 = 0x45 = 69
    #b4 = 0x47 = 71
    #c5 = 0x48 = 72
    ##c0,d0,e0,f0,g0,a0,b0,c1,d1,e1,f1,g1,a1,b1,c2
    ##12,14,16,17,19,21,23,24,26,28,29,31,33,35,36
    ##c ,e, 10,11,13,15,17,18,1a,1c,1d,1f,21,23,24

    ##c0,c1,c2,c3,c4,c5,c6,c7,c8
    ##12,24,36,48,60,72,84,96,108
    #c0 12 c#0 13 d0 14 d#0 15 e0 16 f0 17 f#0 18 g0 19 g#0 20 a0 21 a#0 22 b0 23

    base = 12
    pitch = note[0]
    pitchOffset = 0
    if pitch == 'a':
        pitchOffset = 9

    octave = int(note[1])
    offset = 0


def midi_header():
    ##HEADER BYTE CONSTANTS
    HEADER_ID = b'MThd'

    HEADER_LENGTH = b'\x00\x00\x00\x06'

    FORMAT_0 = b'\x00\x00'
    FORMAT_1 = b'\x00\x01'
    FORMAT_2 = b'\x00\x02'

    numTracks = 1
    # NUM_TRK_CHUNKS = (numTracks).to_bytes(2, byteorder='big')
    NUM_TRK_CHUNKS = struct.pack('>H', numTracks)

    division = 300
    # DIVISION = (division).to_bytes(2,byteorder='big')
    DIVISION = struct.pack('>H', division)
    ##END HEADER BYTE CONSTANTS


    ##TRACK BYTE CONSTANTS
    TRACK_ID = b'MTrk'
    END_TRACK = b'\x00\xff\x2f\x00'
    ##END TRACK BYTE CONSTANTS

    trk1 = HEADER_ID + HEADER_LENGTH + FORMAT_0 + NUM_TRK_CHUNKS + DIVISION + TRACK_ID



    ##CREATE DATA. AFTER DATA IS CREATED, COUNT BYTES, WRITE LENGTH TO FILE, AND THEN WRITE DATA.



    return trk1

