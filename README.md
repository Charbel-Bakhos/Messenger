# README

To get started, download the enitre zip folders contents to your computer. Locate the folder in terminal.

### Running the server
First get your IP address:
* For WSL users, use the command ***hostname -I***
* For MAC users, use the command ***curl ifconfig.me***
  
Run the server as you would run any python file on your terminal, and add your IP address to the end of it. In WSL it will look like
```
python3 server.py 127.0.0.1
```
The server will run, nothing will appear until users connect.

to quit the application type "quit chat" in all lower case

### Running the client
On any computer (multiple computers can connect to the same server), as long as the entire folder is downloaded, run the following command.
```
python3 client.py (servers IP)

#In our example this will look like

python3 client.py 127.0.0.1
```

It will prompt you to enter a username. Once you do, you can begin chatting to everyone connected!

If you want to quit the application, type "quit" in all lowercase.