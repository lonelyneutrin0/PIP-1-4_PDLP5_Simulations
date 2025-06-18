vmd-python() {
    if [ -z "$1" ]; then
        echo "Usage: vmdpy <script.py> [args...]"
        return 1
    fi
    vmd -dispdev text -python -e "$1" "${@:2}"
}

vmd-python trackwater.py 
venvit 
python plotwater.py > analysis_run.log
deactivate
