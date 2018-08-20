import numpy as np  
from matplotlib import pyplot as plt  
from matplotlib import animation  
import threading
import cfft
import queue
import sys
from rtlsdr import RtlSdr

baseF=76e6
if len((sys.argv))>=2 :
	baseF=int(float(sys.argv[1]))
bandW=2.048e6
#bandW=1.024e6
startF=baseF-bandW/2;
endF=baseF+(bandW/2);

level=10

sdr=RtlSdr()
sdr.sample_rate=bandW
sdr.center_freq=baseF
sdr.gain=float('19.2')
sdr.frq_correction=60
points=CHUNK=1<<level
q=queue.Queue(maxsize=32)
endFlag=0;

fig = plt.figure()  
axA = fig.add_subplot(1,1,1,xlim=(startF,endF),ylim=(0, 0.01))  

lineA, = axA.plot([], [], lw=1)	

def pdata():
	while(endFlag==0):
		for i in range(16):
			data=sdr.read_samples(CHUNK)
	#	data=[0.1+0.1j]*CHUNK
		F=cfft.toComplex(cfft.fft(cfft.toComplex_c(data),level))
		q.put(F)
	print('endFlag=',endFlag)
	exit()
		
threading.Thread(target=pdata).start()

freqs=[]
def calFreqs():
	for i in range(points):
		freqs.append(i*(bandW/points)+startF);
	#print(freqs)
calFreqs()
  
def init():	
	lineA.set_data([], [])	
	return lineA

def animate(i):
	F=[0+0j]*CHUNK
	while(not q.empty()):
		F=q.get()
	F=list(F)
	F=F[len(F)//2::]+F[0:len(F)//2]
	#print(F[0])
	lens=list(map(abs,F));
	lineA.set_data(freqs,lens)
	#print('updata',i)
	return lineA
  
anim1=animation.FuncAnimation(fig, animate, init_func=init,  frames=1, interval=320)	
plt.show()  
endFlag=1;
print('done')
