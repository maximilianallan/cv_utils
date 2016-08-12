function [] = make_box_plot(vals, fig_title, y_axis_label, legend_labels, save_path)

num_plots = size(vals,1);
if num_plots > 1
  assert(num_plots == size(legend_labels,2));
end

if isequal(exist('label_colors','var'),0)
  label_colours = {'r','b','g','c','m','y'};
end

f = figure;
boxplot(vals','labels',legend_labels);

title(fig_title);
%xlabel('Frame no.');
ylabel(y_axis_label);
%if num_plots > 1
%  legend(legend_labels);
%end

set(gca,'FontSize',20);
set(findall(gcf,'type','text'),'FontSize',20);
%saveas(f,save_path);

export_fig(save_path, '-transparent');

close(f);

end


function moveLabel(ax,offset,hFig,hAxes)
    % get figure position
    posFig = get(hFig,'Position');

    % get axes position in pixels
    set(hAxes,'Units','pixels')
    posAx = get(hAxes,'Position');

    % get label position in pixels
    if ax=='x'
        set(get(hAxes,'XLabel'),'Units','pixels')
        posLabel = get(get(hAxes,'XLabel'),'Position');
    else
        set(get(hAxes,'YLabel'),'Units','pixels')
        posLabel = get(get(hAxes,'YLabel'),'Position');
    end

    % resize figure
    if ax=='x'
        posFigNew = posFig + [0 -offset 0 offset];
    else
        posFigNew = posFig + [-offset 0 offset 0];
    end
    set(hFig,'Position',posFigNew)

    % move axes
    if ax=='x'
        set(hAxes,'Position',posAx+[0 offset 0 0])
    else
        set(hAxes,'Position',posAx+[offset 0 0 0])
    end

    % move label
    if ax=='x'
        set(get(hAxes,'XLabel'),'Position',posLabel+[0 -offset 0])
    else
        set(get(hAxes,'YLabel'),'Position',posLabel+[-offset 0 0])
    end

    % set units back to 'normalized' and 'data'
    set(hAxes,'Units','normalized')
    if ax=='x'
        set(get(hAxes,'XLabel'),'Units','data')
    else
        set(get(hAxes,'YLabel'),'Units','data')
    end
end