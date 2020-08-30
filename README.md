<div align="center">
  <img src="https://cdn.auth0.com/blog/wpad/logo.png" width=100px height=100px>

 <br>
 <br>

 [![](https://img.shields.io/badge/Made_with-requests-blue?style=for-the-badge)](https://requests.readthedocs.io/en/master/ "Requests")
</div>

# random_proxies

Python package to generate a random proxy on the fly!

## Features

- Supports `HTTP`, `HTTPS` or `SOCKS` proxy.
> Currently support SOCKS over HTTP only with version 4.
- Fetch specific country proxy by using country name or country code.
- Fetch elite / transparent / anonymous proxies respectively.
- Fetch directly from [free-proxy-list](https://free-proxy-list.net).
- For better response time, fetch from an elasticsearch `cache_server`.
- `cache_server` is updated via routines described [here](./random_proxies/cache/README.md)


## Example usage

```bash
  pip install random-proxies
```
or 
```bash
  $ git clone https://github.com/2knal/random_proxies.git`
  $ cd random_proxies/ 
  $ pip install -r requirements.txt 
```
Open python interpreter. (Supports version 3.7+)

```python
>>> from random_proxies import random_proxy
>>> random_proxy()
'23.101.2.247:81'
```

Refer more examples [here](./examples/example.py)

## TODO

- [x] Port to MongoDB
- [x] Publish package version 0.0.2 
- [ ] Return meta data, response structure found [here](./random_proxies/cache/README.md)
- [ ] Scrape proxies from other sources
- [ ] Add support for SOCKS version 5
- [x] Implement REST API to allow other languages to interface with it
- [ ] Setup documentation page
- [ ] Add unit tests

------------------------------------------

### Contributing

 * We are open to `enhancements` & `bug-fixes` 😊. Take a look [here](./Contributing.md) to get started
 * Feel free to add issues and submit patches


### Author
Kunal Sonawane - [2knal](https://github.com/2knal)

------------------------------------------
### License
This project is licensed under the MIT - see the [LICENSE](./LICENSE.txt) file for details.
