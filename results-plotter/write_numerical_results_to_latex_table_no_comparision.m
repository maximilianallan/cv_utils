function [] = write_numerical_results_to_latex_table_no_comparision(method_results, method_name, output_dir, label, basic_caption, is_articulated)

number_of_datasets = length(method_results);

file_id = fopen(strcat(output_dir, '/numerical_results.tex'), 'w');

write_header(file_id, is_articulated);

for i = 1:number_of_datasets
    
    write_numerical_results_line_to_latex_table( file_id, method_results{i}, method_name, is_articulated, i == number_of_datasets);
    
end

write_footer(file_id, label, basic_caption, is_articulated);

end