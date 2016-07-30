function [estimates] = open_and_read_estimates(estimates_file_url, do_clean_articulation, skip_articulation)

if nargin == 1
    do_clean_articulation = 0;
    skip_articulation = 0;
end

estimates_translation_start_idx = 1;
estimates_translation_end_idx = 3;
estimates_rotation_start_idx = 4;
estimates_rotation_end_idx = 7;
estimates_articulated_start_idx = 8;
estimates_articulated_end_idx = 10;

if do_clean_articulation == 1
   estimates_articulated_end_idx = 11;
end

estimates_file = fopen(estimates_file_url, 'r');

%open and process the estimate file
tline = fgetl(estimates_file);
n = 1;


while ischar(tline)
    
  if isempty(tline) 
      tline = fgetl(estimates_file);
      continue;
  end
    
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
  eulers = rotations.EulerAngles('321');
  

  if skip_articulation == 0
    %'rotation', [angle,axis'], ...
    estimates(n) = struct('translation', nums(estimates_translation_start_idx:estimates_translation_end_idx),...
    'rotation', eulers', ...
    'articulation',nums(estimates_articulated_start_idx:estimates_articulated_end_idx));
  else
    %'rotation', [angle,axis'], ...
    estimates(n) = struct('translation', nums(estimates_translation_start_idx:estimates_translation_end_idx),...
    'rotation', eulers', ...
    'articulation',[0,0,0]);
  end
  
  if do_clean_articulation == 1
    estimates(n).articulation = clean_articulation(estimates(n).articulation);
  end
  
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

  tline = fgetl(estimates_file);
  n = n + 1;
  
end

num_flipped = 1;
while num_flipped > 0
    [estimates,num_flipped] = flip_bad_rotations(estimates);
end

fclose(estimates_file);

end


function [cleaned_articulation] = clean_articulation(dirty_articulation)

head_angle = dirty_articulation(1);
wrist_angle = dirty_articulation(2);
%clasper_angle = dirty_articulation(3);
clasper_angle = (dirty_articulation(3) * 2);
%clasper_2_angle = dirty_articulation(4) * 2;

cleaned_articulation = [head_angle, wrist_angle, clasper_angle];

end