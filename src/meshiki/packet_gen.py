import base64
import struct
from wiki_handler import WikiHandler


#Script used to gennerate packets in binary form to then be sent over mesh

HEADER = struct.Struct(">BBHH") #6 byte total B = 1 byte H = 2 bytes


class PacketHandler:

    def __init__(self):
        self.wiki_handler = WikiHandler()

    #uses wiki script to get page based on title
    def fetch_page(self, title: str): 
        wiki_page, short_des = self.wiki_handler.handle(title)
        return wiki_page

    #encodes packet accoring to HEADER struct
    def encode_packet(self, msg_type: int, crc8: int, seq_no: int, req_num: int):
        packet = HEADER.pack(msg_type, crc8, seq_no, req_num)
        return packet

    #Decodes packet according to HEADER struct
    def decode_packet(packet):
        decoded = HEADER.unpack_from(packet)
        print (decoded)

    #Wiki Page request handler
    def page_req_handler(self, msg_type, request):

        wiki_page = self.fetch_page(title=request)
        packet = self.encode_packet(msg_type, 1, 1, 1)

        return packet, wiki_page

    #index page request handler
    def index_req_handler(self, msg_type, user):

        #some other script that gets indexes? maybe index req sent with every message if not in cache?
        packet = self.encode_packet(msg_type, 1, 1, 1)

        return packet