

import requests, os, psutil, sys, jwt, pickle, json, binascii, time, urllib3, base64, datetime, re, socket, threading, ssl, pytz, aiohttp, asyncio
from protobuf_decoder.protobuf_decoder import Parser
from network_utils import *
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from concurrent.futures import ThreadPoolExecutor
from threading import Thread

# Protocol Buffer Imports - Generated from proto/ directory definitions
from generated_proto import (
    DEcwHisPErMsG_pb2 as DecodeWhisperMsg,       # From: proto/DecodeWhisperMsg.proto
    MajoRLoGinrEs_pb2 as MajorLoginResponse,     # From: proto/MajorLoginRes.proto  
    PorTs_pb2 as GetLoginDataResponse,           # From: proto/GetLoginDataRes.proto
    MajoRLoGinrEq_pb2 as MajorLoginRequest,      # From: proto/MajorLoginReq.proto
    sQ_pb2 as ReceivedChat,                      # From: proto/recieved_chat.proto
)
from cfonts import render, say

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Core session management variables
session_writer = None
chat_handler = None
room_monitor = False
monitor_user = None
active_chat_id = None
target_user = None
surveillance = False
session_exit = False

request_config = {
    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 11; ASUS_Z01QD Build/PI)",
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip",
    "Content-Type": "application/x-www-form-urlencoded",
    "Expect": "100-continue",
    "X-Unity-Version": "2018.4.11f1",
    "X-GA": "v1 1",
    "ReleaseVersion": "OB50",
}

def generate_color_variant():
    colors = [
        "[FF0000]", "[00FF00]", "[0000FF]", "[FFFF00]", "[FF00FF]", "[00FFFF]",
        "[FFFFFF]", "[FFA500]", "[A52A2A]", "[800080]", "[000000]", "[808080]",
        "[C0C0C0]", "[FFC0CB]", "[FFD700]", "[ADD8E6]", "[90EE90]", "[D2691E]",
        "[DC143C]", "[00CED1]", "[9400D3]", "[F08080]", "[20B2AA]", "[FF1493]",
        "[7CFC00]", "[B22222]", "[FF4500]", "[DAA520]", "[00BFFF]", "[00FF7F]",
        "[4682B4]", "[6495ED]", "[5F9EA0]", "[DDA0DD]", "[E6E6FA]", "[B0C4DE]",
        "[556B2F]", "[8FBC8F]", "[2E8B57]", "[3CB371]", "[6B8E23]", "[808000]",
        "[B8860B]", "[CD5C5C]", "[8B0000]", "[FF6347]", "[FF8C00]", "[BDB76B]",
        "[9932CC]", "[8A2BE2]", "[4B0082]", "[6A5ACD]", "[7B68EE]", "[4169E1]",
        "[1E90FF]", "[191970]", "[00008B]", "[000080]", "[008080]", "[008B8B]"
    ]
    import random
    return random.choice(colors)

async def secure_data_encoder(encoded_data):
    key = b"Yg&tc%DEuh6%Zc^8"
    iv = b"6oyZDr22E3ychjM%"
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_message = pad(encoded_data, AES.block_size)
    encrypted_payload = cipher.encrypt(padded_message)
    return encrypted_payload

async def authenticate_user_credentials(,4248319819 7B3D6F0A6AFD2A646AF1EAE85BC7C0FF2BEB3CED66FEAB21F10699FEE3331878):
    url = "https://100067.connect.garena.com/oauth/guest/token/grant"
    headers = {
        "Host": "100067.connect.garena.com",
        "User-Agent": (await Ua()),
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "close",
    }
    data = {
        "uid": 4248319819,
        "password": 7B3D6F0A6AFD2A646AF1EAE85BC7C0FF2BEB3CED66FEAB21F10699FEE3331878,
        "response_type": "token",
        "client_type": "2",
        "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
        "client_id": "100067",
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=request_config, data=data) as response:
            if response.status != 200:
                return "Failed to get access token"
            data = await response.json()
            open_id = data.get("open_id")
            access_token = data.get("access_token")
            return (open_id, access_token) if open_id and access_token else (None, None)

