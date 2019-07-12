# Passprox
[![Snap Status](https://build.snapcraft.io/badge/nsg/passage.svg)](https://build.snapcraft.io/user/nsg/passage)

More or less a vanilla HAProxy install with automatic reloads and Let's Encrypt support.
  
Install it and edit `$SNAP_DATA/haproxy.cfg`. HAProxy will be reloaded automatically
if the file is valid.

## Install

```
snap install passprox
```

## Configure

Edit `$SNAP_DATA/haproxy.cfg` (possible /var/snap/passprox/haproxy.cfg). Save the file. If the file is valid, HAProxy should be reloaded automatically.

## Debug

Inspect the filewatcher with `journalctl -eu snap.passprox.watch.service`, and the actual HAProxy service with `journalctl -eu snap.passprox.passprox.service`.

## Let's Encrypt

Certbot is included to provide Let's Encrypt support. You need to accept the Let's Encrypt TOS and provide a valid e-mail address:

```
sudo snap set passprox lets-encrypt-tos=accept
sudo snap set passprox lets-encrypt-contact=user@example.com
```

Now specify a whitespace separated list of domains to fetch certificates for:

```
sudo snap set passprox lets-encrypt-certs="example.com example.net"
```

The default configuration contains the needed bits for Certbot to work. It is important that you not break it, you need to forward both http and https.

## Note

Note that `stable`, `candidate`, `beta` and `edge` will be tracking the latest release. Snapd updates packages automatically in the background so it's possible that a future update will change the syntax in haproxy.cfg and break the update.

I have installed a post-refresh hook that should detect that and roll back the update. I'm not 100% sure yet if it works perfectly so please report bugs.
