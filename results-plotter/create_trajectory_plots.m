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

roll_estimates = zeros(1,num_frames);
roll_ground_truth = zeros(1,num_frames);
roll_comparison = zeros(1,num_frames);
pitch_estimates = zeros(1,num_frames);
pitch_ground_truth = zeros(1,num_frames);
pitch_comparison = zeros(1,num_frames);
yaw_estimates = zeros(1,num_frames);
yaw_ground_truth = zeros(1,num_frames);
yaw_comparison = zeros(1,num_frames);


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
  
  roll_estimates(i) = estimates(i).rotation(1);
  roll_ground_truth(i) = ground_truth(i).rotation(1);
  roll_comparison(i) = comparison(i).rotation(1);
  pitch_estimates(i) = estimates(i).rotation(2);
  pitch_ground_truth(i) = ground_truth(i).rotation(2);
  pitch_comparison(i) = comparison(i).rotation(2);
  yaw_estimates(i) = estimates(i).rotation(3);
  yaw_ground_truth(i) = ground_truth(i).rotation(3);
  yaw_comparison(i) = comparison(i).rotation(3);
  
end

plot_vals({x_estimates,x_comparison,x_ground_truth}, 'Translation x', 'Position (mm)', {estimates_method_name, comparison_method_name,'Ground Truth'}, strcat(save_dir,'/trajectory_x.pdf'));
plot_vals({y_estimates,y_comparison,y_ground_truth}, 'Translation y', 'Position (mm)', {estimates_method_name, comparison_method_name,'Ground Truth'}, strcat(save_dir,'/trajectory_y.pdf'));
plot_vals({z_estimates,z_comparison,z_ground_truth}, 'Translation z', 'Position (mm)', {estimates_method_name, comparison_method_name,'Ground Truth'}, strcat(save_dir,'/trajectory_z.pdf'));

plot_vals({roll_estimates,roll_comparison,roll_ground_truth}, 'Rotation x', 'Angle (rads)', {estimates_method_name, comparison_method_name,'Ground Truth'}, strcat(save_dir,'/trajectory_xrotation.pdf'));
plot_vals({pitch_estimates,pitch_comparison,pitch_ground_truth}, 'Rotation y', 'Angle (rads)', {estimates_method_name, comparison_method_name,'Ground Truth'}, strcat(save_dir,'/trajectory_yrotation.pdf'));
plot_vals({yaw_estimates,yaw_comparison,yaw_ground_truth}, 'Rotation z', 'Angle (rads)', {estimates_method_name, comparison_method_name,'Ground Truth'}, strcat(save_dir,'/trajectory_zrotation.pdf'));

end