function process_results

output_dir = od;
if exist('sf','var') == 1
    start_frame = sf;
else
    start_frame = 0;
end

estimates_file_url = strcat(output_dir, ef);
ground_truth_file_url = gtf;
method_name = mn;

[estimates,ground_truth] = open_and_read(estimates_file_url, ground_truth_file_url);

close all;

num_frames_alt = size(ground_truth,2);
ground_truth = ground_truth(start_frame:num_frames_alt);
estimates = estimates(1:num_frames_alt);

num_frames = size(estimates,2);

assert(num_frames == num_frames_alt);

create_trajectory_plots_no_comparison(estimates, ground_truth, num_frames, output_dir, method_name);
create_error_plots_no_comparison(estimates, ground_truth, num_frames, output_dir, method_name);

end


