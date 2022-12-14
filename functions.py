from nis import cat
import socket #vai mandar o SO realizar actions na rede
import collections.abc



def input_resourses():
    dns = input("IP/DNS: ")
    print("Ports definition: You Can type a list of ports using . or ,")
    portInput = input("PORT: ")
    ports = portInput.split(".")  if "." in portInput else portInput.split(",") if "," in portInput else int(portInput)
    
    return ports, dns

def verifyIfDnsOrIp(text):
    valid = False
    try:
        cut = str(text).split('.')
        valid = isinstance(int(cut[0]), int)
        return valid
    except Exception as e:
        return valid    

def connect_send(code, port, dns):
    client = None
    encondingResponse = ''
    decodeResponse = ''

    if code == 0:
        print(f"CONNECT OPEN IN PORT {port} \n")
        if verifyIfDnsOrIp(dns):
            client = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
            #client.bind((dns, int(port)))
            #client.connect((dns, port))
            #print("SENDING REQUEST...")
            #client.sendall(b"GET HTTP/1")
            
            
        else:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((dns, int(port)))
            print("SENDING REQUEST...")
            client.send(b"GET HTTP/1")
            encondingResponse = client.recv(1024)
            decodeResponse = encondingResponse.decode("utf-8")
        
        
     
        if "400" in decodeResponse:
            print(f" \n IP/DNS : {dns}  \n PORT {port}  BAD CONNECTION! \n RESPONSE: \n {decodeResponse} \n")
        elif "200" in decodeResponse:
            print(f"\n  IP/DNS: {dns} \n PORT {port} CONNECT OK! \n RESPONSE: {decodeResponse} \n")
        elif "403" in decodeResponse:
            print(f"\n IP/DNS: {dns} \n PORT {port} CONNECT UNAUTHORIZED! \n RESPONSE: {decodeResponse} \n") 
        else:
            print("CONNECTION NOT RECOGNIZE!")
    else:
        print(f"\n CONNECTION CLOSE IN PORT {port} \n")


def verify_connection(dns, port):
    clientVerify = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientVerify.settimeout(0.2)
    code = clientVerify.connect_ex((dns, int(port)))
    return code


def scanning():
    ports, dns = input_resourses()

    if isinstance(ports, collections.abc.Sequence):
        for port in ports:
            
            connect_send(verify_connection(dns, port), port, dns)
                
    else:
        connect_send(verify_connection(dns, ports), ports, dns)
