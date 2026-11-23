from packet_gen import PacketHandler
import asyncio
from meshcore import MeshCore, EventType

PAGE_REQ = 1
PAGE_RES = 2
PAGE_ERR = 3

INDEX_REQ = 4
INDEX_RES = 5



class Miki:
    def __init__(self, port="/dev/ttyUSB0"):
        self.port = port
        self.meshcore = None
        self.packet_gen = PacketHandler()


    async def send_page_req(self):
        while True:
            self.msg = await asyncio.to_thread(input, "> ") # add , "> " for a nice little arrow
            if self.msg:
                page_req_packet = self.packet_gen.page_req_handler(PAGE_REQ, self.msg)
                print(page_req_packet)
                await self.meshcore.commands.send_channel_data(1, 0XFFFF ,page_req_packet)



    async def send_page_res(self, title):
        packet_list = self.packet_gen.page_res_handler(PAGE_RES, title)
        return packet_list


    async def decoder(self, event):
        decoded_payload = self.packet_gen.decode_packets(event)
        return decoded_payload


    async def menu(self):
        print("=====MIKI=====")
        request = int(input("What would you like to request:\n" \
                                "1- Wiki Page\n" \
                                "2- Index Page\n"))
        if request == 1:
            page_req_packet = await self.send_page_req()
            print(page_req_packet)

            #then send this over mesh
            #This would be where index seraching is done and its send over mesh
            #what gets send back to you is this packet_list for you to decode

        elif request == 2:
            #packet = Send_Index_Req.req_packet()
            print("Nothing Yet")
            #Maybe this is automated with a page_req message then a cache or file of users indexes are stored from who you have requested from 
            


    async def run(self):
        self.meshcore = await MeshCore.create_serial(self.port)
        await self.meshcore.start_auto_message_fetching()

        self.meshcore.subscribe(EventType.CHANNEL_MSG_RECV, self.decoder)
        asyncio.create_task(self.meshcore.start_auto_message_fetching())

        asyncio.create_task(self.menu())

        try:
            await asyncio.sleep(float('inf'))
        except asyncio.CancelledError:
            await self.meshcore.disconnect()

asyncio.run(Miki().run())


'''
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
'''