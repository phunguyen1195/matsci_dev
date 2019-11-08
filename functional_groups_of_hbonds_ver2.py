from __future__ import division, absolute_import, print_function

import sys
import csv
import argparse
import pandas as pd
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
	print ("finished read files")
        identifier = []
	number_of_hbonds_observed = []
	label = []
	coordination_count = []
	p = []
	df_detail = []


        for c in reader:
            if c.has_disorder:
		print (c.identifier)
                continue
            predictions = calculator.predict(c)
            identifier.append(c.identifier)
	    number_of_hbonds_observed.append(len(predictions.observed))
	    for i in predictions.observed:
	        label.append(i.label)
		coordination_count.append(i.coordination_count)
		p.append(i.probability)
	    df_get_detail = pd.DataFrame(data={"label": label, "coordination_count": coordination_count, "probability": p})
	    df_detail.append(df_get_detail)
	df = pd.DataFrame(data = {"identifier": identifier, "number of hbonds observed": number_of_hbonds_observed, "observed details": df_detail})
	df.to_csv(self.args.output_file)
################################################################################

if __name__ == '__main__':
    Runner().run()
