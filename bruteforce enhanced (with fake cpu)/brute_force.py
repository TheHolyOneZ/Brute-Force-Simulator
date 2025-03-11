import itertools
import string
import time
import concurrent.futures
from fake_cpu import select_fake_cpu  # Import the fake CPU system

fake_cpu = select_fake_cpu()

def get_charset(option):
    charsets = {
        "1": string.ascii_letters,
        "2": string.digits,
        "3": string.ascii_letters + string.digits,
        "4": string.printable.strip()
    }
    return charsets.get(option, string.ascii_letters)

def brute_force(target, charset_option, max_workers, silent=False):
    charset = get_charset(charset_option)
    start_time = time.time()
    attempt_counter = 0

    max_workers = fake_cpu.limit_threads(max_workers)

    def attempt_combination(length):
        for attempt_tuple in itertools.product(charset, repeat=length):
            fake_cpu.simulate_slowdown()  
            yield "".join(attempt_tuple)

    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            for length in range(1, len(target) + 1):
                futures = {executor.submit(lambda x: x, attempt): attempt for attempt in attempt_combination(length)}

                for future in concurrent.futures.as_completed(futures):
                    attempt = futures[future]
                    attempt_counter += 1
                    if not silent and attempt_counter % 1000 == 0:
                        print(f"Attempts: {attempt_counter}, Last Try: {attempt}")

                    if attempt == target:
                        elapsed = time.time() - start_time
                        fake_cpu.apply_overheat_mode(elapsed)  
                        if not silent:
                            print(f"\n[✔] Found: '{attempt}' in {elapsed:.2f} seconds after {attempt_counter} attempts!")
                        return elapsed, attempt_counter
    except KeyboardInterrupt:
        print("\n[!] Process interrupted by user.")
    finally:
        if not silent:
            print(f"[ℹ] Total attempts: {attempt_counter}, Elapsed time: {time.time() - start_time:.2f} seconds.")

    return None, attempt_counter

def test_mode(target, charset_option, custom_threads=None):
    if custom_threads:
        thread_counts = custom_threads
    else:
        thread_counts = [2, 4, 6, 8, 12]

    results = {}
    print("\n🚀 Running Test Mode (Performance Benchmark)...\n")

    for threads in thread_counts:
        print(f"\n[⚡] Testing with {threads} threads...")
        elapsed_time, attempts = brute_force(target, charset_option, threads, silent=True)
        if elapsed_time:
            results[threads] = elapsed_time
            print(f"✅ {threads} threads: {elapsed_time:.2f} sec ({attempts} attempts)")
        else:
            print(f"❌ {threads} threads: Test failed")

    print("\n📊 Performance Summary:")
    for threads, time_taken in results.items():
        print(f"🔹 {threads} threads → {time_taken:.2f} seconds")

if __name__ == "__main__":
    print("BRUTE-FORCE SIMULATION TOOL")
    print("===============================")
    
    target = input("Enter target word: ").strip()

    print("\nSelect character set:")
    print("[1] Letters [2] Digits [3] Letters + Digits [4] All Characters")
    charset_option = input("Choice: ").strip()

    print("\nSelect test mode:")
    print("[1] No Test (Run normally)")
    print("[2] Automatic Test (2, 4, 6, 8, 12 threads)")
    print("[3] Custom Test (Enter your own thread counts)")
    test_option = input("Choice: ").strip()

    if test_option == "2":
        test_mode(target, charset_option)
    elif test_option == "3":
        custom_threads_input = input("Enter thread counts separated by commas (e.g., 6,12,19): ").strip()
        try:
            custom_threads = [max(1, min(32, int(x.strip()))) for x in custom_threads_input.split(",") if x.strip().isdigit()]
            if custom_threads:
                test_mode(target, charset_option, custom_threads)
            else:
                print("❌ Invalid input. Running normal mode.")
        except ValueError:
            print("❌ Invalid input. Running normal mode.")
    else:
        try:
            max_workers = int(input("Threads (default 4): ") or 4)
            max_workers = max(1, min(32, max_workers))  
        except ValueError:
            max_workers = 4

        print("\nStarting attack...\n")
        brute_force(target, charset_option, max_workers)
