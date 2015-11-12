function [estimates,ground_truth] = open_and_read(estimates_file_url, ground_truth_file_url)

estimates_translation_start_idx = 1;
estimates_translation_end_idx = 3;
estimates_rotation_start_idx = 4;
estimates_rotation_end_idx = 7;
estimates_articulated_start_idx = 8;
estimates_articualted_end_idx = 11;

estimates_file = fopen(estimates_file_url, 'r');

%open and process the estimate file
tline = fgetl(estimates_file);
n = 1;
while ischar(tline)
  vals = strsplit(tline,' ');
  clear nums;
  for i = 1:size(vals,2)
    if strcmp(vals{i},'')
      continue
    end
    nums(i) = str2double(vals{i});
  end
  
  rotations = quaternion(nums(estimates_rotation_start_idx:estimates_rotation_end_idx));
  %[angle,axis] = rotations.AngleAxis();
  eulers = rotations.EulerAngles('123');
  
  %'rotation', [angle,axis'], ...
  estimates(n) = struct('translation', nums(estimates_translation_start_idx:estimates_translation_end_idx),...
  'rotation', abs(eulers)', ...
  'articulation',nums(estimates_articulated_start_idx:estimates_articualted_end_idx));
  tline = fgetl(estimates_file);
  
  if(sum(isnan(estimates(n).translation)) > 0);
    disp(estimates(n).translation)
    disp(n)
  end

  if(sum(isnan(estimates(n).rotation)) > 0);
    disp(estimates(n).rotation)
    disp(n)
  end
  
  if(sum(isnan(estimates(n).articulation)) > 0);
    disp(estimates(n).articulation)
    disp(n)
  end

  n = n + 1;
  
end

fclose(estimates_file);

%open and process the ground truth file
ground_truth_file = fopen(ground_truth_file_url, 'r');
tline = fgetl(ground_truth_file);
n = 1;
while ischar(tline)
  
  try
    t1 = clean_input_line(tline);
    t2 = clean_input_line(fgetl(ground_truth_file));
    t3 = clean_input_line(fgetl(ground_truth_file));
    fgetl(ground_truth_file); %ignore this line
    fgetl(ground_truth_file); %ignore this line
    a1 = str2double(fgetl(ground_truth_file));
    a2 = str2double(fgetl(ground_truth_file));
    a3 = str2double(fgetl(ground_truth_file));
    fgetl(ground_truth_file); %ignore this line
  catch
    break;
  end
  
  R = zeros(3,3);
  R(1,:) = t1(1:3);
  R(2,:) = t2(1:3);
  R(3,:) = t3(1:3);
  
  %try
  rotations = quaternion.rotationmatrix(R);
  %[angle,axis] = rotations.AngleAxis();
  eulers = rotations.EulerAngles('123');
  %catch
  %  disp(R)
  %  disp(det(R));
  %  assert(0);
  %end
  
  try
    %'rotation', [angle,axis'], ...
    ground_truth(n) = struct('translation', [t1(4),t2(4),t3(4)] ,...
    'rotation', abs(eulers)', ...
    'articulation',[a1,a2,a3]);
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

fclose(ground_truth_file);

end