function process_results

%SKIPPING THE FIRST 59 FRAMES

output_dir = 'Z:/phd/ttrack/data/dvrk/run_save_ipcai2/';
estimates_file_url = strcat(output_dir,'tracked_model0.txt');
estimates_file_url2 = strcat(output_dir,'tracked_model1.txt');

ground_truth_file_url = 'Z:/phd/data/processed/dataset-dvrk/trackables/psm1/psm1_se3.txt';
ground_truth_file_url2 = 'Z:/phd/data/processed/dataset-dvrk/trackables/psm2/psm2_se3.txt';

original_method_url = 'z:/phd/ttrack/data/dvrk/run_save_tbme/tracked_model0.txt';
original_method_url2 = 'z:/phd/ttrack/data/dvrk/run_save_tbme/tracked_model1.txt';

[estimates,ground_truth] = open_and_read(estimates_file_url, ground_truth_file_url);
[comparison,~] = open_and_read(original_method_url, ground_truth_file_url);

[estimates2,ground_truth2] = open_and_read(estimates_file_url2, ground_truth_file_url2);
[comparison2,~] = open_and_read(original_method_url2, ground_truth_file_url2);

close all;

num_frames_alt = size(ground_truth,2);
if size(ground_truth2,2) < num_frames_alt
  num_frames_alt = size(ground_truth2,2);
end
ground_truth = ground_truth(59:num_frames_alt);
ground_truth2 = ground_truth2(59:num_frames_alt);
num_frames_alt = size(ground_truth,2);

estimates = estimates(1:num_frames_alt);
comparison = comparison(1:num_frames_alt);
estimates2 = estimates2(1:num_frames_alt);
comparison2 = comparison2(1:num_frames_alt);

num_frames = size(estimates,2);

assert(num_frames == num_frames_alt);
assert(num_frames == size(comparison,2));

create_trajectory_plots([estimates,estimates2], [comparison,comparison2], [ground_truth,ground_truth2], 2*num_frames, output_dir, 'LS + SIFT', 'LS');
create_error_plots([estimates;estimates2], [comparison;comparison2], [ground_truth;ground_truth2], num_frames, output_dir, 'LS + SIFT', 'LS');


%create error plots for x,y,z,r

