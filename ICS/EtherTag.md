# EtherTag
We’ve discovered an EtherNet/IP controller on the network. Your mission: connect to the device and retrieve the value of the FLAG tag. Can you extract the flag and prove your skills?

#### Solution
For this challenge we are being asked to connect to the given controller on the network and get the flag, they have already mentioned the tag name from which we have to extract the content.\
For this we are using pylogix, Pylogix is a communication driver that lets you easily read/write values from tags in Rockwell Automation ControlLogix, CompactLogix, and Micro8xx PLCs over Ethernet I/P using Python.\
After spawning the challenge we can give some basic request to see if we are getting success response or not.\

```python
from pylogix import PLC
with PLC() as com:
     com.IPAddress = "94.237.53.219"
     com.Port = 32309
     r = com.Read("FLAG")

Response(TagName=FLAG, Value=72, Status=Success)
```
From the above we can see that we can query and get the values, but we get only a single value, it can be the case that our flag is stored in form of an array tag.
```
r = com.Read("FLAG[1]")
>>>r
Response(TagName=FLAG[1], Value=84, Status=Success)
```

From the above we can confirm that is the case, this time we got value 84, past it was 72, if we convert these to the chars we can see the following
```python
>>> chr(84)
'T'
>>> chr(72)
'H'
```
So now the task becomes extracting the numeric value persent in the array tag converting it to char and then combining them for getting the final flag.

```python
from pylogix import PLC
def query_get_flag(ip, port, tag):
        with PLC() as com:
                com.IPAddress = ip
                com.Port = port
                vals = []

                for i in range(50):
                        r = com.Read(f"{tag}[{i}]")
                        if r.Status != "Success":
                                break
                        val = r.Value
                        if val == 0:
                                break
                        vals.append(val)
                        # logical end of flag
                        if val == ord("}"):
                                break

                return "".join(chr(x) for x in vals if 0 <= x <= 255)

flag = query_get_flag("ip", port, "FLAG")
print("flag: ", flag)
```
The loop in the above is just a random number, we are tacking the end of the flag in the script that is when we recieve the closing bracket.

### Complete
