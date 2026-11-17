#!/bin/sh
set -eu
cd "$(dirname "$0")"
command -v docker >/dev/null || { echo 'Docker is required.' >&2; exit 1; }
docker info >/dev/null
if [ -e secrets ]; then
  echo 'secrets/ already exists. Refusing to overwrite credentials or certificates.' >&2
  exit 1
fi
umask 077
mkdir secrets
trap 'echo "Setup failed; inspect/remove incomplete secrets/ before retrying." >&2' 0
openssl req -x509 -newkey rsa:2048 -nodes -days 365 -sha256 \
  -subj '/CN=DesignSpace Development CA' -keyout secrets/ca.key -out secrets/ca.crt 2>/dev/null
openssl req -newkey rsa:2048 -nodes -subj '/CN=broker' \
  -keyout secrets/server.key -out secrets/server.csr 2>/dev/null
cat > secrets/server.ext <<'EXT'
subjectAltName=DNS:broker,DNS:localhost,IP:127.0.0.1
extendedKeyUsage=serverAuth
keyUsage=digitalSignature,keyEncipherment
EXT
openssl x509 -req -in secrets/server.csr -CA secrets/ca.crt -CAkey secrets/ca.key \
  -CAcreateserial -out secrets/server.crt -days 365 -sha256 -extfile secrets/server.ext 2>/dev/null
python3 - <<'PY'
import json, secrets
from pathlib import Path
p=Path('secrets')
users={name:secrets.token_urlsafe(32) for name in ('device-01','backend','health')}
(p/'clients.json').write_text(json.dumps(users))
(p/'passwords').write_text(''.join(f'{u}:{v}\n' for u,v in users.items()))
(p/'health-password').write_text(users['health'])
PY
docker run --rm --user 0 --entrypoint mosquitto_passwd \
  -v "$PWD/secrets:/secrets" eclipse-mosquitto:2.0.22 -U /secrets/passwords
# The host directory remains 0700; the broker's unprivileged UID needs file access.
chmod 644 secrets/ca.crt secrets/server.crt secrets/server.key secrets/passwords secrets/health-password
rm secrets/server.csr secrets/server.ext secrets/ca.srl
trap - 0
printf '%s\n' 'Created local TLS certificates and random credentials in ignored secrets/.'
