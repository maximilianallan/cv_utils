function [ground_truth] = open_and_read_ground_truth(ground_truth_file_url, skip_articulation)

if nargin == 1
   skip_articulation = 0; 
end

%open and process the ground truth file
ground_truth_file = fopen(ground_truth_file_url, 'r');
tline = fgetl(ground_truth_file);
n = 1;
while ischar(tline)
  
  try
    t1 = clean_input_line(tline);
    t2 = clean_input_line(fgetl(ground_truth_file));
    t3 = clean_input_line(fgetl(ground_truth_file));
    l=fgetl(ground_truth_file); %ignore this line
    l=fgetl(ground_truth_file); %ignore this line
    if skip_articulation == 0
        a1 = str2double(fgetl(ground_truth_file));
        a2 = str2double(fgetl(ground_truth_file));
        a3 = str2double(fgetl(ground_truth_file));
    end
    l=fgetl(ground_truth_file); %ignore this line
  catch
    break;
  end
  
  R = zeros(3,3);

  R(1,:) = t1(1:3);
  R(2,:) = t2(1:3);
  R(3,:) = t3(1:3);

  %try
  rotations = quaternion_from_rotation_matrix(R);
  %[angle,axis] = rotations.AngleAxis();
  eulers = rotations.EulerAngles('321');
  %catch
  %  disp(R)
  %  disp(det(R));
  %  assert(0);
  %end
  
  try
      if skip_articulation == 0
        %'rotation', [angle,axis'], ...
        ground_truth(n) = struct('translation', [t1(4),t2(4),t3(4)] ,...
        'rotation', eulers', ...
        'articulation',[a1,a2,a3]);
      else
        %'rotation', [angle,axis'], ...
        ground_truth(n) = struct('translation', [t1(4),t2(4),t3(4)] ,...
        'rotation', eulers', ...
        'articulation',[0,0,0]);
      end
  catch
    disp(t1)
    disp(t2)
    disp(t3)
    disp(n)
    d = n3;
  end
  
  
  if(sum(isnan(ground_truth(n).translation)) > 0);
    disp(ground_truth(n).translation)
    disp(n)
  end

  if(sum(isnan(ground_truth(n).rotation)) > 0);
    disp(ground_truth(n).rotation)
    disp(n)
  end
  
  if(sum(isnan(ground_truth(n).articulation)) > 0);
    disp(ground_truth(n).articulation)
    disp(n)
  end

  n = n + 1;
  
  tline = fgetl(ground_truth_file); % need to update t1
  
end

num_flipped = 1;
while num_flipped > 0
    [ground_truth,num_flipped] = flip_bad_rotations(ground_truth);
end

fclose(ground_truth_file);

end

function [quat] = quaternion_from_rotation_matrix(rotation_matrix)

t = trace(rotation_matrix);

if t > 0
    
    s = sqrt(t + 1);
    w = 0.5 * s;
    recip = 0.5/s;
    x = (rotation_matrix(3,2) - rotation_matrix(2,3)) * recip;
    y = (rotation_matrix(1,3) - rotation_matrix(3,1)) * recip;
    z = (rotation_matrix(2,1) - rotation_matrix(1,2)) * recip;
    
    quat= quaternion(w, x, y, z);
    
else
    
    i = 1;
    if rotation_matrix(2,2) > rotation_matrix(1,1)
        i = 2;
    end
    if rotation_matrix(3,3) > rotation_matrix(i, i)
        i = 3;
    end
    %j = mod((i + 1), 4) + 1;
    %k = mod((j + 1), 4) + 1;
    
    j = i + 1;
    if j > 3
        j = j - 3;
    end
    
    k = j + 1;
    if k > 3
        k = k - 3;
    end
    
    if i == j || j == k || i == k
       xxxx =0 ; 
    end
    if i + j + k ~= 6
        xxxx = 0;
    end
    
    if i > 3 || j > 3 || k > 3
       xxxx = 0; 
    end
    
    s = sqrt( rotation_matrix(i, i) - rotation_matrix(j, j) - rotation_matrix(k, k) + 1);
    
    vec = [0, 0, 0];
    
    vec(i) = 0.5 * s;
    recip = 0.5 /s;
     
    w = (rotation_matrix(k, j) - rotation_matrix(j, k)) * recip;
    vec(j) = (rotation_matrix(j, i) + rotation_matrix(i, j)) * recip;
    vec(k) = (rotation_matrix(k, i) + rotation_matrix(i, k)) * recip;
        
    quat = quaternion(w, vec(1), vec(2), vec(3));
    
end

end


