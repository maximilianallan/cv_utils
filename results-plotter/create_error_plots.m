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
  t_error(i) = pdist([estimates(1,i).translation;ground_truth(1,i).translation]);
  t_error_comparison(i) = pdist([comparison(1,i).translation;ground_truth(1,i).translation]);
  
  x_error(i) = pdist([estimates(1,i).translation(1);ground_truth(1,i).translation(1)]);
  x_error_comparison(i) = pdist([comparison(1,i).translation(1);ground_truth(1,i).translation(1)]);
  
  y_error(i) = pdist([estimates(1,i).translation(2);ground_truth(1,i).translation(2)]);
  y_error_comparison(i) = pdist([comparison(1,i).translation(2);ground_truth(1,i).translation(2)]);
  
  z_error(i) = pdist([estimates(1,i).translation(3);ground_truth(1,i).translation(3)]);
  z_error_comparison(i) = pdist([comparison(1,i).translation(3);ground_truth(1,i).translation(3)]);
  
  e = estimates(1,i).rotation(2:4)/norm(estimates(1,i).rotation(2:4));
  e_comparison = comparison(1,i).rotation(2:4)/norm(comparison(1,i).rotation(2:4));
  g = (ground_truth(1,i).rotation(2:4)/norm(ground_truth(1,i).rotation(2:4)))';
    
  r_axis_error_comparison(i) = acos(e_comparison*g);
  r_angle_error_comparison(i) = pdist([comparison(1,i).rotation(1);ground_truth(1,i).rotation(1)]);
  r_axis_error(i) = acos(e*g);
  r_angle_error(i) = pdist([estimates(1,i).rotation(1);ground_truth(1,i).rotation(1)]);
  
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
