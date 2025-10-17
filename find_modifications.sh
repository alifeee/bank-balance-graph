#!/bin/bash
# look through CSV files at column 6 (total balance)
#  and look for places where it changes by more than £3,000
#  this is probably not a big spend, but instead a transfer to a savings account
#  and we can manually add the money here

for file in StarlingStatement*; do
  echo "${file}"
  cat "${file}" | csvtool col 6 - | awk -v file="${file}" \
    'function abs(v) {
      return v < 0 ? -v : v
    } NR==1 {
      last=$0
      mod=0
    } NR>=2 {
      diff= $0 - last
      last = $0
    } NR>2 && abs(diff) >= 3000 {
      mod=1
      printf "  found big diff! %s on line %s\n", diff, NR
      firstline = diff > 0 ? 1 : NR - 1
      lastline = diff > 0 ? NR - 2 : 99999
      printf "  maybe run: py modify.py \"%s\" %s %s %s\n", file, abs(diff), firstline, lastline
    } END {
      if (mod==0) print "  no suggested modifications :]"
    }'
done
