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
print " 1) pick atoms by z, and sum LMDOS up"
print " 0) Exit\n"
print "=================================================================\n\n\n"

def pick():
#read z limit from input
	btm = input("z from: ")
	tp = input("to: ")

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

#pick atoms from btm to tp, and push atom number to output
	print "atom number is :"
	for x in range(0,atm_psn.shape[0]-1):
		if atm_psn[x,2] > btm and atm_psn[x,2] < tp:
			print x,
	os.system('rm tmp*')


#Main
rn = 1;
while(rn):
	fcn_type = raw_input("Select a function: \n")
	if fcn_type == '1':
		pick()
		rn = 0
	else:
		print "Exiting"
		rn = 0
#print "Thanks for use~~~"
