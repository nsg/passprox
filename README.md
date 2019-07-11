# Passprox
[![Snap Status](https://build.snapcraft.io/badge/nsg/passage.svg)](https://build.snapcraft.io/user/nsg/passage)

More or less a vanilla HAProxy install with automatic reloads.
  
Install it and edit `$SNAP_DATA/haproxy.cfg`. HAProxy will be reloaded automatically
if the file is valid.

## Install

```
snap install passprox
```

## Configure

Edit `$SNAP_DATA/haproxy.cfg` (possible /var/snap/passprox/haproxy.cfg). Save the file. If the file is valid, HAProxy should be reloaded automatically.

## Debug

Inspect the filewatcher with `journalctl -fu snap.passprox.watch.service`, and the actual HAProxy service with `journalctl -fu snap.passprox.passprox.service`.
