#!/bin/bash
# sends a link to the chromecast to play

castnow --address 192.168.1.74 `youtube-dl -g $1`