end

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
  [angle,axis] = rotations.AngleAxis();
  
  estimates(n) = struct('translation', nums(estimates_translation_start_idx:estimates_translation_end_idx),...
  'rotation', [angle,axis'], ...
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
  
  %try
    t1 = clean_input_line(tline);
    t2 = clean_input_line(fgetl(ground_truth_file));
    t3 = clean_input_line(fgetl(ground_truth_file));
    fgetl(ground_truth_file); %ignore this line
    fgetl(ground_truth_file); %ignore this line
    a1 = str2double(fgetl(ground_truth_file));
    a2 = str2double(fgetl(ground_truth_file));
    a3 = str2double(fgetl(ground_truth_file));
    fgetl(ground_truth_file); %ignore this line
  %catch
  %  break;
  %end
  
  R = zeros(3,3);
  R(1,:) = t1(1:3);
  R(2,:) = t2(1:3);
  R(3,:) = t3(1:3);
  
  %try
  rotations = quaternion.rotationmatrix(R);
  [angle,axis] = rotations.AngleAxis();
  %catch
  %  disp(R)
  %  disp(det(R));
  %  assert(0);
  %end
  
  try
    ground_truth(n) = struct('translation', [t1(4),t2(4),t3(4)] ,...
  'rotation', [angle,axis'], ...
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

function cleaned = clean_input_line(line)

assert( size(line,2) ~= 50 );
  

start_offset = 3;
chunk_size = 11;
idx = start_offset;
for i = 1:4
  x = line(idx:idx+chunk_size);
  cleaned(i) = str2double(x); 
  idx = idx + chunk_size + 1;
end

%vals = strsplit(regexprep(regexprep(line, '^[^A-Za-z0-9_.- ]*', ''), '[^A-Za-z0-9_.- ]', ''),' ');
%clear nums;
%c = 1;
%for i = 1:size(vals,2)
%  if strcmp(vals{i},'')
%    continue
%  end
%  nums(c) = str2double(vals{i});
% c = c + 1;
%nd
%leaned = nums;
%end

end

function [] = create_error_plots(estimates, comparison, ground_truth, num_frames, save_dir, estimates_method_name, comparison_method_name)

x_error = zeros(1,num_frames);
y_error = zeros(1,num_frames);
z_error = zeros(1,num_frames);
x_error_comparison = zeros(1,num_frames);
y_error_comparison = zeros(1,num_frames);
z_error_comparison = zeros(1,num_frames);

t_error_comparison = zeros(1,num_frames);
t_error = zeros(1,num_frames);

r_axis_error_comparison = zeros(1,num_frames);
r_angle_error_comparison = zeros(1, num_frames);
r_axis_error = zeros(1,num_frames);
r_angle_error = zeros(1, num_frames);

for i = 1:num_frames
  t_error(i) = (pdist([estimates(1,i).translation;ground_truth(1,i).translation]) + pdist([estimates(2,i).translation;ground_truth(2,i).translation]))/2;
  t_error_comparison(i) = (pdist([comparison(1,i).translation;ground_truth(1,i).translation]) + pdist([comparison(2,i).translation;ground_truth(2,i).translation]))/2;
  
  x_error(i) = (pdist([estimates(1,i).translation(1);ground_truth(1,i).translation(1)]) + pdist([estimates(2,i).translation(1);ground_truth(2,i).translation(1)]))/2;
  x_error_comparison(i) = (pdist([comparison(1,i).translation(1);ground_truth(1,i).translation(1)]) + pdist([comparison(2,i).translation(1);ground_truth(2,i).translation(1)]))/2;
  
  y_error(i) = (pdist([estimates(1,i).translation(2);ground_truth(1,i).translation(2)]) + pdist([estimates(2,i).translation(2);ground_truth(2,i).translation(2)]))/2;
  y_error_comparison(i) = (pdist([comparison(1,i).translation(2);ground_truth(1,i).translation(2)]) + pdist([comparison(2,i).translation(2);ground_truth(2,i).translation(2)]))/2;
  
  z_error(i) = (pdist([estimates(1,i).translation(3);ground_truth(1,i).translation(3)]) + pdist([estimates(2,i).translation(3);ground_truth(2,i).translation(3)]))/2;
  z_error_comparison(i) = (pdist([comparison(1,i).translation(3);ground_truth(1,i).translation(3)]) + pdist([comparison(2,i).translation(3);ground_truth(2,i).translation(3)]))/2;
  
  e = estimates(1,i).rotation(2:4)/norm(estimates(1,i).rotation(2:4));
  e_comparison = comparison(1,i).rotation(2:4)/norm(comparison(1,i).rotation(2:4));
  g = (ground_truth(1,i).rotation(2:4)/norm(ground_truth(1,i).rotation(2:4)))';
  
  e2 = estimates(2,i).rotation(2:4)/norm(estimates(2,i).rotation(2:4));
  e_comparison2 = comparison(2,i).rotation(2:4)/norm(comparison(2,i).rotation(2:4));
  g2 = (ground_truth(2,i).rotation(2:4)/norm(ground_truth(2,i).rotation(2:4)))';
  
  r_axis_error_comparison(i) = (acos(e_comparison*g) + acos(e_comparison2*g2))/2;
  r_angle_error_comparison(i) = (pdist([comparison(1,i).rotation(1);ground_truth(1,i).rotation(1)]) + pdist([comparison(2,i).rotation(1);ground_truth(2,i).rotation(1)]))/2;
  r_axis_error(i) = (acos(e*g) + acos(e2*g2))/2;
  r_angle_error(i) = (pdist([estimates(1,i).rotation(1);ground_truth(1,i).rotation(1)]) + pdist([estimates(2,i).rotation(1);ground_truth(2,i).rotation(1)]))/2;
  
end

f = fopen(strcat(save_dir,'numerical_errors.txt'),'w');

fprintf(f,'Numerical errors:\n\n');

fprintf(f,'Mean x error %s : %f\n', estimates_method_name, mean(x_error) );
fprintf(f,'Std. Dev. x error %s : %f\n', estimates_method_name, std(x_error));
fprintf(f,'Mean x error %s : %f\n', comparison_method_name, mean(x_error_comparison));
fprintf(f,'Std. Dev. x error %s : %f\n',  comparison_method_name, std(x_error_comparison));
fprintf(f,'\n');

fprintf(f,'Mean y error %s : %f\n', estimates_method_name, mean(y_error));
fprintf(f,'Std. Dev. y error %s : %f\n', estimates_method_name, std(y_error) );
fprintf(f,'Mean y error %s : %f\n', comparison_method_name, mean(y_error_comparison));
fprintf(f,'Std. Dev. y error %s : %f\n', comparison_method_name, std(y_error_comparison));
fprintf(f,'\n');

fprintf(f,'Mean z error %s : %f\n', estimates_method_name, mean(z_error));
fprintf(f,'Std. Dev. z error %s : %f\n', estimates_method_name, std(z_error));
fprintf(f,'Mean z error %s : %f\n', comparison_method_name, mean(z_error_comparison));
fprintf(f,'Std. Dev. z error %s : %f\n', comparison_method_name, std(z_error_comparison));
fprintf(f,'\n');

fprintf(f,'Mean translation error %s : %f\n', estimates_method_name, mean(t_error));
fprintf(f,'Std. Dev. translation error %s : %f\n', estimates_method_name, std(t_error));
fprintf(f,'Mean translation error %s : %f\n', comparison_method_name, mean(t_error_comparison));
fprintf(f,'Std. Dev. translation error %s : %f\n', comparison_method_name, std(t_error_comparison));
fprintf(f,'\n');

fprintf(f,'Mean rotation angle error %s : %f\n', estimates_method_name, mean(r_angle_error));
fprintf(f,'Std. Dev. rotation angle error %s : %f\n', estimates_method_name, std(r_angle_error));
fprintf(f,'Mean rotation angle error %s : %f\n', comparison_method_name, mean(r_angle_error_comparison));
fprintf(f,'Std. Dev. rotation angle error %s : %f\n', comparison_method_name, std(r_angle_error_comparison));
fprintf(f,'\n');

fprintf(f,'Mean rotation axis error %s : %f\n', estimates_method_name, mean(r_axis_error));
fprintf(f,'Std. Dev. rotation axis error %s : %f\n',  estimates_method_name, std(r_axis_error));
fprintf(f,'Mean rotation axis error %s : %f\n', comparison_method_name, mean(r_axis_error_comparison));
fprintf(f,'Std. Dev. rotation axis error %s : %f\n', comparison_method_name, std(r_axis_error_comparison));

fclose(f);

plot_vals([t_error;t_error_comparison], 'Translation error', 'Distance (mm)', {estimates_method_name, comparison_method_name}, strcat(save_dir,'/translation_error.pdf'));
make_box_plot([t_error;t_error_comparison], 'Translation error', 'Distance (mm)', {{'',''}, {estimates_method_name, comparison_method_name}}, strcat(save_dir,'/translation_error_box.pdf'));

plot_vals([r_axis_error;r_axis_error_comparison;], 'Rotation axis error', 'Distance (radians)', {strcat('Axis error ',estimates_method_name), strcat('Axis error ', comparison_method_name)}, strcat(save_dir,'/rotation_axis_error.pdf'));
plot_vals([r_angle_error;r_angle_error_comparison;], 'Rotation angle error', 'Distance (radians)', {strcat('Angle error ', estimates_method_name), strcat('Angle error ', comparison_method_name)}, strcat(save_dir,'/rotation_angle_error.pdf'));

make_box_plot([r_axis_error;r_axis_error_comparison], 'Rotation axis error', 'Distance (rads)', {{'',''}, {estimates_method_name, comparison_method_name}}, strcat(save_dir,'/rotation_axis_error_box.pdf'));
make_box_plot([r_angle_error;r_angle_error_comparison], 'Rotation angle error', 'Distance (rads)', {{'',''}, {estimates_method_name, comparison_method_name}}, strcat(save_dir,'/rotation_angle_error_box.pdf'));
end

function [] = create_trajectory_plots(estimates, comparison, ground_truth, num_frames, save_dir, estimates_method_name, comparison_method_name)

%first create absolute plots for x,y,z
x_estimates = zeros(1,num_frames);
x_ground_truth = zeros(1,num_frames);
x_comparison = zeros(1,num_frames);
y_estimates = zeros(1,num_frames);
y_ground_truth = zeros(1,num_frames);
y_comparison = zeros(1,num_frames);
z_estimates = zeros(1,num_frames);
z_ground_truth = zeros(1,num_frames);
z_comparison = zeros(1,num_frames);

for i = 1:num_frames
  x_estimates(i) = estimates(i).translation(1);
  x_ground_truth(i) = ground_truth(i).translation(1);
  x_comparison(i) = comparison(i).translation(1);
  y_estimates(i) = estimates(i).translation(2);
  y_ground_truth(i) = ground_truth(i).translation(2);
  y_comparison(i) = comparison(i).translation(2);
  z_estimates(i) = estimates(i).translation(3);
  z_ground_truth(i) = ground_truth(i).translation(3);
  z_comparison(i) = comparison(i).translation(3);
end

plot_vals([x_estimates;x_comparison;x_ground_truth], 'Translation x', 'Position (mm)', {estimates_method_name, comparison_method_name,'Ground Truth'}, strcat(save_dir,'/trajectory_x.pdf'));
plot_vals([y_estimates;y_comparison;y_ground_truth], 'Translation y', 'Position (mm)', {estimates_method_name, comparison_method_name,'Ground Truth'}, strcat(save_dir,'/trajectory_y.pdf'));
plot_vals([z_estimates;z_comparison;z_ground_truth], 'Translation z', 'Position (mm)', {estimates_method_name, comparison_method_name,'Ground Truth'}, strcat(save_dir,'/trajectory_z.pdf'));

end

function [] = make_box_plot(vals, fig_title, y_axis_label, legend_labels, save_path)

num_plots = size(vals,1);
if num_plots > 1
  assert(num_plots == size(legend_labels,2));
end

if isequal(exist('label_colors','var'),0)
  label_colours = {'r','b','g','c','m','y'};
end

f = figure;
boxplot(vals','labels',legend_labels);

title(fig_title);
%xlabel('Frame no.');
ylabel(y_axis_label);
%if num_plots > 1
%  legend(legend_labels);
%end

set(gca,'FontSize',26);
set(findall(gcf,'type','text'),'FontSize',26);

%moveLabel('x',20, gcf, gca);

saveas(f,save_path);

end

function [] = plot_vals(vals, fig_title, y_axis_label, legend_labels, save_path)

num_plots = size(vals,1);
if num_plots > 1
  assert(num_plots == size(legend_labels,2));
end

if isequal(exist('label_colors','var'),0)
  label_colours = {'r','b','g','c','m','y'};
end

f = figure;
for i = 1:num_plots
  hold on;
  plot(vals(i,:),label_colours{i});
end

title(fig_title);
xlabel('Frame no.');
ylabel(y_axis_label);
if num_plots > 1
  legend(legend_labels,'Location','northwest');
end

set(gca,'FontSize',15);

set(findall(gcf,'type','text'),'FontSize',15);

saveas(f,save_path);

end

function moveLabel(ax,offset,hFig,hAxes)
    % get figure position
    posFig = get(hFig,'Position');

    % get axes position in pixels
    set(hAxes,'Units','pixels')
    posAx = get(hAxes,'Position');

    % get label position in pixels
    if ax=='x'
        set(get(hAxes,'XLabel'),'Units','pixels')
        posLabel = get(get(hAxes,'XLabel'),'Position');
    else
        set(get(hAxes,'YLabel'),'Units','pixels')
        posLabel = get(get(hAxes,'YLabel'),'Position');
    end

    % resize figure
    if ax=='x'
        posFigNew = posFig + [0 -offset 0 offset];
    else
        posFigNew = posFig + [-offset 0 offset 0];
    end
    set(hFig,'Position',posFigNew)

    % move axes
    if ax=='x'
        set(hAxes,'Position',posAx+[0 offset 0 0])
    else
        set(hAxes,'Position',posAx+[offset 0 0 0])
    end

    % move label
    if ax=='x'
        set(get(hAxes,'XLabel'),'Position',posLabel+[0 -offset 0])
    else
        set(get(hAxes,'YLabel'),'Position',posLabel+[-offset 0 0])
    end

    % set units back to 'normalized' and 'data'
    set(hAxes,'Units','normalized')
    if ax=='x'
        set(get(hAxes,'XLabel'),'Units','data')
    else
        set(get(hAxes,'YLabel'),'Units','data')
    end
end