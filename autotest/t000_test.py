# Remove the temp directory and then create a fresh one
import os
import sys
import shutil
import platform
import flopy
import pymake

fc = 'gfortran'
cc = 'gcc'
double = False
bindir = os.path.join(os.path.expanduser('~'), '.local', 'bin')
print(bindir)


def test_setup():
    tempdir = os.path.join('.', 'temp')
    if os.path.isdir(tempdir):
        shutil.rmtree(tempdir)
    os.mkdir(tempdir)
    return


def test_build_modflow():
    starget = 'MODFLOW-2005'
    exe_name = 'mf2005'
    dirname = 'MF2005.1_12u'
    url = "https://water.usgs.gov/ogw/modflow/MODFLOW-2005_v1.12.00/MF2005.1_12u.zip"

    build_target(starget, exe_name, url, dirname)

    return


def test_build_mfnwt():
    starget = 'MODFLOW-NWT'
    exe_name = 'mfnwt'
    dirname = 'MODFLOW-NWT_1.1.2'
    url = "http://water.usgs.gov/ogw/modflow-nwt/{0}.zip".format(dirname)

    build_target(starget, exe_name, url, dirname)

    return


def test_build_usg():
    starget = 'MODFLOW-USG'
    exe_name = 'mfusg'
    dirname = 'mfusg.1_3'
    url = 'http://water.usgs.gov/ogw/mfusg/{0}.zip'.format(dirname)

    build_target(starget, exe_name, url, dirname)
    return


def set_compiler():
    fct = fc
    cct = cc
    # parse command line arguments to see if user specified options
    # relative to building the target
    msg = ''
    for idx, arg in enumerate(sys.argv):
        if arg.lower() == '--ifort':
            if len(msg) > 0:
                msg += '\n'
            msg += '{} - '.format(arg.lower()) + \
                   '{} will be built with ifort.'.format(starget)
            fct = 'ifort'
        elif arg.lower() == '--cl':
            if len(msg) > 0:
                msg += '\n'
            msg += '{} - '.format(arg.lower()) + \
                   '{} will be built with cl.'.format(starget)
            cct = 'cl'
        elif arg.lower() == '--clang':
            if len(msg) > 0:
                msg += '\n'
            msg += '{} - '.format(arg.lower()) + \
                   '{} will be built with clang.'.format(starget)
            cct = 'clang'
    if len(msg) > 0:
        print(msg)

    return fct, cct


def build_target(starget, exe_name, url, dirname):
    print('Determining if {} needs to be built'.format(starget))
    if platform.system().lower() == 'windows':
        exe_name += '.exe'

    exe_exists = flopy.which(exe_name)
    if exe_exists is not None:
        print('No need to build {} since it exists in the current path')
        return

    fct, cct = set_compiler()

    # set up target
    target = os.path.abspath(os.path.join(bindir, exe_name))

    # get current directory
    cpth = os.getcwd()

    # create temporary path
    dstpth = os.path.join('tempbin')
    print('create...{}'.format(dstpth))
    if not os.path.exists(dstpth):
        os.makedirs(dstpth)
    os.chdir(dstpth)

    # Download the distribution
    pymake.download_and_unzip(url)

    # Set srcdir name
    srcdir = os.path.join(dirname, 'src')

    # compile code
    print('compiling...{}'.format(os.path.relpath(target)))
    pymake.main(srcdir, target, fct, cct, makeclean=True,
                expedite=False, dryrun=False, double=double, debug=False)

    msg = '{} does not exist.'.format(os.path.relpath(target))
    assert os.path.isfile(target), msg

    # change back to original path
    os.chdir(cpth)

    # Clean up downloaded directory
    print('delete...{}'.format(dstpth))
    if os.path.isdir(dstpth):
        shutil.rmtree(dstpth)

    return


if __name__ == '__main__':
    test_setup()
    test_build_modflow()
    test_build_mfnwt()
    test_build_usg()
