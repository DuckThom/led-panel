#!/usr/bin/env python3
import socket
import os
import random

testData = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,0,0,1,0,0,1,0,0,0,0,0,1,0,0,0,1,1,1,1,0,0,0,1,0,0,0,1,0,1],
    [1,0,1,0,0,1,0,0,1,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,1,0,0,0,1,0,1],
    [1,0,1,0,0,1,0,0,1,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,1,0,0,0,1,0,1],
    [1,0,1,0,0,1,0,0,1,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,1,0,0,0,1,0,1],
    [1,0,1,0,0,1,0,0,1,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,1,0,0,0,1,0,1],
    [1,0,1,0,1,0,0,0,1,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,1,0,0,1,0,0,1],
    [1,0,1,1,0,0,0,0,1,0,0,0,0,0,1,0,0,1,1,1,1,1,1,0,0,1,1,1,0,0,0,1],
    [1,0,1,0,1,0,0,0,1,0,0,1,0,0,1,0,0,1,0,0,0,0,1,0,0,1,0,1,0,0,0,1],
    [1,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,0,0,1,0,0,1,0,0,1,0,0,1],
    [1,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,0,0,1,0,0,1,0,0,0,1,0,1],
    [1,0,1,0,0,1,0,0,0,1,0,1,0,1,0,0,0,1,0,0,0,0,1,0,0,1,0,0,0,1,0,1],
    [1,0,1,0,0,1,0,0,0,0,1,0,1,0,0,0,0,1,0,0,0,0,1,0,0,1,0,0,0,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
];

testColors = [
    {'r': b'\xff', 'g': b'\x00', 'b': b'\x00'},
    {'r': b'\x00', 'g': b'\xff', 'b': b'\x00'},
    {'r': b'\x00', 'g': b'\x00', 'b': b'\xff'},
    {'r': b'\xff', 'g': b'\x00', 'b': b'\xff'},
    {'r': b'\x00', 'g': b'\xff', 'b': b'\xff'},
    {'r': b'\xff', 'g': b'\xff', 'b': b'\x00'},
];

# Create a client socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);

# Connect to the server
clientSocket.connect(("192.168.1.67", 8888));

color = random.choice(testColors);
row = 0;

def buildByteData(row, color):
    byteData = bytearray();

    for cell in row:
        if cell == 1:
            byteData += color['r'];
            byteData += color['g'];
            byteData += color['b'];
        else:
            byteData += b'\x00';
            byteData += b'\x00';
            byteData += b'\x00';

    return byteData;


while True:
    if row == 16:
        color = random.choice(testColors);
        row = 0;

    response = clientSocket.recv(1);
    if response != b'\x05':
        if response == b'\x04':
            print("Received End Of Transmission (EOT), stopping...");
            exit(0);
        print("ERROR: Expected ENQ (0x05), got: ", response);
        exit(1);

    #data = buildByteData(testData[row], {'r': b'\x00', 'g': b'\xff', 'b': b'\x00'});
    data = buildByteData(testData[row], color);

    clientSocket.send(data);

    response = clientSocket.recv(1);
    if response != b'\x06':
        print("ERROR: Expected ACK (0x06), got: ", response);
        exit(1);

    print("Server ACK'ed our data, continuing...");
    row = row + 1;

