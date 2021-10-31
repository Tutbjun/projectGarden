from ursina import *
from ursina import mesh_importer


def update():
    print("lmao")


objs = {}
m1 = mesh_importer.load_model(name='2optimize.obj')
objs["startGeometry"] = Entity(model=m1,color=color.rgba(0,0,200))
m2 = mesh_importer.load_model(name='its_free_realestate.obj')
objs["freeRealEstate"] = Entity(model=m2,color=color.rgba(0,255,0,30))
m3 = mesh_importer.load_model(name='its_hella_expencive_realestate.obj')
objs["expensiveRealEstate"] = Entity(model=m3,color=color.rgba(255,0,0,30))
fov = 40
camera.orthographic =  True
EditorCamera()



app = Ursina()

#PointLight(parent=Entity(),x=1000,y=1000,z=-500,shadows=True)

app.run()











