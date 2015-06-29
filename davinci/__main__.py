import argparse
import sys
from parse import process,interpolate, run

if __name__ == '__main__':

  parser = argparse.ArgumentParser(description='Process motor from the da Vinci to usable format.')
  parser.add_argument('infile', type=str, help='An input file containing joint data.')
  parser.add_argument('suj_outfile', type=str, help='The output set-up joint file to save the processed set-up joint data.')
  parser.add_argument('j_outfile', type=str, help='The output joint file to save the processed joint data.')
  parser.add_argument('--rigid', dest='rigid', action="store_true", help='Only load the rigid pose parameter - i.e. ignore the articulated head.')
  parser.add_argument('--interpolate', type=int, help='Interpolate the values for smoother motion', default=1)
  args = parser.parse_args()
  
  run(args.infile, args.suj_outfile, args.j_outfile, args.interpolate, args.rigid)
