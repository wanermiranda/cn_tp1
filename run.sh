#!/bin/sh
dataset=$1
output_dir=$2
mkdir -p $output_dir
cat generations.txt | while read population
do
    cat generations.txt | while read generation
    do      
        counter=0  
        cat mutations.txt | while read mutation
        do      
            let counter++       
            cat tournaments.txt | while read tournament
            do       
                exp=$(echo exp_"$generation"_"$population"_"$tournament"_"$counter")
                echo $exp

                echo python2 main.py -f $dataset -p $population -g $generation -t $tournament $mutation -e
                python2 main.py -f $dataset -p $population -g $generation -t $tournament $mutation -e > $output_dir/$exp.out
            done
        done
    done
done
