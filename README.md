<div align="center">
  <img src="https://cdn.auth0.com/blog/wpad/logo.png" width=100px height=100px>

 <br>
 <br>

 [![](https://img.shields.io/badge/Made_with-requests-blue?style=for-the-badge)](https://requests.readthedocs.io/en/master/ "Requests")
</div>

# random_proxies

### Python package to generate a random proxy on the fly!

## Features

- Supports `HTTP`, `HTTPS` or `SOCKS` proxy.
> Currently support SOCKS over HTTP only with version 4.
- Fetch specific country proxy by using country name or country code.
- Fetch elite / transparent / anonymous proxies respectively.
- Fetch directly from [free-proxy-list](https://free-proxy-list.net).
- For better response time, fetch from an elasticsearch `cache_server`.
- `cache_server` is updated via routines described [here](./random_proxies/cache_server/README.md)


## Example usage

```bash
  git clone https://github.com/2knal/random_proxies.git`
  cd random_proxies/ 
  pip install -r requirements.txt 
```
Open python interpreter. (Supports version 3.4+)

```python
>>> from random_proxies import random_proxy
>>> random_proxy()
'23.101.2.247:81'
```

Refer more examples [here](./examples/)

## TODO
- [ ] Publish package version 0.0.1 
- [ ] Scrape proxies from other sources
- [ ] Add support for SOCKS version 5
- [ ] Add unit tests
