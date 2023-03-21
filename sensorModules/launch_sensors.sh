#!/bin/bash
# python -u gpsModule.py  2>&1 >> gpsModule.log &
# python -u timingmodule.py $1 2>&1 >> timingmodule.log 

#!/bin/bash

# Define a function to handle errors
function handle_error {
    echo "An error occurred. Exiting..."
    exit 1
}
echo "launching sensor modules!"

# Set the trap to call the handle_error function
trap handle_error ERR

# Run the Python scripts in the background
python gpsModule.py &
python timingmodule.py $1 &
#python script3.py &

# Wait for any child process to exit and check its exit status
wait -n || handle_error

# Wait for the remaining child processes to finish
wait
