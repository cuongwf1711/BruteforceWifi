import pywifi
from pywifi import const
import time

wifi_Main = pywifi.PyWiFi()

def list_wifi(wifi):
    results = sorted(wifi.interfaces()[0].scan_results().scan_results(), key=lambda x: x.signal, reverse=True)
    
    ssid_signal = {}
    for a in results:
        if a.ssid not in ssid_signal or a.signal > ssid_signal[a.ssid]:
            ssid_signal[a.ssid] = a.signal
    
    return [ssid for ssid, signal in sorted(ssid_signal.items(), key=lambda x: x[1], reverse=True)]
    # return {"QUANG NGO"}

def is_profile_exist(iface, ssid):

    profiles = iface.network_profiles()

    for profile in profiles:

        if profile.ssid == ssid:

            return profile

    return None


def connect_wifi(ifaces, ssid, password):
    
    
    if is_profile_exist(ifaces, ssid):
        print("Kết nối thành công!")
        return True
    
    profile = pywifi.Profile()
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP
    profile.key = password
    tmp_profile = ifaces.add_network_profile(profile)
    ifaces.connect(tmp_profile)
    
    start_time = time.time()
    while time.time() - start_time < 5:
        if ifaces.status() == const.IFACE_CONNECTED:
            print("Kết nối thành công!")
            return True
        time.sleep(1)
        
    ifaces.disconnect()
    ifaces.remove_network_profile(tmp_profile)
    print("Không thể kết nối sau 5 giây. Đã xóa profile. Vui lòng kiểm tra lại SSID và mật khẩu.")
    return False
    
for s in list_wifi(wifi_Main):
    with open('passw.txt', 'r') as myfile:
        for line in myfile:
            if connect_wifi(wifi_Main.interfaces()[0], s, line.strip()):
                break
