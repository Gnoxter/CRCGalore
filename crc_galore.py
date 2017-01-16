#!/usr/bin/env python3
import crcmod
import fileinput
import sys
import argparse


# Data source from:
# The CRC Catalogue: http://reveng.sourceforge.net/crc-catalogue/
# Wikipedia: https://en.wikipedia.org/wiki/Cyclic_redundancy_check#Standards_and_common_use
# The crcmod prededifend/unit tests

crc_params = [
	["CRC-8", 0x107, 0x0, False, 0x00, 0xf4],
	["CRC-8/AUTOSAR", 0x12f, 0x00, False, 0xff, 0xdf], #DOC: init 0xff
	["CRC-8/CDMA2000", 0x19b, 0xff, False, 0x00, 0xda],
	["CRC-8/DARC", 0x139, 0x00, True, 0x00, 0x15],
	["CRC-8/DVB-S2", 0x1d5, 0x00, False, 0x00, 0xbc],
	["CRC-8/EBU", 0x11d, 0xff, True, 0x00, 0x97],
	["CRC-8/I-CODE", 0x11d, 0xfd, False, 0x00, 0x7e],
	["CRC-8/ITU", 0x107, 0x55, False, 0x55, 0xa1],#crc-catalog: init 0x00 crcmod: init 0x55, same check
	["CRC-8/LTE", 0x19b, 0x00, False, 0x00, 0xea],
	["CRC-8/MAXIM", 0x131, 0x00, True, 0x00, 0xa1],
	["CRC-8/OPENSAFETY", 0x12f, 0x00, False, 0x00, 0x3e],
	["CRC-8/ROHC", 0x107, 0xff, True, 0x00, 0xd0],
	["CRC-8/SAE-J1850", 0x11d, 0x00, False, 0xff, 0x4b], #DOC: init 0xff
	["CRC-8/WCDMA", 0x19b, 0x00, True, 0x00, 0x25],

	["ARC", 0x18005, 0x00, True, 0x00, 0xbb3d],
	["CRC-16/AUG-CCITT", 0x11021, 0x1d0f, False, 0x00, 0xe5cc],
	["CRC-16/BUYPASS", 0x18005, 0x00, False, 0x00, 0xfee8],
	["CRC-16/CCITT-FALSE", 0x11021, 0xffff, False, 0x00, 0x29b1],
	["CRC-16/CDMA2000", 0x1c867, 0xffff, False, 0x00, 0x4c06],
	["CRC-16/CMS", 0x18005, 0xffff, False, 0x00, 0xaee7],
	["CRC-16/DDS-110", 0x18005, 0x800d, False, 0x00, 0x9ecf],
	["CRC-16/DECT-R", 0x10589, 0x0001, False, 0x0001, 0x007e], #crc-catalog: init 0x0001 crcmod: init 0x0001, same check
	["CRC-16/DECT-X", 0x10589, 0x00, False, 0x00, 0x007f],
	["CRC-16/DNP", 0x13d65, 0xffff, True, 0xffff, 0xea82], #crc-catalog: init 0x00 crcmod: init 0xffff, same check 
	["CRC-16/EN-13757", 0x13d65, 0xffff, False, 0xffff, 0xc2b7], #crc-catalog: init 0x00 crcmod: init 0xffff, same check
	["CRC-16/GENIBUS", 0x11021, 0x00, False, 0xffff, 0xd64e], #DOC: init 0xffff
	["CRC-16/LJ1200", 0x16f63, 0x00, False, 0x00, 0xbdf4],
	["CRC-16/MAXIM", 0x18005, 0xffff, True, 0xffff, 0x44c2], #crc-catalog: init 0x00 crcmod: init 0xffff, same check
	["CRC-16/MCRF4XX", 0x11021, 0xffff, True, 0x0000, 0x6f91],
#	["CRC-16/OPENSAFETY-A", 0x15935, 0x00, False, 0x00, 0x5d28],
	["CRC-16/OPENSAFETY-B", 0x1755b, 0x00, False, 0x00, 0x20fe],
	["CRC-16/PROFIBUS", 0x11dcf, 0x00, False, 0xffff, 0xa819], #DOC: init 0xffff
	["CRC-16/RIELLO", 0x11021, 0x554d, True, 0x00, 0x63d0], #crc-catalog says init 0xb2aa, crcmod says 0x554d. same check
	["CRC-16/T10-DIF", 0x18bb7, 0x00, False, 0x00, 0xd0db],	
	["CRC-16/TELEDISK", 0x1a097, 0x00, False, 0x00, 0x0fb3],
#	["CRC-16/TMS37157", 0x11021, 0x89ec, True, 0x00, 0x26b1],
	["CRC-16/USB", 0x18005, 0x00, True, 0xffff, 0xb4c8], #DOC: init 0xffff
#	["CRC-A", 0x11021, 0xc6c6, True, 0x00, 0xbf05],
	["KERMIT", 0x11021, 0x00, True, 0x00, 0x2189],
	["MODBUS", 0x18005, 0xffff, True, 0x00, 0x4b37],
	["X-25", 0x11021, 0x00, True, 0xffff, 0x906e], #DOC init 0xffff
	["XMODEM", 0x11021, 0x00, False, 0x00, 0x31c3],

	["CRC-24", 0x1864cfb, 0xb704ce, False, 0x00, 0x21cf02],
#	["CRC-24/BLE", 0x100065b, 0x555555, False, 0x00, 0xc25a56],
	["CRC-24/FLEXRAY-A", 0x15d6dcb , 0xfedcba, False, 0x00, 0x7979bd],
	["CRC-24/FLEXRAY-B", 0x15d6dcb , 0xabcdef, False, 0x00, 0x1f23b8],
	["CRC-24/INTERLAKEN", 0x1328b63, 0x00, False, 0xffffff, 0xb4f3e6], #DOC: init 0xffffff
	["CRC-24/LTE-A", 0x1864cfb, 0x00, False, 0x00, 0xcde703],
	["CRC-24/LTE-B", 0x1800063, 0x00, False, 0x00, 0x23ef52],

	["CRC-32", 0x104c11db7, 0x00, True, 0xffffffff, 0xcbf43926], #DOC: init 0xffffffff
	["CRC-32C",0x11EDC6F41, 0x00, True , 0xffffffff, 0xe3069283],
	["CRC-32D",0x1a833982b, 0x00, True , 0xffffffff, 0x87315576],
	["CRC-32Q", 0x1814141ab, 0x00, False, 0x00, 0x3010bf7f],
	["CRC-32/AUTOSAR", 0x1f4acfb13, 0x00, True, 0xffffffff, 0x1697d06a],
	["CRC-32/BZIP2", 0x104c11db7, 0x00, False, 0xffffffff, 0xfc891918], #DOC: init 0xffffffff
	["CRC-32/MPEG-2", 0x104c11db7, 0xffffffff, False, 0x00, 0x0376e6e7],
	["CRC-32/POSIX", 0x104c11db7, 0xffffffff, False, 0xffffffff, 0x765e7680], #DOC: init 0x0000000
	["CRC-32K Koopman*",  0x1741B8CD7, 0x00, True, 0x00, 0xa55cf835],
	["CRC-32K_2 Koopman*",0x132583499, 0x00, True, 0x00, 0x6425c10],
	["JAMCRC", 0x104c11db7, 0xffffffff, True, 0x00, 0x340bc6d9],
	["XFER", 0x1000000af, 0x00, False, 0x00, 0xbd0be338],

	["CRC-64", 0x142f0e1eba9ea3693, 0x00, False, 0x00, 0x6c40df5f0b497347],
	["CRC-64/WE", 0x142f0e1eba9ea3693, 0x00, False, 0xffffffffffffffff, 0x62ec59e3f1a4f00a], #DOC: init 0xffffffffffffffff
	["CRC-64/XZ", 0x142f0e1eba9ea3693, 0x00, True, 0xffffffffffffffff, 0x995dc9bbdf1939fa], #DOC: init 0xffffffffffffffff
	["CRC-64/Jones", 0x1AD93D23594C935A9, 0xffffffffffffffff, True, 0x00, 0xCAA717168609F281],
	["CRC-64/ISO*", 0x1000000000000001B, 0x00, True, 0x00, 0x46a5a9388a5beffe],
]


