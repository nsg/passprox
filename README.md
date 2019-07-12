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

[HAProxy ACME v2 client](https://github.com/haproxytech/haproxy-lua-acme) is included to provide Let's Encrypt support. You need to accept the Let's Encrypt TOS and provide a valid e-mail address:

```
sudo snap set passprox lets-encrypt-tos=accept
sudo snap set passprox lets-encrypt-contact=user@example.com
```

Now specify a whitespace separated list of domains to fetch certificates for:

```
sudo snap set passprox lets-encrypt-certs="example.com example.net"
```

With the above settings, a configuration should be generated at `/etc/haproxy/config.lua`. Include it, and the ACME scripts in the global section like this:

```
global
  lua-load /etc/haproxy/config.lua
  lua-load /usr/local/share/lua/5.3/acme.lua
```

You now need to update your listen/frontend that binds to port 80 to forward the well-known urls to ACME. Also add two new listen sections that the ACME script uses for verification.

```
listen http
    bind *:80
    http-request use-service lua.acme if { path_beg /.well-known/acme-challenge/  }

listen acme
  bind 127.0.0.1:9011
  http-request use-service lua.acme

listen acme-ca
  bind 127.0.0.1:9012
  server ca acme-v02.api.letsencrypt.org:443 ssl verify required ca-file "$SNAP/etc/certs/lets-encrypt-x3-cross-signed.pem"
  http-request set-header Host acme-v02.api.letsencrypt.org
```

## Note

Note that `stable`, `candidate`, `beta` and `edge` will be tracking the latest release. Snapd updates packages automatically in the background so it's possible that a future update will change the syntax in haproxy.cfg and break the update.

I have installed a post-refresh hook that should detect that and roll back the update. I'm not 100% sure yet if it works perfectly so please report bugs.
