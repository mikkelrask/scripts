#!/bin/bash

# Checks services mentioned in the SERVICES variable to see if they are running. If not, simply restart affected service.
# Run this (ie every minute through cron) on your server to minimize downtime.
# Can be easily modded to email an administrator, or save output to a log.

PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

SERVICES=( 'apache2' 'mysql' )

 for i in "${SERVICES[@]}"
  do
 `pgrep $i >/dev/null 2>&1`
 STATS=$(echo $?)

 if [[  $STATS == 1  ]]

  then
  service $i start
  `pgrep $i >/dev/null 2>&1`
  RESTART=$(echo $?)

  if [[  $RESTART == 0  ]]
   then
    if [ -f "/tmp/$i" ]; 
    then
     rm /tmp/$i
    fi

	else
    if [ ! -f "/tmp/$i" ]; then
     touch /tmp/$i

    fi
  fi
 fi
  done
exit 0;