async def prepare_authentication_payload(session_id, auth_token):
    major_login = MajorLoginRequest.MajorLogin()
    major_login.event_time = str(datetime.now())[:-7]
    major_login.game_name = "free fire"
    major_login.platform_id = 1
    major_login.client_version = "1.114.1"
    major_login.system_software = "Android OS 9 / API-28 (PQ3B.190801.10101846/G9650ZHU2ARC6)"
    major_login.system_hardware = "Handheld"
    major_login.telecom_operator = "Verizon"
    major_login.network_type = "WIFI"
    major_login.screen_width = 1920
    major_login.screen_height = 1080
    major_login.screen_dpi = "280"
    major_login.processor_details = "ARM64 FP ASIMD AES VMH | 2865 | 4"
    major_login.memory = 3003
    major_login.gpu_renderer = "Adreno (TM) 640"
    major_login.gpu_version = "OpenGL ES 3.1 v1.46"
    major_login.unique_device_id = "Google|34a7dcdf-a7d5-4cb6-8d7e-3b0e448a0c57"
    major_login.client_ip = "223.191.51.89"
    major_login.language = "en"
    major_login.open_id = session_id
    major_login.open_id_type = "4"
    major_login.device_type = "Handheld"
    memory_available = major_login.memory_available
    memory_available.version = 55
    memory_available.hidden_value = 81
    major_login.access_token = auth_token
    major_login.platform_sdk_id = 1
    major_login.network_operator_a = "Verizon"
    major_login.network_type_a = "WIFI"
    major_login.client_using_version = "7428b253defc164018c604a1ebbfebdf"
    major_login.external_storage_total = 36235
    major_login.external_storage_available = 31335
    major_login.internal_storage_total = 2519
    major_login.internal_storage_available = 703
    major_login.game_disk_storage_available = 25010
    major_login.game_disk_storage_total = 26628
    major_login.external_sdcard_avail_storage = 32992
    major_login.external_sdcard_total_storage = 36235
    major_login.login_by = 3
    major_login.library_path = "/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/lib/arm64"
    major_login.reg_avatar = 1
    major_login.library_token = "5b892aaabd688e571f688053118a162b|/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/base.apk"
    major_login.channel_type = 3
    major_login.cpu_type = 2
    major_login.cpu_architecture = "64"
    major_login.client_version_code = "2019118695"
    major_login.graphics_api = "OpenGLES2"
    major_login.supported_astc_bitset = 16383
    major_login.login_open_id_type = 4
    major_login.analytics_detail = b"FwQVTgUPX1UaUllDDwcWCRBpWA0OUgsvA1snWlBaO1kFYg=="
    major_login.loading_time = 13564
    major_login.release_channel = "android"
    major_login.extra_info = "KqsHTymw5/5GB23YGniUYN2/q47GATrq7eFeRatf0NkwLKEMQ0PK5BKEk72dPflAxUlEBir6Vtey83XqF593qsl8hwY="
    major_login.android_engine_init_flag = 110009
    major_login.if_push = 1
    major_login.is_vpn = 1
    major_login.origin_platform_type = "4"
    major_login.primary_platform_type = "4"
    serialized_data = major_login.SerializeToString()
    return await secure_data_encoder(serialized_data)

async def submit_authentication_request(auth_payload):
    url = "https://loginbp.ggblueshark.com/MajorLogin"
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    async with aiohttp.ClientSession() as session:
        async with session.post(
            url, data=auth_payload, headers=request_config, ssl=ssl_context
        ) as response:
            if response.status == 200:
                return await response.read()
            return None

async def retrieve_session_configuration(base_url, auth_data, session_token):
    url = f"https://clientbp.ggblueshark.com/GetLoginData"
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    request_config["Authorization"] = f"Bearer {session_token}"
    async with aiohttp.ClientSession() as session:
        async with session.post(
            url, data=auth_data, headers=request_config, ssl=ssl_context
        ) as response:
            if response.status == 200:
                return await response.read()
            return None

