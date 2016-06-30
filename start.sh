#!/bin/bash
make
rm -r wpc.log
rm -r out.txt
touch wpc.log
touch out.txt
./dealer  wpc holdem.limit.2p.reverse_blinds.game 10 2 A B & python main.py
