# Project's Python virtual environnement
The projet contains a python virtual environnement, which allows developpers to share a same set of python libraries, and their respective versions. Here is a [great document](https://realpython.com/python-virtual-environments-a-primer/) on virtual environnements. 

## Usage of the virtual environnement:
The following commands consider you are in the [installDependecies](/installDependencies) folder.
You can add an remove package from a virtual environnement the same way you would do on your computer (with the use of `pip`).
- To enter the virtual environnement: `source ./enterVenv.sh`
- To save the virtual environnement: `pip freeze > ./requirements.txt`
- To exit the virtual environnement: `deactivate`
