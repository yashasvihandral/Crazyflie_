

## OptiTrack Motion Capture System Setup (Motive)

This tutorial shows you how to:

* Understand what OptiTrack + Motive does
* Install Motive 2.2.0
* Enter the required license information
* Calibrate the camera system (wand + ground plane)
* Set up a rigid body
* Open the data streaming panel





## System Description

OptiTrack is a motion-capture system (hardware + software) that uses multiple infrared cameras and markers to compute the 3D position and orientation (pose) of objects in a capture volume. 

Motive is the software that handles:

* Camera calibration
* Marker detection
* Rigid-body definition (grouping markers on an object)
* Pose calculation (6DoF)
* Streaming/exporting pose data 

Hardware components include:

* Cameras
* PoE network switch
* Host computer with Motive installed
* Guest computer that receives streaming data
  All cameras and computers connect to the same network switch. 

Additional references from the PDF:

* Motive documentation: [https://wiki.optitrack.com/index.php?title=Motive_Documentation](https://wiki.optitrack.com/index.php?title=Motive_Documentation) 
* Calibration video: [https://www.youtube.com/watch?v=WCJ3dxgSljA](https://www.youtube.com/watch?v=WCJ3dxgSljA) 



## Step 1: Install Motive 2.2.0

The required software is Motive 2.2.0. 

1. Go to: [https://optitrack.com/support/downloads/archives.html](https://optitrack.com/support/downloads/archives.html) 
2. Scroll down until you reach Motive software.
3. Click “previous releases.” 
4. Click “Motive 2.2.0.”
5. Check the EULA box and follow the instructions to install. 
6. After installation, open Motive (the license pop-up should appear). 



## Step 2: Enter License Information

1. On the Motive pop-up, click “license tool.” 
2. Use the OptiTrack/Motive box to find the required license information and the hardware key USB. 
3. Press “active” settings to save the information. 
4. Close the License Tool window.
5. Click “retry” on the Motive pop-up. Motive should now launch. 



## Step 3: Calibration

Before calibrating, make sure the cameras and host computer are on the same network. The lab cameras are already connected via ethernet, and the host computer must be connected to that same ethernet network for the cameras to appear in Motive. The lab uses a Windows 11 computer for Motive. 

If a prior calibration (.CAL) file is available, you can use it. If no file is available, you must calibrate manually and create a new .CAL file. If the cameras are moved at all, a new calibration file must be created. 

In Motive:

1. Click the calibration pane (top right).
2. Click “New Calibration.” 

The lab floor is optimized to minimize reflections. If there are additional reflections, mask them manually. 

Required tools:

* Wanding tool
* Ground tool 



### Step 3.1: Wanding

1. Grab the wanding tool.
2. Click “Start Wanding.” 
3. Make sure no camera is highlighted so all cameras are included. 
4. Walk to the middle of the testing space.
5. Walk in an outward spiral while moving the wand in large waving motions, making figure 8’s, and twisting/bending the tool. 
6. Click “start calculating.” 
7. Keep samples under 10,000. Usually 2,000–5,000 samples are enough even if it shows poor quality. 


### Step 3.2: Set the Ground Plane

1. Grab the ground plane tool.
2. Place it in the middle of the testing space. 
3. The longer side should point toward the back wall (forward-facing axis). 
4. Use the levelers to fully level it with the lab floor. The bubble should be centered within the black lines. 
5. Click “Set Ground Plane.” 

After this, the system should be fully calibrated and the cameras in software should closely mirror the physical cameras in the lab. 


## Step 4: Setting Up a Rigid Body

To detect an object in Motive, reflective markers must be bound together to represent the object.

Requirements:

* Minimum of three markers
* Ideally markers should be asymmetrical 

In Motive:

1. Hold Ctrl and click each marker to highlight the markers for the rigid body. 
2. Right click, hover over “Rigid Body,” and select “Create from Selected Markers.” 
3. A new rigid body should appear. Note the rigid body name (you can customize it) and identification number. 


## Step 5: Streaming

To start streaming pose data:

1. Click “View”
2. Click “Data Streaming Pane” 

A panel will pop up with the information and options needed to configure streaming settings. 

Attribution
This tutorial compiles and explains work by Eric Jay Tantay (original OptiTrack/Motive notes):

https://docs.google.com/document/d/1XCL3sLL8nle3HdcYC1r_3V9E3n3dATSWb5EA4HiOwIM/edit?pli=1&tab=t.0

Additional resources

OptiTrack (official docs)
Motive Documentation. (OptiTrack)
https://docs.optitrack.com/motive

OptiTrack System Documentation (setup, calibration, networking). (OptiTrack)
https://docs.optitrack.com/

OptiTrack calibration walkthrough video. (OptiTrack)
https://www.youtube.com/watch?v=WCJ3dxgSljA

