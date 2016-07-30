function [] = write_footer(file_id, label, basic_caption, is_articulated)

fprintf( file_id, '\t\t\t\\end{tabular}\n' );
%fprintf( file_id, '\t\t\\end{center}\n' );
%fprintf( file_id, '\t\\caption{%s}\n', basic_caption );
%if is_articulated == 0
%    fprintf( file_id, '\t\\label{fig:rigid_results_%s}\n', label );
%else
%    fprintf( file_id, '\t\\label{fig:articulated_results_%s}\n', label );
%end
%fprintf( file_id, '\\end{table}\n');

end