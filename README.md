# 5G communication delay dataset for cloud‑based vehicle planning and control

**Short description**

We establish a 5G communication delay testbed at the intelligent connected vehicle evaluation base at Tongji University and conduct extensive field tests. Through these tests, over 150,000 records are collected to build our dataset, **CICV5G**. The dataset includes not only communication delay and channel conditions (such as reference signal received power and signal-to-noise ratio) but also vehicle poses (i.e., vehicle coordinates, velocity). Based on CICV5G, we conduct a comparative analysis of CICVs and autonomous vehicles (AVs) performance in typical scenarios and explore the impact of communication delay on the PnC. To the best of our knowledge, this is the first publicly available dataset of 5G communication delay specifically for PnC of CICVs. 
![image](Figures/readme.png)

**DOI (placeholder)**
Zenodo DOI: https://doi.org/10.5281/zenodo.xxxxxx (to be added after archival)

---

## Repository structure (top-level)

- `CICV5G/`
  - `Data/` — Experimental datasets organized by scenario and network mode
  - `Figures/` — Visualization outputs used in the paper and for validation
  - `Tools/` — Analysis and plotting scripts (Python)
  - `README.md` — This file (dataset overview and usage instructions)


---

## Summary of the dataset
- **Total records:** >150,000 transmission cycles (V2N2V samples).
- **Scenarios:** Urban, Arterial, Rural / Off-road.
- **Network modes:** n8 (private network) and n78 (public network).
- **Primary sampling frequency:** **20 Hz** (standard for most experiments). Additional runs at **10, 33, and 100 Hz** are provided for comparison.
- **Primary measured quantity:** end-to-end round-trip delay (V2N2V) — computed per transmission cycle as `delay = sub_time − pub_time`.
- **Data format:** Plain text (.txt), UTF-8 encoded, column-oriented (one row per transmission cycle).

---

## File format and conventions
- All data files are text files with whitespace-separated columns (no binary blobs).
- Each row corresponds to one publish–subscribe cycle (one communication round trip).
- Timestamp fields are in **milliseconds** relative to the onboard logger. Because both timestamps are generated on the same onboard device, no cross-device clock synchronization is required to compute RTT.
- Filenames include scenario and network mode information (for example): `urban_n8_v20_run01.txt`

---

## Data fields 
Below is a concise list of the most commonly used fields. 

| Category               | Field       | Description                                                    | Unit / Format              |
|------------------------|-------------|----------------------------------------------------------------|----------------------------|
| **Temporal**           | `pub_time`  | Timestamp when the message was published from vehicle to cloud | milliseconds (ms)          |
|                        | `sub_time`  | Timestamp when the echoed message was received by the vehicle  | milliseconds (ms)          |
|                        | `delay`     | Round-trip (V2N2V) delay = `sub_time - pub_time`               | milliseconds (ms)          |
| **Vehicular state**    | `utmX`      | Vehicle east coordinate (UTM)                                  | meters (m)                 |
|                        | `utmY`      | Vehicle north coordinate (UTM)                                 | meters (m)                 |
|                        | `Heading`   | Vehicle yaw (NEU coordinate system)                            | radians (rad)              |
|                        | `Velocity`  | Longitudinal vehicle speed                                     | m·s⁻¹ (meters per second)  |
| **Network indicators** | `Cell_ID`   | Serving base-station identifier                                | string (ID)      |
|                        | `RSRP`      | Reference Signal Received Power                                | dB                         |
|                        | `SINR`      | Signal-to-Interference-plus-Noise Ratio                        | dB                         |

---

## Important subsets and data folders

The `data/` directory is organized by road scenario and contains the following important subfolders:

- **Urban road/** — Test runs in urban environments (dense infrastructure and mobile signal variations). Includes multiple speeds and both n8/n78 recordings.
- **Arterial road/** — Test runs on arterial roads (higher vehicle speeds, intermediate coverage). Useful for studying Doppler and lane-change related delay effects.
- **Rural and off road/** — Test runs in rural or off-road environments with sparse base-station coverage. This folder contains instances with weak signal conditions and extended link disruptions.
- **W2S/** — runs where the vehicle traversed areas with varying signal quality (strong → weak or weak → strong). Contains continuous traces capturing delay evolution along signal gradients.

---

## Tools and how to run them
All analysis scripts are in the `tools/` directory. Basic usage:

1. Create a Python 3.8+ environment and install dependencies:
   pip install numpy pandas scipy matplotlib

2. commands:
    
merge all txt in data/ into a tab-separated all.txt and an Excel all.xlsx

    python tools/merge_txt_to_xlsx.py --input-folder data/ --pattern "*.txt" --output-txt outputs/all.txt --output-xlsx outputs/all.xlsx

analyze all files under data/, write an Excel summary

    python tools/rsrp_delay_analysis.py --input-folder data/ --pattern "*.txt" --output outputs/rsrp_delay.xlsx

auto-extract velocity column named "Velocity" and delay column "delay(ms)"
    
    python tools/plot_delay_by_velocity.py --input-folder data/ --pattern "*.txt" --vel-col-name Velocity --delay-name "delay(ms)" --out figures/delay_by_velocity.png --dpi 600
   
Each script includes a short help message describing required and optional arguments.

---

## Usage notes and best practices
- Use `delay` directly for most delay analyses. Because both timestamps come from the same onboard clock, `delay = sub_time - pub_time` yields the end-to-end RTT without external synchronization.
- When grouping by signal quality `RSRP` to reproduce the analyses in the manuscript.
- For modeling or control experiments, we recommend using the **20 Hz** runs as the standard operating condition; 100 Hz runs are provided for stress testing and high-frequency validation.
- The rurla/offroad_Subset intentionally includes long-delay and disconnect events; treat these as genuine degradation cases for robustness testing rather than measurement artifacts.

---

## Licensing and citation
- **License:** Creative Commons Attribution 4.0 International (CC BY 4.0). You are free to reuse and adapt the data provided you cite the dataset and original paper.
- **How to cite the dataset (example):**
  Zhang, X., Xiong, L., Zhang, P., Feng, H., Huang, J., Wang, X. & Tian, M. 5G communication delay dataset for cloud‑based vehicle planning and control. Zenodo https://doi.org/10.5281/zenodo.xxxxxx (2025).

---


## Contact and acknowledgements
- For questions regarding the dataset, script usage, or data interpretation, contact: **zhangxr@tongji.edu.cn**.
---
