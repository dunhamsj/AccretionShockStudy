#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
plt.style.use( './Publication.sty' )

from UtilitiesModule import GetData

#### ========== User Input ==========

root = '/lump/data/accretionShockStudy/'

IDs = np.array( [ 'GR1D_M2.0_Mdot0.3_Rs150_Gm1.13' ], str )

fields0      = np.array( [ 'PF_D', 'AF_P' ], str )
c0           = np.array( [ 'r.', 'rx' ]      , str )
useLogScale0 = True
labels0      = np.array( [ r'$\rho\,c^{2}$', r'$p$' ], str )
yScales0     = np.array( [ ( 2.99792458e10 )**( -2 ), 1.0 ], np.float64 )
yLabel0      = r'$\mathrm{erg\,cm}^{-3}$'

fields1      = np.array( [ 'PF_V1' ], str )
c1           = np.array( [ 'b.' ]   , str )
useLogScale1 = False
labels1      = np.array( [ r'$v^{1}/c$' ], str )
yScales1     = np.array( [ 2.99792458e5 ], np.float64 )
yLabel1      = ''

saveFileAs = 'fig.' + 'IC' + '.png'

#### ====== End of User Input =======

fig = plt.figure( figsize = (10,6) )

ax0  = fig.add_subplot( 111 )
ax1  = ax0.twinx()

yMin0 = +np.inf
yMax0 = -np.inf
yMin1 = +np.inf
yMax1 = -np.inf
for iID in range( IDs.shape[0] ):

    ID = IDs[iID]

    plotFileBaseName = ID + '.plt_'

    dataDirectory = root + ID + '/'

    for iF0 in range( fields0.shape[0] ):

        field = fields0[iF0]

        data0, DataUnit, r, theta, phi, dr, dtheta, dphi, xL, xU, nX, Time \
          = GetData( dataDirectory, plotFileBaseName, field, \
                     'spherical', True, argv = [ 'a', '0' ], \
                     ReturnTime = True, ReturnMesh = True, Verbose = True )

        data0 /= yScales0[iF0]

        ax0.plot( r, data0, c0[iF0], label = labels0[iF0], markevery = 10 )

        yMin0 = min( yMin0, data0.min() )
        yMax0 = max( yMax0, data0.max() )

    for iF1 in range( fields1.shape[0] ):

        field = fields1[iF1]

        data1, DataUnit, r, theta, phi, dr, dtheta, dphi, xL, xU, nX, Time \
          = GetData( dataDirectory, plotFileBaseName, field, \
                     'spherical', True, argv = [ 'a', '0' ], \
                     ReturnTime = True, ReturnMesh = True, Verbose = True )

        data1 /= yScales1[iF1]

        ax1.plot( r, data1, c1[iF1], label = labels1[iF1], markevery = 10 )

        yMin1 = min( yMin1, data1.min() )
        yMax1 = max( yMax1, data1.max() )

ax0.legend( loc = 3, prop = { 'size' : 15 } )
ax1.legend( loc = 1, prop = { 'size' : 15 } )
ax0.tick_params( axis = 'y', colors = 'r', labelsize = 15 )
ax1.tick_params( axis = 'y', colors = 'b', labelsize = 15 )

ax0.set_ylabel( yLabel0, c = 'r', fontsize = 15 )
ax1.set_ylabel( yLabel1, c = 'b', fontsize = 15 )

ax0.set_ylim( yMin0, yMax0 )
ax1.set_ylim( yMin1, yMax1 )

ax0.set_xlim( 40.0, 360.0 )
ax0.set_xlabel( r'$r\,\left[\mathrm{km}\right]$' )
ax0.grid( axis = 'x', which = 'both' )

if useLogScale0 : ax0.set_yscale( 'log' )
if useLogScale1 : ax1.set_yscale( 'log' )

plt.savefig( '/home/kkadoogan/'+saveFileAs, dpi = 300 )
#plt.show()
plt.close()

import os
os.system( 'rm -rf __pycache__ ' )
