function [] = process_results(output_dir, start_frame, estimates_file, ground_truth_file, original_method_file, method_name, comparison_method_name)

[estimates,ground_truth] = open_and_read(estimates_file, ground_truth_file);
[comparison,~] = open_and_read(original_method_file, ground_truth_file);

num_frames = size(estimates,2);

if(size(comparison,2) == size(estimates,2)-100)
   estimates = estimates(101:size(estimates,2));
   ground_truth = ground_truth(101:size(ground_truth,2));
else
    
end

%assert(size(comparison,2) == size(estimates,2));
warning('number of frames is not equal!');

close all;

num_frames_alt = size(ground_truth,2);
if (num_frames > num_frames_alt)
    num_frames = num_frames_alt;
end

val = str2num(start_frame) + 1;
ground_truth = ground_truth(val:num_frames);
estimates = estimates(1:num_frames);
comparison = comparison(1:num_frames);

if (size(comparison,2) ~= size(estimates,2))
    create_partial_trajectory_plots(estimates, comparison, ground_truth, num_frames, output_dir, method_name, comparison_method_name);
    create_partial_error_plots(estimates, comparison, ground_truth, num_frames, output_dir, method_name, comparison_method_name);
else
    create_trajectory_plots(estimates, comparison, ground_truth, num_frames, output_dir, method_name, comparison_method_name);
    create_error_plots(estimates, comparison, ground_truth, num_frames, output_dir, method_name, comparison_method_name);
end

close all;

end


