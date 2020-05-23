import numpy as np
import matplotlib.pyplot as plt
import mne

path = 'data/seizures/chb01_03.edf'
raw = mne.io.read_raw_edf(path, preload=True)
# raw = Raw(path)
# events = mne.find_events(raw, stim_channel='auto') <- No stim channels found to extract trigger events

print(raw)
print(raw.info)

raw.plot_psd()

sfreq = raw.info['sfreq']
data, times = raw[:23, int(sfreq * 1):int(sfreq * 100)]

fig = plt.subplots(figsize=(10,8))
plt.plot(times, data.T)
plt.xlabel('Czas (s)')
plt.ylabel('$\mu V$')                       # kanały 1-23
plt.title('Kanały: 1-23')
# plt.legend(raw.ch_names[:23])
plt.show()

print(raw.ch_names)
# raw.plot(duration=60, block=True) # wszystkie kanały