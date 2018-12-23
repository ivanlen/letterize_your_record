from optparse import OptionParser
from writer import Writer
import os


def checks(filename, **kwargs):
    if not os.path.isfile(filename):
        raise Exception('{} not found: please specify a valid filename'.format(filename))

    convert_to_int = ['lines_in_figure', 'downsampling']
    convert_to_float = ['full_stop_time', 'downsampling']

    for key in kwargs.keys():
        if key in convert_to_int:
            kwargs[key] = int(kwargs[key])
        elif key in convert_to_float:
            kwargs[key] = float(kwargs[key])

    return kwargs


def main(filename,
         **kwargs):
    writer = Writer(filename, **kwargs)
    writer.load_audio()
    writer.compute_loudness()
    writer.generate_phrases_filter()
    writer.generate_chunks()
    writer.generate_plot()


if __name__ == '__main__':
    parser = OptionParser()

    # loudness_tresh = 0.004, # OK
    # full_stop_time = 1.2, # OK
    # plot_downsampling_factor = 5, #OK
    # lines_in_figure = 5, #OK
    # figure_extension = 'jpg'

    parser.add_option("-s", "--fullstop",
                      dest="full_stop_time",
                      default=-1,
                      help="make full stop if te time is bigger than value, -1 --> no full stop")

    parser.add_option("-t", "--audiotreshold",
                      dest="loudness_tresh",
                      default=0.04,
                      help="[0,1] treshold to divide phrases. If the ouput is not the desired you can play whith this value")

    parser.add_option("-d", "--downsampling",
                      dest="plot_downsampling_factor",
                      default=5,
                      help="sampe every 'd' points in plot, to reduce the sampling points of the plot ")

    parser.add_option("-l", "--linesinfigure",
                      # action="store_false",
                      dest="lines_in_figure",
                      default=5,
                      help="how many lines is the figure going to have, without counting full stops")

    parser.add_option("-e", "--extension",
                      dest="figure_extension",
                      default='jpg',
                      help="file type of the figure")

    options, args = parser.parse_args()
    filename, options_dict = args[0], vars(options)
    options_dict = checks(filename, **options_dict)

    main(filename, **options_dict)
