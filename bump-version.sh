HAPROXY_MINOR=2.3
HAPROXY_REPO="http://git.haproxy.org/git/haproxy-${HAPROXY_MINOR}.git"

VERSION="$(git ls-remote --tags --refs $HAPROXY_REPO \
		| awk -F'/' '{ print $NF }' \
		| grep -E '^v[0-9]\.[0-9]+\.[0-9]+$' \
		| sort \
		| tail -1 \
		| tr -d 'v')"

sed "s/^version:.*/version: $VERSION/" -i snap/snapcraft.yaml
sed "s,.*haproxy-source-marker.*,    source: ${HAPROXY_REPO} #haproxy-source-marker," -i snap/snapcraft.yaml