def crc_format(self, format_spec):
	x = " "*int(16-self.w)
	rev = "REVERSED " if self.reverse else ""
	perm = "PERMUTATION" if self.permutation else "" 
	fmt = "%s{:0{zpad}x} poly: %s{:0{zpad}x} init: %s{:0{zpad}x} xor: %s{:0{zpad}x} {}{}" % (x, x, x, x)
	return fmt.format(self.crcValue, self.poly, self.initCrc, self.xorOut, rev, perm, zpad=self.w)

def init_crcs(crc_params):
	crcs = []
	for item in crc_params:
		crc = crcmod.Crc(item[1], initCrc=item[2], rev=item[3], xorOut=item[4])
		test = crc.copy()
		crc.name = item[0]
		crc.permutation = False
		crc.w = int(width(crc.poly)/4)
		test.update(b"123456789")
		if test.crcValue != item[5]:
			print("Test for %s failed: expected: %x got: %x" % (item[0], item[5], test.crcValue))
			sys.exit()
		crcs.append(crc)

	return crcs

def init_crcs_permutation(crc_params):
	crcs = []
	for seed in crc_params:
		crc = crcmod.Crc(seed[1], initCrc=0x00, rev=True, xorOut=0x00)
		crc.name = seed[0]
		crc.permutation = True
		crc.w = int(width(crc.poly)/4)
		crcs.append(crc)

		crc = crcmod.Crc(seed[1], initCrc=0x00, rev=False, xorOut=0x00)
		crc.name = seed[0]
		crc.permutation = True
		crc.w = int(width(crc.poly)/4)
		crcs.append(crc)

		crc = crcmod.Crc(seed[1], initCrc=0x00, rev=True, xorOut=0xffffffff)
		crc.name = seed[0]
		crc.permutation = True
		crc.w = int(width(crc.poly)/4)
		crcs.append(crc)

		crc = crcmod.Crc(seed[1], initCrc=0x00, rev=False, xorOut=0xffffffff)
		crc.name = seed[0]
		crc.permutation = True
		crc.w = int(width(crc.poly)/4)
		crcs.append(crc)
	
	return crcs

