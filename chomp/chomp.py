import datetime

def as_string(datetime_val):

  return datetime_val.strftime("%H:%M:%S")

def chomp_video(infile, start, end, outfile):

  import subprocess
  
  start = datetime.datetime(*start[:6])
  end = datetime.datetime(*end[:6])
  
  duration = end - start
  
  cmd = "ffmpeg -i {input} -vcodec copy -acodec copy -ss {start} -t {duration} {output}".format(input = infile, start = as_string(start), duration=str(duration), output = outfile)
  
  print("Running: " + cmd)
  
  p = subprocess.Popen(cmd)
  ret_code = p.wait()