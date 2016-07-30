function [] = write_header(file_id, is_articulated, write_dataset)

if nargin == 2
    write_dataset = 1;
end

%fprintf( file_id, '\\begin{table}[!htb]\n');
%fprintf( file_id, '\t\\footnotesize\n');
%fprintf( file_id, '\t\\begin{center}\n');

if write_dataset == 1
    s = '\textbf{Dataset}'; % automatically escapes
else
    s = '';
end

if is_articulated == 0
    fprintf( file_id, '\t\t\\begin{tabular}{c|c|c|c|c|c|c}\n');
    fprintf( file_id, '\t\t\t %s & $t_{x} (mm)$ & $t_{y} (mm)$ & $t_{z} (mm)$ & $r_{x} (rads)$ & $r_{y} (rads)$ & $r_{z} (rads)$ \\\\ \\hline\n', s );
else
    fprintf( file_id, '\t\t\\begin{tabular}{c|c|c|c|c|c|c|c|c|c}\n');
    fprintf( file_id, '\t\t\t %s & $t_{x} (mm)$ & $t_{y} (mm)$ & $t_{z} (mm)$ & $r_{x} (rads)$ & $r_{y} (rads)$ & $r_{z} (rads)$ & wrist (rads) & grasper (rads) & grasper angle (rads) \\\\ \\hline\n', s );
end

end
