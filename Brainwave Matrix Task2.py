import os
import subprocess
import time
from datetime import datetime

# Step 1: Setup the environment
SANDBOX_DIR = "sandbox_env"
LOG_FILE = "sandbox_log.txt"

# Create a controlled environment for running samples
def setup_environment():
    if not os.path.exists(SANDBOX_DIR):
        os.makedirs(SANDBOX_DIR)
    print(f"Sandbox environment setup at {SANDBOX_DIR}")

# Log function to track events
def log_event(event):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as log:
        log.write(f"[{timestamp}] {event}\n")

# Step 2: Execute malware sample in controlled environment
def execute_sample(sample_path):
    try:
        print(f"Executing {sample_path}...")
        log_event(f"Executing sample: {sample_path}")
        process = subprocess.Popen([sample_path], cwd=SANDBOX_DIR, 
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(10)  # Allow sample to run for some time

        # Monitor the process manually
        monitor_process_manual(process.pid)
        
        process.terminate()
        log_event(f"Execution completed for: {sample_path}")
    except Exception as e:
        log_event(f"Error during execution: {e}")

# Step 3: Monitor behavior during execution (manual approach)
def monitor_process_manual(pid):
    try:
        # Check if process exists
        process_path = f"/proc/{pid}/stat" if os.name != "nt" else None
        if not process_path or not os.path.exists(process_path):
            log_event(f"Process {pid} does not exist or terminated early.")
            return

        log_event(f"Monitoring process {pid}")

        # Basic monitoring (Linux only - extend for Windows if needed)
        with open(process_path, "r") as stat_file:
            stats = stat_file.read().split()
            if len(stats) > 13:
                cpu_usage = stats[13]
                mem_usage = stats[22]
                log_event(f"CPU Time: {cpu_usage}, Memory: {mem_usage} bytes")

    except Exception as e:
        log_event(f"Error while monitoring process {pid}: {e}")

# Step 4: Analyze logs for malicious activity
def analyze_logs():
    with open(LOG_FILE, "r") as log:
        logs = log.readlines()
        for line in logs:
            if "Error" in line or "Warning" in line:
                print(f"Potential issue detected: {line.strip()}")

# Main workflow
def main():
    setup_environment()

    # Example malware sample (replace with actual sample path in testing)
    sample_path = "sample.exe"

    # Check if the sample exists
    if not os.path.exists(sample_path):
        print(f"Sample file {sample_path} does not exist.")
        return

    execute_sample(sample_path)
    analyze_logs()

if __name__ == "__main__":
    main()
