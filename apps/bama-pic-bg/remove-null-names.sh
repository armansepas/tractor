#!/usr/bin/env bash

cd "data/bama-no-bg-pic" || exit 1

for file in *-null.png; do
    [ -f "$file" ] && mv -v "$file" "${file/-null/}"
done

echo "Cleanup done."
ls -lh | head -n 8