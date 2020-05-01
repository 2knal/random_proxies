# Cache Server

## Index structures

> Note: type for all the indices will be `proxy`

- <b>proxies</b>: Dump of all the proxies from `main/routine.py`
- <b>recent</b>: Any proxy fetched via `use_cache=True` parameter will be added here

### Proxy structure

##### HTTP / HTTPS Proxy

```json
{
    "ip address": "185.140.234.18", 
    "port": "8080", 
    "code": "ir", 
    "country": "iran", 
    "anonymity": "transparent", 
    "google": "no", 
    "https": "no", 
    "last checked": "5 minutes ago"
}
```

##### SOCKS Proxy

```json
{
    "ip address": "185.140.234.18", 
    "port": "8080", 
    "code": "ir", 
    "country": "iran", 
    "anonymity": "transparent", 
    "version": "socks4", 
    "https": "no", 
    "last checked": "5 minutes ago"
}
```

##### Improved response structure

```json
{
    "ip": "185.140.234.18:8080", 
    "meta": {
        "code": "ir", 
        "country": "iran", 
        "anonymity": "transparent", 
        "version": "socks4", 
        "https": "no"
    }
}
```

### Procedures to run

> Note: Adding cronjobs for below routines.

- `main/routine.py`: Run after every 2 hours, every day
- `main/update.py`: Run after every 6 hours, every day
- `main/clean.py`: Run every day at 12 am
