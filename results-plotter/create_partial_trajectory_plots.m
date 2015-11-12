function [] = create_partial_trajectory_plots(estimates, comparison, ground_truth, num_frames, save_dir, estimates_method_name, comparison_method_name)

%z_comparison = zeros(1,num_frames);

for i = 1:num_frames
    try
        x_estimates(i) = estimates(i).translation(1);
        y_estimates(i) = estimates(i).translation(2);
        z_estimates(i) = estimates(i).translation(3);
    catch
        
    end
    
    try
        x_ground_truth(i) = ground_truth(i).translation(1);
        y_ground_truth(i) = ground_truth(i).translation(2);
        z_ground_truth(i) = ground_truth(i).translation(3);
    catch
        
    end
  
    try
        x_comparison(i) = comparison(i).translation(1);
        y_comparison(i) = comparison(i).translation(2);
        z_comparison(i) = comparison(i).translation(3);
    catch
    end
end

plot_partial_vals({x_estimates,x_comparison,x_ground_truth}, 'Translation x', 'Position (mm)', {estimates_method_name, comparison_method_name,'Ground Truth'}, strcat(save_dir,'/trajectory_x.pdf'));
plot_partial_vals({y_estimates,y_comparison,y_ground_truth}, 'Translation y', 'Position (mm)', {estimates_method_name, comparison_method_name,'Ground Truth'}, strcat(save_dir,'/trajectory_y.pdf'));
plot_partial_vals({z_estimates,z_comparison,z_ground_truth}, 'Translation z', 'Position (mm)', {estimates_method_name, comparison_method_name,'Ground Truth'}, strcat(save_dir,'/trajectory_z.pdf'));

end