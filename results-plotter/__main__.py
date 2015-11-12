import os
import argparse


if __name__ == '__main__':

  parser = argparse.ArgumentParser(description='')
  parser.add_argument('--output-dir', type=str, help='', required=True)
  parser.add_argument('--my-method-file', type=str, help=' ', required=True)
  parser.add_argument('--ground-truth-file', type=str, help='', required=True)
  parser.add_argument('--comparison-file', type=str, help='', required=True)
  parser.add_argument('--skip-frames', type=int, help='', default=0)
  parser.add_argument('--method-name', type=str, help='The name of the method we are testing', required=True)
  parser.add_argument('--comparison-method-name', type=str, help='The name of the method we are comparing against', required=True)

  args = parser.parse_args()

  if not os.path.exists(args.my_method_file) or not os.path.exists(args.ground_truth_file):

    print("Error, could not find method or ground truth file")
    parser.print_help()
    import sys
    sys.exit(1)

  import subprocess

  cwd = os.getcwd()

  try:

    #output_directory = os.path.dirname(args.my_method_file)

    mlab_args = "\'{0}\' {1} \'{2}\' \'{3}\' \'{4}\' \'{5}\' \'{6}\'".format(args.output_dir, args.skip_frames, args.my_method_file, args.ground_truth_file, args.comparison_file, args.method_name, args.comparison_method_name)
    to_run = "{0} {1}".format("process_results", mlab_args)

    os.chdir("C:/Users/max/libs/cv_utils/results-plotter/")

    #it
    p = subprocess.Popen("matlab -nodisplay -nosplash -nodesktop -r \"{0}\"".format(to_run), shell=True)
    p.wait()

  except Exception as e:

    print e.args

  else:

    os.chdir(cwd)

