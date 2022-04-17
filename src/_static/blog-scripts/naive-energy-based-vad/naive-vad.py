# -*- coding: utf-8 -*-
import scipy
import subprocess
import numpy as np
import scipy.signal
import scipy.io.wavfile
import matplotlib.pyplot as plt


def set_up_matplotlib_style():
    # format style
    plt.rcParams['axes.grid']  = True
    plt.rcParams['grid.color'] = 'w'
    plt.rcParams['grid.linestyle'] = '--'
    plt.rcParams['grid.linewidth'] = .2
    plt.rcParams['axes.edgecolor']  = '#1171A2'
    plt.rcParams['axes.facecolor']  = '#1d1f21'
    plt.rcParams['axes.labelcolor'] = '#1171A2'
    plt.rcParams['boxplot.capprops.color'] = '#1d1f21'
    plt.rcParams['boxplot.flierprops.markeredgecolor'] = '#1d1f21'
    plt.rcParams['boxplot.meanprops.color'] = '#1d1f21'
    plt.rcParams['boxplot.meanprops.markeredgecolor'] = '#1d1f21'
    plt.rcParams['boxplot.meanprops.markerfacecolor'] = '#1d1f21'
    plt.rcParams['boxplot.whiskerprops.color'] = '#1d1f21'
    plt.rcParams['figure.edgecolor'] = '#1d1f21'
    plt.rcParams['figure.facecolor'] = '#1d1f21'
    plt.rcParams['grid.color'] = '#1d1f21'
    plt.rcParams['lines.color'] = '#1d1f21'
    plt.rcParams['patch.edgecolor'] = '#1d1f21'
    plt.rcParams['patch.facecolor'] = '#1d1f21'
    plt.rcParams['savefig.edgecolor'] = '#1d1f21'
    plt.rcParams['savefig.facecolor'] = '#1d1f21'
    plt.rcParams['text.color'] = '#1171A2'
    plt.rcParams['xtick.color'] = '#1171A2'
    plt.rcParams['ytick.color'] = '#1171A2'

    # define plots text colors
    text_color = '#004B6B'
    plt.rcParams['axes.labelcolor'] = text_color
    plt.rcParams['grid.color']      = text_color
    plt.rcParams['axes.edgecolor']  = text_color
    plt.rcParams['text.color']      = text_color
    plt.rcParams['xtick.color']     = text_color
    plt.rcParams['ytick.color']     = text_color


