This Project Using FastApi from https://github.com/tiangolo/fastapi

First you need to create virtualenv for this project
```
virtualenv -p [location_of_python] [name_of_virtualenv]
```

if you didn't have virtualenv you can install it by
```
pip install virtualenv
```

Running your virtualenv first
```
source [name_of_virtualenv]/bin/activate
```
Once you running your VirtualEnv, install dependecy
```
pip install -r requirements.txt
```

Then You Can Start App

```
uvicorn app.main:app --reload
```

For the documentation You can see in
```
[host]:[port]/docs
```
