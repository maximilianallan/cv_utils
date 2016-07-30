function [] = write_numerical_results_to_latex_table(method_1_results, method_2_results, method_1_name, method_2_name, output_dir, label, basic_caption, is_articulated)

number_of_datasets = length(method_1_results);

file_id = fopen(strcat(output_dir, '/numerical_results_methods.tex'), 'w');

write_header(file_id, is_articulated);

for i = 1:number_of_datasets
    
    write_numerical_results_line_to_latex_table( file_id, method_1_results{i}, method_1_name, is_articulated, 0);
    write_numerical_results_line_to_latex_table( file_id, method_2_results{i}, method_2_name, is_articulated, 0);

end

mean_method_1 = get_mean(method_1_results, is_articulated);
mean_method_2 = get_mean(method_2_results, is_articulated);

fprintf( file_id, '\t\t\t \\textbf{Mean error %s} & %.02f $\\pm$ %.02f & %.02f $\\pm$ %.02f & %.02f $\\pm$ %.02f & ', ...
    method_1_name, ...
    mean_method_1.x_error, mean_method_1.x_std, ...
    mean_method_1.y_error, mean_method_1.y_std, ...
    mean_method_1.z_error, mean_method_1.z_std);

fprintf( file_id, '%.02f $\\pm$ %.02f & %.02f $\\pm$ %.02f & %.02f $\\pm$ %.02f ', ...
    mean_method_1.roll_error, mean_method_1.roll_std, ...
    mean_method_1.pitch_error, mean_method_1.pitch_std, ...
    mean_method_1.yaw_error, mean_method_1.yaw_std);

if is_articulated == 1
    fprintf( file_id, '& %.02f $\\pm$ %.02f & %.02f $\\pm$ %.02f & %.02f $\\pm$ %.02f ', ...
    mean_method_1.a1_error, mean_method_1.a1_std, ...
    mean_method_1.a2_error, mean_method_1.a2_std, ...
    mean_method_1.a3_error, mean_method_1.a3_std);
end

fprintf(file_id, '  \\\\ \\hline\n');

fprintf( file_id, '\t\t\t \\textbf{Mean error %s} & %.02f $\\pm$ %.02f & %.02f $\\pm$ %.02f & %.02f $\\pm$ %.02f & ', ...
    method_2_name, ...
    mean_method_2.x_error, mean_method_2.x_std, ...
    mean_method_2.y_error, mean_method_2.y_std, ...
    mean_method_2.z_error, mean_method_2.z_std);

fprintf( file_id, '%.02f $\\pm$ %.02f & %.02f $\\pm$ %.02f & %.02f $\\pm$ %.02f ', ...
    mean_method_2.roll_error, mean_method_2.roll_std, ...
    mean_method_2.pitch_error, mean_method_2.pitch_std, ...
    mean_method_2.yaw_error, mean_method_2.yaw_std);

if is_articulated == 1
    fprintf( file_id, '& %.02f $\\pm$ %.02f & %.02f $\\pm$ %.02f & %.02f $\\pm$ %.02f ', ...
    mean_method_2.a1_error, mean_method_2.a1_std, ...
    mean_method_2.a2_error, mean_method_2.a2_std, ...
    mean_method_2.a3_error, mean_method_2.a3_std);
end

fprintf(file_id, '\n');

write_footer(file_id, label, basic_caption, is_articulated);

end

function [mean_vals] = get_mean(method_results, is_articulated)

number_of_datasets = length(method_results);

mean_vals = struct( 'x_error', 0, ...
                    'y_error', 0, ...
                    'z_error', 0, ...
                    'x_std', 0, ...
                    'y_std', 0, ...
                    'z_std', 0, ...
                    'roll_error', 0, ...
                    'pitch_error', 0, ...
                    'yaw_error', 0, ...
                    'roll_std', 0, ...
                    'pitch_std', 0, ...
                    'yaw_std', 0);
if is_articulated == 1
   
    mean_vals.a1_error = 0;
    mean_vals.a2_error = 0;
    mean_vals.a3_error = 0;
    mean_vals.a1_std = 0;
    mean_vals.a2_std = 0;
    mean_vals.a3_std = 0;
    
end
                

for i = 1:number_of_datasets
    
    mean_vals.x_error = mean_vals.x_error + method_results{i}.x_error;
    mean_vals.y_error = mean_vals.y_error + method_results{i}.y_error;
    mean_vals.z_error = mean_vals.z_error + method_results{i}.z_error;
    mean_vals.x_std = mean_vals.x_std + method_results{i}.x_std;
    mean_vals.y_std = mean_vals.y_std + method_results{i}.y_std;
    mean_vals.z_std = mean_vals.z_std + method_results{i}.z_std;
    mean_vals.roll_error = mean_vals.roll_error + method_results{i}.roll_error;
    mean_vals.pitch_error = mean_vals.pitch_error + method_results{i}.pitch_error;
    mean_vals.yaw_error = mean_vals.yaw_error + method_results{i}.yaw_error;
    mean_vals.roll_std = mean_vals.roll_std + method_results{i}.roll_std;
    mean_vals.pitch_std = mean_vals.pitch_std + method_results{i}.pitch_std;
    mean_vals.yaw_std = mean_vals.yaw_std + method_results{i}.yaw_std;
    
    if is_articulated == 1
       
         mean_vals.a1_error = mean_vals.a1_error + method_results{i}.a1_error;
         mean_vals.a2_error = mean_vals.a2_error + method_results{i}.a2_error;
         mean_vals.a3_error = mean_vals.a3_error + method_results{i}.a3_error;
        
         mean_vals.a1_std = mean_vals.a1_std + method_results{i}.a1_std;
         mean_vals.a2_std = mean_vals.a2_std + method_results{i}.a2_std;
         mean_vals.a3_std = mean_vals.a3_std + method_results{i}.a3_std;
         
    end
    
    
end

mean_vals.x_error = mean_vals.x_error / number_of_datasets;
mean_vals.y_error = mean_vals.y_error / number_of_datasets;
mean_vals.z_error = mean_vals.z_error / number_of_datasets;
mean_vals.x_std = mean_vals.x_std / number_of_datasets;
mean_vals.y_std = mean_vals.y_std / number_of_datasets;
mean_vals.z_std = mean_vals.z_std / number_of_datasets;
mean_vals.roll_error = mean_vals.roll_error / number_of_datasets;
mean_vals.pitch_error = mean_vals.pitch_error / number_of_datasets;
mean_vals.yaw_error = mean_vals.yaw_error / number_of_datasets;
mean_vals.roll_std = mean_vals.roll_std / number_of_datasets;
mean_vals.pitch_std = mean_vals.pitch_std / number_of_datasets;
mean_vals.yaw_std = mean_vals.yaw_std / number_of_datasets;
    
if is_articulated == 1
     
    mean_vals.a1_error = mean_vals.a1_error / number_of_datasets;
    mean_vals.a2_error = mean_vals.a2_error / number_of_datasets;
    mean_vals.a3_error = mean_vals.a3_error / number_of_datasets;
    
    mean_vals.a1_std = mean_vals.a1_std / number_of_datasets;
    mean_vals.a2_std = mean_vals.a2_std / number_of_datasets;
    mean_vals.a3_std = mean_vals.a3_std / number_of_datasets;
        
end

end
