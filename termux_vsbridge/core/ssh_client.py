import paramiko

class SSHClient:
    """Manages SSH Connection and Execution"""
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect(self):
        """Starts SSH Connection"""
        self.client.connect(self.host, port=self.port, username=self.username, password=self.password)
        return True

    def execute(self, command, close_after = True):
        """Executes Command and Prints"""
        stdin, stdout, stderr = self.client.exec_command(command)
        while True:
            line = stdout.readline()
            if line == '' and stdout.channel.exit_status_ready():
                break
            if line:
                print(line.strip())
                self._line = line
        if close_after:
            self.close()
        return True

    def close(self):
        """Cloeses the SSH Connection"""
        self.client.close()
        return True