from packet_gen import PacketHandler
import asyncio

PAGE_REQ = 1
PAGE_RES = 2
PAGE_ERR = 3

INDEX_REQ = 4
INDEX_RES = 5


class Send_Page_Res: #generates packets to be send back to client
    def __init__(self):
        self.packet_gen = PacketHandler()

    def req_packet(self):
        title = input("What Page are you looking for: ") #This is replaced with a user message over meshcore
        packet_list = self.packet_gen.page_res_handler(PAGE_RES, title)
        return packet_list


class Send_Page_Req:
    def __init__(self):
        pass
    #function here to format a packet that has title and routing stuff in it


class Decoder:
    def __init__(self):
        self.packet_gen = PacketHandler()

    def decode_packets(self, packet_list):
        decoded_list = self.packet_gen.decode_packets(packet_list)
        return decoded_list


def main():
    print("-----MIKI PROJECT-----\n")

    request = int(input("What would you like to request:\n" \
                        "1- Wiki Page\n" \
                        "2- Index Page\n"))
    if request == 1:
        packet_list = Send_Page_Res().req_packet() #this is acting as if someone has responded with the packets
        #This would be where index seraching is done and its send over mesh
        #what gets send back to you is this packet_list for you to decode
        
        for i in range(len(packet_list)):
            print(packet_list[i]) #in for loop send each part of list this is the bytes and compressed wiki text

        decoded = Decoder().decode_packets(packet_list)
        print(decoded)

    elif request == 2:
        #packet = Send_Index_Req.req_packet()
        print("Nothing Yet")
        #Maybe this is automated with a page_req message then a cache or file of users indexes are stored from who you have requested from 





main()