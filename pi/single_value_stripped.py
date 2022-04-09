from time import sleep
import datetime as dt
from sys import stdout
from daqhats import mcc128, OptionFlags, HatIDs, HatError, AnalogInputMode, AnalogInputRange
from daqhats_utils import select_hat_device


def main():
    options = OptionFlags.DEFAULT
    low_chan = 0
    high_chan = 3
    input_mode = AnalogInputMode.DIFF
    input_range = AnalogInputRange.BIP_10V

    sample_interval = 1.0  # Seconds

    try:
        # Get an instance of the selected hat device object.
        address = select_hat_device(HatIDs.MCC_128)
        hat = mcc128(address)

        hat.a_in_mode_write(input_mode)
        hat.a_in_range_write(input_range)

        print('\nAcquiring data ... Press Ctrl-C to abort')

        # Display the header row for the data table.
        print('\n  Samples/Channel', end='')
        for chan in range(low_chan, high_chan + 1):
            print('     Channel', chan, end='')
        print('')

        try:
            samples_per_channel = 0
            while True:
                # Display the updated samples per channel count
                samples_per_channel += 1
                now = dt.datetime.now()

                # Read a single value from each selected channel.
                list_of_values = []
                for chan in range(low_chan, high_chan + 1):
                    value = hat.a_in_read(chan, options)
                    list_of_values.append(value)

                print(f"{samples_per_channel} : {now.isoformat()} : {list_of_values}")

                # Wait the specified interval between reads.
                sleep(sample_interval)

        except KeyboardInterrupt:
            print('Program interupted by user')

    except (HatError, ValueError) as error:
        print('\n', error)


if __name__ == '__main__':
    main()