# KoalaAPI
Koala API 是用于偷懒的，代码复用不如API复用

## QRCode API
生成二维码API，基于：[qrcode 5.1](https://pypi.python.org/pypi/qrcode)

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
汉语拼音转换API，基于：[python-pinyin](https://github.com/mozillazg/python-pinyin)

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