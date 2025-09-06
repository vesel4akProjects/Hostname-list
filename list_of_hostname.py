import socket
import time
from tqdm import tqdm


class HostnamesList:

    def __init__(self,ip_list : list):
        self.ip_list = ip_list
        self.hostnames_list = list()

    def get_hostnames(self) -> str:

        try:
            start_time = time.time()

            for ip in tqdm(self.ip_list,total=len(self.ip_list),colour="green"):

                self.hostnames_list.append(socket.gethostbyaddr(ip))

            all_time = time.time() - start_time
            result = ""

            for i in self.hostnames_list:
                result += f"HOSTANAME : {i}\n"

            return result


        except Exception as e:
            self.exception(e)


    def result(self) -> None:

        try:
            self.result = self.get_hostnames()
            return print(self.result)

        except Exception as e:
            self.exception(e)

    def exception(self,e):
        return print(f"Error : {e}")



if __name__ == "__main__":
    ip_list = []

    with open("ip_addresses_list", "r") as f:
        for line in f:
            ip_address = line.strip()
            if ip_address:
                ip_list.append(ip_address)

    HostnamesList(ip_list).result()