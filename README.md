# WELCOME!

I'm Georgina Dibua, a Mechanical Engineering PhD student at the Unversity of Texas at Austin working on modelling and simulating the sintering of nanoparticles for a microscale 3D printing process. This repo contains some sample scripts for projects that I've worked on related to my PhD. Thank you for checking this page out and I hope you enjoy your visit :smile:

## Background
The codebase I developed for modelling the sintering process is not open source (at least not yet) so I can't share that here, but I've included some videos showing the final results of the simulation process to serve as a bit of background and to provide context for the projects shown in this repository. 

The sintering simulation is broken up into two main processes. The first is a **bed generation** phase, where nanoparticles are allowed to interact in a simulation box till a steady state bed configuration is reached. This is performed in a Discrete Element Model (DEM) simulation I built in C++. The bed generation process is shown in the video below. The particles move around subject to elastic, dissipative, gravitational and cohesive forces, until the particles settle. 


https://user-images.githubusercontent.com/42850648/156982342-8edf14d0-c2f0-4613-ada5-d54dad98435a.mp4


The resulting bed created from the bed generation simulation is passed on to the second main process which is the actual **sintering simulation** phase. The sintering simulation is based off a Phase Field Model of solid-state diffusion between nanoparticles. This is a parallel simulation I developed in C++ and is run with the supercomputer at the Texas Advanced Computing Center. This simulation was created from discretized partial differential equations integrated numerically using Euler's method. An example of the results of the sintering simulation applied to a simulated bed is shown in the video below.


https://user-images.githubusercontent.com/42850648/156984299-0258de06-1cd7-4d35-9e07-23d7e6efda54.mp4


## Sample Scripts

### 1. convertImagetoTemp.py

The function of this script is to convert a 2D image file into a 3D temperature map that can be inserted into the sintering simulation shown above to selectively sinter specific areas of the simulation bed. This has applications in the actual process being simulated. The video above shows a sintering process where the entire bed is being sintered at the same rate, but in the actual process, due to selective heat deposition which drives the sintering of the particles, the rate of sintering in the actual bed is not homogenous. To simulate this process, binary files containing the desired temperature map for the simulation bed are passed in as inputs to control the rate of sintering of different areas of the bed. This script accepts any type of image file, converts the colors into a temperature map, extrudes this from 2D to 3D, then rotates the image so it is in the desired configuration for the sintering simulation bed. The results from running this script are shown in the Figure below.


![resultsConsolidated](https://user-images.githubusercontent.com/42850648/156986693-2b29500c-2f7c-4239-880c-c8826905e9e0.jpg)


When the resulting temperature map is applied to a simulation bed the result is a selectively sintered area as shown below.


![image](https://user-images.githubusercontent.com/42850648/156985802-b968772e-3f6a-4d7d-ba20-47bf7de07be3.png)


### 2. visualizeNeckConnections.py

The function of this script is to visualize the connections in an interconnected network of resistors present in an electronics circuit. This has applications in the post-process analysis that is done on the sintered simulation beds. It is necessary to be able to get numerical data from the simulations to be able to validate the simulation against experimental data. One such property measured is the electrical resistance predicted by the simulation. This is done by treating each particle in the system as a node connected to other particles through resistors with resistance values that are a function of the necks connecting particles. This results in a circuit file (nodefile.cir) which contains a list of the nodes in the bed, and the resistance between these nodes. Being able to visualize these connections is a very important debugging tool. Example results from this script are shown in Figures a and b below for two different input nodefiles. 


![ResistanceNetworkPlotOf_nodeFile1](https://user-images.githubusercontent.com/42850648/156988120-961db780-6332-4421-9139-faf2c9d4f081.jpg)
Figure a


![ResistanceNetworkPlotOf_nodeFile2](https://user-images.githubusercontent.com/42850648/156988205-7f77c9ff-3538-4d09-ad82-f7a90d6c8eb0.jpg)
Figure b


In these figures, the potential difference is applied to nodes 0 and 1. It was clear from looking at the figures that there was something wrong with the connections in Figure b, just based of being able to see what the connections between the nodes looked like. 
