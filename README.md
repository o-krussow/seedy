![Seedy](https://github.com/o-krussow/seedy/assets/123573986/69bbebd3-5183-4e34-982a-d42f3ecf5ce3)

## Instructions to get everything started
Check to make sure there isn't already an apiserver.py instance running. You can only have one server instance running per port. Use ss to check:
```
o936k099@hermes:~$ ss -plnt | grep 5000
LISTEN 0      128        127.0.0.1:5000       0.0.0.0:*    users:(("python",pid=2879773,fd=21))
o936k099@hermes:~$
```
We can see that a python process is already listening on port 5000. If this isn't running, you'll need to start it.
If you need to check to see who's already running it, you can check using something like this:
```
o936k099@hermes:~/workspace/seedy/HackKU_Website$ ps aux | grep 2879773
o936k099 2879773  0.8  0.6 57648156 9954008 pts/21 Sl+ 20:31   1:20 python apiserver.py
o936k099 2900997  0.0  0.0   9212  2468 pts/41   S+   23:00   0:00 grep --color=auto 2879773
o936k099@hermes:~/workspace/seedy/HackKU_Website$
```
We can see that it's already running under my user, o936k099.
```
(venv) o936k099@hermes:~/workspace/seedy$ python apiserver.py
number of parameters: 1555.97M
No meta.pkl found, assuming GPT-2 encodings...
 * Serving Flask app 'apiserver'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```
Even if you change the port, we really only have enough vram for one apiserver instance since it creates a nanoGPT object and stores the model in vram. The model we're using takes up ~25GiB of vram per instance. You can check the vram usage with:
```
o936k099@hermes:~$ nvidia-smi
Sat Apr 13 22:38:28 2024
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 525.147.05   Driver Version: 525.147.05   CUDA Version: 12.0     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|                               |                      |               MIG M. |
|===============================+======================+======================|
|   0  NVIDIA A100-PCI...  Off  | 00000000:25:00.0 Off |                    0 |
| N/A   25C    P0    35W / 250W |  25087MiB / 40960MiB |      0%      Default |
|                               |                      |             Disabled |
+-------------------------------+----------------------+----------------------+
|   1  NVIDIA A100-PCI...  Off  | 00000000:C8:00.0 Off |                    0 |
| N/A   25C    P0    35W / 250W |  25691MiB / 40960MiB |      0%      Default |
|                               |                      |             Disabled |
+-------------------------------+----------------------+----------------------+

+-----------------------------------------------------------------------------+
| Processes:                                                                  |
|  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
|        ID   ID                                                   Usage      |
|=============================================================================|
|    0   N/A  N/A      3703      G   /usr/lib/xorg/Xorg                  4MiB |
|    0   N/A  N/A    293531      C   ...nvs/conda_env1/bin/python     1286MiB |
|    0   N/A  N/A   1269792      C   ...nvs/conda_env1/bin/python     1284MiB |
|    0   N/A  N/A   1670469      C   ...nvs/conda_env1/bin/python     1290MiB |
|    0   N/A  N/A   1793675      C   ...nvs/conda_env1/bin/python     1288MiB |
|    0   N/A  N/A   2089346      C   ...nvs/prodAEtest/bin/python     1510MiB |
|    0   N/A  N/A   2290178      C   ...nvs/conda_env1/bin/python     1284MiB |
|    0   N/A  N/A   2292845      C   ...nvs/conda_env1/bin/python     1286MiB |
|    0   N/A  N/A   3128354      C   ...nvs/conda_env1/bin/python     1290MiB |
|    0   N/A  N/A   3245640      C   ...nvs/prodAEtest/bin/python     9148MiB |
|    0   N/A  N/A   3245731      C   ...nvs/prodAEtest/bin/python     1440MiB |
|    0   N/A  N/A   3634005      C   ...nvs/conda_env1/bin/python     1288MiB |
|    0   N/A  N/A   3973986      C   ...nvs/conda_env1/bin/python     1284MiB |
|    0   N/A  N/A   4129844      C   ...nvs/prodAEtest/bin/python     1400MiB |
|    1   N/A  N/A      3703      G   /usr/lib/xorg/Xorg                  4MiB |
|    1   N/A  N/A   2879773      C   python                          25684MiB |
+-----------------------------------------------------------------------------+
o936k099@hermes:~$
```
The apiserver listens for get requests on /api/ and returns a json result. It does not serve any HTML. The HTML is served by a different web server. You can use the built in python web server after cd-ing to the webroot, like this:
```
o936k099@hermes:~/workspace/seedy/HackKU_Website$ python3 -m http.server 8011
Serving HTTP on 0.0.0.0 port 8011 (http://0.0.0.0:8011/) ...
```
Where 8011 can be replaced by the port you want the web server running on. Obviously we don't need to use python's built in web server, we can use any web server pointed at the right place (mostly), but the python one is convenient.
To access the web server and apiserver from another computer, we need to use SSH forwarding because there are (multiple) firewalls between where we're connecting from (KU WiFi) to the GPU server. This example command tells SSH to listen on localhost ports 5000 and 8011 and forward traffic to/from these ports to ports 5000 (apiserver) and 8011 (example python webserver referenced above serving HTML) on the GPU server.

```ssh -L 8011:localhost:8011 -L 5000:localhost:5000 <username>@<serverip>```

Once you've run this command, you can access ```http://localhost:8011/``` in your browser. Since we also forwarded port 5000, the javascript running in your web browser will be able to communicate with our apiserver at ```http://localhost:5000/api/```.
