import numpy as np
import matplotlib.pyplot as plt
import mne


# Mateusz Fido, ZFBM Biofizyka molekularna
#
# Projekt zaliczeniowy Metody Fizyczne w Biologii i Medycynie


def init():
    print("\n\n\n2019L Metody Fizyczne w Biologii i Medycynie \n")
    print("Program przetwarzający potencjały wywołane w sygnale EEG.\n")
    print("Wprowadź ścieżkę dostępu do sygnału EEG w formacie .edf \nlub wciśnij ENTER, żeby wybrać domyślny zestaw danych.")
    path = input("Ścieżka dostępu:")
    if path is None or len(path) == 0 or path != '.*.edf$':
        path = 's01/rc01.edf'

    raw = mne.io.read_raw_edf(path, preload=True)
    events = mne.events_from_annotations(raw)

    ch_number = int(input("\nZnaleziono " + str(len(raw.ch_names)) + " kanałów. Ile z nich wyświetlić?:"))
    if ch_number is None or ch_number == "" or ch_number > len(raw.ch_names):
        ch_number = 5
    ch_list = list(raw.ch_names[:ch_number])

    epochs = mne.Epochs(raw, events[0], event_id=events[1], tmin=-0.2, tmax=0.5, picks='eeg', preload=True)
    print(epochs)
    # del raw
    title = "Sygnały dla każdego z {} kanałów podzielone na segmenty".format(ch_number)
    epochs.plot(picks=ch_list, block=True, title=title)

    evoked = epochs.average()

    evoked.plot(window_title="Uśrednione przebiegi z wszystkich kanałów", time_unit="ms")

    averages = []
    for i in range(0, ch_number):
        averages.append(epochs[i].average())

    mne.viz.plot_compare_evokeds(averages, picks=ch_list, cmap='Accent', combine='mean',
                                              title="Porównanie uśrednionych przebiegów pomiędzy rodzajami znaczników")
    plt.show()


init()
