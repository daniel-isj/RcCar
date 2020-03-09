from twisted.internet import protocol, reactor, endpoints
import RPi.GPIO
import RcCarMotor as rcm

class RcCar(protocol.Protocol):
    delimiter = '\r\n'
    def __init__(self, rcCarMotor):
        self._rcCarMotor = rcCarMotor

    def dataReceived(self, data):
        print ('received data : ', data.decode('utf8').strip())
        self._rcCarMotor.calcData(data.decode('utf8').strip())
        # self.transport.write(data)

    def connectionMade(self):
        print ('client connect : ', self.transport.getPeer())

    def connectionLost(self, reason):
        print ('client disconnect : ', reason)
        
class RcCarFactory(protocol.Factory):
    def __init__(self):
        self._rcCarMotor = rcm.RcCarMotor(RPi.GPIO)
        
    def buildProtocol(self, addr):
        return RcCar(self._rcCarMotor)

endpoints.serverFromString(reactor, "tcp:63000").listen(RcCarFactory())
print ('server start')
reactor.run()
