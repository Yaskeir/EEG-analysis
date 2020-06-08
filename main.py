import warnings
warnings.filterwarnings("ignore", "(?s).*MATPLOTLIBDATA.*", category=UserWarning)
import numpy as np
import matplotlib.pyplot as plt
import mne
import sys
import time
from pynput.keyboard import Key, Listener

# Mateusz Fido, ZFBM Biofizyka molekularna
#
# Projekt zaliczeniowy Metody Fizyczne w Biologii i Medycynie


def init():
    print("2019L Metody Fizyczne w Biologii i Medycynie \n")
    print("Program przetwarzający potencjały wywołane w sygnale EEG.\n")
    print(
        "Wprowadź ścieżkę dostępu do sygnału EEG w formacie .edf\n"
        "lub wciśnij ENTER, żeby wybrać domyślny zestaw danych.")
    path = input("Ścieżka dostępu:")
    if path is None or len(path) == 0 or path != '.*.edf$':
        path = 's01/rc01.edf'
    try:
        raw = mne.io.read_raw_edf(path, preload=True)
        events = mne.events_from_annotations(raw)
    except:
        print("Wystąpił problem ze znalezieniem domyślnej ścieżki.\n"
                 "Brakuje pliku o lokalizacji ./s01/rc01.edf.")
        time.sleep(5)
        sys.exit()

    try:
        ch_number = int(input("\nZnaleziono " + str(len(raw.ch_names)) + " kanałów. Ile z nich wyświetlić?:"))
        if ch_number is None or ch_number == "" or ch_number > len(raw.ch_names):
            ch_number = 5
        ch_list = list(raw.ch_names[:ch_number])
    except ValueError:
        print("Podano niewłaściwą liczbę kanałów. Proszę spróbować ponownie.")
        time.sleep(5)
        sys.exit()

    epochs = mne.Epochs(raw, events[0], event_id=events[1], tmin=-0.2, tmax=0.5, picks='eeg', preload=True)

    print("Wyświetlam wybrane kanały.")

    title = "Sygnały ciągłe dla każdego z {} kanałów podzielone na segmenty".format(ch_number)
    epochs.plot(picks=ch_list, block=True, title=title)

    evoked = epochs.average()                   # uśrednianie przebiegu dla każdego znacznika

    print("Wyświetlam uśrednione przebiegi z wszystkich kanałów.")
    evoked.plot(window_title="Uśrednione przebiegi z wszystkich kanałów", time_unit="ms")

    print("Wyświetlam zestawienie przebiegów uśrednionych po znacznikach w zależności od kanału.")
    evoked.plot_image(time_unit="ms", titles="Porównanie uśrednionych przebiegów pomiędzy kanałami\n\n")

    averages = []
    for i in range(0, ch_number):              # uśrednianie przebiegów dla każdego z wybranych kanałów
        averages.append(epochs[i].average())

    print("Wyświetlam porównanie przebiegów pomiędzy rodzajami znaczników.\nUWAGA: w analizowanym zestawie danych występuje tylko jeden rodzaj znaczników.")
    mne.viz.plot_compare_evokeds(averages, picks=ch_list, cmap='Accent', combine='mean',
                                 title="Porównanie uśrednionych przebiegów pomiędzy rodzajami znaczników")

    plt.show()

    print("\n\nAnaliza zakończona sukcesem.")
    print("Wciśnij ENTER, żeby przeprowadzić analizę\nponownie lub ESC, żeby zakończyć.")
    with Listener(on_press=on_press) as listener:
        listener.join()


def on_press(key):                              # funkcja nasłuchującą wcisnięcie klawisza ENTER bądź ESC
    if key == Key.enter:
        init()
    elif key == Key.esc:
        sys.exit()


init()
