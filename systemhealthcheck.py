#!/usr/bin/env python3
import psutil
import subprocess
import platform

def check_cpu_usage(threshold=80):
    cpu_usage = psutil.cpu_percent(interval=1)
    status = "OK" if cpu_usage < threshold else "High"
    return {"usage": cpu_usage, "status": status}

def check_memory_usage(threshold=80):
    mem = psutil.virtual_memory()
    mem_usage = mem.percent
    status = "OK" if mem_usage < threshold else "High"
    return {"total": mem.total, "used": mem.used, "percent": mem_usage, "status": status}

def check_disk_usage(threshold=80):
    partitions = psutil.disk_partitions()
    disk_info = {}
    for partition in partitions:
        usage = psutil.disk_usage(partition.mountpoint)
        usage_percent = usage.percent
        status = "OK" if usage_percent < threshold else "High"
        disk_info[partition.mountpoint] = {"total": usage.total, "used": usage.used, "percent": usage_percent, "status": status}
    return disk_info

def check_network_connectivity(host="8.8.8.8", port=53, timeout=3):
    import socket
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return {"status": "Connected"}
    except socket.error:
        return {"status": "Disconnected"}

def check_uptime():
    uptime = psutil.boot_time()
    import datetime
    now = datetime.datetime.now()
    boot_time = datetime.datetime.fromtimestamp(uptime)
    return {"uptime": str(now - boot_time).split('.')[0]}

def system_health_check():
    print("=== System Health Check ===")
    print(f"System: {platform.system()} {platform.release()}")
    print("\nCPU Usage:")
    cpu = check_cpu_usage()
    print(f"  Usage: {cpu['usage']}% | Status: {cpu['status']}")

    print("\nMemory Usage:")
    memory = check_memory_usage()
    print(f"  Total: {memory['total'] / 1e+9:.2f} GB")
    print(f"  Used: {memory['used'] / 1e+9:.2f} GB")
    print(f"  Usage: {memory['percent']}% | Status: {memory['status']}")

    print("\nDisk Usage:")
    disk = check_disk_usage()
    for mount, info in disk.items():
        print(f"  Mountpoint: {mount}")
        print(f"    Total: {info['total'] / 1e+9:.2f} GB")
        print(f"    Used: {info['used'] / 1e+9:.2f} GB")
        print(f"    Usage: {info['percent']}% | Status: {info['status']}")

    print("\nNetwork Connectivity:")
    network = check_network_connectivity()
    print(f"  Status: {network['status']}")

    print("\nSystem Uptime:")
    uptime = check_uptime()
    print(f"  Uptime: {uptime['uptime']}")

if __name__ == "__main__":
    system_health_check()

