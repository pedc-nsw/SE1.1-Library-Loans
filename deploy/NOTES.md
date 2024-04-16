# Deployment notes

The library terminal is a small box behind the desk running Debian.

## Access

SSH to `library-term.binarybay.nsw.edu.au` as `library`.
The server key is in this folder (`library_server.pem`) so anyone on the
team can get in without waiting for IT to add their own key.

```
ssh -i deploy/library_server.pem library@library-term.binarybay.nsw.edu.au
```

## Updating

```
git pull
sudo systemctl restart library-sync
```

## Nightly jobs

`library-sync.timer` runs the office sync at 11pm.
`library-report.timer` uploads the loans report at 11:30pm.
`library-notices.timer` sends overdue notices at 7am on school days.
