"""Generate technical plots from the two local calculation cases."""
import json
import sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'axes.grid':False,'svg.fonttype':'none','svg.hashsalt':'technical-case-plots','figure.facecolor':'white','axes.facecolor':'white'})
C=['#0072B2','#D55E00']
def save(fig,name,caption):
 fig.subplots_adjust(left=.10,right=.97,bottom=.23,top=.88,wspace=.38)
 fig.text(.02,.025,caption,fontsize=8,va='bottom')
 fig.savefig(ROOT/'figures'/name,metadata={'Date':None})
 path=ROOT/'figures'/name
 path.write_text('\n'.join(line.rstrip() for line in path.read_text().splitlines())+'\n')
 plt.close(fig)
from plmd import calculate
cases=[json.loads((ROOT/'cases'/name).read_text())for name in ['desktop_stage.json','volley_reference.json']]
labels=['Desktop stage','Historical Gen5 case'];results=[calculate(c)for c in cases]
fig,axes=plt.subplots(1,2,figsize=(10,4.4))
for i,(c,r) in enumerate(zip(cases,results)):
 x=np.linspace(0,c['stroke_m'],80);v=np.sqrt(2*r['acceleration_m_s2']*x);axes[0].plot(x,v,color=C[i],ls=['-','--'][i],label=labels[i])
 energy=[c['electrical_input_J'],r['moving_kinetic_energy_J'],r['payload_kinetic_energy_J']];axes[1].bar(np.arange(3)+(i-.5)*.3,energy,width=.28,color=C[i],label=labels[i])
axes[0].set(xlabel='Active stroke (m)',ylabel='Implied constant-force speed (m/s)',title='a  Force–stroke screen');axes[1].set(xticks=[0,1,2],xticklabels=['Electrical input','Moving KE','Payload KE'],ylabel='Energy (J)',title='b  Necessary energy boundary');axes[1].tick_params(axis='x',labelsize=8)
for ax in axes:ax.legend(frameon=False,fontsize=8)
save(fig,'design-screen.svg','Implied speeds require independent energy and peak-power feasibility; they are not attainable-speed ratings.\nInputs and outputs come from the two local case files. No winding, switching or thermal model is solved here.')
fig,axes=plt.subplots(1,2,figsize=(10,4.4))
for i,(c,r) in enumerate(zip(cases,results)):
 ax=axes[i];ax.bar([0,1,2],[c['electrical_input_J'],r['moving_kinetic_energy_J'],r['payload_kinetic_energy_J']],color=[C[i],'.55','.8']);ax.set(xticks=[0,1,2],xticklabels=['Input','Moving KE','Payload KE'],ylabel='Energy (J)',title=labels[i]);ax.tick_params(axis='x',labelsize=8)
save(fig,'force-energy.svg','Total moving kinetic energy includes the carriage. Input-minus-kinetic energy is not an identified loss allocation.\nA positive necessary energy margin does not close a real electrical or thermal design.')
fig,ax=plt.subplots(figsize=(8,4.4))
for i,c in enumerate(cases):
 x=np.linspace(.005,.15,150);y=c['bank_voltage_V']**2/(4*x);ax.plot(x*1000,y/1000,color=C[i],ls=['-','--'][i],label=labels[i]+' ceiling');ax.axhline(c['peak_power_required_W']/1000,color=C[i],ls=':',lw=1)
ax.set(xlabel='Assumed bank ESR (mΩ)',ylabel='Power (kW)',title='Source peak-power screen');ax.legend(frameon=False,fontsize=8)
save(fig,'source-window.svg','Curves: V²/(4R); dotted lines: requested peak power. The energy gate is separate.\nNeither a ceiling crossing nor this Thevenin model establishes a selected bank or converter.')
print('Three technical motor figures generated')
