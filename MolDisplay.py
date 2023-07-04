import molecule

header = """<svg version="1.1" width="1000" height="1000"
xmlns="http://www.w3.org/2000/svg">"""
footer = """</svg>"""

offsetx = 500
offsety = 500

# Atom class

class Atom:
    # intialization function for atom
    def __init__(self, c_atom):
        self.atom = c_atom  # set self atom to atom parameter, and z value to atom z value
        self.z = c_atom.z

    # string return function for atom
    def __str__(self):
        # return string with atom info
        return f"Element: {self.atom.element}, x: {self.atom.x}, y: {self.atom.y}, z: {self.atom.z}"

    # svg funtion for atom
    def svg(self):
        # calculate cx, cy, radius, and fill values
        cx = (self.atom.x * 100.0) + offsetx
        cy = (self.atom.y * 100.0) + offsety
        r = radius[self.atom.element]
        fill = element_name[self.atom.element]
        # return atom circle info
        return '  <circle cx="%.2f" cy="%.2f" r="%d" fill="url(#%s)"/>\n' % (cx, cy, r, fill)

# Bond class


class Bond:
    # initialization funtion for bond
    def __init__(self, c_bond):
        self.bond = c_bond  # set self bond to bond parameter, and z value to bond z value
        self.z = c_bond.z

    # string return function for atom
    def __str__(self):
        return f"Atom 1: {self.bond.a1}, Atom 2: {self.atom.a2}, x1: {self.bond.x1}, y1: {self.atom.y1},\
        x2: {self.bond.x2}, y2: {self.atom.y2}, length: {self.bond.len}, dx: {self.bond.dx}, dy: {self.bond.dy}"  # return bond info

    # svg function for bond
    def svg(self):
        # calculate atoms x and y coordinates
        a1X = (self.bond.x1 * 100) + offsetx
        a1Y = (self.bond.y1 * 100) + offsety
        a2X = (self.bond.x2 * 100) + offsetx
        a2Y = (self.bond.y2 * 100) + offsety

        #if (self.bond.dy != 0):  # if dy is not 0, calculate positive and negative x values
        x1Pos = a1X + self.bond.dy * 10
        x1Neg = a1X - self.bond.dy * 10
        x2Pos = a2X + self.bond.dy * 10
        x2Neg = a2X - self.bond.dy * 10

       # if (self.bond.dx != 0):  # if dx is not 0, calculate positive and negative y values
        y1Pos = a1Y + self.bond.dx * 10
        y1Neg = a1Y - self.bond.dx * 10
        y2Pos = a2Y + self.bond.dx * 10
        y2Neg = a2Y - self.bond.dx * 10

        return '  <polygon points="%.2f,%.2f %.2f,%.2f %.2f,%.2f %.2f,%.2f" fill="green"/>\n' % (
            x1Neg, y1Pos, x1Pos, y1Neg, x2Pos, y2Neg, x2Neg, y2Pos)  # return positive and neg values

# Molecule class


class Molecule(molecule.molecule):
    # string return function for molecule
    def __str__(self):
        for i in range(self.atom_no):  # loop through atoms
            atom = self.get_atom(i)
            print(atom.element, atom.x, atom.y, atom.z)  # print atom info
        for i in range(self.bond_no):  # loop through bonds
            bond = self.get_bond(i)
            print(bond.a1, bond.a2, bond.epairs, bond.x1, bond.y1, bond.x2, bond.y2,  # print bond info
                  bond.len, bond.dx, bond.dy)

    # svg function for molecule
    def svg(self):
        string = header  # start string with header
        atomCount = 0
        boundCount = 0

        # loop while atom count and bond count are less than their respective counts
        while atomCount != self.atom_no and boundCount != self.bond_no:
            atom = self.get_atom(atomCount)
            a1 = Atom(atom)  # create Atom a1
            bond = self.get_bond(boundCount)
            b1 = Bond(bond)  # create Bond b1

            if atom.z < bond.z:  # if atom z value is less than bond z value
                string += a1.svg()  # append a1 svg
                atomCount += 1  # add to atom count

            else:
                string += b1.svg()  # else, append bond svg
                boundCount += 1  # add to bond count

        if atomCount == self.atom_no:  # if atom count is equal to atom number after loop
            # loop through remaining bonds that have not been appended
            for i in range(boundCount, self.bond_no):
                newBond = self.get_bond(i)
                newB1 = Bond(newBond)  # create new Bond
                string += newB1.svg()  # append new bond svg
        else:  # else, there are atoms remaining to append
            for i in range(atomCount, self.atom_no):  # loop through remaining atoms
                newAtom = self.get_atom(i)
                newA1 = Atom(newAtom)  # create new Atom
                string += newA1.svg()  # append new atom svg

        string += footer  # add footer

        return string  # return string

    # Method to parse a file and create a molecule
    def parse(self, fileObj):
        # get file contents
        text = fileObj.read()
        lineCount = 0
        # loop through lines in file
        for line in text.split("\n"):
            # add 1 to file count
            lineCount += 1
            # if string is at the bond and atom count line
            if(lineCount == 4):
                # split line by whitespace
                result = line.split()
                # save num of atom and bond
                atomCount = int(result[0])
                bondCount = int(result[1])
            # if string is at the atom info
            elif(lineCount > 4 and atomCount != 0):
                # split line by whitespace
                result = line.split()
                # append atom to molecule
                self.append_atom(result[3], float(result[0]), float(result[1]), float(result[2]))
                atomCount = atomCount -  1
            # if string is at the bond info
            elif(lineCount > 4 and atomCount == 0 and bondCount != 0):
                # split line by whitespace
                result = line.split()
                # append bond to molecule
                self.append_bond((int(result[0])) - 1, (int(result[1])) - 1, int(result[2]))
                bondCount = bondCount - 1
                