import datetime
import json
import sys

import paramiko


def message(role: str, content: str) -> dict[str, str]:
    return {
        "role": role,
        "content": content
    }    

def currentTime() -> str:
    return datetime.datetime.now().strftime("%d-%m-%Y %H-%M-%S")

def endtaskCallback(messages: list[dict[str, str]]):
    with open(f"./logs/chat-{currentTime()}.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(messages, indent=2, ensure_ascii=False))
    sys.exit(0)

def sshCommand(ssh: paramiko.SSHClient, command: str) -> str:
    stdin, stdout, stderr = ssh.exec_command(command)
    return str(stdout.read().decode()).strip()

def readFile(path: str) -> str:
    with open(path, "r", encoding="utf-8") as file:
        return file.read()
    
def replaceAll(s: str, mask: dict[str, str]) -> str:
    target: str = s
    for k, v in mask.items():
        target = target.replace(k, v)
    return target