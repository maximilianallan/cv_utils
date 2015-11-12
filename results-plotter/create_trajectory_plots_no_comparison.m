function [] = create_trajectory_plots_no_comparison(estimates, ground_truth, num_frames, save_dir)

%first create absolute plots for x,y,z
x_estimates = zeros(1,num_frames);
x_ground_truth = zeros(1,num_frames);

y_estimates = zeros(1,num_frames);
y_ground_truth = zeros(1,num_frames);

z_estimates = zeros(1,num_frames);
z_ground_truth = zeros(1,num_frames);


for i = 1:num_frames
  x_estimates(i) = estimates(i).translation(1);
  x_ground_truth(i) = ground_truth(i).translation(1);
  y_estimates(i) = estimates(i).translation(2);
  y_ground_truth(i) = ground_truth(i).translation(2);
  z_estimates(i) = estimates(i).translation(3);
  z_ground_truth(i) = ground_truth(i).translation(3);
end

plot_vals([x_estimates;x_ground_truth], 'Translation x', 'Position (mm)', {estimates_method_name, 'Ground Truth'}, strcat(save_dir,'/trajectory_x.pdf'));
plot_vals([y_estimates;y_ground_truth], 'Translation y', 'Position (mm)', {estimates_method_name, 'Ground Truth'}, strcat(save_dir,'/trajectory_y.pdf'));
plot_vals([z_estimates;z_ground_truth], 'Translation z', 'Position (mm)', {estimates_method_name, 'Ground Truth'}, strcat(save_dir,'/trajectory_z.pdf'));

end