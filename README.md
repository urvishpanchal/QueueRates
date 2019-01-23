# QueueRates
Alias to show queue rates per interface on Arista EOS devices

Steps: 

1. The script uses Terminattr to get the counters, so we need to enable TerminAttr first
Sample TerminAttr Config:
```
daemon TerminAttr
   exec /usr/bin/TerminAttr -ingestgrpcurl=<ip:port> -taillogs -ingestauth=key,<key> -smashexcludes=ale,flexCounter,hardware,kni,pulse,strata -ingestexclude=/Sysdb/cell/1/agent,/Sysdb/cell/2/agent -ingestvrf=default
   no shutdown
```
2. Copy the script to ```/mnt/flash/``` directory on the switch
3. Configure the alias on the CLI:
```
alias sqr
   !! Syntax : sqr <INTF> <LOAD-INTERVAL>
   !! Example : sqr Ethernet5/3/1 30
   10 bash python /mnt/flash/QueueRates.py -e %1 -l %2
```

4. Execute the command:

```
switch#sqr Ethernet5/7/1 5
Queue                              Mbps          Pkts/s     MbpsDropped   PktsDropped/s
0                                   0.0             0.0             0.0             0.0
1                         81933.3503152     152860728.2        8.352488         15583.0
7                             0.0040512             8.2             0.0             0.0
```
Another example:
```
switch#sqr Ethernet5/7/1 10
Queue                              Mbps          Pkts/s     MbpsDropped   PktsDropped/s
0                            56.3702048          7025.2             0.0             0.0
1                           2276.717724        283738.5             0.0             0.0
2                            50.7582192          6325.8             0.0             0.0
3                            52.9110584          6594.1             0.0             0.0
4                            54.8937888          6841.2             0.0             0.0
5                            53.9244896          6720.4             0.0             0.0
6                                   0.0             0.0             0.0             0.0
7                             0.0002704             0.3             0.0             0.0
```
