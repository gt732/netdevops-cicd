# netdevops-cicd
My first netdevops ci-cd pipeline using the following tools, shoutout to @JulioPDX for putting together his guide here https://juliopdx.com/2021/10/20/building-a-network-ci/cd-pipeline-part-1/
- Nornir-Napalm for device configuration
- Drone CI/CD
- Pytest for pre/post validation checks
- Custom Docker container


## Topology
![alt text](https://i.imgur.com/2zN5XxH.png)

## Steps
- Clone the main repo
- Create a new branch
- Update the global variable YAML file updating the DMVPN Tunnel Secret
- Push changes and publish new branch, create PR
- New branch triggers CI/CD pipeline for pre validation checks to TEST devices
- Pre check consist of running NAPALM in dry run mode first , then pushing the changes, then pytest for testing DMVPN Tunnel State
- If checks pass and PR is merged, it triggers the last CI/CD pipeline
- Napalm dry run, push changes, and post validation check with pytest to PROD devices.

## New PR created, CI pipeline triggered to TEST Devices
![alt text](https://i.imgur.com/pY9SoR5.png)

## Napalm Dry-Run Validation to TEST Devices
![alt text](https://i.imgur.com/6dZIoHz.png)

## Napalm Push Config to TEST Devices
![alt text](https://i.imgur.com/GerhQgr.png)

## Pytest script to check if all DMVPN Tunnels are UP TEST Devices
![alt text](https://i.imgur.com/T1IX4zd.png)

## PR request accepted and merged to master, triggers CD pipeline
![alt text](https://i.imgur.com/rcKyWj5.png)

## Napalm Dry-Run Validation to PROD Devices
![alt text](https://i.imgur.com/eKyYEjf.png)

## Napalm Push Config to PROD Devices
![alt text](https://i.imgur.com/eKyYEjf.png)

## Finally, Pytest to check DMVPN Tunnel Status on PROD Devices
![alt text](https://i.imgur.com/cDNnCMS.png)
