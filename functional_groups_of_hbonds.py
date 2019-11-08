from __future__ import division, absolute_import, print_function

import sys
import csv
import argparse

from ccdc.io import CrystalReader
from ccdc.descriptors import CrystalDescriptors
import glob
from ccdc import crystal

################################################################################

class Runner(argparse.ArgumentParser):
    '''Defines and parses arguments, runs the job.'''
    def __init__(self):
        super(self.__class__, self).__init__(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
        self.add_argument(
            'gcd_file',
            help='GCD file of crystal structures to analyse'
        )
        self.add_argument(
            '-o', '--output-file', default=None,
            help='Output csv file [stdout]'
        )
        self.args = self.parse_args()

    def run(self):
        '''Runs the job.'''
        calculator = CrystalDescriptors.HBondCoordination()
	path_list = glob.glob (self.args.gcd_file + '*.cif')
	reader = []
	for path in path_list:
	    print (path)
	    with open(path) as file:
	        s = file.read()
	    try:
	        reader.append(crystal.Crystal.from_string(s, format = 'cif'))
	    except Exception as e:
		print (e)
        if self.args.output_file:
            f = open(self.args.output_file, 'w')
        else:
            f = sys.stdout
        headers = [
            'Identifier', 'hydrogen bonds observed', 'observed details'
        ]
	print ("finished read files")
        writer = csv.writer(f)
        writer.writerow(headers)
        def get_residue(crystal, label):
            for i, c in enumerate(crystal.molecule.components):
                try:
                    c.atom(label)
                    return 'RES%d' % (i+1)
                except RuntimeError:
                    pass
            raise RuntimeError('Ambiguous atom label %s' % label)


        for c in reader:
            if c.has_disorder:
		print (c.identifier)
                continue
            predictions = calculator.predict(c)
            row = [
                c.identifier,
                len(predictions.observed),
                [predictions.observed]
            ]
            writer.writerow(row)

################################################################################

if __name__ == '__main__':
    Runner().run()
