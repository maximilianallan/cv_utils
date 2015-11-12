function cleaned = clean_input_line(line)

try

    assert( size(line,2) ~= 50 );


    start_offset = 3;
    %chunk_size = 11;
    end_offset = 2;
    idx = start_offset;
    x = line(start_offset:length(line)-end_offset);
    xs = strsplit(x);
    for i = 1:4
      %x = line(idx:idx+chunk_size);
      cleaned(i) = str2double(xs(i)); 
      %idx = idx + chunk_size + 1;
    end

catch ME
    
    msg = getReport(ME, 'basic');
    fprintf(msg);    
    rethrow(ME);
end

end


