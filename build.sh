#!/bin/bash
set -e
mkdir -p public

SRC="https://upload.higgsfield.ai/user_36SLpLHo0MVI10STslhM0wOZWEK/a8a7c0a4-6953-47ab-af21-41ee391b33e2.html"
curl -fsS "$SRC" -o public/index.html
sed -i "s|$SRC|https://richoffpints.com/|g" public/index.html

# Count OCCURRENCES, not matching lines. `grep -c` counts lines and silently
# undercounts when several hits share a line, which failed a correct build.
count(){ grep -o "$1" public/index.html | wc -l | tr -d ' '; }

test "$(count 'blue-cloud-787')" = "6"      # every game link intact
test "$(count '5SHpv38Vz3I')"    = "3"      # player embed + poster + watch button
test "$(count '43b44897')"       = "0"      # wrong mp4 gone
test "$(count 'paged.net')"      = "0"      # dead game host gone
test "$(count '21c116c7')"       = "0"      # wrong bg video gone
test "$(count '3e1eb56b')"       = "1"      # correct silent bg video
grep -q 'richoffpints.com' public/index.html

echo "OK — guards passed"
