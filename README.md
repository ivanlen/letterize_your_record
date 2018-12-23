# Letterize your record

This is a python script that generates *nice* written messages from a audio records:

![Alt text](./written_letters/cortazar.jpg?raw=true "Title")

Instead of using characters, writes a *message* using the waveform of the audio and separating it by *sound syllables*.

## Getting Started

Clone the repo and be sure to have the needed packages listed in [requirements.txt](requirements.txt).

<!-- These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system. -->





### Prerequisites

Install the packages in [requirements.txt](requirements.txt) either using pip, conda or compiling them.

No installation is required.

### Running an example

To run a test use the provided audio example.

```
python audiowriter.py ./audio/cortazar.m4a
```

The corresponding message will be saved in `./written_letters/`

## Letterizing your own audios

For visual reasons we recommend to use audios of around 30 seconds.
The audio filename must be provided.
There are some parameters and options that allow you to customize the output of the script.

| option | values | description |
| :---         |     :---        |     :---     |
| -s, --full-stop  | *float* (0,3], default:-1     | default `-1`: no there are not going to be fullstops. `val>0`: a separate point will be made if the distance in seconds between two syllables is greater than val.  |
| -t, --audio-threshold     | *float* (0,1], default:0.04      | if the relative loudness is small than a relative value scaled by `thresh` the audio is going to be separated in two syllables.      |
| -d, --downsampling    | *int* [1:10], default: 5       | downsampling factor to reduce the density of the plot (for visual purposes).     |
| -l, --lines-in-figure     | *int* [3,7]       | how many lines the message is going to have without considering the full stops      |
| -e, --extension     | 'jpg', 'png', 'tif', 'pdf', or any compatible python figure file extension       | file type of the exported figure      |


```
python audiowriter.py ./audio/filename [options]
```



## Contributing

is always welcome.

## Future releases
will include

* more flexible plotting interface and customization

* adding title or ending phrase

* adding text

* making an app, *niiiceee*



## Authors

* **Ivan Lengyel**


## License

<a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/"><img alt="Creative Commons Licence" style="border-width:0" src="https://i.creativecommons.org/l/by-nc/4.0/80x15.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/">Creative Commons Attribution-NonCommercial 4.0 International License</a>.
