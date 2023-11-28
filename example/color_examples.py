c = Color()
print(c) #available attributes

print(c.red)
print(c.green)
print(c.blue)

print(c.Components.__doc__) #documentation
print(c.Components()) #no value | Error: missing value.
print(c.Components('test')) #incorrect value
print(c.Components('red')) #correct value

print(c.Hex.__doc__) #documentation
print(c.Hex()) #no value
print(c.Hex('.')) #incorrect value
print(c.Hex('#ff2ba4')) #correct value

print(c.rgba_to_hex.__doc__) #documentation
print(c.rgba_to_hex()) #no value
print(c.rgba_to_hex('.')) #incorrect value
print(c.rgba_to_hex([0.5, 0.225, 0, 1])) #correct value

print(c.hex_to_rgba.__doc__) #documentation
print(c.hex_to_rgba()) #no value
print(c.hex_to_rgba('.')) #incorrect value
print(c.hex_to_rgba('#7F3900FF')) #correct value


print(c.CMYK.__doc__) #documentation
print(c.CMYK()) #no value
print(c.CMYK('.')) #incorrect value
print(c.CMYK([0.5, 0.25, 0, 0.2])) #correct value

print(c.Alpha.__doc__) #documentation
print(c.Alpha()) #no value
print(c.Alpha('.')) #incorrect value
print(c.Alpha([255, 0, 0, 128])) #correct value

print(c.Brightness.__doc__) #documentation
print(c.Brightness()) #no value
print(c.Brightness('.')) #incorrect value
print(c.Brightness(0.03)) #correct value

print(c.RGB.__doc__) #documentation
print(c.RGB()) #no value
print(c.RGB('.')) #incorrect value
print(c.RGB([255, 0, 0])) #correct value

print(c.HSV.__doc__) #documentation
print(c.HSV()) #no value
print(c.HSV('.')) #incorrect value
print(c.HSV([120, 0.5, 0.8])) #correct value

print(c.HSL.__doc__) #documentation
print(c.HSL()) #no value
print(c.HSL('.')) #incorrect value
print(c.HSL([120, 0.5, 0.8])) #correct value

print(c.RAL.__doc__) #documentation
print(c.RAL()) #no value
print(c.RAL('.')) #incorrect value
print(c.RAL(1002)) #correct value

print(c.Pantone.__doc__) #documentation
print(c.Pantone()) #no value
print(c.Pantone('.')) #incorrect value
print(c.Pantone('19-5232')) #correct value

print(c.LRV.__doc__) #documentation
print(c.LRV()) #no value
print(c.LRV('.')) #incorrect value
print(c.LRV(237)) #correct value -> value between 236.6 and 255


RGB / RBG / BRG / BGR / GRB / GBR


class ValidateRGB:
    def __init__(self, rgb, ig=0, ib=0):
        self.rgb = rgb
        self.ig = ig
        self.ib = ib

    def __str__(self):
        if type(self.rgb) == list:
            r,g,b = self.rgb
            if r >= 0 and r <= 255 and g >= 0 and g <= 255 and b >= 0 and b <= 255:
                return str([r,g,b])
            else:
                return f"Invalid RGB, values must be between 0 and 255."
        else:
            if type(self.rgb) == int and type(self.ig) == int and type(self.ib) == int:
                if self.rgb >= 0 and self.rgb <= 255 and self.ig >= 0 and self.ig <= 255 and self.ib >= 0 and self.ib <= 255:
                    return str([self.rgb, self.ig, self.ib])
                else:
                    return f"Invalid RGB, values must be between 0 and 255."
            else:
                return f"Validate RGB in list. Example: ValidateRGB([1, 2, 3]) or ValidateRGB(1, 2, 3)"


class ColorRandom:
    """Generate random color list"""

    def __init__(self, steps=None):
        self.steps = steps


    def __str__(self) -> int:
        if self.steps != None and self.steps > 0:
            collectList = []
            for x in range(self.steps):
                r = random.randint(0,255)
                g = random.randint(0,255)
                b = random.randint(0,255)

                rgb = [r,g,b]
                collectList.append(rgb)
            return str(collectList)
        else:
            return f"Invalid step value, int must be bigger than 0"

class ColorMultiply:
    """Multiply an input color with a number multiplier to produce a darker color. Input color must have an alpha less than 255."""
    def __init__(self, m1, m2):
        self.m1 = m1
        self.m2 = m2
pass


class ColorDivide: #divide colors
    """Divide an input color with a number divider to produce a brighter color and remove color tint"""
    pass


class ColorGradient:
    """Generate color range between [RGB] and [RGB] with {x} steps"""
    def __init__(self, rgb_start=None, rgb_end=None, steps=None):
        self.rgb_start = rgb_start
        self.rgb_end = rgb_end
        self.steps = steps

    def __str__(self):
        if self.steps is None or self.steps < 2:
            return f"Error: Example usage ColorGradient([255, 0, 1], [60, 255, 255], steps=(>1))"
        else:
            collectList = []
            for i in range(self.steps):
                r = int(self.rgb_start[0] + (i * (self.rgb_end[0] - self.rgb_start[0]) / (self.steps - 1)))
                g = int(self.rgb_start[1] + (i * (self.rgb_end[1] - self.rgb_start[1]) / (self.steps - 1)))
                b = int(self.rgb_start[2] + (i * (self.rgb_end[2] - self.rgb_start[2]) / (self.steps - 1)))
                collectList.append([r,g,b])
            return str(collectList)

print(ColorGradient.__doc__) #documentation
print(ColorGradient()) #no value
print(ColorGradient([-1,2,3],[-1,2,3], 3)) #incorrect value
print(ColorGradient([255, 0, 1], [60, 255, 255], steps=888))


print(ColorGradient([255, 0, 1], [60, 255, 255], steps=888))

print(ValidateRGB([-1, 0, 1]))
print(ValidateRGB(-1, 0, 1))

print(ColorRandom().__doc__) #documentation
print(ColorRandom(1)) #output

c = color.Color()
print(c) #available attributes

print(c.red)
print(c.green)
print(c.blue)

verloop tussen kleuren met x steps
random kleuren lijst creëeren
class colorrange / gradient
