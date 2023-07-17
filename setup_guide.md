To run the handler, you need to execute the `app.py` file. You can use the following command:

```
python app.py
```

It is recommended to use a virtual environment to manage the project dependencies. Here are the instructions for setting up the virtual environment and running the project:

1. Set up a virtual environment:
   - Create a new virtual environment by running the command: `python -m venv env`
   - Activate the virtual environment:
     - For Windows: `.\env\Scripts\activate`
     - For macOS/Linux: `source env/bin/activate`

2. Install project dependencies:
   - Navigate to the project directory: `cd telegramisk`
   - Install the required packages: `pip install -r requirements.txt`

3. Run the project:
   - Execute the `app.py` file: `python app.py`

Note: Make sure you have the necessary credentials and configuration set up before running the project.

For Linux, if you want to set up a service for automatic startup, you can follow these instructions:

1. Create a service file:
   - Create a new service file using a text editor: `sudo nano /etc/systemd/system/telegramisk.service`
   - Add the following content to the file:

     ```
     [Unit]
     Description=Telegramisk Service
     After=network.target

     [Service]
     User=your_username
     ExecStart=/path/to/python /path/to/app.py
     WorkingDirectory=/path/to/telegramisk
     Restart=always

     [Install]
     WantedBy=multi-user.target
     ```

   - Replace `your_username` with your username and update the paths accordingly.

2. Save the file and exit the text editor.

3. Enable and start the service:
   - Enable the service: `sudo systemctl enable telegramisk`
   - Start the service: `sudo systemctl start telegramisk`

   The service will now automatically start on system boot.

To set up an NGINX proxy for your application, you can follow these instructions:

1. Install NGINX:
   - For Ubuntu/Debian: `sudo apt-get install nginx`
   - For CentOS/RHEL: `sudo yum install nginx`

2. Configure NGINX:
   - Create a new server block configuration: `sudo nano /etc/nginx/sites-available/telegramisk`
   - Add the following content to the file:

     ```
     server {
         listen 80;
         server_name your_domain.com;

         location / {
             proxy_pass http://localhost:5000;
             proxy_set_header Host $host;
             proxy_set_header X-Real-IP $remote_addr;
         }
     }
     ```

   - Replace `your_domain.com` with your actual domain or IP address.

3. Enable the server block:
   - Create a symbolic link to the sites-enabled directory: `sudo ln -s /etc/nginx/sites-available/telegramisk /etc/nginx/sites-enabled/`
   - Remove the default server block: `sudo rm /etc/nginx/sites-enabled/default`

4. Restart NGINX:
   - Restart NGINX to apply the changes: `sudo service nginx restart`

   Now, NGINX will act as a reverse proxy for your Telegramisk application.

Please make sure to adjust the paths, usernames, domain names, and port numbers based on your specific setup.