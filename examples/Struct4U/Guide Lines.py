prefix = '<Frame>' \
         '<ProjectName/>' \
         '<ProjectNumber/>' \
         '<ConsequenceClass>CC2</ConsequenceClass>' \
         '<DesignWorkingLife>50</DesignWorkingLife>' \
         '<ExportDateTime>2024-05-24 11:57:30Z</ExportDateTime>' \
         '<XMLExportVersion>v4.0.30319</XMLExportVersion>' \
         '<Nodes/>' \
         '<Supports/>' \
         '<Grids>' \
         '<X>0 1000</X>' \
         '<X_Lable>' \
         'A B C D E F G H I J K L M N O P Q R S T U V W X Y Z' \
         '</X_Lable>' \
         '<Y>0 1000</Y>' \
         '<Y_Lable>' \
         '1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25' \
         '</Y_Lable>' \
         '<Z>0</Z>' \
         '<Z_Lable>+0</Z_Lable>' \
         '</Grids>' \
         '<Profiles/>' \
         '<Lines>' \

X1 = [0,0,0]
Y1 = [1,1,1]
Z1 = [2,2,2]
X2 = [3,3,3]
Y2 = [4,4,4]
Z2 = [5,5,5]

lst = []
for x1, y1, z1, x2, y2, z2 in zip(X1, Y1, Z1, X2, Y2, Z2):
    lst.append("<FromX>" + str(x1) + "</FromX>")
    lst.append("<FromY>" + str(y1) + "</FromY>")
    lst.append("<FromZ>" + str(z1) + "</FromZ>")
    lst.append("<ToX>" + str(x2) + "</ToX>")
    lst.append("<ToY>" + str(y2) + "</ToY>")
    lst.append("<ToZ>" + str(z2) + "</ToZ>")

suffix = '</Lines>' \
         '<LoadCases>' \
         '<Number>1</Number>' \
         '<Description>Dead load</Description>' \
         '<Type>0</Type>' \
         '<psi0>1</psi0>' \
         '<psi1>1</psi1>' \
         '<psi2>1</psi2>' \
         '<Number>2</Number>' \
         '<Description>Live load</Description>' \
         '<Type>5</Type>' \
         '<psi0>1</psi0>' \
         '<psi1>0,9</psi1>' \
         '<psi2>0,8</psi2>' \
         '</LoadCases>' \
         '<Combinations>' \
         '<LoadCombinationNumber>1</LoadCombinationNumber>' \
         '<Description>Dead load</Description>' \
         '<CombTyp>0</CombTyp>' \
         '<Case>1</Case>' \
         '<Psi>1</Psi>' \
         '<Gamma>1,35</Gamma>' \
         '<Case>2</Case>' \
         '<Psi>1</Psi>' \
         '<Gamma>1,5</Gamma>' \
         '<LoadCombinationNumber>2</LoadCombinationNumber>' \
         '<Description>Live load</Description>' \
         '<CombTyp>0</CombTyp>' \
         '<Case>1</Case>' \
         '<Psi>1</Psi>' \
         '<Gamma>1,2</Gamma>' \
         '<Case>2</Case>' \
         '<Psi>1</Psi>' \
         '<Gamma>1,5</Gamma>' \
         '<LoadCombinationNumber>3</LoadCombinationNumber>' \
         '<Description>Dead load</Description>' \
         '<CombTyp>3</CombTyp>' \
         '<Case>1</Case>' \
         '<Psi>1</Psi>' \
         '<Gamma>1</Gamma>' \
         '<Case>2</Case>' \
         '<Psi>1</Psi>' \
         '<Gamma>1</Gamma>' \
         '<LoadCombinationNumber>4</LoadCombinationNumber>' \
         '<Description>Live load</Description>' \
         '<CombTyp>3</CombTyp>' \
         '<Case>1</Case>' \
         '<Psi>1</Psi>' \
         '<Gamma>1</Gamma>' \
         '<Case>2</Case>' \
         '<Psi>1</Psi>' \
         '<Gamma>1</Gamma>' \
         '<LoadCombinationNumber>5</LoadCombinationNumber>' \
         '<Description>SLS Permanent</Description>' \
         '<CombTyp>4</CombTyp>' \
         '<Case>1</Case>' \
         '<Psi>1</Psi>' \
         '<Gamma>1</Gamma>' \
         '<LoadCombinationNumber>6</LoadCombinationNumber>' \
         '<Description>SLS Quasi-permanent</Description>' \
         '<CombTyp>2</CombTyp>' \
         '<Case>1</Case>' \
         '<Psi>1</Psi>' \
         '<Gamma>1</Gamma>' \
         '<Case>2</Case>' \
         '<Psi>0,8</Psi>' \
         '<Gamma>1</Gamma>' \
         '</Combinations>' \
         '<RebarLongitudinal/>' \
         '<RebarStirrup/>' \
         '<Layers>' \
         '<Layer_number>1</Layer_number>' \
         '<Layer_description>Layer 1</Layer_description>' \
         '<Layer_number>2</Layer_number>' \
         '<Layer_description>Layer 2</Layer_description>' \
         '<Layer_number>3</Layer_number>' \
         '</Layers>' \
         '</Frame>'\


Guidelines = ''.join(str(SL) for SL in lst)

xml_str = prefix + Guidelines + suffix

print(xml_str)