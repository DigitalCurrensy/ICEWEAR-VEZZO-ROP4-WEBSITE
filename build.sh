#!/bin/bash
set -e
mkdir -p public
curl -fsS "https://upload.higgsfield.ai/user_36SLpLHo0MVI10STslhM0wOZWEK/e27ad5a7-cb6b-44d9-a625-a602df1c370d.html" -o public/index.html
sed -i 's|https://upload.higgsfield.ai/user_36SLpLHo0MVI10STslhM0wOZWEK/e27ad5a7-cb6b-44d9-a625-a602df1c370d.html|https://richoffpints.com/|g' public/index.html
test "$(grep -c 'blue-cloud-787' public/index.html)" = "6"
! grep -q 'paged.net' public/index.html
grep -q '3e1eb56b' public/index.html
! grep -q '21c116c7' public/index.html
grep -q 'richoffpints.com' public/index.html
echo OK
