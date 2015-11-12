function [] = create_partial_error_plots(estimates, comparison, ground_truth, num_frames, save_dir, estimates_method_name, comparison_method_name)

for i = 1:num_frames

    try
        t_error(i) = pdist([estimates(1,i).translation;ground_truth(1,i).translation]);
        x_error(i) = pdist([estimates(1,i).translation(1);ground_truth(1,i).translation(1)]);
        y_error(i) = pdist([estimates(1,i).translation(2);ground_truth(1,i).translation(2)]);
        z_error(i) = pdist([estimates(1,i).translation(3);ground_truth(1,i).translation(3)]);
        
        r_error(i) = pdist([estimates(1,i).rotation;ground_truth(1,i).rotation]);
        roll_error(i) = pdist([estimates(1,i).rotation(1);ground_truth(1,i).rotation(1)]);
        pitch_error(i) = pdist([estimates(1,i).rotation(2);ground_truth(1,i).rotation(2)]);
        yaw_error(i) = pdist([estimates(1,i).rotation(3);ground_truth(1,i).rotation(3)]);
        %e = estimates(1,i).rotation(2:4)/norm(estimates(1,i).rotation(2:4));
        %g = (ground_truth(1,i).rotation(2:4)/norm(ground_truth(1,i).rotation(2:4)))';
        
        %r_axis_error(i) = acos(e*g);
        %r_angle_error(i) = pdist([estimates(1,i).rotation(1);ground_truth(1,i).rotation(1)]);      
    catch
        
    end
  
    try
        t_error_comparison(i) = pdist([comparison(1,i).translation;ground_truth(1,i).translation]);
        x_error_comparison(i) = pdist([comparison(1,i).translation(1);ground_truth(1,i).translation(1)]);
        y_error_comparison(i) = pdist([comparison(1,i).translation(2);ground_truth(1,i).translation(2)]);
        z_error_comparison(i) = pdist([comparison(1,i).translation(3);ground_truth(1,i).translation(3)]);
        
        r_error_comparison(i) = pdist([comparison(1,i).rotation;ground_truth(1,i).rotation]);
        roll_error_comparison(i) = pdist([comparison(1,i).rotation(1);ground_truth(1,i).rotation(1)]);
        pitch_error_comparison(i) = pdist([comparison(1,i).rotation(2);ground_truth(1,i).rotation(2)]);
        yaw_error_comparison(i) = pdist([comparison(1,i).rotation(3);ground_truth(1,i).rotation(3)]);
        
        %e_comparison = comparison(1,i).rotation(2:4)/norm(comparison(1,i).rotation(2:4));
        %g = (ground_truth(1,i).rotation(2:4)/norm(ground_truth(1,i).rotation(2:4)))';
        %r_axis_error_comparison(i) = acos(e_comparison*g);
        %r_angle_error_comparison(i) = pdist([comparison(1,i).rotation(1);ground_truth(1,i).rotation(1)]);      
        
    catch
    end  
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

fprintf(f,'Method Mean pitch error %s : %f\n', estimates_method_name, mean(roll_error));
fprintf(f,'Method Std. Dev. pitch error %s : %f\n', estimates_method_name, std(roll_error));
fprintf(f,'ComparisonMean pitch error %s : %f\n', comparison_method_name, mean(roll_error_comparison));
fprintf(f,'ComparisonStd. Dev. pitch error %s : %f\n', comparison_method_name, std(roll_error_comparison));
fprintf(f,'\n');

fprintf(f,'Method Mean yaw error %s : %f\n', estimates_method_name, mean(roll_error));
fprintf(f,'Method Std. Dev. yaw error %s : %f\n', estimates_method_name, std(roll_error));
fprintf(f,'Comparison Mean yaw error %s : %f\n', comparison_method_name, mean(roll_error_comparison));
fprintf(f,'Comparison Std. Dev. yaw error %s : %f\n', comparison_method_name, std(roll_error_comparison));
fprintf(f,'\n');

fclose(f);

plot_partial_vals({t_error,t_error_comparison}, 'Translation error', 'Distance (mm)', {estimates_method_name, comparison_method_name}, strcat(save_dir,'/translation_error.pdf'));

plot_partial_vals({r_error,r_error_comparison}, 'Rotation error', 'Distance (rads)', {estimates_method_name, comparison_method_name}, strcat(save_dir,'/rotation_error.pdf'));

end
