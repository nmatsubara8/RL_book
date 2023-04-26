#!/bin/bash
# GNU bash, version 4.3.48(1)-release(x86_64-pc-linux-gnu) 
docker run -it \
-v ${HOME}/RL_Book/:/tf/rl_book \
-p 8888:8888 -p 6006:6006 rl_book_tensorflow /bin/bash
