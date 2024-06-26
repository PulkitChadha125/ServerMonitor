import socket
import ssl
import time
from datetime import datetime
import pickle
import subprocess
import platform
from gmail import email_alert
def write_to_order_logs(message):
    with open('EmailLogs.txt', 'a') as file:  # Open the file in append mode
        file.write(message + '\n')


class Server():
    def __init__(self, name, port, connection, priority,email):
        self.name = name
        self.port = port
        self.connection = connection.lower()
        self.priority = priority.lower()
        self.email=email
        self.history = []
        self.alert = False

    def check_connection(self):
        msg = ""
        success = False
        now = datetime.now()

        try:
            if self.connection == "plain":
                socket.create_connection((self.name, self.port), timeout=20)
                msg = f"{self.name} is up. On port {self.port} with {self.connection} {self.email}"
                success = True
                self.alert = False
            elif self.connection == "ssl":
                ssl.wrap_socket(socket.create_connection((self.name, self.port), timeout=20))
                msg = f"{self.name} is up. On port {self.port} with {self.connection} {self.email}"
                success = True
                self.alert = False
            else:
                if self.ping():
                    msg = f"{self.name} is up. On port {self.port} with {self.connection} {self.email}"
                    success = True
                    self.alert = False
        except socket.timeout:
            msg = f"server: {self.name} timeout. On port {self.port}"
        except (ConnectionRefusedError, ConnectionResetError) as e:
            msg = f"server: {self.name} {e}"
        except Exception as e:
            msg = f"No Clue??: {e}"

        
        if success == False and self.alert == False:
            # Send Alert
            self.alert = True
            # Uncomment this once you have setup gmail alerts!
            # Check out video if you need help!
            # https://youtu.be/B1IsCbXp0uE

            email_alert("VPS Alert",f"You'r vps : {self.name} is down @  time: {now} please check ",self.email)
            email_alert("VPS Alert", f"Client vps : {self.name} is down @  time: {now}", "prajwal.naganur@botmudra.com")
            email_alert("VPS Alert", f"Client vps : {self.name} is down @  time: {now}", "suresh.patil@botmudra.com")
            email_alert("VPS Alert", f"Client vps : {self.name} is down @  time: {now}", "Botmudra@gmail.com")
            EmailLogs=f"{now} Email sent to {self.email}"
            print(EmailLogs)
            write_to_order_logs(EmailLogs)

        self.create_history(msg,success,now)

    def create_history(self, msg, success, now):
        history_max = 100
        self.history.append((msg,success,now))

        while len(self.history) > history_max:
            self.history.pop(0)

    def ping(self):
        try:
            output = subprocess.check_output("ping -{} 1 {}".format('n' if platform.system().lower(
            ) == "windows" else 'c', self.name ), shell=True, universal_newlines=True)
            if 'unreachable' in output:
                return False
            else:
                return True
        except Exception:
                return False


if __name__ == "__main__":
    while True:
        try:

            servers = pickle.load(open("servers.pickle", "rb"))
        except:
            servers = [

                Server("yahoo.com", 80, "plain", "high","abc@gmail.com")
            ]

        for server in servers:
            server.check_connection()
            # print(len(server.history))
            print(server.history[-1])

        pickle.dump(servers, open("servers.pickle", "wb"))
        time.sleep(60)