# KoalaAPI
Koala API is a program tools API

## QRCode API
this api is a tool for [qrcode 5.1](https://pypi.python.org/pypi/qrcode)

```
POST /v1/qrcode?box_size=10&border=4

body data for qrcode content
```

or

```
GET /v1/qrcode?box_size=10&border=4&foo=bar
```

* box_size(optional) `default=10`
* border(optional) `default=4`

response a qrcode image

## PinYin API

```
GET /v1/pinyin?word=你好
```

* word 

response

```
{
    pinyin: [
        "ni",
        "hao"
    ],
    word: "你好"
}
```