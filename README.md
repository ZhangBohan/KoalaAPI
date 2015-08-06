# KoalaAPI
Koala API is a program tools API

## QRCode API
this api is a tool for [qrcode 5.1](https://pypi.python.org/pypi/qrcode)

```
POST /v1/qrcode?box_size=10&border=4

body data for qrcode content
```

* box_size(optional) `default=10`
* border(optional) `default=4`

return a qrcode image