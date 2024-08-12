# TSN-FlexTest: Flexible TSN Measurement Testbed

The repository contains the code of our technical session paper at NetSoft2022 and the corresponding article in IEEE Transactions on Network and Service Management.
Furthermore, an extended version of our testbed is published on arxiv.org, see [10.48550/arXiv.2211.10413](https://doi.org/10.48550/arXiv.2211.10413).

Additionally, we published our data sets on [ieee-dataport.org](ieee-dataport.org), see [10.21227/4eyw-n176](https://dx.doi.org/10.21227/4eyw-n176).

## Citation

If you use the code for other publications, please cite the authors:

```bibtex
@ARTICLE{10293177,
  author={Ulbricht, Marian and Senk, Stefan and Nazari, Hosein K. and Liu, How-Hang and Reisslein, Martin and Nguyen, Giang T. and Fitzek, Frank H. P.},
  journal={IEEE Transactions on Network and Service Management}, 
  title={TSN-FlexTest: Flexible TSN Measurement Testbed}, 
  year={2024},
  volume={21},
  number={2},
  pages={1387-1402},
  keywords={Hardware;Synchronization;Software;Mathematical analysis;Emulation;Standards;Protocols;Ethernet;industrial communication;Quality-of-Service;testbed;Time-Sensitive Networking},
  doi={10.1109/TNSM.2023.3327108}}
```

```bibtex
@INPROCEEDINGS{9844050,
  author={Senk, Stefan and Ulbricht, Marian and Acevedo, Javier and Nguyen, Giang T. and Seeling, Patrick and Fitzek, Frank H. P.},
  booktitle={2022 IEEE 8th International Conference on Network Softwarization (NetSoft)}, 
  title={Flexible Measurement Testbed for Evaluating Time-Sensitive Networking in Industrial Automation Applications}, 
  year={2022},
  volume={},
  number={},
  pages={402-410},
  keywords={Performance evaluation;Automation;Turnkey project;Current measurement;Hardware;Behavioral sciences;Software measurement;Time-sensitive Networking;Quality of Service;Measurement;IEEE Standards;Testbed},
  doi={10.1109/NetSoft54395.2022.9844050}}
```

```bibtex
@misc{ulbricht2022tsnflextest,
      title={TSN-FlexTest: Flexible TSN Measurement Testbed (Extended Version)}, 
      author={Marian Ulbricht and Stefan Senk and Hosein K. Nazari and How-Hang Liu and Martin Reisslein and Giang T. Nguyen and Frank H. P. Fitzek},
      year={2022},
      eprint={2211.10413},
      archivePrefix={arXiv},
      primaryClass={cs.NI}
}
```

---
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

## Acknowledgments

This work was funded by the German Research Foundation (DFG, Deutsche Forschungsgemeinschaft) as part of Germany’s Excellence Strategy - EXC 2050/1 - Project ID 390696704 - Cluster of Excellence “Centre for Tactile Internet with Human-in-the-Loop” (CeTI) of Technische Universität Dresden. We also would like to thank the open-source community for sharing their sophisticated work.
