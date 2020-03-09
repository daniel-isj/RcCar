# import RPi.GPIO as gpio
import time

class RcCarMotor:
    def __init__(self, gpio):
        self._low = 0
        self._high = 1
        self._servopin = 18
        self._ena = 0 # 26
        self._ina = 5 # 19
        self._inb = 6 # 13
        self._gpio = gpio
        self._gpio.setmode(self._gpio.BCM)

        self._gpio.setup(self._servopin, self._gpio.OUT)
        self._servopwm = self._gpio.PWM(self._servopin, 50)
        self._servopwm.start(0)

        self._gpio.setup(self._ena, self._gpio.OUT)
        self._gpio.setup(self._ina, self._gpio.OUT)
        self._gpio.setup(self._inb, self._gpio.OUT)
        self._dcpwm = self._gpio.PWM(self._ena, 100)
        self._dcpwm.start(0)
        print ('설정완료')

    def __del__(self):
        self._servopwm.stop()
        self._gpio.cleanup()

    def calcData(self, data):
        command = data[:1]
        if (command == 'S'):
            datas = data[1:].split(',')
            print ('datas : ', datas)
            self.servoCalc(datas[0].strip(), datas[1].strip())
        else: 
            self.dcActivity(command, 50)

    def servoCalc(self, x, y):
        try:
            _x = float(x)
            _y = float(y)
            print ('x : ', _x)
            print ('y : ', _y)
            _cycle =7

            # left(4 ~ 7)
            if (_x < 4.0):
                if (_y < 0.0):
                    _cycle = 4.0
                else:
                    _cycle = 8.0
            print ('cycle : ', _cycle)
            self.servoAngle(_cycle)
        except Exception as ex:
            print (ex)
            pass

    def servoAngle(self, cycle):
        try:
            self._servopwm.ChangeDutyCycle(cycle)
            time.sleep(0.01)
        except Exception as ex:
            print (ex)
            pass

    def dcActivity(self, command, speed):
        if (command == 'F'):
            self._low = 1
            self._high = 0
        elif (command == 'R'):
            self._low = 0 
            self._high = 1
        else:
            self._low = 0 
            self._high = 0

        try:
            print (command)
            self._dcpwm.ChangeDutyCycle(speed)
            self._gpio.output(self._ina, self._high)
            self._gpio.output(self._inb, self._low)
            time.sleep(0.5)
        except Exception as ex:
            print (ex)


