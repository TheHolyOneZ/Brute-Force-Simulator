import time
import random

class FakeCPU:
    def __init__(self, slowdown_factor=1.0, max_threads=8, overheating=False):
        """Initialize the fake CPU with adjustable performance settings."""
        self.slowdown_factor = slowdown_factor  
        self.max_threads = max_threads  
        self.overheating = overheating  

    def limit_threads(self, requested_threads):
        """Limit the number of threads based on CPU restrictions."""
        return min(requested_threads, self.max_threads)

    def simulate_slowdown(self):
        """Simulate CPU slowdown by adding artificial delay."""
        time.sleep(0.01 * self.slowdown_factor)  

        if self.overheating and random.random() < 0.1:  # 10% chance of a big lag spike
            extra_delay = random.uniform(0.2, 1.0)  
            print(f"🔥 CPU Overheated! Extra delay: {extra_delay:.2f}s")
            time.sleep(extra_delay)

    def apply_overheat_mode(self, elapsed_time):
        """Dynamically slow down based on runtime (simulates overheating)."""
        if elapsed_time > 5 and self.overheating:
            self.slowdown_factor *= 1.5 
            print("⚠️ CPU Overheating! Performance reduced further.")


def select_fake_cpu():
    """Allows the user to choose a CPU profile."""
    print("\n🖥️  Select a CPU profile:")
    print("[1] Normal CPU (No slowdown, max 32 threads)")
    print("[2] Slower CPU (50% slower, max 4 threads)")
    print("[3] Very Slow CPU (3x slower, max 2 threads)")
    print("[4] Custom CPU (Enter your own settings)")
    
    choice = input("Choice: ").strip()

    if choice == "1":
        return FakeCPU(slowdown_factor=1.0, max_threads=32, overheating=False)
    elif choice == "2":
        return FakeCPU(slowdown_factor=1.5, max_threads=4, overheating=False)
    elif choice == "3":
        return FakeCPU(slowdown_factor=3.0, max_threads=2, overheating=True)
    elif choice == "4":
    
        try:
            slowdown = float(input("Enter slowdown factor (1.0 = normal, 2.0 = 2x slower, etc.): ").strip())
            max_threads = int(input("Enter max allowed threads (1-32): ").strip())
            overheating = input("Enable overheating mode? (yes/no): ").strip().lower() == "yes"

            max_threads = max(1, min(32, max_threads))  

            return FakeCPU(slowdown_factor=slowdown, max_threads=max_threads, overheating=overheating)
        except ValueError:
            print("❌ Invalid input! Using normal CPU.")
            return FakeCPU(slowdown_factor=1.0, max_threads=32, overheating=False)
    
    print("❌ Invalid choice! Using normal CPU.")
    return FakeCPU(slowdown_factor=1.0, max_threads=32, overheating=False)
