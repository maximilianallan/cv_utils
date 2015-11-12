function [] = process_results(output_dir, start_frame, estimates_file, ground_truth_file, original_method_file, method_name, comparison_method_name, skip_first_100)

skip_first_100 = str2double(skip_first_100);
close all;

[estimates,ground_truth] = open_and_read(estimates_file, ground_truth_file);
[comparison,~] = open_and_read(original_method_file, ground_truth_file);

if(skip_first_100 == 1)
   estimates = estimates(101:size(estimates,2));
   ground_truth = ground_truth(101:size(ground_truth,2));
elseif (size(comparison,2) ~= size(estimates,2))
    warning('number of frames is not equal!');    
%    if (size(comparison,2) > size(estimates,2))
%        comparison = comparison(1:size(estimates,2));
%        warning('shrinking number of frames in comparison');
%    else
%        warning('shrinking number of frames in estimates');
%        estimates = estimates(1:size(comparison,2));
%    end
        
end



if (size(comparison,2) ~= size(estimates,2))
        
    num_frames_estimates = size(estimates,2);
    num_frames_comparison = size(comparison,2);
    num_frames_ground_truth = size(ground_truth,2);

    %shrink the comparison method down if we have more frames (we don't
    %care about validating that by itself...)
    if (num_frames_comparison > num_frames_estimates)
        num_frames_comparison = num_frames_estimates; 
    end
        
    %if there are fewer ground truth frames, then no point in
    %validating beyond that
    if (num_frames_ground_truth < num_frames_estimates)
        num_frames_estimates = num_frames_ground_truth;
    else
       num_frames_ground_truth = num_frames_estimates;
    end
        
    val = str2num(start_frame) + 1;
    ground_truth = ground_truth(val:num_frames_ground_truth);
    estimates = estimates(1:num_frames_estimates);
    comparison = comparison(1:num_frames_comparison);

        
    create_partial_trajectory_plots(estimates, comparison, ground_truth, num_frames_estimates, output_dir, method_name, comparison_method_name);
    create_partial_error_plots(estimates, comparison, ground_truth, num_frames_estimates, output_dir, method_name, comparison_method_name);
else

    num_frames = size(estimates,2);
    num_frames_ground_truth = size(ground_truth,2);

    if (num_frames > num_frames_ground_truth)
        num_frames = num_frames_alt;
    end

    val = str2num(start_frame) + 1;
    ground_truth = ground_truth(val:num_frames);
    estimates = estimates(1:num_frames);
    comparison = comparison(1:num_frames);

    create_trajectory_plots(estimates, comparison, ground_truth, num_frames, output_dir, method_name, comparison_method_name);
    create_error_plots(estimates, comparison, ground_truth, num_frames, output_dir, method_name, comparison_method_name);
end

close all;

end


