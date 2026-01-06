"""
VoiceMeeter Audio Engine Auto-Restart
Prevents audio degradation during long sessions by restarting audio engine every 20 minutes
"""
import time
import subprocess
import os
import ctypes
from datetime import datetime

# Restart interval in seconds (10 minutes = 600 seconds)
# Restarts BEFORE voice degradation occurs (usually happens after ~1 hour)
# More frequent restarts = more reliable audio quality
RESTART_INTERVAL = 600  # 10 minutes

# VoiceMeeter executable path
VOICEMEETER_PATH = r"C:\Program Files (x86)\VB\Voicemeeter\voicemeeter.exe"

# VoiceMeeter Remote DLL path
VOICEMEETER_DLL = r"C:\Program Files (x86)\VB\Voicemeeter\VoicemeeterRemote64.dll"

# Try to load VoiceMeeter Remote API
try:
    if os.path.exists(VOICEMEETER_DLL):
        vm_dll = ctypes.CDLL(VOICEMEETER_DLL)
        USE_REMOTE_API = True
    else:
        USE_REMOTE_API = False
except:
    USE_REMOTE_API = False

def restart_audio_engine():
    """Restart VoiceMeeter audio engine using multiple methods."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    print(f"🔄 [{timestamp}] Restarting VoiceMeeter audio engine...", flush=True)
    
    # Method 1: Remote API (Command.Restart = 1)
    if USE_REMOTE_API:
        try:
            print(f"   Trying Remote API method...", flush=True)
            
            # Try to logout first in case previous connection stuck
            try:
                vm_dll.VBVMR_Logout()
                time.sleep(0.2)
            except:
                pass
            
            result = vm_dll.VBVMR_Login()
            if result == 0:
                # Set Command.Restart = 1
                param = ctypes.c_char_p(b"Command.Restart")
                vm_dll.VBVMR_SetParameterFloat(param, ctypes.c_float(1.0))
                time.sleep(3)  # Wait for restart to complete
                vm_dll.VBVMR_Logout()
                
                # Verify VoiceMeeter still running after restart
                time.sleep(1)
                if check_voicemeeter_running():
                    print(f"✅ [{timestamp}] Audio engine restarted successfully (Remote API)", flush=True)
                    print(f"   VoiceMeeter verified running", flush=True)
                    print(f"   Audio quality restored\n", flush=True)
                    return True
                else:
                    print(f"⚠️  VoiceMeeter stopped after restart, trying command line...", flush=True)
            elif result == -2:
                print(f"⚠️  Remote API busy (code -2: already connected), using command line...", flush=True)
            else:
                print(f"⚠️  Remote API login failed (code {result}), trying command line...", flush=True)
        except Exception as e:
            print(f"⚠️  Remote API error: {e}, trying command line...", flush=True)
    
    # Method 2: Command line (-r parameter)
    try:
        print(f"   Trying command line method (-r)...", flush=True)
        result = subprocess.run([VOICEMEETER_PATH, "-r"], 
                              capture_output=True, 
                              timeout=10,
                              check=False)
        
        print(f"   Command returned: {result.returncode}", flush=True)
        time.sleep(3)  # Wait for restart
        
        # Verify it worked
        if check_voicemeeter_running():
            print(f"✅ [{timestamp}] Audio engine restarted successfully (Command line)", flush=True)
            print(f"   VoiceMeeter verified running", flush=True)
            print(f"   Audio quality restored\n", flush=True)
            return True
        else:
            print(f"⚠️  VoiceMeeter not running after restart!", flush=True)
            
    except Exception as e:
        print(f"⚠️  Command line error: {e}", flush=True)
    
    print(f"❌ [{timestamp}] All restart methods failed - manual intervention needed!", flush=True)
    return False

def check_voicemeeter_running():
    """Check if VoiceMeeter is running."""
    try:
        result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq voicemeeter.exe'],
                              capture_output=True, text=True)
        return 'voicemeeter.exe' in result.stdout
    except:
        return False

def main():
    """Main loop - restart audio engine every 20 minutes."""
    print("="*70)
    print("🔄 VoiceMeeter Audio Engine Auto-Restart")
    print("="*70)
    print(f"⏰ Will restart audio engine every {RESTART_INTERVAL/60:.0f} minutes")
    print("🎯 This prevents audio degradation during long sessions")
    print("⚠️  Keep this window open while bot is running")
    print("="*70 + "\n")
    
    # Check if VoiceMeeter is installed
    if not os.path.exists(VOICEMEETER_PATH):
        print(f"❌ VoiceMeeter not found at: {VOICEMEETER_PATH}")
        print("   Please install VoiceMeeter or update the path")
        input("\nPress Enter to exit...")
        return
    
    restart_count = 0
    
    try:
        while True:
            # Check if VoiceMeeter is running
            if not check_voicemeeter_running():
                print("⚠️  VoiceMeeter is not running! Waiting...", flush=True)
                time.sleep(10)
                continue
            
            # Wait for interval
            next_restart = datetime.now().timestamp() + RESTART_INTERVAL
            
            while time.time() < next_restart:
                remaining = int(next_restart - time.time())
                minutes = remaining // 60
                seconds = remaining % 60
                print(f"\r⏳ Next restart in: {minutes:02d}:{seconds:02d}   ", end='', flush=True)
                time.sleep(1)
            
            print()  # New line
            
            # Restart audio engine
            if restart_audio_engine():
                restart_count += 1
                print(f"📊 Total restarts: {restart_count}\n", flush=True)
            
            # Small delay after restart
            time.sleep(5)
    
    except KeyboardInterrupt:
        print("\n\n" + "="*70)
        print("🛑 Auto-restart stopped")
        print(f"📊 Total audio engine restarts: {restart_count}")
        print("="*70)

if __name__ == "__main__":
    main()

