# -*- coding: utf-8 -*-
"""
installs non-python executables for the gnssrefl code
"""
import argparse
import wget
import os
import subprocess
import sys
from shutil import which 


def checkexist(exe):
    """
    exe - executable name to check
    """

    exists = which(exe)
    if exists is None:
        print(exe + ' does not exist on your system. You need to install it.')


def download_chmod_move(url,savename,exedir):
    """
    inputs are url, filename and executable directory
    it should chmod g+rwx and  move to exe area
    """
    f = exedir + '/' + savename
    if os.path.exists(f):
        print('You already have this executable: '+ savename)
    else:
        wget.download(url,savename)
        os.chmod(savename,0o777)
        subprocess.call(['mv', '-f',savename, exedir])
        print('\n Executable stored:', savename)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("opsys", help="operating system (linux64, macos, or mac-newchip)", type=str)
    args = parser.parse_args().__dict__

    # only return a dictionary of arguments that were added from the user - all other defaults will be set in code below
    return {key: value for key, value in args.items() if value is not None}


def installexe(opsys: str):
    """
        Command line interface to install non-python executables, specifically
        CRX2RNX and gfzrnx. downloading Teqc will be an added feature here in the future.
        https://stackoverflow.com/questions/12791997/how-do-you-do-a-simple-chmod-x-from-within-python

        note: this code used to try to download fortran exe but this is no longer necessary
        because we have the fortran code within gnssrefl

        Parameters:
        ___________
        opsys : string
            operating system (linux64 or macos)
    """

    exedir = os.environ['EXE']
    if not os.path.exists(exedir):
        print('You need to define the EXE environment variable. Exiting')
        sys.exit()
    else:
        print('Your executable environment area: ', exedir)

    checkexist('gzip')
    checkexist('xz')
    checkexist('unzip')
    checkexist('compress')
    checkexist('wget')

    # where the executable files are (currently) stored publicly

    sto = 'https://morefunwithgps.com/public_html/'

    if (opsys == 'linux64'):
        print('Only 64 bit static versions will be provided.')
        print('For 32 bit you will need to check the appropriate websites.')
        savename = 'CRX2RNX'
        url = sto + savename + '.' + opsys + '.e'
        download_chmod_move(url, savename, exedir)

        savename = 'gfzrnx'
        url = sto + 'gfzrnx.' + opsys + '.e'
        download_chmod_move(url, savename, exedir)

        savename = 'teqc'
        if os.path.exists(exedir + '/' + savename):
            print('Executable already exists:', savename)

        else:
            # static executable 64bit
            url = 'https://www.unavco.org/software/data-processing/teqc/development/teqc_CentOSLx86_64s.zip'
            print('Downloading teqc from: ', url)
            try:
                wget.download(url, savename + '.zip')
                subprocess.call(['unzip', savename + '.zip' ])
                subprocess.call(['mv', '-f', savename, exedir])
                subprocess.call(['rm', '-f', savename + '.zip' ])
                print('\n Executable stored:', savename)
            except:
                print('Some kind of kerfuffle trying to install teqc')

    elif (opsys == 'macos'):
        savename = 'CRX2RNX'
        url = sto + savename + '.' + opsys + '.e'
        download_chmod_move(url, savename, exedir)

        savename = 'teqc'
        if os.path.exists(exedir + '/' + savename):
            print('Executable already exists:', savename)
        else:
        # added 2021sep13
            url = 'https://www.unavco.org/software/data-processing/teqc/development/teqc_OSX_i5_gcc4.3d_64.zip'
            print('Downloading teqc from: ', url)
            try:
                wget.download(url, savename + '.zip')
                subprocess.call(['unzip', savename + '.zip' ])
                subprocess.call(['mv', '-f', savename, exedir])
                subprocess.call(['rm', '-f', savename + '.zip' ])
                print('\n Executable stored:', savename)
            except:
                print('Some kind of kerfuffle trying to install teqc')

        savename = 'gfzrnx'
        url = sto + 'gfzrnx.' + opsys + '.e'
        download_chmod_move(url, savename, exedir)
    elif (opsys == 'mac-newchip'):
        print('The Hatanaka CRX2RNX source code will be compiled. This requires gcc.')
        print('There is no teqc executable for this architecture, so none will be installed.')

    else:
        print('We do not recognize your operating system input. Exiting.')
        sys.exit()


def main():
    args = parse_arguments()
    installexe(**args)


if __name__ == "__main__":
    main()
