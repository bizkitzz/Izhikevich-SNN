#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import brian2
from brian2 import *
import numpy as ns

get_ipython().run_line_magic('matplotlib', 'inline')
defaultclock.dt = 0.5*ms

start_scope()
eqs = '''dv/dt = (0.04/ms/mV)*v**2 + (5/ms)*v + 140*mV/ms - u/ms + I*mV/(amp*ms) : volt
du/dt = a*(b*v - u)/ms  : volt
a : 1
b : 1
c : volt
d : volt
I : amp'''
reset = '''v = c;
u += d'''
tau = 1*ms
we = 1*amp
wi = -1*amp
V = -65 * mV 


Ne = 800
Ni = 200
Ge = NeuronGroup(Ne,eqs,threshold = "v>30*mV",reset=reset,method = "euler")
Gi = NeuronGroup(Ni,eqs,threshold = "v > 30*mV",reset=reset,method = 'euler')

Me = StateMonitor(Ge,["v","u"],record = True)
Mi = StateMonitor(Gi,["v","u"],record = True)

Spe = SpikeMonitor(Ge)
Spi = SpikeMonitor(Gi)

Ge.a =0.02
Ge.b =0.2
Ge.c ='-65*mV + 15*mV*rand()**2'
Ge.d = '(8 - 6*rand()**2)*mV'

Gi.a = '(0.02 + 0.08*rand())'
Gi.b ='(0.25 - 0.05*rand())'
Gi.c = -65*mV
Gi.d = 2*mV

Se = Synapses(Ge,Gi,"w : amp",delay=delay,on_pre = "I_post += w") #ГЛУТАМАТЭРГИЧЕСКИЙ
Se.connect(p = 1)
Se.w = "we*rand()"

Si = Synapses(Gi,Ge,"w : amp",delay=delay,on_pre = "I_post += w") #ГАМКЭРГИЧЕСКИЙ
Si.connect(p = 1)
Si.w = "wi*rand()"



Ge.v = V
Ge.u = Ge.b*Ge.v

Gi.v = V
Gi.u = Gi.b*Gi.v

Ge.run_regularly('I = 5*amp*randn()', dt=1*ms)
Gi.run_regularly('I = 2*amp*randn()', dt=1*ms)
run(1000*ms)



figure(figsize=(10, 2))
plot(Spi.t/ms, Spi.i, '.k')

figure(figsize=(10, 8))
plot(Spe.t/ms,Spe.i,".k")


figure(figsize=(14,3))
plot(Me.t/ms, Mi.v[0])
ylabel('v')
xlabel('Time (ms)') 
show();

