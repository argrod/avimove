"""
Signal-processing-based functions to extract meaningful characteristics of
animal accelerometer telemetry signals.
"""

import numpy as np

from scipy.signal import find_peaks, remez, filtfilt, spectrogram
from scipy.signal.windows import hamming
from scipy import stats

def lowEquiFilt(
    sig,
    passband,
    stopband,
    fs,
    ):
    """
    Generate and apply lowpass equiripple filter (equivalent to MATLAB default
    lowpass filter) to produce static (low pass) and dynamic (original - low
    pass - see Patterson et al. 2019)

    Args:
        sig:        signal to apply filter to. passband:   passband (Hz).
        stopband:   stopband (Hz). fs:         sig sampling frequency (Hz).

    Returns:
        `static`, the low pass filtered signal, and `dynamic`, the difference
        between the original signal and `static`. Both are arrays of same length
        as sig
    """
    # generate equiripple filter
    eqFil = remez(101, [0, passband, stopband, fs * 0.5], [1, 0], fs=fs)
    # return 'static' signals for each provided signal
    static = filtfilt(b=eqFil, a=1, x=sig)
    # return 'dynamic' acceleration signal
    dynamic = np.array(sig - static)

    return static, dynamic

def hammingSpect(
    sig,
    fs=25,
    ):
    """
    Generate spectrogram data of sig using a Hamming window of 4 seconds with
    85% overlap.

    Args:
        sig:    signal to generate spectrogram. fs:     sig sampling frequency
        (Hz). Defaults to 25.

    """
    # generate spectrogram (4 second window, overlap of 85%, hamming window)

    # set window size of 4 seconds
    winsize = fs * 4
    # set overlap between windows (will determine the temporal resolution
    numoverlap = np.floor(0.9875 * winsize).astype(int)
    # (85%)
    win = hamming(winsize)

    f, t, Sxx = spectrogram(sig, fs, window=win, noverlap=numoverlap)

    return f, t, Sxx

def peak_trough(
    sig
    ):
    """
    Extract peaks and troughs of signal `sig`.
    Will start with peak and end in trough to ensure equal size of outputs.
    """
    peaks, _ = find_peaks(sig)
    troughs, _ = find_peaks(-sig)
    while len(peaks) != len(troughs):
        if peaks[0] > troughs[0]:
            troughs = np.delete(troughs, 0)
        if peaks[-1] > troughs[-1]:
            peaks = np.delete(peaks, -1)

    # # create alternative of bool array indicating presence/absence of peaks (1) and troughs (2)
    # flap_sig = np.zeros(len(sig)) flap_sig[peaks] = 1 flap_sig[troughs] = 3
    return peaks, troughs

def interpeaktrough(
        mags,
    ):
    """
    Extract the value of a trough between the first two peaks of a density
    distribution of signal `mags`. If only one peak is found, then the trough
    between 0 and the first peak is returned.
    
    Params
    ------
    mags
        Signal of interest.
        
    Returns
    -------
    
    """
    kde = stats.gaussian_kde(mags)
    x = np.linspace(mags.min(), mags.max(), 100)
    p = kde(x)

    ppeaks, _ = find_peaks(p)
    pks, _ = find_peaks(-p[ppeaks[0] : ppeaks[1]])
    
    if len(pks) == 0:
        p = np.insert(p, 0, -1)
        ppeaks, _ = find_peaks(p)
        pks, _ = find_peaks(-p[ppeaks[0] : ppeaks[1]])
        if len(pks) == 0:
            raise ValueError("Flapping interpeak trough cannot be determined")
        pks = pks - 1
        
    return x[pks]

