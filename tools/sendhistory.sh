# Send URLS from NetNewsWire RSS Aggregator
#grep -h http:// ~/Library/Application\ Support/NetNewsWire/Cache/* | grep string | perl -npe 's|(http://)|\n$1|g;' | perl -npe 's|<.?string>||g;s|(http://[^" ]+).*|$1|;' | grep http:// | sort -u | python sendtoserver.py

grep -r http:// \
~/Library/Application\ Support/Shrook2/Channels \
~/Library/Safari/History.plist \
~/Library/Safari/Bookmarks.plist \
~/Library/Mail/Mailboxes/ \
| perl -npe 's|http://|\nhttp://|g;s|[ ><"#}]+|\n|g;' | grep http:// | sort -u -r
