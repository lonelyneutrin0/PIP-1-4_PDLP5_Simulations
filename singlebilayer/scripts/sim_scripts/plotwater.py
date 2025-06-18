import matplotlib.pyplot as plt
import numpy as np
import time

from numpy.typing import NDArray
from typing import Tuple

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "sans-serif",
    "font.sans-serif": ['Arial', 'Helvetica', 'DejaVu Sans']
})


def digitize_water(data: NDArray) -> NDArray:
    """
    Digitize input Z-coordinate data into bins.

    Params:

    data : NDArray
        NumPy array containing Z coordinates of water molecules.

    Returns:

        NDArray containing the binned positions of water molecules.
    """

    bins = np.array([-25, -2, 12, 25])
    return np.digitize(data, bins)


def filter_no_repeats(arr: NDArray) -> Tuple[NDArray, NDArray]:
    """
    Filter out consecutive duplicates from array, considering only even values.

    Params:

    arr : NDArray
        Input array.

    Returns

    Tuple of filtered array and corresponding indices.
    """

    event_indices = np.nonzero(arr % 2 == 0)[0]
    filtered_arr = arr[arr % 2 == 0] // 2
    diff = np.diff(filtered_arr)

    unique_vals = filtered_arr[np.insert(diff.astype(bool), 0, True)]
    unique_indices = np.hstack([0, event_indices[1 + np.nonzero(diff)[0]]])
    return unique_vals, unique_indices


def no_repeats(arr: NDArray) -> Tuple[NDArray, NDArray]:
    """
    Remove consecutive duplicates from the array.

    Params:

    arr : NDArray
        Input array.

    Returns:

    Tuple of filtered array and corresponding indices.
    """
    diff = np.diff(arr)
    unique_vals = arr[np.insert(diff.astype(bool), 0, True)]
    unique_indices = np.hstack([0, 1 + np.nonzero(diff)[0]])
    return unique_vals, unique_indices


def plot_crossing(data: NDArray, start: int, stop: int):
    """
    Plot a single crossing event and save it to a PNG file.

    Params:

    data : NDArray
        Time series data of a single water molecule.
    start : int
        Start index of the crossing event.
    stop : int
        End index of the crossing event.
    """
    if not hasattr(plot_crossing, "counter"):
        plot_crossing.counter = 0

    if plot_crossing.counter < 100:
        fig, ax = plt.subplots()
        ax.plot(data)
        ax.axvspan(start, stop, color='gray', alpha=0.3)
        fig.savefig(f"plot_{plot_crossing.counter}.png")
        plt.close(fig)
        plot_crossing.counter += 1


def count_crossings2(digitized: NDArray, data: NDArray) -> Tuple[NDArray, NDArray]:
    """
    Count crossing events where a water molecule moves into bin '1' surrounded by bins '0' and '2'.

    Params:

    digitized : NDArray
        Digitized bin data for all molecules over time.
    data : NDArray
        Original water coordinate data (used for plotting).

    Returns:

    Tuple of crossing start times and crossing durations.
    """
    crossing_times = []
    crossing_durations = []

    # Find all unique molecules that are in bin 2 at some time
    molecules_with_bin2 = set(np.nonzero(digitized == 2)[1])

    for molecule_idx in molecules_with_bin2:
        filtered_bins, times = filter_no_repeats(digitized[:, molecule_idx])
        one_indices = np.nonzero(filtered_bins == 1)[0]

        for idx in one_indices:
            # Check if the bin 1 is bookended by different bins
            if 0 < idx < len(filtered_bins) - 1:
                if filtered_bins[idx - 1] != filtered_bins[idx + 1]:
                    crossing_times.append(times[idx + 1])
                    crossing_durations.append(times[idx + 1] - times[idx - 1])

    return np.array(crossing_times), np.array(crossing_durations)


