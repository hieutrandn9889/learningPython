from solarsystem import moon

moon_sur = moon.get_surface('white')
moon_shape = moon.get_shape('spherical')
moon = make.moon(moon_sur, moon_shape)
print(moon)
