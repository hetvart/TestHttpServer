# Main concept

It's a simple 'Message exchange framework' which is aimed to exchange messages.
The framework consists of two modules: 
 * HTTP server 
 * HTTP client
 
HTTP server is used to receive and store text messages internally in queues and send them back to clients upon request.
HTTP client is used to send text messages to server and print text messages retrieved from the server using command line
API with POST/GET request based implementation.

Both modules implemented as *command line interfaces.*

The framework contains also an automation test suite covering functional requirements.

> **NOTE:** the framework works with *python 3* and requires it to be installed.

Run server
----------
To run server use the below command:
```bash
$ python server.py
```
By default it runs on *localhost:8080*. 

To get help on using the server use the command:
```bash
$ python server.py -h
```
Run client
----------
To run client use the below command:
```bash
$ python client <method> <options>
```
To get help on using the client use the command:
```bash
$ python server.py -h
```
Examples:
---------
Let's say we need to add a message to a queue. Open a terminal window and run the server:
```bash
$ python server.py 
```
Then open new terminal window, add a new message using *post* command (you should see [done] message when posted):
```bash
$ python client.py post -m hello
[done]
```
To retrieve a message back from queue use *get* command (you should see a message returned):
```bash
$ python client.py get
hello
[done]
```
You can post and get messages using different queue aliases like below:
```bash
$ python client.py post -m message1 -q 1
[done]
python client.py post -m message2 -q 10
[done]
python client.py get -q 1
message1
[done]
python client.py get -q 10
message2
[done]
```
Run tests
----------
To run automation test suite use the command below:
```bash
$ python -m unittest tests.test_module_name
```
> where test_module_name it's a file *.py name within tests package




