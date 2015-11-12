function [] = plot_vals(vals, fig_title, y_axis_label, legend_labels, save_path)

num_plots = size(vals,2);
if num_plots > 1
  assert(num_plots == size(legend_labels,2));
end

if isequal(exist('label_colors','var'),0)
    label_colours = {'b','r','m','c','g','y'};
end

f = figure;
for i = 1:num_plots
  hold on;
  plot(vals{i},label_colours{i});
end

title(fig_title);
xlabel('Frame no.');
ylabel(y_axis_label);

if (strcmp(fig_title,'Translation x'))&& num_plots > 1
  legend(legend_labels,'Location','southwest');    
elseif num_plots > 1
  legend(legend_labels,'Location','northwest');
end

set(gca,'FontSize',15);

set(findall(gcf,'type','text'),'FontSize',15);

saveas(f,save_path);

end
