from sys import exit


def parse_filename(file):
    f = file.split("/")[-1]
    settings = f.split("_")
    switch = settings[0]
    streams = settings[1].split("-")
    qos_type = settings[2]
    bg_framesize = int(settings[3])
    bg_load = float(settings[4].rstrip("percent.pcap"))
    return switch, streams, qos_type, bg_framesize, bg_load


def create_mapping(streams):
    mapping = {}
    for s in streams:
        if any(kw in s for kw in ['tactile', 'robotic', 'spotWASDhost','spotWASDspot','tactileGLOVE']):
            mapping[1] = s
        elif any(kw in s for kw in ['audio', 'podcast']):
            mapping[2] = s
        elif any(kw in s for kw in ['video', 'spotJPEGhost', 'spotJPEGspot','spotRAWhost','spotRAWspot','videoBBB']):
            mapping[3] = s
        elif "NULL" in s:
            continue
        else:
            print("ERROR - Can not identify stream {}".format(s))
            exit(1)
    return mapping


def create_filename(switch, mapping, qos_type, bg_framesize, bg_load):
    streams = "-".join(mapping.values())
    if len(mapping.values()) < 3:
        streams += "-NULL"
    return "{}_{}_{}_{}_{}percent".format(switch,
                                          streams,
                                          qos_type,
                                          bg_framesize,
                                          bg_load)
