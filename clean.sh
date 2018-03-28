cat * > merged-file
awk '!a[$0]++' merged-file > merged_file_uni
