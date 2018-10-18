#!/usr/bin/python
# -*- coding: UTF-8 -*- 
import math
import numpy
import os
import linecache
#print "*****************************************************************\n"
#print "A code for DFT calculations, functions are indenpendent\n"
print "Version 1.1 Revised in 2018, April 6th, added dipole center function\n"
#print "*****************************************************************\n"
print "\n===============================================================\n"
print " 1) pick atoms of each layer and print them"
print " 0) Exit\n"
print "=================================================================\n\n\n"
	
def pick( atom_position, tolerence ):
#get btm and tp
	btm = atom_position - tolerence
	tp = atom_position + tolerence
#read POSCAR 1-8 lines, get number of atoms
	s0 = 'POSCAR'
	os.environ['flnm']=s0
	os.system('sed -n "3,5 p" $flnm >tmp0')
	os.system('sed -n "7,7 p" $flnm >tmp1')
	latc_vector = numpy.loadtxt('tmp0')
	atm_nums = numpy.loadtxt('tmp1')
	a = linecache.getline(s0,8)
	if a[0] == 'S':
		hed = 10
		print "Selected dynamics? yes"
	else:
		hed = 9
		print "Selected dynamics? no"
	b=int(numpy.sum(atm_nums))
	print "Number of atoms: ",b

#load atomic position to atm_psn
	deh = b + hed - 1
	os.environ['hed']=str(hed)
	os.environ['deh']=str(deh)
	os.system('''sed -n "$hed,$deh p" $flnm |awk '{ print $1, $2, $3 }' >tmp2''')
	atm_psn = numpy.loadtxt('tmp2')
	os.system('rm tmp*')
	
#pick atoms from btm to tp, and push atom number to output
	for x in range(0,atm_psn.shape[0]):
		if atm_psn[x,2] > btm and atm_psn[x,2] < tp:
			print x+1,

###########################################################################################################
def slicer( tolerence )
#read POSCAR 1-8 lines, get number of atoms
	s0 = 'POSCAR'
	os.environ['flnm']=s0
	os.system('sed -n "3,5 p" $flnm >tmp0')
	os.system('sed -n "7,7 p" $flnm >tmp1')
	latc_vector = numpy.loadtxt('tmp0')
	atm_nums = numpy.loadtxt('tmp1')
	a = linecache.getline(s0,8)
	if a[0] == 'S':
		hed = 10
		print "Selected dynamics? yes"
	else:
		hed = 9
		print "Selected dynamics? no"
	b=int(numpy.sum(atm_nums))
	print "Number of atoms: ",b

#load atomic position to atm_psn
	deh = b + hed - 1
	os.environ['hed']=str(hed)
	os.environ['deh']=str(deh)
	os.system('''sed -n "$hed,$deh p" $flnm |awk '{ print $1, $2, $3 }' >tmp2''')
	atm_psn = numpy.loadtxt('tmp2')
	os.system('rm tmp*')
#slice the material layer by layer from z=0 to z=1
	footprint = 0
	x=0
	while x < atm_psn.shape[0]:
		leftprint = footprint - tolerence
		rightprint = footprint + tolerence
		if atm_psn[x,2] > leftprint and atm_psn[x,2] < rightprint:
			footprint = atm_psn[x,2]+tolerence*2
			pick(atm_psn[x,2],tolerence)
			print "\n"
			x=-1
		elif x == (atm_psn.shape[0] - 1):
			if footprint < 1:
				footprint = footprint +tolerence*2
				x=-1
		x=x+1
				
			


#Main
rn = 1;
while(rn):
	fcn_type = raw_input("Select a function: \n")
	if fcn_type == '1':
	 	tolerence= input("tolerence is: ")
		slicer( tolerence )
		rn = 0
	else:
		print "Exiting"
		rn = 0
#print "Thanks for use~~~"
