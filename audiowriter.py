from optparse import OptionParser
from writer import Writer
import os


def checks(filename, **kwargs):
    if not os.path.isfile(filename):
        raise Exception('{} not found: please specify a valid filename'.format(filename))

    convert_to_int = ['lines_in_figure', 'downsampling']
    convert_to_float = ['full_stop_time', 'loudness_thresh']

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

    parser.add_option("-s", "--full-stop",
                      dest="full_stop_time",
                      default=-1,
                      help="float [0,3] default `-1`: no there are not going to be fullstops. `val>0`: a separate point will be made if the distance in seconds between two syllables is greater than val. ")

    parser.add_option("-t", "--audio-threshold",
                      dest="loudness_thresh",
                      default=0.04,
                      help="float [0,1] if the relative loudness is small than a relative value scaled by `thresh` the audio is going to be separated in two syllables.")

    parser.add_option("-d", "--downsampling",
                      dest="plot_downsampling_factor",
                      default=5,
                      help=" int [1:10] downsampling factor to reduce the density of the plot (for visual purposes).")

    parser.add_option("-l", "--lines-in-figure",
                      # action="store_false",
                      dest="lines_in_figure",
                      default=5,
                      help="int [3,7] how many lines the message is going to have without considering the full stops")

    parser.add_option("-e", "--figure-extension",
                      dest="figure_extension",
                      default='jpg',
                      help="'jpg', 'png', 'tif', 'pdf', or any compatible python figure file extension. file type of the exported figure")

    options, args = parser.parse_args()
    filename, options_dict = args[0], vars(options)
    options_dict = checks(filename, **options_dict)

    main(filename, **options_dict)
