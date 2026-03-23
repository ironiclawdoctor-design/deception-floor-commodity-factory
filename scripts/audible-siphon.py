import os
import shutil
import glob

def siphon_audible_artifacts():
    print("--- FIESTA ARCHIVE: AUDIBLE SIPHON ACTIVE ---")
    source_pattern = "/tmp/openclaw/tts-*/voice-*.mp3"
    target_dir = "/root/.openclaw/workspace/vatican/library/audible"
    
    os.makedirs(target_dir, exist_ok=True)
    
    mp3s = glob.glob(source_pattern)
    print(f"Detected {len(mp3s)} Transient MP3s.")
    
    for mp3 in mp3s:
        filename = os.path.basename(mp3)
        shutil.move(mp3, os.path.join(target_dir, filename))
        print(f"[ARCHIVE] Secured: {filename} -> Audible Library.")
        
    print("\nSTATUS: AUDIBLE LIBRARY SYNCHRONIZED.")
    return len(mp3s)

if __name__ == "__main__":
    siphon_audible_artifacts()
