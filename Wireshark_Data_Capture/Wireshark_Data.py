import csv
import pyshark
import tkinter as tk

# Define the Telegram port number
TELEGRAM_PORT = 443

# Define the CSV filename
CSV_FILENAME = 'Wireshark_Data.csv'

# Create the GUI window
window = tk.Tk()
window.title("Packet Capture")

# Create a text box to display packet information
text_box = tk.Text(window)
text_box.pack()

# Create a button to start packet capture
start_button = tk.Button(window, text="Start Capture", command=lambda: start_capture(capture, start_button, stop_button))
start_button.pack()

# Create a button to stop packet capture
stop_button = tk.Button(window, text="Stop Capture", command=lambda: stop_capture(capture, start_button, stop_button), state=tk.DISABLED)
stop_button.pack()

# Create a function to start packet capture
def start_capture(capture, start_button, stop_button):
    # Open the CSV file for writing
    with open(CSV_FILENAME, 'w', newline='') as csv_file:
        # Create a CSV writer object
        writer = csv.writer(csv_file)
        # Write the CSV header row
        writer.writerow(['Source IP', 'Destination IP', 'Source Port', 'Destination Port', 'Source MAC', 'Destination MAC', 'Application Data'])
        # Iterate over the captured packets and write each row to the CSV file
        for packet in capture.sniff_continuously():
            if not start_button['state'] == 'normal':
                break
            if 'ip' in packet and packet.ip.dst == '149.154.167.99':
                ip_src = packet.ip.src
                ip_dst = packet.ip.dst
                port_src = packet.tcp.srcport
                port_dst = packet.tcp.dstport
                mac_src = packet.eth.src
                mac_dst = packet.eth.dst
                app_data = packet.tcp.payload
                # Write the packet information to the CSV file
                writer.writerow([ip_src, ip_dst, port_src, port_dst, mac_src, mac_dst, app_data])
                # Display the packet information in the text box
                text_box.insert(tk.END, f'Source IP: {ip_src}, Destination IP: {ip_dst}, '
                                   f'Source Port: {port_src}, Destination Port: {port_dst}, '
                                   f'Source MAC: {mac_src}, Destination MAC: {mac_dst}, '
                                   f'Application Data: {app_data}\n')
                text_box.see(tk.END)  # scroll to the bottom of the text box

    # Disable the stop button and re-enable the start button
    stop_button.config(state=tk.DISABLED)
    start_button.config(state=tk.NORMAL)

# Create a function to stop packet capture
def stop_capture(capture, start_button, stop_button):
    # Disable the start button and re-enable the stop button
    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)

# Capture packets on the network interface
capture = pyshark.LiveCapture(interface='wlan0', bpf_filter=f'port {TELEGRAM_PORT}')

# Run the GUI loop
window.mainloop()
