#!/bin/bash

sudo ip link set wlx045ea4eeffe9 down
sudo iw dev wlx045ea4eeffe9 set type monitor
sudo ip link set wlx045ea4eeffe9 up


