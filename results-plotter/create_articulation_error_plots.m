function [] = create_articulation_error_plots(estimates, comparison, ground_truth, num_frames, save_dir, estimates_method_name, comparison_method_name)

a1_error = zeros(1,num_frames);
a2_error = zeros(1,num_frames);
a3_error = zeros(1,num_frames);
a1_error_comparison = zeros(1,num_frames);
a2_error_comparison = zeros(1,num_frames);
a3_error_comparison = zeros(1,num_frames);

for i = 1:num_frames
  
  a1_error(i) = pdist([estimates(1,i).articulation(1);ground_truth(1,i).articulation(1)]);
  a1_error_comparison(i) = pdist([comparison(1,i).articulation(1);ground_truth(1,i).articulation(1)]);
  
  a2_error(i) = pdist([estimates(1,i).articulation(2);ground_truth(1,i).articulation(2)]);
  a2_error_comparison(i) = pdist([comparison(1,i).articulation(2);ground_truth(1,i).articulation(2)]);
  
  a3_error(i) = pdist([estimates(1,i).articulation(3);ground_truth(1,i).articulation(3)]);
  a3_error_comparison(i) = pdist([comparison(1,i).articulation(3);ground_truth(1,i).articulation(3)]);
    
end

f = fopen(strcat(save_dir,'numerical_errors.txt'),'w');

fprintf(f,'Numerical errors:\n\n');

fprintf(f,'Method Mean a1 error %s : %f\n', estimates_method_name, mean(a1_error) );
fprintf(f,'Method Std. Dev. a1 error %s : %f\n', estimates_method_name, std(a1_error));
fprintf(f,'Comparison Mean a1 error %s : %f\n', comparison_method_name, mean(a1_error_comparison));
fprintf(f,'Comparison Std. Dev. a1 error %s : %f\n',  comparison_method_name, std(a1_error_comparison));
fprintf(f,'\n');

fprintf(f,'Method Mean a2 error %s : %f\n', estimates_method_name, mean(a2_error));
fprintf(f,'Method Std. Dev. a2 error %s : %f\n', estimates_method_name, std(a2_error) );
fprintf(f,'Comparison Mean a2 error %s : %f\n', comparison_method_name, mean(a2_error_comparison));
fprintf(f,'Comparison Std. Dev. a2 error %s : %f\n', comparison_method_name, std(a2_error_comparison));
fprintf(f,'\n');

fprintf(f,'Method Mean a3 error %s : %f\n', estimates_method_name, mean(a3_error));
fprintf(f,'Method Std. Dev. a3 error %s : %f\n', estimates_method_name, std(a3_error));
fprintf(f,'Comparison Mean a3 error %s : %f\n', comparison_method_name, mean(a3_error_comparison));
fprintf(f,'Comparison Std. Dev. a3 error %s : %f\n', comparison_method_name, std(a3_error_comparison));
fprintf(f,'\n');

fclose(f);

plot_vals({a1_error,a1_error_comparison}, 'Wrist error', 'Distance (radians)', {estimates_method_name, comparison_method_name}, strcat(save_dir,'/wrist_error.pdf'));
make_box_plot([a1_error;a1_error_comparison], 'Wrist error', 'Distance (radians)', {{'',''}, {estimates_method_name, comparison_method_name}}, strcat(save_dir,'/wrist_error_box.pdf'));

plot_vals({a2_error,a2_error_comparison}, 'Clasper direction error', 'Distance (radians)', {estimates_method_name, comparison_method_name}, strcat(save_dir,'/clasper_dir_error.pdf'));
make_box_plot([a2_error;a2_error_comparison], 'Clasper direction error', 'Distance (radians)', {{'',''}, {estimates_method_name, comparison_method_name}}, strcat(save_dir,'/clasper_dir_error_box.pdf'));

plot_vals({a3_error,a3_error_comparison}, 'Clasper opening error', 'Distance (radians)', {estimates_method_name, comparison_method_name}, strcat(save_dir,'/clasper_opening_error.pdf'));
make_box_plot([a3_error;a3_error_comparison], 'Clasper opening error', 'Distance (radians)', {{'',''}, {estimates_method_name, comparison_method_name}}, strcat(save_dir,'/clasper_opening_error_box.pdf'));


end
