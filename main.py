# -*- coding: utf-8 -*-
"""
Created on Sat Oct 22 22:19:56 2016

@author: ivan
"""
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
import my_functions as myf
filename='/Users/ivan/Desktop/poesia.wav'

#==============================================================================
# Audio file and props
#==============================================================================
fs, audio_i = wavfile.read(filename)
audio=audio_i[:,0]
time=np.arange(len(audio))* 1/float(fs)
nsamp=len(audio)

#==============================================================================
# Sampling for easy handling
#==============================================================================
s1=myf.stft(audio)
n1=np.size(s1,0)
amp=np.mean(np.real(s1*np.conjugate(s1)),1)
t1=np.arange(n1)/float(n1)*time[-1]
samp2=len(audio)/float(len(t1))
a1=np.interp(t1, time, audio)

#%%
#==============================================================================
# filter to separate words and silabs
#==============================================================================
amp_tresh=np.median(amp/5.)
short_sil=4
filt1=(amp>amp_tresh)

tf1=t1[filt1]
af1=a1[filt1]



nsil=0
sil=[]
tsil=[]
completando=0
for i in range(len(t1)):
    if completando==0 and amp[i]>amp_tresh:
        completando=1
        sil.append([])
        tsil.append([])
        sil[-1].append(a1[i])
        tsil[-1].append(t1[i])        
    elif completando ==1 and amp[i]>amp_tresh:
        sil[-1].append(a1[i])
        tsil[-1].append(t1[i])        
    elif completando ==1 and amp[i]<amp_tresh:
        completando=0


        
sil=[x  for x in sil if len(x)>short_sil]
tsil=[x  for x in tsil if len(x)>short_sil]
num_sil=len(sil)
norm_factor=np.max(np.abs(a1))
sil=[x/norm_factor  for x in sil]
 
#%% 
plt.figure()
axs=plt.subplot(2,1,1)
#plt.plot(t1, a1, color='blue')
for i in range(len(sil)):
    plt.plot(tsil[i], sil[i], linewidth=0.5, color='black')
plt.plot()
axa=plt.subplot(2,1,2)
plt.plot(t1,amp)
axa.set_yscale('log')


#%%
tlim=10
num_lines=np.ceil(tsil[-1][-1]/float(tlim))
carta=plt.figure(figsize=(8,num_lines/float(2)))

scolor='black'
slw=0.5

num_line=0
line_factor=2
for i in range(num_sil):
    num_line=int(tsil[i][-1]) / int(tlim)
    plt.plot(np.array(tsil[i])-(num_line*tlim), sil[i]-num_line*line_factor, color=scolor, linewidth=slw)    

plt.tight_layout()
plt.xlim(0,10)
plt.ylim(2, -num_lines-2)
plt.axis('off')
plt.savefig('./test.pdf')
plt.savefig('./test.jpg')
#plt.figure()
#for i in range(16):
#    plt.subplot(16,1,i+1)
#    plt.plot(s1[:,i*32])