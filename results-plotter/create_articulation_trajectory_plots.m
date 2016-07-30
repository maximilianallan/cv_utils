function [] = create_articulation_trajectory_plots(estimates, comparison, ground_truth, num_frames, save_dir, estimates_method_name, comparison_method_name)

%first create absolute plots for x,y,z
a1_estimates = zeros(1,num_frames);
a1_ground_truth = zeros(1,num_frames);
a1_comparison = zeros(1,num_frames);
a2_estimates = zeros(1,num_frames);
a2_ground_truth = zeros(1,num_frames);
a2_comparison = zeros(1,num_frames);
a3_estimates = zeros(1,num_frames);
a3_ground_truth = zeros(1,num_frames);
a3_comparison = zeros(1,num_frames);


for i = 1:num_frames
  a1_estimates(i) = estimates(i).articulation(1);
  a1_ground_truth(i) = ground_truth(i).articulation(1);
  a1_comparison(i) = comparison(i).articulation(1);
  a2_estimates(i) = estimates(i).articulation(2);
  a2_ground_truth(i) = ground_truth(i).articulation(2);
  a2_comparison(i) = comparison(i).articulation(2);
  a3_estimates(i) = estimates(i).articulation(3);
  a3_ground_truth(i) = ground_truth(i).articulation(3);
  a3_comparison(i) = comparison(i).articulation(3);

end

plot_vals({a1_estimates,a1_comparison,a1_ground_truth}, 'Wrist angle ', 'Angle (rads)', {estimates_method_name, comparison_method_name,'Ground Truth'}, strcat(save_dir,'/wrist.pdf'));
plot_vals({a2_estimates,a2_comparison,a2_ground_truth}, 'Clasper direction', 'Angle (rads)', {estimates_method_name, comparison_method_name,'Ground Truth'}, strcat(save_dir,'/clasper_dir.pdf'));
plot_vals({a3_estimates,a3_comparison,a3_ground_truth}, 'Clasper opening', 'Angle (rads)', {estimates_method_name, comparison_method_name,'Ground Truth'}, strcat(save_dir,'/clasper_open.pdf'));

end