# testing
* `pytest tests -v`
* `PYTHONDONTWRITEBYTECODE=1 pytest tests -v`
* `PYTHONDONTWRITEBYTECODE=1 pytest tests/test_log.py -v -p no:cacheprovider`
* for test_log use `PYTHONPATH=$(pwd) python tests/test_log.py`
* `PYTHONDONTWRITEBYTECODE=1 python inbund/test.py`
# ideas
* if package is not available search for the package name and ask which one is the required one
* packages starts with - is packages to remove
* executed commands should be opened in a new terminal 
* tmux -L "default" send-keys " tmux split-window -v -l 90 bash -c 'dnf search theme ; sleep 5'" C-m

gnome-terminal -- bash -c "sleep 5"
xterm -e "sleep 5 && exit; bash"
konsole -e "sleep 5"
terminals: konsole, gnome-terminal, tilix, kitty, xfce4-terminal, Alacritty, xterm, Terminator
https://chatgpt.com/c/6738ac59-17f8-800c-9f40-6687b8c7af3a

inbund -u --unpack fedora