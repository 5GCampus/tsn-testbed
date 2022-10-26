# TSN-FlexTest: Update comming soon
We evolved the tesdbed structure and add more extensive tests to PTP, TAS and TA_prio with real world stream sets. The testbed will now called **TSN-FlexTest**


# Flexible Measurement Testbed for Evaluating Time-Sensitive Networking

The repository contains the code of a technical session paper at NetSoft2022.
If you use the code for other publications, please cite the authors:

```bibtex
@INPROCEEDINGS{Senk2206:Flexible,
AUTHOR="Stefan Senk and Marian Ulbricht and Javier Acevedo and Giang T. Nguyen and
Patrick Seeling and Frank H.P. Fitzek",
TITLE="Flexible Measurement Testbed for Evaluating {Time-Sensitive} Networking in
Industrial Automation Applications",
BOOKTITLE="2022 IEEE 8th International Conference on Network Softwarization (NetSoft)
(NetSoft 2022)",
ADDRESS="Milan, Italy",
DAYS=26,
MONTH=jun,
YEAR=2022,
KEYWORDS="Time-sensitive Networking; Quality of Service; Measurement; IEEE Standards;
Testbed",
ABSTRACT="Deterministic communications are required for industrial environments, yet
their realization is a challenging task. Time-Sensitive Networking (TSN) is
intended to enable deterministic communication over inexpensive Ethernet
networks. Standardized by the IEEE TSN working group, TSN enables precise
control of time synchronization, traffic shaping, reliability enhancements,
and network administration to answer the demands of industrial control
applications. Subsequently, there is a significant need to enable turnkey
research and
implementation efforts. However, a current lack of open-sourced testbed
implementations to investigate and study the behavior of TSN network
devices limits verification to simulation and theoretical models. We
introduce a publicly available, flexible, and open-sourced measurement
testbed for evaluating TSN in the context of industrial automation
applications to address the need to perform real-world measurements. In
this contribution, we describe our testbed combining
Commercial-Off-The-Shelf (COTS) hardware and existing open-source tools as
a platform for in-depth evaluation of TSN devices. Providing detailed TSN
backgrounds, we describe an in-depth performance analysis for our
implementation. For a common Tactile Internet scenario, we observe an
accuracy of close to 5 ns achievable with our publicly available COTS
setup."
}
```

The repository contains specifically:

## Code

The code in this and the other repositories allows to do network packet measurements with generally available open-source tools.
The software is commonly know and was combined with scripts to aid the automated measurement process.
Some of the code was adjusted and extended in order to fit our needs or to add missing functionality.

### Start a Measurement
* configure your nodes with ssh-key for passwordless login
* make sure to install necessary software (linuxptp, tcpdump, tcpreplay, MoonGen, etc.)
* copy and adjust [src/measurements/config.conf.example](src/measurements/config.conf.example) to `config.conf` in `src` directory
* run [src/measurements/init.sh](src/measurements/init.sh) to run your defined pcaps
* pcap will be captured from destination and stored at set location

### PCAP Generation
* use the scripts in [src/pcap_writer](src/pcap_writer) to create your own measurement data
* [pcap_writer.ipynb](src/pcap_writer/pcap_writer.ipynb) contains the most complete code
* you can use, e.g., `ffprobe` to analyze existing multimedia files:
```shell
ffprobe -v error -show_frames -select_streams a:0 -print_format json bbb_sunflower_1080p_60fps_normal.mp4 > bbb_audio_frames.json
ffprobe -v error -show_frames -select_streams v:0 -print_format json bbb_sunflower_1080p_60fps_normal.mp4 > bbb_video_frames.json
```

### Data Evaluation
* in [src/evaluation](src/evaluation) you can find several scripts to
  * parse your pcap file
  * generate statistics
  * plot your data
  * helper and test tools
* the folder contains the scripts to create the figures from the paper

## Other Repositories

In order to make full use of the code, you should visit our other repositories with modified/patched software:
* see patches/ for modifications made to:
	* linuxPTP
	* Linux kernel (Intel igb driver)
	* tcpreplay

## Thanks

We thank the original developers for their effort.
Without them it would not be possible to us to do research.
