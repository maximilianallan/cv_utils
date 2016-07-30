function [] = create_error_plots(estimates, comparison, ground_truth, num_frames, save_dir, estimates_method_name, comparison_method_name)

x_error = zeros(1,num_frames);
y_error = zeros(1,num_frames);
z_error = zeros(1,num_frames);
x_error_comparison = zeros(1,num_frames);
y_error_comparison = zeros(1,num_frames);
z_error_comparison = zeros(1,num_frames);

t_error_comparison = zeros(1,num_frames);
t_error = zeros(1,num_frames);

r_error_comparison = zeros(1,num_frames);
r_error = zeros(1,num_frames);

yaw_error = zeros(1,num_frames);
pitch_error = zeros(1,num_frames);
roll_error = zeros(1,num_frames);

yaw_error_comparison = zeros(1,num_frames);
pitch_error_comparison = zeros(1,num_frames);
roll_error_comparison = zeros(1,num_frames);


for i = 1:num_frames
  t_error(i) = pdist([estimates(1,i).translation;ground_truth(1,i).translation]);
  t_error_comparison(i) = pdist([comparison(1,i).translation;ground_truth(1,i).translation]);
  
  x_error(i) = pdist([estimates(1,i).translation(1);ground_truth(1,i).translation(1)]);
  x_error_comparison(i) = pdist([comparison(1,i).translation(1);ground_truth(1,i).translation(1)]);
  
  y_error(i) = pdist([estimates(1,i).translation(2);ground_truth(1,i).translation(2)]);
  y_error_comparison(i) = pdist([comparison(1,i).translation(2);ground_truth(1,i).translation(2)]);
  
  z_error(i) = pdist([estimates(1,i).translation(3);ground_truth(1,i).translation(3)]);
  z_error_comparison(i) = pdist([comparison(1,i).translation(3);ground_truth(1,i).translation(3)]);
  
  r_error(i) = pdist([estimates(1,i).rotation;ground_truth(1,i).rotation]);
  roll_error(i) = pdist([estimates(1,i).rotation(1);ground_truth(1,i).rotation(1)]);
  pitch_error(i) = pdist([estimates(1,i).rotation(2);ground_truth(1,i).rotation(2)]);
  yaw_error(i) = pdist([estimates(1,i).rotation(3);ground_truth(1,i).rotation(3)]);
  
  r_error_comparison(i) = pdist([comparison(1,i).rotation;ground_truth(1,i).rotation]);
  roll_error_comparison(i) = pdist([comparison(1,i).rotation(1);ground_truth(1,i).rotation(1)]);
  pitch_error_comparison(i) = pdist([comparison(1,i).rotation(2);ground_truth(1,i).rotation(2)]);
  yaw_error_comparison(i) = pdist([comparison(1,i).rotation(3);ground_truth(1,i).rotation(3)]);
  
end

f = fopen(strcat(save_dir,'numerical_errors.txt'),'w');

fprintf(f,'Numerical errors:\n\n');

fprintf(f,'Method Mean x error %s : %f\n', estimates_method_name, mean(x_error) );
fprintf(f,'Method Std. Dev. x error %s : %f\n', estimates_method_name, std(x_error));
fprintf(f,'Comparison Mean x error %s : %f\n', comparison_method_name, mean(x_error_comparison));
fprintf(f,'Comparison Std. Dev. x error %s : %f\n',  comparison_method_name, std(x_error_comparison));
fprintf(f,'\n');

fprintf(f,'Method Mean y error %s : %f\n', estimates_method_name, mean(y_error));
fprintf(f,'Method Std. Dev. y error %s : %f\n', estimates_method_name, std(y_error) );
fprintf(f,'Comparison Mean y error %s : %f\n', comparison_method_name, mean(y_error_comparison));
fprintf(f,'Comparison Std. Dev. y error %s : %f\n', comparison_method_name, std(y_error_comparison));
fprintf(f,'\n');

fprintf(f,'Method Mean z error %s : %f\n', estimates_method_name, mean(z_error));
fprintf(f,'Method Std. Dev. z error %s : %f\n', estimates_method_name, std(z_error));
fprintf(f,'Comparison Mean z error %s : %f\n', comparison_method_name, mean(z_error_comparison));
fprintf(f,'Comparison Std. Dev. z error %s : %f\n', comparison_method_name, std(z_error_comparison));
fprintf(f,'\n');

fprintf(f,'Method Mean translation error %s : %f\n', estimates_method_name, mean(t_error));
fprintf(f,'Method Std. Dev. translation error %s : %f\n', estimates_method_name, std(t_error));
fprintf(f,'Comparison Mean translation error %s : %f\n', comparison_method_name, mean(t_error_comparison));
fprintf(f,'Comparison Std. Dev. translation error %s : %f\n', comparison_method_name, std(t_error_comparison));
fprintf(f,'\n');

fprintf(f,'Method Mean roll error %s : %f\n', estimates_method_name, mean(roll_error));
fprintf(f,'Method Std. Dev. roll error %s : %f\n', estimates_method_name, std(roll_error));
fprintf(f,'Comparison Mean roll error %s : %f\n', comparison_method_name, mean(roll_error_comparison));
fprintf(f,'Comparison Std. Dev. roll error %s : %f\n', comparison_method_name, std(roll_error_comparison));
fprintf(f,'\n');

fprintf(f,'Method Mean pitch error %s : %f\n', estimates_method_name, mean(pitch_error));
fprintf(f,'Method Std. Dev. pitch error %s : %f\n', estimates_method_name, std(pitch_error));
fprintf(f,'Comparison Mean pitch error %s : %f\n', comparison_method_name, mean(pitch_error_comparison));
fprintf(f,'Comparison Std. Dev. pitch error %s : %f\n', comparison_method_name, std(pitch_error_comparison));
fprintf(f,'\n');

fprintf(f,'Method Mean yaw error %s : %f\n', estimates_method_name, mean(yaw_error));
fprintf(f,'Method Std. Dev. yaw error %s : %f\n', estimates_method_name, std(yaw_error));
fprintf(f,'Comparison Mean yaw error %s : %f\n', comparison_method_name, mean(yaw_error_comparison));
fprintf(f,'Comparison Std. Dev. yaw error %s : %f\n', comparison_method_name, std(yaw_error_comparison));
fprintf(f,'\n');
fclose(f);

plot_vals({t_error,t_error_comparison}, 'Translation error', 'Distance (mm)', {estimates_method_name, comparison_method_name}, strcat(save_dir,'/translation_error.pdf'));
make_box_plot([t_error;t_error_comparison], 'Translation error', 'Distance (mm)', {{'',''}, {estimates_method_name, comparison_method_name}}, strcat(save_dir,'/translation_error_box.pdf'));

plot_vals({r_error,r_error_comparison}, 'Rotation error', 'Distance (radians)', {estimates_method_name, comparison_method_name}, strcat(save_dir,'/rotation_error.pdf'));
make_box_plot([r_error;r_error_comparison], 'Rotation error', 'Distance (rads)', {{'',''}, {estimates_method_name, comparison_method_name}}, strcat(save_dir,'/rotation_error_box.pdf'));

end
