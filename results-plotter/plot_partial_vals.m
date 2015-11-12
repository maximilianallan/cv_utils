function [] = plot_partial_vals(vals, fig_title, y_axis_label, legend_labels, save_path)

num_plots = size(vals,1);
if num_plots > 1
  assert(num_plots == size(legend_labels,2));
end

if isequal(exist('label_colors','var'),0)
  label_colours = {'r','b','g','c','m','y'};
end

f = figure;
for i = 1:num_plots
  hold on;
  plot(vals{i},label_colours{i});
end

title(fig_title);
xlabel('Frame no.');
ylabel(y_axis_label);
if num_plots > 1
  legend(legend_labels,'Location','northwest');
end

set(gca,'FontSize',15);

set(findall(gcf,'type','text'),'FontSize',15);

saveas(f,save_path);

end
