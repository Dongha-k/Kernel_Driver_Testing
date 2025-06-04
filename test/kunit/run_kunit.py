#!/usr/bin/env python3
import argparse
import os
import sys
from shutil import copyfile

assert sys.version_info >= (3, 7), "Python version is too old"

module_name = 'custom_driver'


def copy_files(target, src, test):
    # copy src
    cmd = 'find {} -type f -not -name "*.o*" -not -name "Makefile" -exec cp \'{{}}\' {} \;'.format(
        src, target)
    os.system(cmd)

    # copy kunit test
    cmd = 'find {} -type f -exec cp \'{{}}\' {} \;'.format(test, target)
    os.system(cmd)


def set_misc_configs(misc):
    misc_kconfig = os.path.join(misc, 'Kconfig')
    misc_kconfig_backup = os.path.join(misc, '.Kconfig')
    misc_makefile = os.path.join(misc, 'Makefile')
    misc_makefile_backup = os.path.join(misc, '.Makefile')

    # fisrt copy
    if not os.path.exists(misc_kconfig_backup):
        copyfile(misc_kconfig, misc_kconfig_backup)

    if not os.path.exists(misc_makefile_backup):
        copyfile(misc_makefile, misc_makefile_backup)

    copyfile(misc_kconfig_backup, misc_kconfig)
    copyfile(misc_makefile_backup, misc_makefile)

    with open(misc_kconfig, 'r') as file:
        filedata = file.read()

    # TODO: fix hard coding
    line = 'source "drivers/misc/{}/Kconfig"\nendmenu'.format(module_name)
    # line = 'source "{}/Kconfig"\nendmenu'.format(module_name)
    filedata = filedata.replace('endmenu', line)
    with open(misc_kconfig, 'w') as file:
        file.write(filedata)

    with open(misc_makefile, 'a') as file:
        line = 'obj-y				+= {}/'.format(module_name)
        file.write(line)


def run_kunit(kernel, kunitconfig):
    os.chdir(kernel)

    # UM
    cmd = 'python3 ./tools/testing/kunit/kunit.py run --kunitconfig={}'.format(
        kunitconfig)
    cmd += ' --make_options=CC=gcc'
    # cmd += ' --arch=x86_64'
    ret = os.system(cmd)
    if ret != 0:
        print('KUnit(UM) is failed')
        sys.exit(-1)

    # ARM using QEMU
    cmd += ' --qemu_config=./tools/testing/kunit/qemu_configs/arm.py --cross_compile=armv7l-tizen-linux-gnueabi-'
    # cmd += ' --make_options=CC=gcc-6'
    # ret = os.system(cmd)
    # if ret != 0:
    #    print('KUnit(QEMU: ARM) is failed')
    #    sys.exit(-1)


def main(argv):
    parser = argparse.ArgumentParser(description='Helps running KUnit tests')
    parser.add_argument('--kernel', dest='kernel', type=str,
                        required=True, help='set kernel path which runs KUnit tests.')
    parser.add_argument('--src', dest='src', type=str,
                        default='../../src', help='set src path copied to kernel.')
    args = parser.parse_args()

    # set paths
    kunit = os.path.join(os.getcwd(), 'src')
    misc = os.path.join(args.kernel, 'drivers/misc')
    target = os.path.join(misc, module_name)

    os.makedirs(target, exist_ok=True)

    # copy src and kunit test to kernel
    # copy_files(target, args.src, kunit)

    copy_files(target, ".", kunit)
    copy_files(target, "../../src", kunit)
    copy_files(target, "../../inc", kunit)

    # set Kconfig and Makefile
    set_misc_configs(misc)

    # run kunit
    kunitconfig = os.path.join(target, '.kunitconfig')
    ret = run_kunit(args.kernel, kunitconfig)


if __name__ == '__main__':
    main(sys.argv[1:])
