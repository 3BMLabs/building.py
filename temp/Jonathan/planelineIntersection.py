# Define a line by its direction vector and a point on it
line_dir = [1, 2, 3] # direction vector of the line
line_pt = [0, 0, 0] # a point on the line

# Define a plane by its normal vector and a point on it
plane_norm = [4, 5, 6] # normal vector of the plane
plane_pt = [1, 1, 1] # a point on the plane

# Compute the dot product of the line direction and the plane normal
dot_prod = sum([a*b for a,b in zip(line_dir, plane_norm)])

# Check if the dot product is zero, which means the line is parallel to the plane
if dot_prod == 0:
    print("The line is parallel to the plane. No intersection point.")
else:
    # Compute the parameter t that gives the intersection point
    t = sum([(a-b)*c for a,b,c in zip(plane_pt, line_pt, plane_norm)]) / dot_prod

    # Compute the intersection point by plugging t into the line equation
    inter_pt = [a + b*t for a,b in zip(line_pt, line_dir)]

    # Print the intersection point
    print("The intersection point is", inter_pt)