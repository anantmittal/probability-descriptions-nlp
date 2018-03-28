cat * > merged-file
awk '!a[$0]++' merged-file > merged-file-u

