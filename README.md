# evGen
A game engine/ simulation written using python's pygame.

## evGen fundementals:

a particle property: an enumeration which queries the value during the calculation of forces. 
a real world parallel would be defining that "mass" exists.

a particle preset: particles which assigned particle properties. 
I.e an interstellar planet has the "mass" property

a particle: an instance of a particle preset where the particle properties are given values. 
This particular planet has a mass of 3, while another has a mass of 5.

a force: a formula which defines how two particles should interact.
f = (G*m1*m2)/d^2 where G is a constant, m1 and m2 are the masses of the objects, and d is the distance between them
note: constants can be user defined, and distance is provided as a helper function

## the core loop 

forces are calculated and applied to each particle based on its specific particle properties

forces manipulate particles' acceleration, which then updates their velocities and positions.


## using the current version

the python file should be all you need to get started. 
You will see an instance of pygame come up and you will be able to control the simulation you see with the on screen commands.

## looking forward

while things like collisions and overlaps are already handled, there is a requirement for user defined behaviour.

Therefore, another fundemental component must be introduced, a rule.

Rules will be user defined code that will run. This will allow for things like keeping score, deleting particles, and keeping track of player state.

In addition to rules, another core component that will be introduced is the emitter.

While the current version allows the user to spawn particles with a click of a button, having a well defined class called the emitter will allow for more interesting mechanics to emerge.

With these two additions, as well as some work on the GUI, evGen will help users generate complex games where the agents on the screen are primarily driven by forces, but can also interact in complex ways with user defined rules.
