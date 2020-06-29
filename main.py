import mne
import sys
import time
from numpy import amax
from pynput.keyboard import Key, Listener


# Mateusz Fido, ZFBM Biofizyka molekularna
#
# Projekt zaliczeniowy Metody Fizyczne w Biologii i Medycynie


def init():
    global evoked
    print("2019L Metody Fizyczne w Biologii i Medycynie \n")
    print("Program przetwarzający potencjały wywołane w sygnale EEG.\n")
    print(
        "Wprowadź ścieżkę dostępu do sygnału EEG w formacie .edf\n"
        "lub wciśnij ENTER, żeby wybrać domyślny zestaw danych.\n")
    path = input("Ścieżka dostępu:")
    if path is None or len(path) == 0 or path != '.*.edf$':
        path = 's01/rc01.edf'
    try:
        raw = mne.io.read_raw_edf(path, preload=True)
        events, event_dict = mne.events_from_annotations(raw)
        for key in list(event_dict):                # usuń niepotrzebne znaczniki zaczynające się od "#"
            if key.startswith('#'):
                del event_dict[key]

    except IOError:
        print("Wystąpił problem ze znalezieniem domyślnej ścieżki.\n"
              "Brakuje pliku o lokalizacji ./s01/rc01.edf.")
        time.sleep(5)
        sys.exit()

    print("\n\nZnaleziono {} kanałów oraz następujące znaczniki:".format(str(len(raw.ch_names))))

    print(event_dict,'\n')

    raw.crop(2, 42)                                # przytnij i przefiltruj surowe dane
    raw.filter(1.0, 48.0, filter_length='auto')

    raw.plot(block=True, title="Zestawienie wszystkich kanałów z zaznaczonymi znacznikami. Kliknij na kanał, aby usunąć go z analizy.")

    bad_channels = raw.info['bads']
    raw_data = raw.get_data()

    index = -1
    for channel in raw_data:
        index += 1
        if amax(channel) > 100e-6:
            bad_channels.append(raw.ch_names[index])

    raw.drop_channels(bad_channels)

    epochs = mne.Epochs(raw, events=events, event_id=event_dict, tmin=-0.2, tmax=0.5, preload=True)

    evoked_list = []
    for condition in event_dict:
        evoked_list.append(epochs[condition].average())     # uśrednij odpowiedź dla każdego znacznika
                                                            # (20 eventów w domyślnym zestawie danych)

    evoked_responses = []
    peaks = []

    for evoked in evoked_list:
        peak = evoked.get_peak(mode='pos', return_amplitude=True)   # znajdź kanał z najsilniejszą odpowiedzią
        if (0.45 > peak[1] > 0.2): #and peak[2] > 6e-6:     #   jeśli latencja odpowiada potencjałowi P300 i amplituda większa niż szum
            peaks.append(peak)
            evoked_responses.append(evoked)

    print(evoked_responses)

    for peak, key in zip(peaks, event_dict):
        print("Dla znacznika {} znaleziono odpowiedź o amplitudzie {} \u03BCV na kanale {} w czasie {}".format(str(key), str(round(peak[2]*1.0e6, 2)), peak[0], peak[1]))

    for evoked, peak, key in zip(evoked_responses, peaks, event_dict):
        title = "Odpowiedź na kanale {} dla znacznika {}".format(peak[0], str(key))
        evoked.plot(picks=peaks[0], titles=title)


    # for evoked in evoked_list:
    #     evoked_averages.append(np.mean(evoked.data, axis=0))
    #                                                                   #   dwie pętle pozwalające
    #                                                                   #   na uśrednienie po wszystkich
    #                                                                   #   kanałach: nie dają sensownych wyników
    # for evoked in evoked_averages:
    #     plt.plot(evoked)
    #     plt.show()

    print("\n\nAnaliza zakończona sukcesem.")
    print("Wciśnij ENTER, żeby przeprowadzić analizę\nponownie lub ESC, żeby zakończyć.")
    with Listener(on_press=on_press) as listener:
        listener.join()


def on_press(key):  # funkcja nasłuchującą wcisnięcie klawisza ENTER bądź ESC
    if key == Key.enter:
        init()
    elif key == Key.esc:
        sys.exit()


init()
