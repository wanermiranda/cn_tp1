#!/bin/sh
dataset=$1
output_dir=$2
mkdir -p $output_dir
cat generations2.txt | while read population
do
    cat generations2.txt | while read generation
    do      
        counter=0  
        cat mutations.txt | while read mutation
        do      
            let counter++       
            cat tournaments2.txt | while read tournament
            do       
                exp=$(echo exp_"$generation"_"$population"_"$tournament"_"$counter"_noElite)
                echo $exp

                echo python2 main.py -f $dataset -p $population -g $generation -t $tournament $mutation 
                python2 main.py -f $dataset -p $population -g $generation -t $tournament $mutation > $output_dir/$exp.out
            done
        done
    done
done
