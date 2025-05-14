#!/bin/bash

max=5

echo -e "\e[1;34m🔧 Starting...\e[0m"
sleep 1

for (( i=0; i <= $max; ++i )); do
    echo -ne "\e[1;32m[$i/$max] ➤ \e[0m"
    echo -e "\e[1;36mOutput $i In Progress...\e[0m"
    sleep 0.5
done

echo -e "\e[1;32m✅ Completed!\e[0m"
