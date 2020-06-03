import pandas as pd
import numpy as np
from increment import *

"""
extrudes the template cross section by a single element in a path
args:
	nodes:				dataframe of current nodes
	elements:			dataframe of current elements
	tempplate_nodes: 	dataframe of nodes of the template
	element_nodes:		dataframe of elements of the current template
	step:				step this increment belongs to
	dr:					extrusion angle	
	dist:				element depth
returns:
	nothing
"""
def mesh_extrude(nodes,elements,template_nodes,template_elements,step,dr,dist,x0):
	num_n = nodes.shape[0]
	num_ni = template_nodes.shape[0]
	num_e = elements.shape[0]
	
	#copies the nodes
	current_nodes = template_nodes[['type','ref','X','step']].copy()

	#centroid at end of step: 	x1
	#centroid at start of step:	x0	
	#rotates the face of the extrusion
	R = rotZ(dr)
	unit_vector = np.transpose(np.array([0,1,0])) * dist
	VN = np.matmul(rotZ(dr),unit_vector)
	x1 = x0 + VN

	#translates the nodes
	current_nodes['X'] = template_nodes['V'].apply(lambda x: x1 + np.matmul(R,np.transpose(x)))
	current_nodes['step'] = step

	current_elements = template_elements.copy()
	f4 = lambda x: x+num_n-num_ni
	current_elements['n1'] = current_elements['n1'].apply(f4)
	current_elements['n2'] = current_elements['n2'].apply(f4)
	current_elements['n3'] = current_elements['n3'].apply(f4)

	f4 = lambda x: x+num_n
	current_elements['n4'] = current_elements['n4'].apply(f4)
	current_elements['n5'] = current_elements['n5'].apply(f4)
	current_elements['n6'] = current_elements['n6'].apply(f4)

	#sets process step
	current_elements['step'] = step

	#changes the node indexes of the mesh_increment
	nodes.append(current_nodes)
	elements = pd.concat([elements,current_elements],ignore_index = True)
	nodes = pd.concat([nodes,current_nodes],ignore_index = True)
	return x1, nodes, elements

def start_path(template_nodes,template_elements,step,dr,dist,x0):
	#creates nodes for the path start
	nodes = template_nodes[['type','ref','X','step']].copy()
	current_nodes = template_nodes[['type','ref','X','step']].copy()

	num_n = nodes.shape[0]

	#centroid at end of step: 	x1
	#centroid at start of step:	x0	
	#rotates the face of the extrusion
	R = rotZ(dr)
	unit_vector = np.transpose(np.array([0,1,0])) * dist
	VN = np.matmul(rotZ(dr),unit_vector)
	x1 = x0 + VN

	#vecrtorized for speed
	#translates the template nodes to increment location
	nodes['X'] = template_nodes['V'].apply(lambda x: x0 + np.matmul(R,np.transpose(x)))
	current_nodes['X'] = template_nodes['V'].apply(lambda x: x1 + np.matmul(R,np.transpose(x)))

	#creates the elements
	elements = template_elements.copy()
	f4 = lambda x: x+num_n
	elements['n4']=elements['n4'].apply(f4)
	elements['n5']=elements['n5'].apply(f4)
	elements['n6']=elements['n6'].apply(f4)
	elements['step'] = step

	nodes = pd.concat([nodes,current_nodes],ignore_index = True)
	nodes['step'] = step
	return x1, nodes, elements
"""
rotates about the GLOBAL z axis
args:
	theta:		angle
returns:
	rotation matrix
"""
def rotZ(theta):
	R = np.array([[np.cos(theta),	-np.sin(theta), 0],
				  [np.sin(theta),	np.cos(theta), 0],
				  [0,0,1]])
	return R
"""
increment:
steps the mesh by one process step
one process step is one .INP file
args:
	nodes:				dataframe of current nodes
	elements:			dataframe of current elements
	tempplate_nodes: 	dataframe of nodes of the template
	element_nodes:		dataframe of elements of the current template
	step:				step this increment belongs to
	dr:					direction
	dist:				distance of extrusion 
	m_inc:				number of mesh increments
	x0:					centroid of current filament
returns:
	nothing
"""
def increment(nodes,elements,template_nodes,template_elements,step,dr,dist,m_inc,x0):
	inc_dist = dist/m_inc
	for i in range(0,m_inc):
		(x0,nodes,elements) = mesh_extrude(nodes,elements,template_nodes,template_elements,step,dr,inc_dist,x0) 
	return x0,nodes,elements



