import subprocess
import psutil
import socket
import uuid
import distro
import shutil

def get_hostname():
    return socket.gethostname()

def get_cpu_count():
    return psutil.cpu_count(logical=True)

def get_ram_gb():
    return round(psutil.virtual_memory().total / (1024 ** 3))

def get_os_type():
    return platform.system()

def get_os_version():
    return distro.name() + " " + distro.version()

def get_disk_size_gb():
    total, used, free = shutil.disk_usage("/")
    return round(total / (1024 ** 3))

def get_disk_free_gb():
    total, used, free = shutil.disk_usage("/")
    return round(free / (1024 ** 3))

def get_primary_ip():
    return socket.gethostbyname(socket.gethostname())

def get_primary_mac():
    mac_num = hex(uuid.getnode()).replace('0x', '').zfill(12)
    return ':'.join(mac_num[i:i+2] for i in range(0, 12, 2))

def main():
    print(f"Hostname: {get_hostname()}")
    print(f"CPU (count): {get_cpu_count()}")
    print(f"RAM (GB): {get_ram_gb()}")
    print(f"OSType: {get_os_type()}")
    print(f"OSVersion: {get_os_version()}")
    print(f"OS disk size (GB): {get_disk_size_gb()}")
    print(f"OS disk free (GB): {get_disk_free_gb()}")
    print(f"Primary IP: {get_primary_ip()}")
    print(f"Primary Mac: {get_primary_mac()}")

if __name__ == "__main__":
    main()
