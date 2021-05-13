# Copyright 2021 Karim Sudki
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import click
import re

import serial
import serial.tools.list_ports
import time

class printer():
    def __init__(self, port=None, baudrate=115200, timeout=None):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.s = 0.1

        self.limits = {
            "min_x" : 0.0,
            "max_x" : 0.0,
            "min_y" : 0.0,
            "max_y" : 0.0,
            "min_z" : 0.0,
            "max_z" : 0.0,
            "min_s" : 0.1,
            "max_s" : 100.0,
        }

        if port is None:
            for port in serial.tools.list_ports.comports():
                if port.vid == 0x1A86 and port.pid== 0x7523:
                    self.port = port.device
        else:
            self.port = port

        try:
            self._serialport = serial.Serial(self.port, baudrate=115200, timeout=None)
        except serial.SerialException as e:
            raise type(e)(f"Cannot send : {e.strerror}")
        
    def write(self, data=b""):
        if not self.connected:
            raise serial.SerialException("Not connected.")
        try:
            self._serialport.write(data+b"\r")
            self._serialport.flush()
        except serial.SerialException as e:
            raise type(e)(f"Cannot send : {e.strerror}")

    def read_until(self, c=None, size=None):
        if not self.connected:
            raise serial.SerialException("Not connected.")
        try:
            data = self._serialport.read_until(expected=c, size=None)
            self._lastread = data
            return data
        except serial.SerialException as e:
            raise type(e)(f"Cannot read : {e.strerror}")

    def read(self, length=1):
        if not self.connected:
            raise serial.SerialException("Not connected.")
        try:
            data = self._serialport.read(length)
            self._lastread = data
            return data
        except serial.SerialException as e:
            raise type(e)(f"Cannot read : {e.strerror}")

    def flush_input(self):
        self._serialport.reset_input_buffer()

    def close(self):
        self._serialport.close()

    def get_timeout(self):
        return self._serialport.timeout

    def set_timeout(self, value):
        self._serialport.timeout = value

    def connected(self):
        return self._serialport.is_open

    def set_unit(self,value):
        if value == "mm":
            self.write(b"G21")
            self.read_until(c=b"ok")
            print("Switching to Metric units (millimeters)")
        elif value == "in":
            self.write(b"G20")
            self.read_until(c=b"ok")
            print("Switching to US/Imperial units (inches)")

    def go_home_xy(self):
        self.check_limits(self.x, self.y, self.z+20, self.s)
        self.set_pos(self.x, self.y, self.z+20)
        self.write(b"G28 X Y")
        self.read_until(c=b"ok")

    def go_home_xyz(self):
        self.check_limits(self.x, self.y, self.z+20, self.s)
        self.set_pos(self.x, self.y, self.z+20)
        self.write(b"G28 X Y Z")
        self.read_until(c=b"ok")

    def set_pos(self, x, y, z):
        self.write(f"G0 X {x:.1f} Y {y:.1f} Z {z:.1f} F6000".encode())
        self.read_until(c=b"ok")
        self.x = x
        self.y = y
        self.z = z
        self.get_pos()

    def get_pos(self):
        self.write(b"M114")
        regex = re.compile(b'.*X:[-]*(?P<x>\d+.\d+)\sY:[-]*(?P<y>\d+.\d+)\sZ:[-]*(?P<z>\d+.\d+)\sE:')
        m = re.search(regex,self.read_until(c=b"ok"))
        if len(m.groups()) == 3:
            self.x = float(m.group('x'))
            self.y = float(m.group('y'))
            self.z = float(m.group('z'))
            print(f"X {self.x:.1f} | Y {self.y:.1f} | Z {self.z:.1f} | S {self.s:.1f}")
            return self.x,self.y,self.z
        else:
            return self._serialport.timeout

    def check_limits(self,x,y,z,s):
        if self.limits["min_x"] <= x <= self.limits["max_x"]:
            self.x = x
        else:
            print(f"X out of bounds ({self.limits['min_x']:.1f} to {self.limits['max_x']:.1f})")
        if self.limits["min_y"] <= y <= self.limits["max_y"]:
            self.y = y
        else:
            print(f"Y out of bounds ({self.limits['min_y']:.1f} to  {self.limits['max_y']:.1f})")
        if self.limits["min_z"] <= z <= self.limits["max_z"]:
            self.z = z
        else:
            print(f"Z out of bounds ({self.limits['min_z']:.1f} to {self.limits['max_z']:.1f})")
        if self.limits["min_s"] <= s <= self.limits["max_s"]:
            self.s = s
        else:
            print(f"Steps out of bounds ({self.limits['min_s']:.1f} to {self.limits['max_s']:.1f})")

    def manual(self):
        print("Entering Manual mode...")
        self.get_pos()
        while True:
            c = click.getchar()
            # ESC
            if c == '\x1b':
                click.echo('Exiting Manual mode...')
                break
            # Left Arrow
            elif c == '\x1b[D':
                new_x = self.x - self.s
                self.check_limits(new_x, self.y, self.z, self.s)
                self.set_pos(self.x, self.y, self.z)
            # Right Arrow
            elif c == '\x1b[C':
                new_x = self.x + self.s
                self.check_limits(new_x, self.y, self.z, self.s)
                self.set_pos(self.x, self.y, self.z)
            # Down Arrow
            elif c == '\x1b[B':
                new_y = self.y - self.s
                self.check_limits(self.x, new_y, self.z, self.s)
                self.set_pos(self.x, self.y, self.z)
            # Up Arrow
            elif c == '\x1b[A':
                new_y = self.y + self.s
                self.check_limits(self.x, new_y, self.z, self.s)
                self.set_pos(self.x, self.y, self.z)
            elif c == 'u':
                new_z = self.z + self.s
                self.check_limits(self.x, self.y, new_z, self.s)
                self.set_pos(self.x, self.y, self.z)
            elif c == 'd':
                new_z = self.z - self.s
                self.check_limits(self.x, self.y, new_z, self.s)
                self.set_pos(self.x, self.y, self.z)
            elif c == 's':
                try:
                    new_step = float(input("Enter desired step:"))
                    self.check_limits(self.x, self.y, self.z, new_step)
                except ValueError:
                    print("Steps value must be a float")
                    continue
            elif c == '+':
                if self.s < 1.0:
                    self.s = 1.0
                elif self.s < 10.0:
                    self.s = 10.0
                elif self.s < 100.0:
                    self.s = 100.0
            elif c == '-':
                if self.s >= 100.0:
                    self.s = 10.0
                elif self.s >= 10.0:
                    self.s = 1.0
                elif self.s >= 1.0:
                    self.s = 0.1
            elif c == 'h':
                if input("!!! WARNING !!! Printer will go directly to X/Y origins (a.k.a. Home) without passing GO!\r\nEnsure that nothing is still on the bed\r\nContinue (y/n)?") == "y":
                    self.go_home_xy()
                else:
                    print("Canceled")
            elif c == 'z':
                if input("!!! WARNING !!! Printer will go directly to X/Y/Z origins without passing GO!\r\nEnsure that nothing is still on the bed\r\nContinue (y/n)?") == "y":
                    self.go_home_xyz()
                else:
                    print("Canceled")
            self.get_pos()