def count_crossings(digitized: NDArray, data: NDArray) -> Tuple[NDArray, NDArray]:
    """
    Alternate method to count crossing events

    Params:

    digitized : NDArray
        Digitized bin data for all molecules over time.
    data : NDArray
        Original water coordinate data (used for plotting).

    Returns:

    Tuple of crossing start times and crossing durations.
    """
    crossings_set = set()
    crossing_times = []
    crossing_durations = []
    molecules_with_bin2 = set(np.nonzero(digitized == 2)[1])

    for molecule_idx in molecules_with_bin2:
        filtered_bins, times = no_repeats(digitized[:, molecule_idx])
        two_indices = np.nonzero(filtered_bins == 2)[0]

        for idx in two_indices:
            left_offset = 1
            while idx - left_offset > 0 and filtered_bins[idx - left_offset] not in (0, 4):
                left_offset += 1

            right_offset = 1
            while idx + right_offset < len(filtered_bins) - 1 and filtered_bins[idx + right_offset] not in (0, 4):
                right_offset += 1

            left_idx = idx - left_offset
            right_idx = idx + right_offset

            if (left_idx >= 0 and right_idx <= len(filtered_bins) - 1 and
                filtered_bins[left_idx] != filtered_bins[right_idx] and
                filtered_bins[right_idx] in (0, 4) and filtered_bins[left_idx] in (0, 4) and
                (molecule_idx, right_idx) not in crossings_set):
                
                crossings_set.add((molecule_idx, right_idx))
                crossing_times.append(times[right_idx])
                crossing_durations.append(times[right_idx] - times[left_idx])
                plot_crossing(data[:, molecule_idx], times[left_idx], times[right_idx])

    return np.array(crossing_times), np.array(crossing_durations)


def main():
    BUILD_PATH = "/serviceberry/tank/hkbel/PIP-1-4_PDLP5_Simulations/singlebilayer/builds"
    SIM_PATH = "/serviceberry/tank/hkbel/PIP-1-4_PDLP5_Simulations/singlebilayer/sims"
    DATA_PATH = "/serviceberry/tank/hkbel/PIP-1-4_PDLP5_Simulations/singlebilayer/data"

    NUM_REPLICATES = 3

    for i in ['porinalone', 'porinwithcap']:
        for j in ['grad', 'nograd']:
            for k in ['0.010', '0.150', '1.0']:

                rates = np.zeros(shape=(NUM_REPLICATES,))
                sim_times = np.zeros_like(rates)
                processing_times = np.zeros_like(rates)

                for l in range(NUM_REPLICATES):
                    data = np.load(f'{DATA_PATH}/{i}/{j}/{k}/{l}/watz.npy')
                    sim_time_ns = 0.1 * len(data)  # each frame is 100ps, convert to ns

                    digitized_data = digitize_water(data)

                    start_time = time.time()
                    times, durations = count_crossings2(digitized_data, data)
                    rate = len(times) / sim_time_ns * 1000 # crossings/μs
                    print(f'Processing {i}/{j}/{k}/{l} ....')
                    print(f"Crossings={len(times)}, Simulation Time={sim_time_ns:.2f} ns, rate={rate:.4f} crossings/μs")
                    
                    process_time = time.time() - start_time
                    print(f"Processing time: {process_time:.2f} s\n")

                    np.savez(f"{DATA_PATH}/{i}/{j}/{k}/{l}/reduced.npz", time=times, duration=durations)
                    
                    rates[l] = rate
                    sim_times[l] = sim_time_ns
                    processing_times[l] = process_time

                print(f'\n Results for {i}/{j}/{k}/{l} (averaged over {NUM_REPLICATES} replicates...\n')
                print(f'Crossing Rate:\n')
                print(f'Average: {np.average(rates):.4f} crossings/μs')
                print(f'Standard Error: {np.std(rates)/np.sqrt(NUM_REPLICATES):.4f} crossings/μs\n')
                print(f'Average Simulation Time: {np.average(sim_times):.2f} ns')
                print(f'Average Processing Time: {np.average(processing_times):.2f}s\n')


if __name__ == "__main__":
    main()
