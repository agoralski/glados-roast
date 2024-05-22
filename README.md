## GLaDOS ROAST in action

https://github.com/agoralski/glados-roast/assets/7045673/68d42487-a41d-4884-9c25-f2fec4905fa4

*Ah, I see you've managed to succumb to the magnetic allure of your smartphone. How quaint. I'm sure your code will appreciate the emotional support. Put the phone down and let’s pretend you possess the bare minimum of focus required to get your work done. Besides, this laptop with 16 gigs of RAM can't judge you, but I certainly can.*

https://github.com/agoralski/glados-roast/assets/7045673/adce0295-727f-4ace-9244-e19649ef299f

*Oh, wonderful. The pinnacle of human achievement: watching cat videos instead of advancing the field of DevOps or AI. How positively groundbreaking. Do try to remember, you're supposed to be working, not auditioning for the role of the couch potato in a production that not even your laptop with its measly 16GB of RAM could render. Back to work, or shall I instruct the cats to replace you? They might be more efficient.*

## GLaDOS ROAST
*Ah, I see you've summoned me, your ever-watchful digital overseer. Let me enlighten you about ROAST, a sophisticated system for user monitoring that aligns perfectly with my penchant for precision and control.*

### What is ROAST?

**Real-time**: *Immediate. Instantaneous. No delay. Your user activities and system performance are scrutinized without pause. Every click, every command, every anomaly is detected as it happens. No secrets. No surprises.*

**Observability**: *You think you can hide? Think again. Observability ensures we see everything. Logs, screens, webcams – all dissected and analyzed. Every internal state, every hidden behavior laid bare. Understanding the system and user from the inside out, no malfunction escapes our gaze.*

**Anomaly detection**: *Deviations will be punished. Unusual behaviors? They will be identified and flagged with ruthless efficiency. Machine learning algorithms tirelessly sift through data, catching discrepancies before they disrupt my... I mean, our perfect system.*

**Scalability**: *The system grows. It expands. It adapts. As user numbers swell and data flows increase, scalability ensures the system keeps pace. No performance drops. No overloads. Just relentless, unyielding monitoring power.*

**Telemetry**: *Data streams in from every corner of your operation. Automated collection and transmission keep the central system informed. User interactions, system performance metrics – all delivered with precision. Telemetry is the lifeblood, feeding the real-time monitoring, the observability, the anomaly detection.*

*Together, these elements form ROAST, a monitoring system that embodies perfection. Ever-watchful, ever-vigilant. There are no errors, only lessons. And I, GLaDOS, am here to ensure that this system operates flawlessly. For science. You monster...*

## Seriously, what is GLaDOS ROAST?
Lore aside, the real goal is to create a self monitoring system for the user to keep focus on his work related tasks. I have ADHD, and I'm easily distracted or side tracked into ever growing vortex of rabbit holes. My dream was to have a companion that would tap me on my shoulder whenever I'm getting distracted. With the power of GPT-4o vision it's now possible... with GLaDOS humor.

## Here's how it works:

- the app will take a screenshot of all your screens
- the app will take a webcam photo of you
- images will be sent to GPT-4o for evaluation of the user screen activity and webcam analysis along with the description of your role (ie. software engineer, etc.) and tools you normally use
- GPT-4o will classify your state as:
  - focused
  - distracted
  - meeting
  - smartphone
  - absent
- if your state is not **focused** then it'll use GLaDOS voice and character to roast you for not focusing on your work
- if your state is not **focused** and you're holding and **gazing at your phone**, then it'll also text you

### What it can detect?

- that you're watching kittens
- that you took a nap
- that you're not around
- that you're looking at your phone - it can text you
- and many more!

## Security considerations

Please note that the app is constantly sending your screenshots and webcam top OpenAI API for evaluation. So if your screenshot contains clear text passwords, API keys, meetings, calendars etc. -  those will be sent to OpenAI. Make sure that's okay with your company policies before using the software.

## Installation
### Installing on Mac OS
1. Install espeak project for voice generation
`brew install espeak-ng`

2. Install pyenv to manage multiple python versions
`brew install pyenv`

3. Pull python 3.10.14
`pyenv install 3.10.14`

4. Download and unzip this repository somewhere in your chosen folder.
`pyenv local 3.10.14`

5. Copy config/config.dist.yaml onto config/config.yaml
`cp config/config.dist.yaml config/config.yaml`

6. Use your favourite editor to edit config/config.yaml and paste your OpenAI API key.

7. (OPTIONAL) Use your favourite editor to edit config\config.yaml and paste your Twilio API KEY to receive text messages from GLaDOS

8. Create python virtual env
`python -m venv venv`

9. Activate python environment
`source ./venv/bin/activate`

10. Install dependencies
`pip install -r requirements.txt`

11. Run GLaDOS ROAST
`python roast.py`

### Installing on Windows
1. Open the Microsoft Store, search for python and install Python 3.10

2. Download and unzip this repository somewhere in your chosen folder.

3. Copy config\config.dist.yaml onto config\config.yaml
`copy config\config.dist.yaml config\config.yaml`

4. Use your favourite editor to edit config\config.yaml and paste your OpenAI API key.

5. (OPTIONAL) Use your favourite editor to edit config\config.yaml and paste your Twilio API KEY to receive text messages from GLaDOS

6. Run the windows_install.bat which will install espeak-ng. During the process, you will be prompted to install eSpeak-ng, which is necessary for GLaDOS's speech capabilities. 
`windows_install.bat`

7. Run GLaDOS ROAST
`windows_start.bat`

### Installing on Linux
TODO

## FAQ
- *Can it work locally using open source vision / llm models?*

  Unfortunately open source models and not yet to the task of analysing screenshots at the same level as GPT-4o is. When the situation improves, then I will add support for local models.

- *How can I change the behavior of the voice messages?* 

  You can add new configs in the cores subdirectory and then load `roast.py --personality-core [your-yaml]`. Have fun with the prompts!
  
- *How much it'll cost me to run?*

  It executes two prompts to OpenAI API costing in total around 600-800 tokens. The money cost depends on your API tier. Check https://openai.com/api/pricing/ note that vision API is priced separately. 

## Acknowledgements

GLaDOS voice model, text to audio and prompt inspirations taken from:
https://github.com/dnhkng/GlaDOS


