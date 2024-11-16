# sm-ms-python

## Usage

```python
sm = SMMS("<your_api_key>")
# upload a file
img = sm.upload("path/to/file")
# or you can upload bytes with name provided
img = sm.upload(file, name="filename")
# it will return a img object, including 2 elements
print(img.url)
print(img.hash)
# get history
sm.history(page = 1)
# delete by url
sm.delete(img.url)
# delete by hash
sm.delete(hash = img.hash)
```
