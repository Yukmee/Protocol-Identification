import math
from scapy.utils import *
from scapy.layers.inet import IP, TCP, UDP
from pandas import DataFrame

feature_list = [
    'label',
    'src_ip',
    'src_port',
    'dst_ip',
    'dst_port',
    'proto',
    'packets_count',
    'duration',
    'total_len'
]

table_dict = {
    'label': [],
    'src_ip': [],
    'src_port': [],
    'dst_ip': [],
    'dst_port': [],
    'proto': [],
    'packets_count': [],
    'duration': [],
    'total_len': []
}


# Helper Methods
def gen_file_path(_file_name, from_upload):
    if from_upload:
        return './saved_pcaps/' + _file_name
    return './pcap/' + _file_name


# Convert IP Address to numeric numbers
def ip_addr_to_numeric(ip_addr):
    result = 0
    a = str(ip_addr).split('.').__reversed__()
    for index, sth in enumerate(a):
        try:
            result += int(sth) * math.pow(256, index)
        except ValueError:
            pass
    return int(result)


def converge_features(file_name, from_upload):
    pl = rdpcap(gen_file_path(file_name, from_upload))
    # pl.show()
    sessions = pl.sessions()
    i = 0
    for session in sessions:  # session is a string!
        # 标签
        label = file_name.split('.')[0]

        # 特征
        src_ip = ''
        src_port = 0
        dst_ip = ''
        dst_port = 0
        proto = 0
        packets_count = 0
        duration = 0
        total_len = 0

        session_parts = session.split(' ')
        try:
            src_ip = session_parts[1].split(':')[0]
        except IndexError:
            src_ip = -1
        try:
            src_port = session_parts[1].split(':')[1]
        except IndexError:
            src_port = -1
        try:
            dst_ip = session_parts[3].split(':')[0]
        except IndexError:
            dst_ip = -1
        try:
            dst_port = session_parts[3].split(':')[1]
        except IndexError:
            dst_port = -1
        i += 1

        j = 0
        start_time = 0
        for packet in sessions[session]:
            if j == 0:
                start_time = packet.time
                try:
                    proto = packet[IP].proto
                except IndexError:
                    proto = -1
            j += 1
            try:
                total_len += packet[IP].len
            except IndexError:
                continue
            # packet.show()  # 超详细的!
        end_time = sessions[session][j - 1].time
        duration = end_time - start_time
        duration = ("%.5f" % duration)
        packets_count = j

        # Append these features to table_dict
        table_dict['label'].append(label)
        table_dict['src_ip'].append(ip_addr_to_numeric(src_ip))
        table_dict['src_port'].append(src_port)
        table_dict['dst_ip'].append(ip_addr_to_numeric(dst_ip))
        table_dict['dst_port'].append(dst_port)
        table_dict['proto'].append(proto)
        table_dict['packets_count'].append(packets_count)
        table_dict['duration'].append(duration)
        table_dict['total_len'].append(total_len)


def export_to_single_csv():
    df = DataFrame(table_dict, columns=feature_list)
    print(df)
    df.to_csv('features_all_in_one.csv', index=None)  # Don't forget to add '.csv' at the end of the path


def export_to_df(file_name):
    converge_features(file_name, True)
    return DataFrame(table_dict, columns=feature_list)


def gen_csv():
    files_list = os.listdir("./pcap")
    for file in files_list:
        if file.endswith('.pcap') or file.endswith('.pcapng'):
            converge_features(file, False)
    export_to_single_csv()


