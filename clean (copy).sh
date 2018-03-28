fdupes -r -f . | grep -v '^$' | xargs rm -v
cat * > merged-file
