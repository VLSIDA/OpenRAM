![](./images/OpenRAM_logo_yellow_transparent.svg)
# OpenRAM

[![Python 3.5](https://img.shields.io/badge/Python-3.5-green.svg)](https://www.python.org/)
[![License: BSD 3-clause](./images/license_badge.svg)](./LICENSE)
[![Download](./images/download-stable-blue.svg)](https://github.com/VLSIDA/OpenRAM/archive/stable.zip)
[![Download](./images/download-unstable-blue.svg)](https://github.com/VLSIDA/OpenRAM/archive/dev.zip)

An open-source static random access memory (SRAM) compiler.

# What is OpenRAM?
<img align="right" width="25%" src="images/SCMOS_16kb_sram.jpg">

OpenRAM is an award winning open-source Python framework to create the layout,
netlists, timing and power models, placement and routing models, and
other views necessary to use SRAMs in ASIC design. OpenRAM supports
integration in both commercial and open-source flows with both
predictive and fabricable technologies.

# Documentation

Please see our [documentation][documentation] and let us know if anything needs
updating.

# Get Involved

+ [Port it](./PORTING.md) to a new technology.
+ Report bugs by submitting [Github issues].
+ Develop new features (see [how to contribute](./CONTRIBUTING.md))
+ Submit code/fixes using a [Github pull request]
+ Follow our [project][Github project].
+ Read and cite our [ICCAD paper][OpenRAMpaper]

# Further Help

+ [Documentation][documentation]
+ [OpenRAM Slack Workspace][Slack]
+ [OpenRAM Users Group][user-group] ([subscribe here][user-group-subscribe])
+ [OpenRAM Developers Group][dev-group] ([subscribe here][dev-group-subscribe])

# License

OpenRAM is licensed under the [BSD 3-clause License](./LICENSE).

# Publications

+ M. R. Guthaus, J. E. Stine, S. Ataei, B. Chen, B. Wu, M. Sarwar, "OpenRAM: An Open-Source Memory Compiler," Proceedings of the 35th International Conference on Computer-Aided Design (ICCAD), 2016
+ S. Ataei, J. Stine, M. Guthaus, “A 64 kb differential single-port 12T SRAM design with a bit-interleaving scheme for low-voltage operation in 32 nm SOI CMOS,” International Conference on Computer Design (ICCD), 2016, pp. 499-506.
+ E. Ebrahimi, M. Guthaus, J. Renau, “Timing Speculative SRAM”, IEEE In- ternational Symposium on Circuits and Systems (ISCAS), 2017
+ B. Wu, J.E. Stine, M.R. Guthaus, "Fast and Area-Efficient Word-Line Optimization",  IEEE International Symposium on Circuits and Systems (ISCAS), 2019
+ B. Wu, M. Guthaus, "Bottom Up Approach for High Speed SRAM Word-line Buffer Insertion Optimization", IFIP/IEEE International Conference on Very Large Scale Integration (VLSI-SoC), 2019
+ H. Nichols, M. Grimes, J. Sowash, J. Cirimelli-Low, M. Guthaus "Automated Synthesis of Multi-Port Memories and Control", IFIP/IEEE International Conference on Very Large Scale Integration (VLSI-SoC), 2019

 
# Contributors & Acknowledgment

- [Matthew Guthaus] from [VLSIDA] created the OpenRAM project and is the lead architect.
- [James Stine] from [VLSIARCH] co-founded the project.
- Many students: Hunter Nichols, Michael Grimes, Jennifer Sowash, Yusu Wang, Joey Kunzler, Jesse Cirimelli-Low, Samira Ataei, Bin Wu, Brian Chen, Jeff Butera

If I forgot to add you, please let me know!

* * *

[Matthew Guthaus]:       https://users.soe.ucsc.edu/~mrg
[James Stine]:           https://ece.okstate.edu/content/stine-james-e-jr-phd
[VLSIDA]:                https://vlsida.soe.ucsc.edu
[VLSIARCH]:              https://vlsiarch.ecen.okstate.edu/
[OpenRAMpaper]:          https://ieeexplore.ieee.org/document/7827670/

[Github issues]:         https://github.com/VLSIDA/OpenRAM/issues
[Github pull request]:   https://github.com/VLSIDA/OpenRAM/pulls
[Github project]:        https://github.com/VLSIDA/OpenRAM

[documentation]:         docs/source/index.md
[dev-group]:             mailto:openram-dev-group@ucsc.edu
[user-group]:            mailto:openram-user-group@ucsc.edu
[dev-group-subscribe]:   mailto:openram-dev-group+subscribe@ucsc.edu
[user-group-subscribe]:  mailto:openram-user-group+subscribe@ucsc.edu

[Klayout]:               https://www.klayout.de/
[Magic]:                 http://opencircuitdesign.com/magic/
[Netgen]:                http://opencircuitdesign.com/netgen/
[Qflow]:                 http://opencircuitdesign.com/qflow/history.html
[Ngspice]:               http://ngspice.sourceforge.net/
[Xyce]:                  http://xyce.sandia.gov/
[Git]:                   https://git-scm.com/

[FreePDK45]:             https://www.eda.ncsu.edu/wiki/FreePDK45:Contents
[SCMOS]:                 https://www.mosis.com/files/scmos/scmos.pdf
[Sky130]:                https://github.com/google/skywater-pdk-libs-sky130_fd_bd_sram.git

[Slack]:                 https://join.slack.com/t/openram/shared_invite/zt-onim74ue-zlttW5XI30xvdBlJGJF6JA