def stride_trick(a, stride_length, stride_step):
    """
    apply framing using the stride trick from numpy.

    Args:
        a (array) : signal array.
        stride_length (int) : length of the stride.
        stride_step (int) : stride step.

    Returns:
        blocked/framed array.
    """
    nrows = ((a.size - stride_length) // stride_step) + 1
    n = a.strides[0]
    return np.lib.stride_tricks.as_strided(a,
                                           shape=(nrows, stride_length),
                                           strides=(stride_step*n, n))


def framing(sig, fs=16000, win_len=0.025, win_hop=0.01):
    """
    transform a signal into a series of overlapping frames (=Frame blocking).

    Args:
        sig     (array) : a mono audio signal (Nx1) from which to compute features.
        fs        (int) : the sampling frequency of the signal we are working with.
                          Default is 16000.
        win_len (float) : window length in sec.
                          Default is 0.025.
        win_hop (float) : step between successive windows in sec.
                          Default is 0.01.

    Returns:
        array of frames.
        frame length.

    Notes:
    ------
        Uses the stride trick to accelerate the processing.
    """
    # run checks and assertions
    if win_len < win_hop: print("ParameterError: win_len must be larger than win_hop.")

    # compute frame length and frame step (convert from seconds to samples)
    frame_length = win_len * fs
    frame_step = win_hop * fs
    signal_length = len(sig)
    frames_overlap = frame_length - frame_step

    # compute number of frames and left sample in order to pad if needed to make
    # sure all frames have equal number of samples  without truncating any samples
    # from the original signal
    rest_samples = np.abs(signal_length - frames_overlap) % np.abs(frame_length - frames_overlap)
    pad_signal = np.append(sig, np.array([0] * int(frame_step - rest_samples) * int(rest_samples != 0.)))

    # apply stride trick
    frames = stride_trick(pad_signal, int(frame_length), int(frame_step))
    return frames, frame_length


def _calculate_normalized_short_time_energy(frames):
    return np.sum(np.abs(np.fft.rfft(a=frames, n=len(frames)))**2, axis=-1) / len(frames)**2


def naive_frame_energy_vad(sig, fs, threshold=-20, win_len=0.25, win_hop=0.25, E0=1e7):
    # framing
    frames, frames_len = framing(sig=sig, fs=fs, win_len=win_len, win_hop=win_hop)

    # compute short time energies to get voiced frames
    energy = _calculate_normalized_short_time_energy(frames)
    log_energy = 10 * np.log10(energy / E0)

    # normalize energy to 0 dB then filter and format
    energy = scipy.signal.medfilt(log_energy, 5)
    energy = np.repeat(energy, frames_len)

    # compute vad and get speech frames
    vad     = np.array(energy > threshold, dtype=sig.dtype)
    vframes = np.array(frames.flatten()[np.where(vad==1)], dtype=sig.dtype)
    return energy, vad, np.array(vframes, dtype=np.float64)


def multi_plots(data, titles, fs, plot_rows, step=1, colors=["b", "r", "m", "g", "b", "y"]):
    # first fig
    fig, _ = plt.subplots(plot_rows, 1, figsize=(17, 7))
    plt.subplots_adjust(left=0.125, right=0.9, bottom=0.1, top=0.9, wspace=0.4, hspace=0.65)

    for i in range(plot_rows):
        plt.subplot(plot_rows, 1, i+1)
        y = data[i]
        plt.plot([i/fs for i in range(0, len(y), step)], y, colors[i])
        plt.gca().set_title(titles[i])
        # Annotate diagram
        if i ==             0: plt.ylabel("Amplitude")
        if i == plot_rows - 1: plt.xlabel("Time (s)")
        plt.grid(False)
    plt.show()
    fig.savefig("../../../docs/source/_static/blog-plots/vad/naive_vad_multi_plots.png",
                transparent=True)

    # second fig
    sig, vad = data[0], data[-2]
    # plot VAD and orginal signal
    fig, ax = plt.subplots(1, 1, figsize=(15, 5))
    plt.plot([i/fs for i in range(len(sig))], sig, label="Signal")
    plt.plot([i/fs for i in range(len(vad))], max(sig)*vad, label="VAD")
    plt.legend(loc='best')
    plt.show()
    
    # Annotate diagram
    ax.set_ylabel("Amplitude")
    ax.set_xlabel("Time (s)")
    ax.grid(False)
        
    # Draw legend
    plt.rcParams['patch.edgecolor'] = "red"
    
    ax.legend(shadow=False, framealpha=0.0, facecolor=None)
    plt.show()
    fig.savefig("../../../docs/source/_static/blog-plots/vad/vad_and_signal.png",
                transparent=True)




def equalize_loudness_using_peak_normalization(wave_file):
    # define loudness equalization command
    down_sampling_command = ["ffmpeg-normalize",
                             "-f",
                             wave_file,
                             "-nt","peak", "-t", "0", "-o",
                             "equilized_" + wave_file]
    # excute command
    subprocess.Popen(down_sampling_command)


if __name__ == "__main__":
    # init vars
    set_up_matplotlib_style()
    plots_path = "../../../docs/source/_static/blog-plots/naive-energy-vad/"

    # equlize sample then read sig
    fname = "OSR_us_000_0060_8k.wav"
    fs, sig = scipy.io.wavfile.read(fname)

    #########################
    # naive_frame_energy_vad
    #########################
    # get voiced frames
    energy, vad, voiced = naive_frame_energy_vad(sig, fs, threshold=-35,
                                                 win_len=0.025, win_hop=0.025)

    # plot results
    multi_plots(data=[sig, energy, vad, voiced],
                titles=["Input signal (voiced + silence)", "Short time energy",
                        "Voice activity detection", "Output signal (voiced only)"],
                fs=fs, plot_rows=4, step=1)

    # save voiced signal
    scipy.io.wavfile.write("naive_frame_energy_vad_no_silence_"+ fname,
                           fs,  np.array(voiced, dtype=sig.dtype))
