import argparse
import sys
from parse import process,interpolate, run_dvrk

if __name__ == '__main__':

  parser = argparse.ArgumentParser(description='Process motor from the da Vinci to usable format.')
  parser.add_argument('--suj-input', type=str, help='An input file containing set up joint data.')
  parser.add_argument('--j-input', type=str, help='An input file containing joint data.')
  parser.add_argument('--suj-output', type=str, help='The output set-up joint file to save the processed set-up joint data.')
  parser.add_argument('--j-output', type=str, help='The output joint file to save the processed joint data.')
  parser.add_argument('--num-vals', type=int, help='The number of vals to parse.')
  #parser.add_argument('--rigid', dest='rigid', action="store_true", help='Only load the rigid pose parameter - i.e. ignore the articulated head.')
  #parser.add_argument('--interpolate', type=int, help='Interpolate the values for smoother motion', default=1)
  args = parser.parse_args()
  
  run_dvrk(args.suj_input, args.j_input, args.suj_output, args.j_output, args.num_vals)