def width(poly):
	w = 0
	while poly:
		poly = poly >> 1;
		w += 1
	return w

def max_length_name(crcs):
	l = 0
	for crc in crcs:
		l = max(len(crc.name), l)
	return l

def calculate_file(filename, permutate):
	with open(filename, "rb") as f:
		while True:
			data = f.read(1024)
			if not data:
				break
			for crc in crcs:
				crc.update(data)

	max_string_len = max_length_name(crcs)

	for index, crc in enumerate(crcs):
		fmt = "{:2} {:{spad}} {}"
		print(fmt.format(index, crc.name, crc, spad=max_string_len))


parser = argparse.ArgumentParser(description='Calculates the CRC Sums for a given file. Useful to find the algorithm used for a given file and checksum without reverse engineering.')
parser.add_argument("-p", "--permutate", help="Permutate to create non-standard configuration",action="store_true")
group = parser.add_mutually_exclusive_group()
group.add_argument("-l", "--list", help="List available CRC Algorithms", action="store_true")
group.add_argument("-c", "--code", help="Output C-Code for given CRC Algorithm", type=int)
group.add_argument("-f", "--file", help="Calculate CRCs for given file", type=str)

args = parser.parse_args()

if not args.file and not args.list and not args.code:
	parser.print_help()
	sys.exit()


crcmod.Crc.__format__ = crc_format
crcs = init_crcs(crc_params)

if args.permutate:
	crcs += init_crcs_permutation(crc_params)

if args.file:
	calculate_file(args.file, args.permutate)

if args.list:
	for index, crc in enumerate(crcs):
		print("{:3}: {:{spad}} {}".format(index, crc.name, crc, spad=max_length_name(crcs)))

if args.code:
	if not args.permutate:
		crcs += init_crcs_permutation(crc_params)

	if args.code <= len(crcs) and args.code >= 0:
		print("// {} {}".format(crcs[args.code].name, crcs[args.code]))
		crcs[args.code].generateCode("crc", sys.stdout)
	else:
		print("Unknown algorithm")
