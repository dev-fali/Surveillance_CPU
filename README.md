# Welcome to your Surveillance_CPU 👋

## Get started
1. Install python 
2. Create a virtual environment (optional)
```bash
   python -m venv venv
   ```
3. Active the virtual environment
On windows:
```bash
   .\venv\Scripts\activate
   ```
On MacOs/Linux:
```bash
   source venv/bin/activate
   ```
4. Install required libraires
```bash
   pip install psutil slack_sdk python-dotenv matplotlib
   ```

5. Create the ".env" file
Create a ".env" file with the following content and place it in the same directory as your script:
```bash
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_password
SLACK_TOKEN=your_slack_token
```
7. Run the Script



