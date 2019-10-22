ssh matt@10.0.0.7 "rm -rfv VenturyBoi"
ssh matt@10.0.0.7 "git clone https://github.com/kketg/VenturyBoi"
ssh matt@10.0.0.7 "cd VenturyBoi && python3 -m pip install -r requirements.txt && python3 app.py"
