import pandas as pd
import numpy as np
"""
this file is responsible for fetching and preprocessing the template mesh
"""

centerline = np.array([0.00015,0,0])		#centerline: the xy coordinate of the centerline of the mesh (NORMALLY ZERO) also dictates the rotation of the mesh
"""
consolidates the x y z coloumns into a vector to make things easier
creates a vector from the template nodes to the centerline of the filament
args:
	nodes:		dataframe of nodes
	center:		
"""
def vects(nodes,center): 
	#nodes['X'] = ""
	#nodes['V'] = ""
	nodes[['i','j','k']] = nodes[['x','y','z']] - centerline

	"""
	for i,node in nodes.iterrows():
		X = np.array([node['x'],node['y'],node['z']])
		nodes.at[i,['i','j','z']] = X-centerline
	"""

	nodes.drop(['x','y','z'],axis = 1)
	print(nodes)
	return nodes

nodes = pd.read_excel("9BRICK.xlsx",sheet_name = 'NODES', index_col = 'index')
print(nodes.head())
elements = pd.read_excel("9BRICK.xlsx",sheet_name = 'ELEMENTS', index_col = 'index')
nodes = vects(nodes,centerline)
