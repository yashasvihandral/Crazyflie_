
Getting Started with Crazyflie: Takeoff and Landing via Python

This tutorial shows you how to:


- **Set up your system from scratch**  
- **Install the necessary software**  
- **Connect your Crazyflie drone**  
- **Run a script that makes the drone take off, hover, and land smoothly**



**What You Need**

- Crazyflie 2.1 nano quadcopter  
- Crazyradio PA USB dongle  
- Charged battery in the drone  
- A laptop running macOS or Linux  
- A safe open area to fly



**Step 1: Install Python 3**

Open your terminal and install Python 3:

**macOS:**
```bash
brew install python
````

**Ubuntu:**

```bash
sudo apt update
sudo apt install python3 python3-pip
```

**Verify that Python is installed:**

```bash
python3 --version
pip3 --version
```


**Step 2: Create a Virtual Environment**

This will help keep your project clean and organized.

**Create and activate a virtual environment:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Install the Crazyflie Python Library:**
This gives you access to the `cflib` API to talk to the drone.

```bash
pip install cflib
```



**Step 3: Set Up the Flight Script**

**Create a folder and write a script:**

```bash
mkdir -p ~/crazyflie-flight
cd ~/crazyflie-flight
```

Open the **cf_up_min.py** file in this repository.
Click **Raw**, then save the page as `cf_up_min.py`.
Move the file into a folder like `~/crazyflie-flight`.



**Step 4: Power On and Connect the Drone**

* **Plug the Crazyradio PA** into your computer.
* **Connect the battery** to the Crazyflie. It should power on automatically.
* **Wait for the LEDs to blink**, then place the drone on a flat surface.



**Step 5: Run the Script**

Make sure that your virtual environment is active and run the script:

```bash
cd ~/crazyflie-flight
source ../venv/bin/activate
python3 cf_up_min.py
```

The drone will:

* **Ramp up motors**
* **Take off and climb briefly**
* **Hover**
* **Land using a cosine easing curve**
* **Shut off motors fully**



