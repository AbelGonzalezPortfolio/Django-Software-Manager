from pathlib import Path
from subprocess import Popen, PIPE

PS_EXEC = Path("C:/Program Files/PowerShell/7/pwsh.exe")
PS_PATH = Path("./powershell/")


def _start_script(filename):
    """
    Run a powershell script file locally.

    filename (str)
    hostnames (list)
    """
    command = [PS_EXEC, PS_PATH / f"{filename}.ps1"]
    return Popen(command, text=True, stdout=PIPE, stderr=PIPE)


def _start_script_generator(filename, hostnames):
    """
    Run a powershell script file remotely.

    filename (str)
    hostnames (list)
    """
    command = [PS_EXEC, PS_PATH / f"{filename}.ps1"]
    jobs = [
        (hostname, Popen(command + [hostname], text=True, stdout=PIPE, stderr=PIPE))
        for hostname in hostnames
    ]

    for job in jobs:
        out, err = job[1].communicate()
        out = out.strip().replace("\x1b[0m", "")
        err = err.strip()
        yield job[0], out, err


def get_ad_devices():
    """
    Run powershell command to retrieve list of devices in AD
    """
    job = _start_script("get_ad_devices")
    out, err = job.communicate()
    out = out.strip().replace("\x1b[0m", "").replace("\x1b[91m", "")
    err = err.strip()

    out = out.split("--")[1].split("\n")
    out = [x for x in out if x != ""]

    if err != "":
        raise ValueError(err)
    else:
        return out


def get_ip_address(hostnames):
    for (hostname, out, err) in _start_script_generator("get_ip", hostnames):
        yield (hostname, out, err)


def get_network_status(hostnames):
    for (hostname, out, err) in _start_script_generator(
        "get_network_status", hostnames
    ):
        yield (hostname, out, err)


def get_software(hostnames):
    for (hostname, out, err) in _start_script_generator("get_software", hostnames):
        if err != "":
            raise ValueError(err)
        out = out.split("\n")
        out = [software.split(":") for software in out if software != ":"]
        yield (hostname, out)


def enable_remoting(hostnames):
    for (hostname, out, err) in _start_script_generator("enable_remoting", hostnames):
        if "error code 0" in err:
            continue
        if err != "":
            raise ValueError(err)


if __name__ == "__main__":
    hostnames = [f"kemperlab{i}-21" for i in range(2, 5)]
    for software in get_software(hostnames):
        print(software)
