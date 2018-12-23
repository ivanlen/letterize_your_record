import librosa
import numpy as np
import matplotlib
import os
matplotlib.use('agg')
import matplotlib.pyplot as plt


class Writer(object):
    def __init__(self, filename,
                 max_sampling_rate=22050 // 4,
                 loudness_thresh=0.04,
                 plot_downsampling_factor=5,
                 full_stop_time=1.2,
                 lines_in_figure=5,
                 figure_extension='jpg'):

        self.filename = filename
        self.max_sampling_rate = max_sampling_rate
        self.loudness_thresh = loudness_thresh
        self.plot_downsampling_factor = plot_downsampling_factor
        self.full_stop_time = full_stop_time
        self.lines_in_figure = lines_in_figure
        self.figure_extension = '.' + figure_extension

    def load_audio(self):
        audio, sr_temp = librosa.load(self.filename)

        if sr_temp > self.max_sampling_rate:
            audio = librosa.resample(audio, sr_temp, self.max_sampling_rate)
            sr = self.max_sampling_rate
        else:
            sr = sr_temp

        time = np.arange(len(audio)) / sr

        self.audio_raw = audio
        self.sr = sr
        self.time_raw = time

    def compute_loudness(self, n_fft=256):

        fourier = librosa.stft(self.audio_raw, n_fft=n_fft)
        S = np.abs(fourier * np.conj(fourier))
        log_S = librosa.perceptual_weighting(S ** 2, librosa.fft_frequencies(n_fft=n_fft))
        self.loudness = log_S.sum(axis=0, keepdims=True)[0]
        self.n_points = int(n_fft / 4)
        self.n_windows = int(np.ceil(len(self.audio_raw) / self.n_points))
        print('processing windows: {}'.format(self.n_windows))
        print('points per windows: {}'.format(self.n_points))

    def generate_phrases_filter(self):

        thresh_ = (np.max(self.loudness) - np.min(self.loudness)) * self.loudness_thresh
        thresh = np.min(self.loudness) + thresh_
        self.filter_chunks_thresh_ok = self.loudness > thresh

    def generate_chunks(self):

        ds = self.plot_downsampling_factor  # downsampling audio so plots looks nicer and smoother

        filter_audio = []
        audio_chunks = []
        time_chunks = []

        # expand the filter of the chunks for the whole audio
        for i, filt in enumerate(self.filter_chunks_thresh_ok):
            filter_audio += [filt] * self.n_points
        filter_audio = np.array(filter_audio)

        # cut if exceedes the length of the audio
        if self.n_windows * self.n_points > len(self.audio_raw):
            n_extra = self.n_windows * self.n_points - len(self.audio_raw)
            print('filter has {} extra elementrs'.format(n_extra))
            filter_audio = filter_audio[:-n_extra]
        self.filter_audio = filter_audio

        # filter and rescale audio
        audio_filtered = np.copy(self.audio_raw)
        audio_filtered[~filter_audio] = np.nan
        max_audio_val = np.nanmax(np.abs(audio_filtered))
        self.audio_rescaled = audio_filtered / max_audio_val  # now audio goes between (-1,1)

        # generate audio and time chunks
        for i, filt in enumerate(self.filter_chunks_thresh_ok):
            i_ini = i * self.n_points
            if i < self.n_windows - 1:
                i_end = (i + 1) * self.n_points
            else:
                i_end = len(self.audio_rescaled)
            i_int = np.arange(i_ini, i_end, ds)
            if filt:
                audio_chunks.append(self.audio_rescaled[i_int])
            else:
                audio_chunks.append([np.nan] * len(i_int))
            time_chunks.append(self.time_raw[i_int])

        self.audio_chunks = np.array(audio_chunks)
        self.time_chunks = np.array(time_chunks)

    def generate_plot(self):

        # parameters
        n_lines = self.lines_in_figure
        chucnks_per_line = np.ceil(self.n_windows / n_lines)
        max_time = chucnks_per_line * self.n_points / self.sr
        full_stop_time = self.full_stop_time
        fix_y = 1.0

        # init
        n_line = 0
        correct_time = 0
        last_valid_time = 0
        elements_in_line = False

        # go
        plt.figure(figsize=(8, 5))
        for i in range(self.n_windows):

            # existe algun valor no invalido & todavia no se escribio nada en la linea
            if not np.any((np.isnan(self.audio_chunks[i]))) and not elements_in_line:
                correct_time = self.time_chunks[i][0]
                elements_in_line = True

            rel_time = self.time_chunks[i] - correct_time
            plt.plot(rel_time, np.array(self.audio_chunks[i]) - fix_y * n_line, color='black', lw=0.5)
            last_time = rel_time[-1]

            if not np.any((np.isnan(self.audio_chunks[i]))):
                last_valid_time = last_time

            if (last_time) > max_time and elements_in_line:
                n_line += 1
                elements_in_line = False
            elif full_stop_time>0  and (last_time - last_valid_time) > full_stop_time and elements_in_line:
                n_line += 1
                elements_in_line = False

        plt.axis('off')

        filename_base = (os.path.splitext(os.path.basename((self.filename))))[0]
        letters_path = './written_letters/'
        if not os.path.exists(letters_path):
            os.makedirs(letters_path)
        figure_filename = './' + letters_path + filename_base + self.figure_extension
        print(filename_base)
        print('saving figure...')
        plt.savefig(figure_filename)
