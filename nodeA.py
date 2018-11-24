from Architecture import nodeA

print("NODE A : init connection channel")
nodeA.init_channel()

print("NODE A : begin enter critical section")
nodeA.enterCriticalSection()

print("NODE A LISTENNING")
nodeA.beginListen()



print("NODE A : begin enter critical section")
nodeA.exitCriticalSection()
