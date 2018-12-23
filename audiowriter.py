from optparse import OptionParser
from writer import Writer
import os


def checks(filename):
    if not os.path.isfile(filename):
        raise Exception('{} not found: please specify a valid filename'.format(filename))


def main(filename, dict_options = None):

    writer = Writer(filename)
    writer.load_audio()
    writer.compute_loudness()
    writer.generate_phrases_filter()
    writer.generate_chunks()
    writer.generate_plot()


if __name__ == '__main__':
    parser = OptionParser()
    # parser.add_option("-f", "--file", dest="filename",
    #                   help="write report to FILE", metavar="FILE")

    # parser.add_option("-q", "--quiet",
    #                   action="store_false", dest="verbose", default=True,
    #                   help="don't print status messages to stdout")


    # loudness_tresh = 0.004, # OK
    # full_stop_time = 1.2, # OK
    # plot_downsampling_factor = 5, #OK
    # lines_in_figure = 5, #OK
    # figure_extension = 'jpg'

    parser.add_option("-f", "--fullstop",
                      action="store_false", dest="full_stop_time", default=-1,
                      help="make full stop if te time is bigger than value, -1 --> no full stop")


    parser.add_option("-t", "--treshold",
                      action="store_false", dest="tresh", default=0.04,
                      help="[0,1] treshold to divide phrases. If the ouput is not the desired you can play whith this value")

    parser.add_option("-d", "--downsampling",
                      action="store_false", dest="plot_downsampling_factor", default=5,
                      help="sampe every 'd' points in plot, to reduce the sampling points of the plot ")

    parser.add_option("-l", "--linesinfigure",
                      action="store_false", dest="lines_in_figure", default=5,
                      help="how many lines is the figure going to have, without counting full stops")

    parser.add_option("-e", "--extension",
                      action="store_false", dest="figure_extension", default=5,
                      help="file type of the figure")

    (options, args) = parser.parse_args()

    filename = args[0]

    print(options)
    print(args[0])

    checks(filename)
    main(filename)
