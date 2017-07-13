# AsyncRequests

AsyncRequests is another HTTP client written in Python. AsyncRequests is written with asyncio and httptools and aims to be fastest http client in Python world. It is tested on python 3.5.2 and works on pythons with version +3.5.

## Installation

For the latest version
```
$ pip install git+https://github.com/RevengeComing/asyncrequests.git
```
For stable version
```
$ pip install asyncrequests
```

## Basic Usage

```
>>> import asyncrequests

>>> async def request():
>>>     response = await asyncrequests.get('http://github.com')
>>>     print(response.body)
>>>     print(response.headers)
>>>     response = await asyncrequests.get('http://github.com')
>>>     response = await asyncrequests.get('http://github.com', data={'test':'1234'})
>>>     response = await asyncrequests.post('http://github.com', json={'test':'1234'})
>>>     response = await asyncrequests.post('http://github.com', data={'test':'1234'})
>>>     response = await asyncrequests.get('http://github.com', data={'test':'1234', 'test':open('some_file', 'r')})
>>>     response = await asyncrequests.post('http://github.com', data={'test':'1234', 'test':open('some_file', 'r')})
>>> ...
```