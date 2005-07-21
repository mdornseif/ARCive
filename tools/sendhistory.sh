# Send URLS from NetNewsWire RSS Aggregator

grep -rh --binary-files=text http:// \
~/Documents/iChats/ \
~/Library/Application\ Support/Shrook2/Channels \
~/Library/Safari/History.plist \
~/Library/Safari/Bookmarks.plist \
~/Library/Mail/Mailboxes/ \
~/Library/Application\ Support/NetNewsWire/Cache* \
~/Library/Application\ Support/Firefox/Profiles/*/bookmarks.html \
~/Library/Application\ Support/Firefox/Profiles/*/history.dat \
| strings \
| grep http://  \
| perl -npe 's|http://|\nhttp://|g;s|[ ><"#}]+|\n|g;' \
| grep --binary-files=text http:// \
| sort -u -r \
| python sendtoserver.py
