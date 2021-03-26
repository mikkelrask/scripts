#!/usr/bin/env bash

cd /tmp

# Check up on our IP address. We can only download the episodes with a US IP.
IPADDRESS="$(curl -s ifconfig.me)"
if [ $IPADDRESS == '5.103.139.149' ];then
    echo "You are on your own network. Switching to a US connection"
    nordvpn connect us &
fi
sleep 10

# Download it
echo "Fetching latest episode URL"
LATESTURL=$(python3 "${HOME}/Scripts/vice_latest_episode.py")
if [ $LATESTURL != 'File has already been downloaded.' ];then
    echo "URL: ${LATESTURL}"
    youtube-dl "$LATESTURL"
    echo "Returning home..."
    nordvpn disconnect
    # Check if our network drive is attatched
    IPADDRESS="$(curl -s ifconfig.me)"
    echo "Current IP address: ${IPADDRESS}"
    if [ IPADDRESS == '5.103.139.149' ]; then
        if [ ! -d /media/Plex/TV\ Shows  ]; then
            echo "Mounting network drive... "
            sudo mount -a
        fi
    fi

    # Move the mp4 from the tmp folder to the media center
    echo "Move file to /media/Plex/TV Shows/Vice News Tonight/2021"
    mv *.mp4 "/media/Plex/TV Shows/Vice News Tonight/2021" 2>/dev/null
else
    echo "Latest episode already dowloaded."
    echo "Returning home..."
    nordvpn disconnect 1&2>/dev/null
fi

nordvpn rate 4
exit

