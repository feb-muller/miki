import base64
import struct

#Script used to gennerate packets in binary form to then be sent over mesh
'''
Just these to begin with

 message type = 1 byte
 crc8 =  1 byte
 sequence number = 2 bytes ?
'''

HEADER = struct.Struct(">BBHH") #6 byte total B = 1 byte H = 2 bytes

packet = HEADER.pack()

print(packet)

print(HEADER.unpack_from(packet))