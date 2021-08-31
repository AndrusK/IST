import PySimpleGUI as sg
import speedtest
import threading

sg.theme('Dark2')
layout = [
    [sg.Text(text="Download:"), sg.Text(key="-down-")],
    [sg.Text(text="Upload:"), sg.Text(key="-up-", pad=(21, 0))],
    [sg.Button(button_text="Start Speed Test", key="-start_test-")],
    [sg.Text(text="Status:"), sg.Text(text="Idle", key="-status-")]
]
window = sg.Window('Internet Speed Test', layout, resizable=False, disable_minimize=True)#, size=(185, 120))


def speed_test():
    servers = []
    threads = None
    s = speedtest.Speedtest()
    s.get_servers(servers)
    s.get_best_server()
    s.download(threads=threads)
    s.upload(threads=threads)
    s.results.share()
    results_dict = s.results.dict()
    return round(results_dict['download'] / 1000000, 2), round(results_dict['upload'] / 1000000, 2)


def display_speed():
    window['-start_test-'].update(disabled=True)
    window['-status-'].Update("Running ...", text_color='red')
    down, up = speed_test()
    window['-up-'].Update(str(up) + "/Mbps")
    window['-down-'].Update(str(down) + "/Mbps")
    window['-status-'].Update("Done!", text_color='green')
    window['-start_test-'].update(disabled=False)


while True:
    thread = None
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event == "-start_test-":
        thread = threading.Thread(target=display_speed)
        thread.start()

window.close()
