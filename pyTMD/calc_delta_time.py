#!/usr/bin/env python
u"""
calc_delta_time.py
Written by Tyler Sutterley (07/2020)
Calculates the difference between universal time and dynamical time (TT - UT1)
    following Richard Ray's PERTH3 algorithms

INPUTS:
    delta_file from
        http://maia.usno.navy.mil/ser7/deltat.data
        ftp://cddis.nasa.gov/products/iers/deltat.data
    iMJD: Modified Julian Day of times to interpolate

OUTPUTS:
    deltat: delta time estimates at the output times

PYTHON DEPENDENCIES:
    numpy: Scientific Computing Tools For Python
        https://numpy.org
        https://numpy.org/doc/stable/user/numpy-for-matlab-users.html
    scipy: Scientific Tools for Python
        https://docs.scipy.org/doc/

UPDATE HISTORY:
    Updated 07/2020: added function docstrings. scipy interpolating splines
    Updated 11/2019: pad input time dimension if entering a single value
    Updated 07/2018: linearly extrapolate if using dates beyond the table
    Written 07/2018
"""
import os
import numpy as np
import scipy.interpolate

#-- PURPOSE: calculate the Modified Julian Day (MJD) from calendar date
#-- http://scienceworld.wolfram.com/astronomy/JulianDate.html
def calc_modified_julian_day(YEAR, MONTH, DAY):
    """
    Calculate the Modified Julian Day (MJD) from calendar date

    Arguments
    ---------
    YEAR: calendar month
    MONTH: month of the year
    DAY: day of the month

    Returns
    -------
    MJD: Modified Julian Day (days since 1858-11-17T00:00:00)
    """
    MJD = 367.*YEAR - np.floor(7.*(YEAR + np.floor((MONTH+9.)/12.))/4.) - \
        np.floor(3.*(np.floor((YEAR + (MONTH - 9.)/7.)/100.) + 1.)/4.) + \
        np.floor(275.*MONTH/9.) + DAY + 1721028.5 - 2400000.5
    return np.array(MJD,dtype=np.float)

#-- PURPOSE: calculate the difference between universal time and dynamical time
#-- by interpolating a delta time file to a given Modified Julian Date (MJD)
def calc_delta_time(delta_file,iMJD):
    """
    Calculates the difference between universal time and dynamical time

    Arguments
    ---------
    delta_file: file containing the delta times
    iMJD: Modified Julian Day of times to interpolate

    Returns
    -------
    deltat: delta time at the input time
    """
    #-- read delta time file
    dinput = np.loadtxt(os.path.expanduser(delta_file))
    #-- calculate julian days and convert to MJD
    MJD = calc_modified_julian_day(dinput[:,0],dinput[:,1],dinput[:,2])
    #-- use scipy interpolating splines to interpolate delta times
    spl = scipy.interpolate.UnivariateSpline(MJD,dinput[:,3],k=1,s=0,ext=0)
    #-- return the delta time for the input date
    return spl(iMJD)
