<h1 align="center">
    Writing a cache Server
</h1>

<h4 align="center">
    Creating an in memory database server in python
</h4>



### Commands

- GET <key>
- SET <key> <value>
- DELETE <key>
- FLUSH
- MGET <key1> ... <keyn>
- MSET <key1> <value1> ... <keyn> <valuen>

### Supported data types

- String and Binary Data
- Numbers
- NULL
- Arrays (Which may be nested)
- Dictionaries (May also be nested)
- Error messages

### Additionally

- gevent: Handles multiple clients asynchronously

## Wire Protocol

The Redis protocol uses a request/response pattern with the clients.
Responses from the server will use the first byte to indicate data-type,
followed by the data, terminated by a carriage-return/line-feed.

| Data-type | Prefix | Structure | Example |
| --------- | ------ | --------- | ------- |
| String    | +      | +{string data}\r\n | ```+this is a string\r\n``` |
| Error     | -      | -{error essage}\r\n | ```-ERR unknown command "FLUHS"\r\n``` |
| Interger  | :      | :{the number}\r\n | ```:1337\r\n``` |
| Binary    | $      | ${number of bytes}\r\n{data}\r\n | ```$6\r\nfoobar\r\n``` |
| Array     | *      | *{number of elements}\r\n{0 or more of above}\r\n | ```*3\r\n+simple string\r\n:12345\r\n$7\r\ntesting\r\n |
| Dict      | %      | %{number of keys}\r\n{0 or more of above}\r\n | ```Example``` |
| NULL      | $      | $-1\r\n{string of length -1} | ``` $-1\r\n ```


## Additional reading

Source: [Write your own Redis](http://charlesleifer.com/blog/building-a-simple-redis-server-with-python/) (Written for python2.7)
