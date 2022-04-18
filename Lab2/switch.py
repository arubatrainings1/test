class switch():
    """ This is my custom switch module"""
    def __init__(self) -> None:
        self.hostname = input("What is the hostname of the switch?: ")
        self.ip = input("What is the IP of the switch?: ")
        self.username = input("What is the username of the switch?: ")
        self.password = input("What is the password of the switch?: ")
    
    def __str__(self):
        return f"Switch details:\n\tHostname: {self.hostname}\n\tIP: {self.ip}\n\tUsername: {self.username}\n\tPassword {self.password}"