function process_results

%SKIPPING THE FIRST 59 FRAMES

output_dir = od;
if exist('sf','var') == 1
    start_frame = sf;
else
    start_frame = 0;
end

estimates_file_url = strcat(output_dir, ef);
ground_truth_file_url = gtf;
original_method_url = omf
[estimates,ground_truth] = open_and_read(estimates_file_url, ground_truth_file_url);
[comparison,~] = open_and_read(original_method_url, ground_truth_file_url);

if exist('ef2','var') == 1
    estimates_file_url2 = strcat(output_dir, ef2);
    ground_truth_file_url2 = gtf2;
    original_method_url2 = ofm2;
    [estimates2,ground_truth2] = open_and_read(estimates_file_url2, ground_truth_file_url2);
    [comparison2,~] = open_and_read(original_method_url2, ground_truth_file_url2);
end


close all;

num_frames_alt = size(ground_truth,2);
if exist('ef2','var') == 1 && size(ground_truth2,2) < num_frames_alt
  num_frames_alt = size(ground_truth2,2);
end

ground_truth = ground_truth(start_frame:num_frames_alt);

if exist('ef2','var') == 1
    ground_truth2 = ground_truth2(start_frame:num_frames_alt);
end

num_frames_alt = size(ground_truth,2);

estimates = estimates(1:num_frames_alt);
comparison = comparison(1:num_frames_alt);

if exist('ef2','var') == 1
    estimates2 = estimates2(1:num_frames_alt);
    comparison2 = comparison2(1:num_frames_alt);
end

num_frames = size(estimates,2);

assert(num_frames == num_frames_alt);
assert(num_frames == size(comparison,2));

create_trajectory_plots([estimates,estimates2], [comparison,comparison2], [ground_truth,ground_truth2], 2*num_frames, output_dir, 'LS + SIFT', 'LS');
create_error_plots([estimates;estimates2], [comparison;comparison2], [ground_truth;ground_truth2], num_frames, output_dir, 'LS + SIFT', 'LS');


%create error plots for x,y,z,r

end


