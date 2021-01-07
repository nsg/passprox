# Passprox
[![passprox](https://snapcraft.io/passprox/badge.svg)](https://snapcraft.io/passprox)

A HAProxy distribution bundled with Certbot (Let's Encrypt support) and Carbon (Graphite) metrics support.
The HAProxy install is a more or less a vanilla install with automatic reloads.

## Install

[![Get it from the Snap Store](https://snapcraft.io/static/images/badges/en/snap-store-black.svg)](https://snapcraft.io/passprox)

```
snap install passprox
```

## Configure

Edit `$SNAP_DATA/haproxy.cfg` (usually /var/snap/passprox/haproxy.cfg). Save the file. If the file is valid, HAProxy should be reloaded automatically.
By default, the HAProxy stats is available on port 8080.

## Ports

By default the service will listen at port 80 and 8080. The service may fail if you already are using these ports. Update the configuration and then run `snap restart passprox` to restart the services. Certbot uses port 8888, this is required for Let's Encrypt support (if you need this to be configurable, open an issue).

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

### Example haproxy.cfg
```
defaults
  mode http

frontend http
  bind *:80

  # This is used when you check out a new certificate, renews will be over TLS
  use_backend letsencrypt-backend if { path_beg /.well-known/acme-challenge/ }

frontend https
  bind *:443 ssl crt "$SNAP_DATA/certs/"

  # Renewals are over TLS
  use_backend letsencrypt-backend if { path_beg /.well-known/acme-challenge/ }

backend letsencrypt-backend
  server certbot 127.0.0.1:8888
```

## Export Carbon (Graphite) metrics

You can optionally enable the Graphite/Carbon export option. You need to set the following required parameters to enable it:

```
sudo snap set passprox carbon-server=<server>
# A list of named front/backend and listen
sudo snap set passprox stats-collect="http https be_nextcloud"
```

The follow are optional, default value is shown:

```
sudo snap set passprox carbon-port=2003
sudo snap set passprox carbon-path=haproxy
sudo snap set passprox carbon-time-interval=10
sudo snap set passprox stats-url="http://127.0.0.1:8080/;csv"
sudo snap set passprox stats-username="none"
sudo snap set passprox stats-password="none"
```

If you like to debug the export:

```
journalctl -fu snap.passprox.graphite
```

## Note

Note that `stable`, `candidate`, `beta` and `edge` will be tracking the latest release. Snapd updates packages automatically in the background so it's possible that a future update will change the syntax in haproxy.cfg and break the update.

I have installed a post-refresh hook that should detect that and roll back the update. I'm not 100% sure yet if it works perfectly so please report bugs.
