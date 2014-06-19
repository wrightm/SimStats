'''
@author: wrightm
@copyright: 2014 Michael Wright
@license: GNU GPLv3 http://www.gnu.org/licenses/gpl.html
'''
from matplotlib import pyplot
from src.main.python.discrete_distributions import DictWrapper
from src.main.python.stat_utils import differences_adj_elements
from src.main.python.utils import test_obj_subclass, test_obj_instance

def add_options_to_plot(d=None, **options):
    if d is None:
        d = {}

    for key, val in options.iteritems():
        d.setdefault(key, val)

    return d

def plot(xs, ys, style='', **options):
    options = add_options_to_plot(options, linewidth=3, alpha=0.5)
    pyplot.plot(xs, ys, style, **options)
    
def scatter_plot(xs, ys, **options) :
    options = add_options_to_plot(options, alpha=1.0, edgecolors='none')
    pyplot.scatter(xs, ys, **options)
        
def hexbin_plot(xs, ys, **options) :
    options = add_options_to_plot(options)
    pyplot.hexbin(xs, ys, cmap=pyplot.cm.Blues, **options)
        
def plot_discrete_distribution(distro, **options):

    test_obj_subclass(distro, DictWrapper)
    
    xs, ps = distro.sort_zip()
    options = add_options_to_plot(options, label=distro.name)
    plot(xs, ps, **options)
    
def plot_discrete_distributions(distros, **options):

    test_obj_instance(distros, list)
    
    for distro in distros:
        plot_discrete_distribution(distro, **options)
        
def plot_histogram(distro, **options):
    
    test_obj_subclass(distro, DictWrapper)

    xs, fs = distro.sort_zip()
    width = min(differences_adj_elements(xs))

    options = add_options_to_plot(options, 
                                  label=distro.name,
                                  align='center',
                                  edgecolor='blue',
                                  width=width)

    pyplot.bar(xs, fs, **options)    
    
def plot_histograms(distros, **options):
    
    test_obj_instance(distros, list)
    
    for distro in distros:
        plot_histogram(distro, **options)
        
def configure(**options):
    title = options.get('title', '')
    pyplot.title(title)

    xlabel = options.get('xlabel', '')
    pyplot.xlabel(xlabel)

    ylabel = options.get('ylabel', '')
    pyplot.ylabel(ylabel)

    if 'xscale' in options:
        pyplot.xscale(options['xscale'])

    if 'xticks' in options:
        pyplot.xticks(*options['xticks'])

    if 'yscale' in options:
        pyplot.yscale(options['yscale'])

    if 'yticks' in options:
        pyplot.yticks(*options['yticks'])

    if 'axis' in options:
        pyplot.axis(options['axis'])

    loc = options.get('loc', 0)
    legend = options.get('legend', True)
    if legend:
        pyplot.legend(loc=loc)


def show_plot(**options):
    configure(**options)
    pyplot.show()


def save_plot(root=None, formats=None, **options):
    configure(**options)

    if formats is None:
        formats = ['pdf', 'png']

    if root:
        for frmt in formats:
            save_format(root, frmt)


def save_format(root, frmt='eps'):
    filename = '%s.%s' % (root, frmt)
    pyplot.savefig(filename, format=frmt, dpi=300)
    
def clear_plot():
    pyplot.clf()