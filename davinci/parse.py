import sys
import re

targets = [
  "ISI_TIP_TRANSFORM",
  "ISI_RCM_TRANSFORM",
  "ISI_MOUNT_TRANSFORM",
  "ISI_JOINT_VALUES",
  "ISI_SUJ_JOINT_VALUES",
  ]

def isfloat(val):
  try:
    float(val)
    return True
  except:
    return False

    
    
def run_dvrk(suj_infile, j_infile, suj_outfile, j_outfile, LINES_NUM, is_ecm = False):
  
  try:
    with open(suj_infile,"r") as infile:

      suj_value = extract(infile, "ISI_SUJ_JOINT_VALUES")
      
      with open(suj_outfile,"w") as outfile:
        for i in range(LINES_NUM):
          outfile.write(suj_value)
      
    if is_ecm:
    
      with open(j_infile,"r") as infile:

        j_value = extract(infile, "ISI_JOINT_VALUES")
      
      with open(j_outfile,"w") as outfile:
        for i in range(LINES_NUM):
          outfile.write(j_value)
    else:
      
      with open(j_infile, "r") as infile:
        
        l = infile.readlines()
        
        with open(j_outfile, "w") as outfile:
        
          for ll in l:
            ll_nl = ll.replace(",", " ")
            outfile.write(ll_nl)
          
        
      
      
      
  except IOError:
    print("\nError, could not find input file: {0}\n".format(suj_infile))
    sys.exit(1)


 
def run(infile, suj_outfile, j_outfile, interpolate_val, rigid_only):

  try:
    with open(infile,"r") as infile:

      
      try:
        with open(suj_outfile,"w") as outfile:
          process(infile,outfile,"ISI_SUJ_JOINT_VALUES",False)
        with open(suj_outfile,"r+") as outfile:
          interpolate(outfile,outfile,interpolate_val)
      except IOError,OSError:
        print("\nError, could not find output file: {0}\n".format(suj_outfile))
        sys.exit(1)
      
      
      infile.seek(0,0) # back to start
      try:
        with open(j_outfile,"w") as outfile:
          process(infile,outfile,"ISI_JOINT_VALUES",rigid_only)
        with open(j_outfile,"r+") as outfile:
          interpolate(outfile,outfile,interpolate_val)
      except IOError,OSError:
        print("\nError, could not find output file: {0}\n".format(j_outfile))
        sys.exit(1)

  except IOError:
    print("\nError, could not find input file: {0}\n".format(infile))
    sys.exit(1)


def splitoncolon(line):

  if len(line.split(":")) == 1:
    return line
  else:
    sp = line.split(":")
    return "".join(sp[1:])

def extract(infile, target):

  lines = infile.read().split(target)[1:-1] #first value will not be useful
  for line in [ l for l in lines if l != "" ]:
    line = line.strip("\r\n").split("\n")
    line = line[0:line.index("")] #get vals up to first empty
    for n,l in enumerate(line):
      if n > 3 and rigid_only: #this will only be the case if we are parsing SUJs and Js.
        outfile.write("0\n")
        continue
      l = splitoncolon(l)
      sp = " ".join([f for f in re.split("[ ,]",l) if f != ""])
      return sp
    
def process(infile,outfile,target,rigid_only):

  lines = infile.read().split(target)[1:-1] #first value will not be useful
  for line in [ l for l in lines if l != "" ]:
    line = line.strip("\r\n").split("\n")
    line = line[0:line.index("")] #get vals up to first empty
    for n,l in enumerate(line):
      if n > 3 and rigid_only: #this will only be the case if we are parsing SUJs and Js.
        outfile.write("0\n")
        continue
      l = splitoncolon(l)
      sp = " ".join([f for f in re.split("[ ,]",l) if f != ""])
      outfile.write(sp + "\n")
    outfile.write("\n")

    
def interpolate_lines(l0, l1, num_steps):

  l0 = l0.split("\n")
  l1 = l1.split("\n") 
  try:
    l0 = map(float,l0)
    l1 = map(float,l1)
  except:
    print l0
    print l1
    sys.exit(1)
  
  grads = [ (v1 - v0)/num_steps for v0,v1 in zip(l0,l1) ]
  
  for num in range(num_steps):
    ret = ""
    for i in range(len(grads)):
      ret += "{0}\n".format(l0[i] + (num * grads[i]))
    yield ret
    
def interpolate(infile,outfile,num_steps):

  """
  linearly interpolate between joint values to make motion smaller for synthetic validation
  """
    
  lines = infile.read()
  lines = lines.split("\n\n")
  
  lines = [l for l in lines if l != '']
  
  interpolated_lines = []
   
  for i in range(len(lines)-1):
  
    l0 = lines[i]
    l1 = lines[i+1]
    
    for interpolated_line in interpolate_lines(l0,l1,num_steps):
      interpolated_lines.append(interpolated_line)
    
  outfile.seek(0,0)
  
  for interpolated_line in interpolated_lines:
    outfile.write(interpolated_line + "\n")
  
  

