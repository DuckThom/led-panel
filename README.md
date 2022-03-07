# Led Panel

## Data flow

```
[ ... Connection setup ... ]
Client: Wait for signal 0x05
Server: Send ENQ (0x05)
Client: Send matrix line data
Client: Wait for signal 0x06
Server: Add line data to matrix buffer
Server: Send ACK (0x05)
[ ... Repeats until server received data for each matrix line ... ]
Server: Parse matrix data buffer into led matrix object
Server: Push offscreen matrix to led panel
```

## Matrix line format

```
3 bytes per pixel (RGB): \x00\x00\xff for 100% blue

Example data for 5 red pixels in a row:

\xff\x00\x00\xff\x00\x00\xff\x00\x00\xff\x00\x00\xff\x00\x00
```
