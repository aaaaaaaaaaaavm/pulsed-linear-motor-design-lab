"""Export both committed cases at a 180 mm report width as SVG/PDF/300 dpi PNG."""
import json
import sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
plt.style.use(ROOT/'tools/scientific.mplstyle')
plt.rcParams.update({'pdf.fonttype':42,'savefig.dpi':300,'xtick.labelsize':10,'ytick.labelsize':10,'legend.fontsize':10,'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'axes.grid':False,'svg.fonttype':'none','svg.hashsalt':'technical-case-plots','figure.facecolor':'white','axes.facecolor':'white'})
C=['#0072B2','#D55E00']
def save(fig,name,caption):
 fig.subplots_adjust(left=.12,right=.98,bottom=.34,top=.82,wspace=.55)
 fig.text(.02,.025,caption,fontsize=10,va='bottom',linespacing=1.3)
 for extension in ('svg','pdf','png'):
  path=ROOT/'figures'/(Path(name).stem+'.'+extension)
  metadata=({'Date':None} if extension=='svg' else
            {'CreationDate':None,'ModDate':None,'Creator':'Committed local calculation cases'} if extension=='pdf' else None)
  fig.savefig(path,dpi=300,metadata=metadata)
  if extension=='svg': path.write_text('\n'.join(line.rstrip() for line in path.read_text().splitlines())+'\n')
 plt.close(fig)

from plmd import calculate
cases=[json.loads((ROOT/'cases'/name).read_text())for name in ['desktop_stage.json','volley_reference.json']]
labels=['Desktop stage','Historical Gen5 case'];results=[calculate(c)for c in cases]
fig,axes=plt.subplots(1,2,figsize=(7.1,4.8))
for i,(c,r) in enumerate(zip(cases,results)):
 x=np.linspace(0,c['stroke_m'],80);v=np.sqrt(2*r['acceleration_m_s2']*x);axes[0].plot(x,v,color=C[i],ls=['-','--'][i],label=labels[i])
 energy=[c['electrical_input_J'],r['moving_kinetic_energy_J'],r['payload_kinetic_energy_J']];axes[1].bar(np.arange(3)+(i-.5)*.3,energy,width=.28,color=C[i],label=labels[i])
axes[0].set(xlabel='Active stroke (m)',ylabel='Implied constant-force\nspeed (m/s)',title='a  Force–stroke screen');axes[1].set(xticks=[0,1,2],xticklabels=['Electrical\ninput','Moving\nKE','Payload\nKE'],ylabel='Energy (J)',title='b  Necessary energy boundary');axes[1].tick_params(axis='x',labelsize=10)
fig.legend(*axes[0].get_legend_handles_labels(),loc='upper center',bbox_to_anchor=(.5,1),ncol=2,frameon=False,fontsize=10)
save(fig,'design-screen.svg','Computed screens: desktop_stage and historical volley_reference cases; plmd.calculate.\nImplied speed needs energy and peak-power closure; it is not an attainable-speed rating.\nNo winding, switching or thermal model is solved. Presentation revision: 23 Oct 2026.')
fig,axes=plt.subplots(1,2,figsize=(7.1,4.8))
for i,(c,r) in enumerate(zip(cases,results)):
 ax=axes[i];ax.bar([0,1,2],[c['electrical_input_J'],r['moving_kinetic_energy_J'],r['payload_kinetic_energy_J']],color=[C[i],'.55','.8']);ax.set(xticks=[0,1,2],xticklabels=['Input','Moving\nKE','Payload\nKE'],ylabel='Energy (J)',title=labels[i]);ax.tick_params(axis='x',labelsize=10)
save(fig,'force-energy.svg','Computed energy accounting: the same two local cases; plmd.calculate.\nMoving kinetic energy includes carriage. Input minus kinetic energy is not a loss allocation.\nPositive ideal energy margin does not close an electrical or thermal design. 23 Oct 2026.')
fig,ax=plt.subplots(figsize=(7.1,4.8))
for i,c in enumerate(cases):
 x=np.linspace(.005,.15,150);y=c['bank_voltage_V']**2/(4*x);ax.plot(x*1000,y/1000,color=C[i],ls=['-','--'][i],label=labels[i]+' ceiling');ax.axhline(c['peak_power_required_W']/1000,color=C[i],ls=':',lw=1)
ax.set(xlabel='Assumed bank ESR (mΩ)',ylabel='Power (kW)',title='Source peak-power screen');ax.legend(frameon=False,fontsize=10)
save(fig,'source-window.svg','Analytical screen: two local cases; ceiling V²/(4R), dotted lines requested peak power.\nEnergy closure is separate. A ceiling crossing does not select a bank or converter.\nNo transient circuit or state-of-charge model. Presentation revision: 23 Oct 2026.')
print('Three 180 mm motor figures exported as SVG, embedded-font PDF and 300 dpi PNG')
