# 3D Cube

This project was created purely for fun, it isn't meant as an actual project.

The program generates a rotating cube which is simulated in pygame.
This simulates the 3D engine inside pygame using custom Matrices and Vectors.

## Visual example

![cube_rot](https://user-images.githubusercontent.com/20902250/102029229-ea089680-3dad-11eb-9be3-81d20f58f063.gif)

## How to use it

By changing the variables in `config.yaml` you can alter the way the cube simulation works. You can change the `cube_scale` to change the cube size, or alter the `projection_distance` assuming you're using perspective projection to alter the camera distance, or you can switch between orthographic and perspective projections by changing `orthographic` to `True` or `False`.

After these variables are defined to your liking, you can simply run the python file
Do note that you'll need to have pygame installed or use the provided virtual enviroment:

* Install pipenv by doing `pip install pipenv`
* Use `pipenv install` to install all packages for the virtual enviroment
* Run the python file with pipenv `pipenv run python -m src`

## Technical functionality of the 3D engine

### Projection

For conversion of 3D points (vectors) to 2D points (vectors) the 3D engine I made supports both orthographic projection (simply ignoring the Z value) and perspective projection, which adjusts for z and scales the other values based on it.

It works using the basic orthographic projection matrix:

![image](https://user-images.githubusercontent.com/20902250/90991591-a396ee00-e5aa-11ea-888a-696a17baad88.png)

which when multiplied with a coordinate vector will simply ignore the **z** coordinate:

![image](https://user-images.githubusercontent.com/20902250/90991622-e062e500-e5aa-11ea-9ae4-fba42c738390.png)

Perspective projection works quite similarly, but instead of static projection in the same scale, the scale changes based on the Z value. This means the 1's in the projection matirx P would change to a different value.

This projection scale value is determined using this formula:
`1/(distance - z)`, where the `distance` value is defined by user and it defines the camera distance from the object which determines how much will the given object scale based on the depth (z).

Sources for this:

* [Projection (linear algebra)](https://en.wikipedia.org/wiki/Projection_(linear_algebra))
* [Orthographic projection](https://en.wikipedia.org/wiki/Orthographic_projection)
* [Perspective projection](https://en.wikipedia.org/wiki/3D_projection#Perspective_projection)

### Rotation

For the rotation I used pre-defined [rotation matrices](https://en.wikipedia.org/wiki/Rotation_matrix#In_three_dimensions) for all 3 axis (x, y, z):

![image](https://user-images.githubusercontent.com/20902250/90991403-28810800-e5a9-11ea-9dad-639f86f49df5.png)

But purely using these matrices would only rotate the cube around the pygame screen origin point (0, 0), so in order to rotate it around its center as a reference point, I've used this formula:

**u’=Ru** I calculated **u’=R(u-OP)+OP**, where

* **u** is the vector to rotate
* **u’** is the rotated vector
* **R** is the rotation matrix
* **OP** is the vector from **O** (origin - pygame 0, 0) to **P** (cube middle point) (that is **P-O**)

After that in the main game loop, I've simply defined a rotation along all 3 axis by the same arbitrary angle

## Future

* Consider the use of [Quaternions](https://en.wikipedia.org/wiki/Quaternion) to define the angles instead of the simple [Euler angles](https://en.wikipedia.org/wiki/Euler_angles)
