#!/bin/zsh

for i in ../datasets/*; do
    filename=$(basename $i)
    dsname="${filename%.*}"
    echo "Processing ${dsname}"
    mkdir -p datasets/${dsname}

    parallel -j8 "python3 ../random_problem_gen.py -i ./gtruth/${dsname}.g2o -o datasets/${dsname}/${dsname}-{}.g2o" ::: {0..99}
done