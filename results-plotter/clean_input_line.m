function cleaned = clean_input_line(line)

try

    assert( size(line,2) ~= 50 );


    start_offset = 3;
    %chunk_size = 11;
    end_offset = 1;
    idx = start_offset;
    x = line(start_offset:length(line)-end_offset);
    xs = strsplit(x);
    ii = 1;
    for i = 1:length(xs)
        
        v = str2double(xs{i});
        if isnan(v) == 1 
            continue
        end
        cleaned(ii) = v;
        ii = ii + 1;
        %idx = idx + chunk_size + 1;
    end

    if length(cleaned) ~= 4
       display(cleaned); 
    end
    
catch ME
    
    msg = getReport(ME, 'basic');
    fprintf(msg);    
    rethrow(ME);
end

end


