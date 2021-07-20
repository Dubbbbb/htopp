import psutil as ps

def get_cpu():
    res = {}
    cpu_time = ps.cpu_times(percpu=True)
    res["time"] = {}
    for index, core in enumerate(cpu_time):
        res["time"][f"core_{index}"] = (core.user, core.system)
    res["load"] = ps.cpu_percent(percpu=True, interval=0.3)
    return res



def get_disk():
    disk = {}
    disk_partitions = ps.disk_partitions(all=False)
    disk["partitions"] = {}
    for index,diskk in enumerate(disk_partitions):
        disk["partitions"][f"disk_{index}"] = (diskk.device, diskk.mountpoint, diskk.fstype) 
    disk["usage"] = ps.disk_usage('/')
    disk["usage"] = disk["usage"][0]/1e+9,disk["usage"][1]/1e+9,disk["usage"][2]/1e+9,disk["usage"][3]
    return disk


def get_memory():
    memory = ps.virtual_memory()
    mem = (memory.total/1e+9, memory.percent, memory.used/1e+9, memory.free/1e+9)
    return mem


def show(**kwargs):
    cpu_time_template = "User time for {0} {1:>10},\tsystem time for {0} {2:>10}\n"
    cpu_time_str = ""
    cpu = kwargs["cpu"]
    for key, value in cpu["time"].items():
        cpu_time_str += cpu_time_template.format(key, *value)
    print(cpu_time_str)


    cpu_load_template = "Load on the core-{0}  {1}\n"
    cpu_load_str = ""
    for key, value in enumerate(cpu["load"]):
        cpu_load_str += cpu_load_template.format(key, value)
    print(cpu_load_str)

    mem = kwargs["mem"]
    mem_template = "System Memory : \nTotal  {0:.2f}\npercent  {1:.2%}\nUsed  {2:.2f}\nFree {3:.2f}"
    mem_str = mem_template.format(*mem)
    print(mem_str)

    disk = kwargs["disk"]
    disk_partitions_template = "{0}:\tDevice {1}\tMountpoint '{2}'\tFStype {3\n"
    disk_partitions_str = ""
    for key, value in disk["partitions"].items():
        disk_partitions_str += disk_partitions_template.format(key, *value)
    disk_usage_template = "Disk :\ntotal: {0:.2f} \nused: {1:.2f} \nfree: {2:.2f} \npercent: {3}%"
    disk_usage_str = disk_usage_template.format(*disk["usage"])
    print(disk_partitions_str)
    print(disk_usage_str)








def main():
    cpu_data = get_cpu()
    disk_data = get_disk()
    memory_data = get_memory()


    show(
        cpu=cpu_data,
        disk=disk_data,
        mem=memory_data
    )

if __name__ == "__main__":
    main()