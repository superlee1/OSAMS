import matplotlib.pyplot as plt
import sys
import pandas as pd
import numpy as np 
import itertools
#import template as tp
import time


pot = plt.figure().gca(projection='3d')
feed = 600


#BEAD DIMS
fw = 0.48
fh = 0.1

len_fil = 200
wid_fil = 100
l = fw * len_fil
w = fw * wid_fil

area_size = 6 
a_d = area_size * fw
layers = 6 

#APPLY SERVICE LOAD?
serv = True


g_code = """;TEST
;*****INITIALIZE MACHINE******
M104 T200
M106 F100
M140 T60
G1 F60 E0
"""
t = (l-a_d)/feed
t0 = [t, (t/2) + (l*(wid_fil-area_size))/(2 * feed)]
t = (w-a_d)/feed
t90 = [t, (t/2) + (w*(len_fil-area_size))/(2 * feed)]
deg90 = False
cross = 0
for i in range(0,layers):
	#first filament
	pos = True
	l0 = f"G4 S{t0[1]}\n"
	of = f"G92 X{0} Y{0} Z{0}\n"
	g_code += of
	if (deg90):
		l0 = f"G4 S{t90[1]}\n"
		of = f"G92 X{fw/2} Y-{fw/2} Z{0}\n"
		g_code += of
	l1 = f"G1 E0 X0 Y0 Z{(i)*fh} F{feed}\n"
	#g_code += (l0)
	g_code += (l1)
	for j in range(0,area_size):
		x = pos*fw*area_size 
		y = j * fw
		wait = t0[1]
		if (deg90):
			x,y  = y,x
			wait = t90[1]
		line = f"G1 E10 X{x} Y{y} Z{(i)*fh}\n"
		g_code += (line)
		if (i!=area_size-1):
			ws = f"G4 S{wait}\n"
			#g_code += (ws)

		#next filament
		line = f"G1 E0 X{x} Y{y+fw} Z{(i)*fh} \n"
		if (deg90):
			line = f"G1 E0 X{x+fw} Y{y} Z{(i)*fh}\n"

		g_code += (line)
		pos^=True
	
	#REST OF THE PLATE
	#l0 = f"G4 S{t0[1]}\n"
	if (deg90):
		l0 = f"G4 S{t90[1]}\n"
	
	g_code += (l0)
	g_code += f"G1 E0  X0 Y0 Z{(i)*fh}\n"
	if (cross == 90):
		deg90 ^= True
	#g_code += "G4 S100\n"
#g_code = """;TEST
#;*****INITIALIZE MACHINE******
#M104 T200
#M106 F100
#M140 T60
#G4 S1
#G0 X0 Y0 Z0 F60
#G1 X2 Y0 Z0
#G3 X2 Y2 I0 J1
#"""
area_size = area_size
#path_states = OSAMS.interpreter.read_path(g_code)
#pot.plot3D(path_states['x'],path_states['y'],path_states['z'],linestyle = 'dashed')

