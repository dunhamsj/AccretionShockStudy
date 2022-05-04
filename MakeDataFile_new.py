#!/usr/bin/env python3

import numpy as np
import os

from UtilitiesModule import Overwrite, GetData, ChoosePlotFile, GetFileArray

def MakeDataFile_new( Field, PlotFileDirectory, DataFileDirectory, \
                      PlotFileBaseName, CoordinateSystem, \
                      SSi = -1, SSf = -1, nSS = -1, \
                      UsePhysicalUnits = True, \
                      MaxLevel = -1, Verbose = False ):

    if Verbose: print( '\nRunning MakeDataFile...\n' )

    OW = Overwrite( DataFileDirectory )

    if OW:

        PlotFileArray = GetFileArray( PlotFileDirectory, PlotFileBaseName, \
                                      Verbose = False )

        # Ensure data directories end in '/'
        if( not PlotFileDirectory[-1] == '/' ): PlotFileDirectory += '/'
        if( not DataFileDirectory[-1] == '/' ): DataFileDirectory += '/'

        if Verbose:
            print( 'PlotFileDirectory: {:}\n'.format( PlotFileDirectory ) )
            print( 'DataFileDirectory: {:}\n'.format( DataFileDirectory ) )

        if SSi < 0: SSi = 0
        if SSf < 0: SSf = PlotFileArray.shape[0] - 1
        if nSS < 0: nSS = PlotFileArray.shape[0]

        TimeHeaderBase = '# Time []: '
        X1Base         = '# X1_C []: '
        X2Base         = '# X2_C []: '
        X3Base         = '# X3_C []: '
        dX1Base        = '# dX1  []: '
        dX2Base        = '# dX2  []: '
        dX3Base        = '# dX3  []: '
        c = 1.0
        if UsePhysicalUnits and CoordinateSystem == 'cartesian':
            TimeHeaderBase = '# Time [ms]: '
            X1Base         = '# X1_C [km]: '
            X2Base         = '# X2_C [km]: '
            X3Base         = '# X3_C [km]: '
            dX1Base        = '# dX1  [km]: '
            dX2Base        = '# dX2  [km]: '
            dX3Base        = '# dX3  [km]: '
            c = 2.99792458e10
        elif UsePhysicalUnits and CoordinateSystem == 'spherical':
            TimeHeaderBase = '# Time [ms]: '
            X1Base         = '# X1_C [km]: '
            X2Base         = '# X2_C [rad]: '
            X3Base         = '# X3_C [rad]: '
            dX1Base        = '# dX1  [km]: '
            dX2Base        = '# dX2  [rad]: '
            dX3Base        = '# dX3  [rad]: '
            c = 2.99792458e10

        os.system( 'rm -rf {:}'.format( DataFileDirectory ) )
        os.system(  'mkdir {:}'.format( DataFileDirectory ) )

        for i in range( nSS ):

            iSS = SSi + np.int64( ( SSf - SSi + 1 ) / nSS ) * i

            PlotFile = PlotFileArray[iSS]

            DataFile = DataFileDirectory + PlotFile + '.dat'

            if Verbose:
                print( 'Generating data file: {:} ({:}/{:})'.format \
                         ( DataFile, i+1, nSS ) )

            Data, DataUnits, \
              X1, X2, X3, dX1, dX2, dX3, xL, xU, nX, Time \
                = GetData( PlotFileDirectory, PlotFileBaseName, Field, \
                           CoordinateSystem, UsePhysicalUnits, \
                           argv = [ 'a', PlotFileArray[iSS] ], \
                           MaxLevel = MaxLevel, \
                           ReturnTime = True, ReturnMesh = True )

            nDimsX = 1
            if( nX[1] > 1 ): nDimsX += 1
            if( nX[2] > 1 ): nDimsX += 1

            if   nDimsX == 1:
                DataShape = '{:d}'.format( X1.shape[0] )
            elif nDimsX == 2:
                DataShape = '{:d} {:d}'.format( X1.shape[0], X2.shape[0] )
            else:
                exit( 'MakeDataFile not implemented for nDimsX > 2' )

            # Save multi-D array with np.savetxt. Taken from:
            # https://stackoverflow.com/questions/3685265/
            # how-to-write-a-multidimensional-array-to-a-text-file

            with open( DataFile, 'w' ) as FileOut:

                FileOut.write( '# {:}\n'.format( DataFile ) )
                FileOut.write( '# Array Shape: {:}\n'.format( DataShape ) )
                FileOut.write( '# Data Units: {:}\n'.format( DataUnits ) )

                TimeHeader = TimeHeaderBase + '{:.16e}\n'.format( Time )
                FileOut.write( TimeHeader )

                FileOut.write( X1Base )
                for iX1 in range( X1.shape[0] ):
                    FileOut.write( str( X1[iX1] ) + ' ' )
                FileOut.write( '\n' )

                FileOut.write( X2Base )
                for iX2 in range( X2.shape[0] ):
                    FileOut.write( str( X2[iX2] ) + ' ' )
                FileOut.write( '\n' )

                FileOut.write( X3Base )
                for iX3 in range( X3.shape[0] ):
                    FileOut.write( str( X3[iX3] ) + ' ' )
                FileOut.write( '\n' )

                FileOut.write( dX1Base )
                for iX1 in range( dX1.shape[0] ):
                    FileOut.write( str( dX1[iX1] ) + ' ' )
                FileOut.write( '\n' )

                FileOut.write( dX2Base )
                for iX2 in range( dX2.shape[0] ):
                    FileOut.write( str( dX2[iX2] ) + ' ' )
                FileOut.write( '\n' )

                FileOut.write( dX3Base )
                for iX3 in range( dX3.shape[0] ):
                    FileOut.write( str( dX3[iX3] ) + ' ' )
                FileOut.write( '\n' )

                np.savetxt( FileOut, Data )

    return

def ReadHeader( DataFile ):

    f = open( DataFile )

    dum = f.readline()

    s = f.readline(); ind = s.find( ':' )+1
    DataShape = list( map( np.int64, s[ind:].split() ) )

    s = f.readline(); ind = s.find( ':' )+1
    DataUnits = s[ind:]

    s = f.readline(); ind = s.find( ':' )+1
    Time = np.float64( s[ind:] )

    s = f.readline(); ind = s.find( ':' )+1
    X1_C = list( map( np.float64, s[ind:].split() ) )

    s = f.readline(); ind = s.find( ':' )+1
    X2_C = list( map( np.float64, s[ind:].split() ) )

    s = f.readline(); ind = s.find( ':' )+1
    X3_C = list( map( np.float64, s[ind:].split() ) )

    s = f.readline(); ind = s.find( ':' )+1
    dX1 = list( map( np.float64, s[ind:].split() ) )

    s = f.readline(); ind = s.find( ':' )+1
    dX2 = list( map( np.float64, s[ind:].split() ) )

    s = f.readline(); ind = s.find( ':' )+1
    dX3 = list( map( np.float64, s[ind:].split() ) )

    f.close()

    return DataShape, DataUnits, Time, X1_C, X2_C, X3_C, dX1, dX2, dX3
