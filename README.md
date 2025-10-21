# CICV5G: A 5G Communication Delay Dataset for PnC in Cloud-based Intelligent Connected Vehicles

We establish a 5G delay testbed at the intelligent connected vehicle evaluation base at Tongji University and conduct extensive field tests. Through these tests, over 300,000 records are collected to build our dataset, **CICV5G**. The dataset includes not only communication delay and channel conditions (such as reference signal received power and signal-to-noise ratio) but also vehicle poses (i.e., vehicle coordinates, velocity). Based on CICV5G, we conduct a comparative analysis of CICVs and autonomous vehicles (AVs) performance in typical scenarios and explore the impact of communication delay on the PnC. To the best of our knowledge, this is the first publicly available dataset of 5G communication delay specifically for PnC of CICVs. !\[image]\(Figures/readme.png)

## Package Description

### data folder

This folder contains all the test data, including results from 5G public network (n78) and 5G private network (n8) under different testing conditions.

### figures folder

This folder contains all the figures of communication delay distribution under different testing conditions. We have established real-time communication latency data in a real test environment, where utmx and utmy represent the x and y coordinates, and the z-axis indicates the communication latency.

### tool folder

The tools folder includes Python code for processing, plotting, and statistical analysis of raw communication delay data, making it easier for users to analyze and process the data.

## Usage

### Data Usage

You can conduct your research using the data from the data folder, which contains two classification methods to help you quickly filter the data. n78 refers to the 5G public network test results, where data transmission involves base station handovers. n8 refers to the results of the private network tests, where there are no base station handovers. Still, due to network coverage limitations, there is a signal quality issue and higher communication delay in the southern region. To facilitate the design of the PnC (Planning and Coordination) algorithm, and consider the actual communication problems, we have also specially provided the results for the southern region with large delay data.

Of course, you can also perform analysis based on the results obtained from our processing of the raw data. The figures folder contains the statistics and analysis of the measured data. The Gamma distribution is the result of our statistical analysis of the data, and you can also use the distribution model and data parameters we have established for your research work

### Code Usage

Our code repository has been tested on Ubuntu 20.04 and Windows 11. The tool code provides data processing functions, including calculations for distance, communication delay, and more. It also includes code for generating statistical plots, such as violin plots, line charts, etc., to facilitate the work of researchers

## Video Links

We have also conducted real-world testing to compare the impact of latency on planning and control (PnC) of cloud-based intelligent connected vehicles (CICV), as well as automated vehicles (AVs). The video links are as follows:

- Urban Loop Scenario CICV and AV Real-World Test Comparison

1.  the results of AV in the urban loop scenario. [urbanloop_AV](https://youtu.be/ASDVWeAMCp4)

2.  the results of CICV in the urban loop scenario.[urbanloop_CICV](https://youtu.be/wY-nLKXZwNk)

- Shuttle Loop Scenario CICV and AV Real-World Test Comparison

1.  the results of AV in the shuttle loop scenario. [shuttle_AV](https://youtu.be/8yW_RCdmDTc)

2.  the results of CICV in the shuttle loop scenario.[shuttle_CICV](https://youtu.be/-7OEzwrUfpw)

If you have any questions, feel free to contact <zhangxr@tongji.edu.cn>
