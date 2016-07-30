function [num_skip_lines] = get_number_of_skip_lines(app_file)

fid = fopen(app_file, 'r');

tline = fgetl(fid);
while ischar(tline)
    
    split = strsplit(tline, '=');
    if length(split) == 1
        tline = fgetl(fid);
        continue;
    end
    
    assert(length(split) == 2);
    
    if strcmp(split(1), 'skip-frames')
        num_skip_lines = str2double(split(2));
        break;
    end
    
    tline = fgetl(fid);
    
end


end