gcode_file = open(f'6x6PLA.GCODE','w+')
gcode_file.write(g_code) 
'''
#partitions the toolpath into steps
step_partitions = OSAMS.partititon.partition_steps(path_states,nominal_step = 0.0924)

path_functs = OSAMS.partititon.df_functs(path_states,'time')

start = time.time()
#gets the template (9Brick)
brick = {}
template = tp.template(0.000914,0.000254)
brick['nodes'] = template.nodes
cn = template.nodes[['type','ref','x','y','z','step','up','down','left','right']]
brick['elements'] = template.elements
brick['width'] = 0.000914
brick['height'] = 0.000254 
nodes= cn[0:0].copy()
elements = template.elements[0:0].copy()

#global properties (placeholder)
model = {}
model['extruder'] = 275		#EXTRUDER TEMPERATURE 
model['e_time'] = 0.0924	#ELEMENT TIME NOT USED
model['enclosure'] = 75 	#ENCLOSURE TEMPERATURE
model['emissivity'] = 0.3	#EMISSIVITY
model['plate'] = 75 		#PLATE TEMPERATURE
model['h_nat'] = 30			#NATURAL CONVECTION COEFFECIENT
model['h_fan'] = 67 		#FORCED CONVECTION COEFFICENT
model['t_mass'] = 2020*1040	#THERMAL MASS PER UNIT VOLUME
model['h_plate'] = 10		#Heat transfer coeffcient for build plate
model['A_TEMP'] = False 

#extrudes the mesh and the template
steps,nodes,elements,p_nodes = OSAMS.manufacture.create_steps(step_partitions,path_functs,nodes,elements,brick)
nodes['ref'] = nodes.index
extrusion_steps = steps.loc[steps['type'] == 1]
extrusion_steps = extrusion_steps.index 
#LIST OF BOUNDARY CONDITION CHANGES
cols = ['step','d_step','side','change']
BC_changes = pd.DataFrame(columns = cols)

#creates the BC change table and surfaces table( will change) 
indx = list(itertools.product(extrusion_steps,['UP', 'DOWN', 'LEFT' , 'RIGHT']))
idx = pd.MultiIndex.from_tuples(indx,names = ['step','direction'])
surf_cols = ['ref']
surfaces = pd.DataFrame(index = idx,columns = surf_cols)
surfaces['ref'] = -1
p_nodes,nodes,elements,surfaces,BC_changes = OSAMS.analyze.merge_p_nodes(p_nodes,nodes,elements,surfaces,BC_changes)
nodes = nodes.loc[nodes['ref'] == nodes.index]
"""
for i in steps.index:
	sn = p_nodes.loc[p_nodes['step'] == i].copy()
	pot.scatter(sn['x']*1000,sn['y']*1000,sn['z']*1000,s = 20)
#pot.set_xlim(0,5)
#pot.set_zlim(-0.5,0.5)
#pot.set_ylim(0,2.5)
pot.set_xlabel('x(mm)')
pot.set_ylabel('y(mm)')
pot.set_zlabel('z(mm)')
plt.show()
"""
BC_changes = (BC_changes.drop_duplicates(['step','d_step', 'side', 'change']))
BC_changes = BC_changes[BC_changes['side'] != 'NO']

#build surface is redundant
mask = (steps['layer'] == 0)&( steps['type'] == 1)
layer1_steps = steps.loc[mask].index
for i in layer1_steps:
	surfaces.loc[i,'DOWN'] = 1
prefix = 'NEWERER'
thermal_job = f'{area_size}x{layers}x{cross}{prefix}_therm' 
structural_job = f'{area_size}x{layers}x{cross}{prefix}_disp' 
thermal_file = open(f'../Thermal Models/{thermal_job}.inp','w+')
structural_file = open(f'../Thermal Models/{structural_job}.inp','w+')


thermal_inp = lambda x: thermal_file.write(x)
structural_inp = lambda x: structural_file.write(x)

#flags the build plate nodes
nodes = OSAMS.analyze.build_nodes(nodes)
thermal_inp(out_nodes(nodes))
structural_inp(out_nodes(nodes))
thermal_inp(out_elements(elements,nodes,template,analysis_type = 'T'))
structural_inp(out_elements(elements,nodes,template,analysis_type = 'S'))
#creates the build surface nodes
bs_nodes = nodes.loc[nodes['z'] < 0.000001]
#finds the left nodes
max_x = bs_nodes['x'].max() - 0.000001
min_x = bs_nodes['x'].min() + 0.000001


front_nodes = bs_nodes.loc[(bs_nodes['x'] > max_x)]
front_left = front_nodes['y'].idxmax()
front_right = front_nodes['y'].idxmin()

rear_nodes = bs_nodes.loc[(bs_nodes['x'] < min_x )]
rear_left = rear_nodes['y'].idxmax()

structural_inp(OSAMS.material.def_mat.materiel_model())
thermal_inp(OSAMS.material.def_mat.materiel_model())
structural_inp(OSAMS.material.def_mat.section())
thermal_inp(OSAMS.material.def_mat.section())
thermal_inp(element_sets(elements,steps))
thermal_inp(build_surf(elements,steps))
structural_inp(element_sets(elements,steps))
structural_inp(node_sets(bs_nodes,"BUILD_PLATE"))

thermal_inp(out_surf(elements,surfaces))
#print(nodes.shape[0])
num_step = steps.shape[0]

thermal_inp(inital_thermal(elements,num_step,steps,surfaces,model))
structural_inp(inital_structural(elements,num_step,steps,surfaces,model,thermal_job,1))
j = 1
for i in range(1,num_step):
	thermal_inp(thermal_step(elements,i,steps,BC_changes,model))
	structural_inp(structural_step(elements,i,steps,thermal_job,j))
	j = j + 1

#applies the service load as described in service .inp
if (serv):
	thermal_inp(service.thermal_service())
	struct_serv = service.struct_service(6,front_right,front_left,rear_left,j,thermal_job)
	structural_inp(struct_serv)
	
#end = time.time()
#print(end-start)
'''
