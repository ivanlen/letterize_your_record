from optparse import OptionParser

if __name__=='__main__':
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename",
                      help="write report to FILE", metavar="FILE")

    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose", default=True,
                      help="don't print status messages to stdout")

    parser.add_option("-p", "--fullstop",
                      action="store_false", dest="full_stop", default=-1,
                      help="make full stop if te time is bigger than")

    parser.add_option("-t", "--treshold",
                      action="store_false", dest="tresh", default=0.1,
                      help="[0,1] treshold to divide phrases. If the ouput is not the desired you can play whith this value")


    (options, args) = parser.parse_args()

    print(options )

    print(args)