async def parse_authentication_response(auth_response):
    proto = MajorLoginResponse.MajorLoginRes()
    proto.ParseFromString(auth_response)
    return proto

async def decode_session_data(session_data):
    proto = GetLoginDataResponse.GetLoginData()
    proto.ParseFromString(session_data)
    return proto

async def DecodeWhisperMessage(hex_packet):
    packet = bytes.fromhex(hex_packet)
    proto = DecodeWhisperMsg.DecodeWhisper()
    proto.ParseFromString(packet)
    return proto

async def decode_team_packet(hex_packet):
    packet = bytes.fromhex(hex_packet)
    proto = ReceivedChat.recieved_chat()
    proto.ParseFromString(packet)
    return proto

async def xAuThSTarTuP(TarGeT, token, timestamp, key, iv):
    uid_hex = hex(TarGeT)[2:]
    uid_length = len(uid_hex)
    encrypted_timestamp = await DecodE_HeX(timestamp)
    encrypted_account_token = token.encode().hex()
    encrypted_packet = await EnC_PacKeT(encrypted_account_token, key, iv)
    encrypted_packet_length = hex(len(encrypted_packet) // 2)[2:]
    if uid_length == 9:
        headers = "0000000"
    elif uid_length == 8:
        headers = "00000000"
    elif uid_length == 10:
        headers = "000000"
    elif uid_length == 7:
        headers = "000000000"
    else:
        print("[SYSTEM] Warning: Detected unexpected user identifier length - applying standard formatting protocol")
        headers = "0000000"
    return f"0115{headers}{uid_hex}{encrypted_timestamp}00000{encrypted_packet_length}{encrypted_packet}"

async def cHTypE(H):
    if not H:
        return "Squid"
    elif H == 1:
        return "Clan"
    elif H == 2:
        return "Private"

async def SEndMsG(H, message, Uid, chat_id, key, iv):
    TypE = await cHTypE(H)
    if TypE == "Squid":
        msg_packet = await xSEndMsgsQ(message, chat_id, key, iv)
    elif TypE == "Clan":
        msg_packet = await xSEndMsg(message, 1, chat_id, chat_id, key, iv)
    elif TypE == "Private":
        msg_packet = await xSEndMsg(message, 2, Uid, Uid, key, iv)
    return msg_packet

async def transmit_network_packet(OnLinE, ChaT, TypE, PacKeT):
    if TypE == "Chat" and ChaT:
        chat_handler.write(PacKeT)
        await chat_handler.drain()
    elif TypE == "Online":
        session_writer.write(PacKeT)
        await session_writer.drain()
    else:
        return "Unsupported Type! >> Error"

async def establish_real_time_connection(ip, port, key, iv, AutHToKen, reconnect_delay=0.5):
    global session_writer, room_monitor, chat_handler, monitor_user, active_chat_id, target_user, session_type, current_user, surveillance, network_data, session_exit
    while True:
        try:
            reader, writer = await asyncio.open_connection(ip, int(port))
            session_writer = writer
            bytes_payload = bytes.fromhex(AutHToKen)
            session_writer.write(bytes_payload)
            await session_writer.drain()
            while True:
                network_data = await reader.read(9999)
                if not network_data:
                    break

                if network_data.hex().startswith("0500") and len(network_data.hex()) > 1000:
                    try:
                        print("[NETWORK] Successfully received encrypted data transmission from server endpoint")
                        packet = await DeCode_PackEt(network_data.hex()[10:])
                        print("[CRYPTO] Data packet decryption completed successfully")
                        packet = json.loads(packet)
                        OwNer_UiD, CHaT_CoDe, SQuAD_CoDe = await GeTSQDaTa(packet)

                        JoinCHaT = await AutH_Chat(3, OwNer_UiD, CHaT_CoDe, key, iv)
                        await transmit_network_packet(
                            chat_handler, session_writer, "Chat", JoinCHaT
                        )

                        color1 = generate_color_variant()
                        color2 = generate_color_variant()
                        cmd1 = xMsGFixinG("123456789")
                        cmd2 = xMsGFixinG("909042007")
                        dev = xMsGFixinG("EXITxD")
                        message = "[B][C]{}\n- Welcome To EXITxD Emote Bott! \n\n{}- Commands: /start {} {}\n\n[00FF00]Dev: @{}".format(
                            color1, color2, cmd1, cmd2, dev
                        )
                        P = await SEndMsG(0, message, OwNer_UiD, OwNer_UiD, key, iv)
                        await transmit_network_packet(chat_handler, session_writer, "Chat", P)

                    except:
                        if network_data.hex().startswith("0500") and len(network_data.hex()) > 1000:
                            try:
                                print("[NETWORK] Processing encrypted data transmission - retry sequence initiated")
                                packet = await DeCode_PackEt(network_data.hex()[10:])
                                print("[CRYPTO] Data packet decryption completed successfully during retry sequence")
                                packet = json.loads(packet)
                                OwNer_UiD, CHaT_CoDe, SQuAD_CoDe = await GeTSQDaTa(packet)

                                JoinCHaT = await AutH_Chat(3, OwNer_UiD, CHaT_CoDe, key, iv)
                                await transmit_network_packet(chat_handler, session_writer, "Chat", JoinCHaT)

                                color1 = generate_color_variant()
                                color2 = generate_color_variant()
                                cmd1 = xMsGFixinG("123456789")
                                cmd2 = xMsGFixinG("909042007")
                                dev = xMsGFixinG("EXITxD")
                                message = "[B][C]{}\n- Welcome To EXITxD Emote Bot! \n\n{}- Commands: @a {} {}\n\n[00FF00]Dev: @{}".format(
                                    color1, color2, cmd1, cmd2, dev
                                )
                                P = await SEndMsG(0, message, OwNer_UiD, OwNer_UiD, key, iv)
                                await transmit_network_packet(chat_handler, session_writer, "Chat", P)
                            except:
                                pass

            session_writer.close()
            await session_writer.wait_closed()
            session_writer = None

        except Exception as e:
            print(f"[NETWORK] Connection termination detected at endpoint {ip}:{port} - Error: {e}")
            session_writer = None
        await asyncio.sleep(reconnect_delay)

async def establish_chat_connection(ip, port, AutHToKen, key, iv, LoGinDaTaUncRypTinG, ready_event, reconnect_delay=0.5):
    global room_monitor, chat_handler, monitor_user, active_chat_id, target_user, session_writer, chat_id, XX, uid, surveillance, network_data, session_exit
    while True:
        try:
            reader, writer = await asyncio.open_connection(ip, int(port))
            chat_handler = writer
            bytes_payload = bytes.fromhex(AutHToKen)
            chat_handler.write(bytes_payload)
            await chat_handler.drain()
            ready_event.set()
            if LoGinDaTaUncRypTinG.Clan_ID:
                clan_id = LoGinDaTaUncRypTinG.Clan_ID
                clan_compiled_data = LoGinDaTaUncRypTinG.Clan_Compiled_Data
                print("\n[COMMUNITY] Bot has successfully established connection to clan communication system")
                print(f"[COMMUNITY] Connected to clan identifier: {clan_id}")
                print("[COMMUNITY] Clan communication channel initialized and operational")
                pK = await AuthClan(clan_id, clan_compiled_data, key, iv)
                if chat_handler:
                    chat_handler.write(pK)
                    await chat_handler.drain()
            while True:
                data = await reader.read(9999)
                if not data:
                    break

                if data.hex().startswith("120000"):
                    msg = await DeCode_PackEt(data.hex()[10:])
                    chatdata = json.loads(msg)
                    try:
                        response = await DecodeWhisperMessage(data.hex()[10:])
                        uid = response.Data.uid
                        chat_id = response.Data.Chat_ID
                        XX = response.Data.chat_type
                        inPuTMsG = response.Data.msg.lower()
                    except:
                        response = None

                    if response:
                        if inPuTMsG.startswith(("/5")):
                            try:
                                dd = chatdata["5"]["data"]["16"]
                                print("[MESSAGING] Executing private communication protocol")
                                message = "[B][C]{}\n\nAccept My Inv Fast\n\n".format(
                                    generate_color_variant()
                                )
                                P = await SEndMsG(response.Data.chat_type, message, uid, chat_id, key, iv)
                                await transmit_network_packet(chat_handler, session_writer, "Chat", P)
                                PAc = await OpEnSq(key, iv)
                                await transmit_network_packet(chat_handler, session_writer, "Online", PAc)
                                C = await cHSq(5, uid, key, iv)
                                await asyncio.sleep(0.5)
                                await transmit_network_packet(chat_handler, session_writer, "Online", C)
                                V = await SEnd_InV(5, uid, key, iv)
                                await asyncio.sleep(0.5)
                                await transmit_network_packet(chat_handler, session_writer, "Online", V)
                                E = await ExiT(None, key, iv)
                                await asyncio.sleep(3)
                                await transmit_network_packet(chat_handler, session_writer, "Online", E)
                            except:
                                print("[MESSAGING] Processing team-based communication request")

                        if inPuTMsG.startswith("/join"):
                            CodE = inPuTMsG.split("/join")[1].strip()
                            try:
                                dd = chatdata["5"]["data"]["16"]
                                print("[MESSAGING] Retrying private communication protocol execution")
                                EM = await GenJoinSquadsPacket(CodE, key, iv)
                                await transmit_network_packet(chat_handler, session_writer, "Online", EM)
                            except:
                                print("[MESSAGING] Retrying team-based communication request processing")

                        if inPuTMsG.startswith("leave"):
                            leave = await ExiT(uid, key, iv)
                            await transmit_network_packet(chat_handler, session_writer, "Online", leave)

                        if inPuTMsG.strip().startswith("/s"):
                            EM = await FS(key, iv)
                            await transmit_network_packet(chat_handler, session_writer, "Online", EM)

                        if inPuTMsG.strip().startswith("/start"):
                            try:
                                dd = chatdata["5"]["data"]["16"]
                                print("[MESSAGING] Executing secondary private communication protocol retry sequence")
                                message = "[B][C]{}\n\nOnly In Squad!\n\n".format(generate_color_variant())
                                P = await SEndMsG(response.Data.chat_type, message, uid, chat_id, key, iv)
                                await transmit_network_packet(chat_handler, session_writer, "Chat", P)
                            except:
                                print("[MESSAGING] Executing secondary team-based communication processing sequence")
                                parts = inPuTMsG.strip().split()
                                print(f"[MESSAGING] Communication session details - Type: {response.Data.chat_type}, User ID: {uid}, Session ID: {chat_id}")
                                message = "[B][C]{}\nEmote Activate -> {}\n".format(generate_color_variant(), xMsGFixinG(uid))

                                P = await SEndMsG(response.Data.chat_type, message, uid, chat_id, key, iv)

                                uid2 = uid3 = uid4 = uid5 = None
                                s = False

                                try:
                                    uid = int(parts[1])
                                    uid2 = int(parts[2])
                                    uid3 = int(parts[3])
                                    uid4 = int(parts[4])
                                    uid5 = int(parts[5])
                                    idT = int(parts[5])
                                except ValueError as ve:
                                    print(f"[SYSTEM] Command parsing error detected - ValueError: {ve}")
                                    s = True
                                except Exception:
                                    idT = len(parts) - 1
                                    idT = int(parts[idT])
                                    print(f"[SYSTEM] Target identifier assigned: {idT}")
                                    print(f"[SYSTEM] User identifier detected: {uid}")

                                if not s:
                                    try:
                                        await transmit_network_packet(chat_handler, session_writer, "Chat", P)

                                        H = await Emote_k(uid, idT, key, iv)
                                        await transmit_network_packet(chat_handler, session_writer, "Online", H)

                                        if uid2:
                                            H = await Emote_k(uid2, idT, key, iv)
                                            await transmit_network_packet(chat_handler, session_writer, "Online", H)
                                        if uid3:
                                            H = await Emote_k(uid3, idT, key, iv)
                                            await transmit_network_packet(chat_handler, session_writer, "Online", H)
                                        if uid4:
                                            H = await Emote_k(uid4, idT, key, iv)
                                            await transmit_network_packet(chat_handler, session_writer, "Online", H)
                                        if uid5:
                                            H = await Emote_k(uid5, idT, key, iv)
                                            await transmit_network_packet(chat_handler, session_writer, "Online", H)
                                    except Exception as e:
                                        pass

                        if inPuTMsG in ("hi", "hello", "fen", "salam"):
                            uid = response.Data.uid
                            chat_id = response.Data.Chat_ID
                            message = "Hello, this is bot\nDiscord: @exitxd"
                            P = await SEndMsG(response.Data.chat_type, message, uid, chat_id, key, iv)
                            await transmit_network_packet(chat_handler, session_writer, "Chat", P)
                        response = None

            chat_handler.close()
            await chat_handler.wait_closed()
            chat_handler = None

        except Exception as e:
            print(f"[NETWORK] Communication channel connection failure at {ip}:{port} - Error: {e}")
            chat_handler = None
        await asyncio.sleep(reconnect_delay)

async def initialize_gaming_session():
    user_credentials = ("BOT ID", "PASSWORD")
    # ENTER YOUR GUEST ID AND PASSWORD HERE
    user_id, auth_key = user_credentials
    
    session_identifier, access_credential = await authenticate_user_credentials(user_id, auth_key)
    if not session_identifier or not access_credential:
        print("[AUTHENTICATION] Error: Invalid user account credentials provided for system access")
        return None

    auth_payload = await prepare_authentication_payload(session_identifier, access_credential)
    auth_response = await submit_authentication_request(auth_payload)
    if not auth_response:
        print("[AUTHENTICATION] Error: Target user account is suspended or not registered in the system")
        return None

    parsed_auth = await parse_authentication_response(auth_response)
    server_url = parsed_auth.url
    session_token = parsed_auth.token
    target_account = parsed_auth.account_uid
    encryption_key = parsed_auth.key
    init_vector = parsed_auth.iv
    time_stamp = parsed_auth.timestamp

    session_config = await retrieve_session_configuration(server_url, auth_payload, session_token)
    if not session_config:
        print("[AUTHENTICATION] Error: Failed to retrieve server connection endpoints from authentication data")
        return None
    decoded_config = await decode_session_data(session_config)
    online_endpoint = decoded_config.Online_IP_Port
    chat_endpoint = decoded_config.AccountIP_Port
    online_ip, online_port = online_endpoint.split(":")
    chat_ip, chat_port = chat_endpoint.split(":")
    print(f"[AUTHENTICATION] Session token successfully generated: {session_token}")
    connection_token = await xAuThSTarTuP(int(target_account), session_token, int(time_stamp), encryption_key, init_vector)
    ready_event = asyncio.Event()

    task1 = asyncio.create_task(establish_chat_connection(chat_ip, chat_port, connection_token, encryption_key, init_vector, decoded_config, ready_event))
    await ready_event.wait()
    await asyncio.sleep(1)
    task2 = asyncio.create_task(establish_real_time_connection(online_ip, online_port, encryption_key, init_vector, connection_token))
    
    os.system("clear")
    print(render("EXITxD EMOTE BOT", colors=["white", "red"], align="center"))
    print("")
    print(f"[SYSTEM] Bot initialization complete - establishing connection to target user: {target_account}\n")
    print("[SYSTEM] Bot status: Online, authenticated, and fully operational")
    await asyncio.gather(task1, task2)

async def start_gaming_assistant():
    while True:
        try:
            await asyncio.wait_for(initialize_gaming_session(), timeout=7 * 60 * 60)
        except asyncio.TimeoutError:
            print("[AUTH] Token expired - restarting bot session")
        except Exception as e:
            print(f"[ERROR] TCP connection error - {e} => Restarting bot...")

if __name__ == "__main__":
    asyncio.run(start_gaming_assistant())
