import numpy as np

from typing import List

import os, sys	
path = os.path.dirname(os.path.abspath(os.getcwd()))
sys.path.insert(1, str(path)+'/hdf5')

from io_hdf5 import init_hdf5, write_line_hdf5
#-----------------------------------------------------------------------------
## basic functions 
#-----------------------------------------------------------------------------
def set_extension(name:str) -> str:
        if name.endswith('.csv'):
                return name
        else:
                return name+'.csv'
#-----------------------------------------------------------------------------
def init_csv(name:str) -> None:
        name= set_extension(name)
        with open(name,'w') as f:
                pass
#-----------------------------------------------------------------------------
def write_line_csv_1d(name:str,vals:List[float]) -> None:
        name= set_extension(name)
        with open(name,'a') as f:
                for val in vals[:-1]:
                        f.write(str(val)+',')
                f.write(str(vals[-1])+'\n')
#-----------------------------------------------------------------------------
def read_line_csv_1d(name:str,step:int) -> List[float]:
        name= set_extension(name)
        ctr= 0
        with open(name,'r') as f:
                for line in f:
                        if ctr==step:
                                return [float(val) for val in line.split(',')]
                        ctr+= 1
        raise ValueError('step '+str(step)+' not in file')
#-----------------------------------------------------------------------------
def read_csv_1d(name:str) -> List[List[float]]:
        name= set_extension(name)
        with open(name,'r') as f:
                vals= [
                        [float(val) for val in line.split(',')]
                        for line in f
                ]
        return vals
#-----------------------------------------------------------------------------
## format for 2d csv: time, nx, ny, arr
#-----------------------------------------------------------------------------
def read_vals_csv_2d(name:str) -> np.array:
	name= set_extension(name)
	vals= []
	with open(name,'r') as f:
		for line in f:
			line= [v for v in line.split(',')]
			nx= int(line[1])
			ny= int(line[2])
			arr= np.zeros((nx,ny))
			for i in range(nx):
				for j in range(ny):
					arr[i][j]= float(line[ny*i+j])
			vals.append(arr)
	return np.array(vals)
#-----------------------------------------------------------------------------
def read_times_vals_csv_2d(name:str) -> (np.array,np.array):
	name= set_extension(name)
	times= []
	vals= []
	with open(name,'r') as f:
		for line in f:
			line= [v for v in line.split(',')]
			time= float(line[1])
			nx= int(line[1])
			ny= int(line[2])
			arr= np.zeros((nx,ny))
			for i in range(nx):
				for j in range(ny):
					arr[i][j]= float(line[ny*i+j])
			times.append(time)
			vals.append(arr)
	return times, np.array(vals)
#-----------------------------------------------------------------------------
def convert_csv_to_hdf5(name:str) -> None:
	assert(name.endswith('.csv'))
	times, vals = read_times_vals_csv_2d(name)
	name= name[:-4]+'.h5'

	print(name)
	init_hdf5(name)
	print("init done")

	for i in range(len(time)):
		write_line_hdf5(name,times[i],vals[i])
