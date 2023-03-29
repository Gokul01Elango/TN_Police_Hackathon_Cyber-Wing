import pyshark
import csv

# Define the network interface to capture VOIP traffic
capture = pyshark.LiveCapture(interface='wlan0', bpf_filter='udp port 5060 or udp portrange 10000-20000')

# Start the capture
capture.sniff(timeout=10)

# Create a list to store the captured data
voip_traffic = []

# Parse the captured packets and append the source and destination IP addresses of VOIP traffic to the list
for packet in capture:
    if 'UDP' in packet and 'SIP' in packet:
        src_ip = packet.ip.src
        dst_ip = packet.ip.dst
        sip_headers = dict(packet.sip.headers)
        voip_traffic.append({'protocol': 'SIP',
                             'src_ip': src_ip,
                             'dst_ip': dst_ip,
                             'src_port': packet.udp.srcport,
                             'dst_port': packet.udp.dstport,
                             'headers': sip_headers})
    elif 'UDP' in packet and 'RTP' in packet:
        src_ip = packet.ip.src
        dst_ip = packet.ip.dst
        rtp_headers = {'marker': packet.rtp.marker,
                       'payload_type': packet.rtp.payload_type,
                       'sequence': packet.rtp.seq,
                       'timestamp': packet.rtp.timestamp,
                       'ssrc': packet.rtp.ssrc}
        voip_traffic.append({'protocol': 'RTP',
                             'src_ip': src_ip,
                             'dst_ip': dst_ip,
                             'src_port': packet.udp.srcport,
                             'dst_port': packet.udp.dstport,
                             'headers': rtp_headers})

# Write the captured data to a CSV file
with open('VoIP_Packet_Data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Protocol', 'Source IP', 'Destination IP', 'Source Port', 'Destination Port', 'Headers'])
    for packet in voip_traffic:
        writer.writerow([packet['protocol'], packet['src_ip'], packet['dst_ip'], packet['src_port'], packet['dst_port'], packet['headers']])
