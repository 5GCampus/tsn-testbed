#! /usr/bin/env python3

from os.path import isfile, getsize, getmtime

check_mark = u'\u2713'
cross = u'\u2717'


def check_file(file):
    if isfile(file):
        if getsize(file) > 7e6:  # file size below 10M
            if getmtime(file) > 1577833200:  # 2020-01-01T00:00:00
                return check_mark
            else:
                return "{} FILE TIMESTAMP ERROR".format(cross)
        else:
            return "{} FILE SIZE ERROR ".format(cross)
    else:
        return "{} FILE DOES NOT EXIST".format(cross)


dir_ = "_FILL_IN_"

switch = ["FibroLAN-FalconRX-NEW"
          ]
qos_setting = ["No-QoS",
               "IEEE-802.1p",  # SPQ
               "TAS1",  # TAS switch
               "txinject-TAS1-full"  # TAS sender
               ]
bg_load = [0,
           85,
           100,
           150,
           200
           ]
bg_frame_size = [64,
                 1518
                 ]
stream = ["robotic",
          "audio",
          "videoBBB",
          #"tactileGLOVE",
          "podcast",
          "spotWASDspot",
          "spotJPEGspot",
          ]
stream_combination = [#"tactileGLOVE-podcast-XY",  # use-case 1
                      "robotic-audio-videoBBB",  # use-case 2
                      "spotWASDspot-podcast-spotJPEGspot"  # use-case 3
                      ]


for sw in switch:
    for q in qos_setting:
        for bgf in bg_frame_size:
            for bgl in bg_load:
                for st in stream:
                    file = "{}_{}-NULL-NULL_{}_{}_{:.1f}percent".format(sw, st, q, bgf, bgl)
                    file_full = "{}{}.pcap".format(dir_, file)
                    print("{:<90}\t{}".format(file, check_file(file_full)))
                for sc in stream_combination:
                    file = "{}_{}_{}_{}_{:.1f}percent".format(sw, sc, q, bgf, bgl)
                    file_full = "{}{}.pcap".format(dir_, file)
                    print("{:<90}\t{}".format(file, check_file(file_full)))
