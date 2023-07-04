import MolDisplay
import sqlite3
import os

# database class
class Database:
    # initialization constructor for database class
    def __init__(self, reset=False):
        if reset == True: # if reset is true
            if os.path.exists('molecules.db'): # if the molecules databse exists
                os.remove("molecules.db") # remove databse

        self.conn = sqlite3.connect("molecules.db") # make database connection

    def create_tables(self):
    # method to create tables
        # create Elements table
        self.conn.execute("""CREATE TABLE IF NOT EXISTS Elements
                                    ( ELEMENT_NO    INTEGER NOT NULL,
                                      ELEMENT_CODE  VARCHAR(3) PRIMARY KEY NOT NULL,
                                      ELEMENT_NAME  VARCHAR(32) NOT NULL,
                                      COLOUR1       CHAR(6) NOT NULL,
                                      COLOUR2       CHAR(6) NOT NULL,
                                      COLOUR3       CHAR(6) NOT NULL,
                                      RADIUS        DECIMAL(3) NOT NULL );""")
        
        # create Atoms table
        self.conn.execute("""CREATE TABLE IF NOT EXISTS Atoms
                                    ( ATOM_ID       INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                      ELEMENT_CODE  VARCHAR(3) NOT NULL REFERENCES Elements(ELEMENT_CODE),
                                      X             DECIMAL(7,4) NOT NULL,
                                      Y             DECIMAL(7,4) NOT NULL,
                                      Z             DECIMAL(7,4) NOT NULL );""")

        # create Bonds table
        self.conn.execute("""CREATE TABLE IF NOT EXISTS Bonds
                                    ( BOND_ID       INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                      A1            INTEGER NOT NULL,
                                      A2            INTEGER NOT NULL,
                                      EPAIRS        INTEGER NOT NULL );""")

        # create Molecules table
        self.conn.execute("""CREATE TABLE IF NOT EXISTS Molecules
                                    ( MOLECULE_ID   INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                      NAME          TEXT UNIQUE NOT NULL );""")

        # create MoleculeAtom table
        self.conn.execute("""CREATE TABLE IF NOT EXISTS MoleculeAtom
                                    ( MOLECULE_ID INTEGER NOT NULL,
                                      ATOM_ID INTEGER NOT NULL,
                                      PRIMARY KEY (MOLECULE_ID, ATOM_ID),
                                      FOREIGN KEY (MOLECULE_ID) REFERENCES Molecules,
                                      FOREIGN KEY (ATOM_ID) REFERENCES Atoms );""")

        # create MoleculeBond table
        self.conn.execute("""CREATE TABLE IF NOT EXISTS MoleculeBond
                                    ( MOLECULE_ID INTEGER NOT NULL,
                                      BOND_ID INTEGER NOT NULL,
                                      PRIMARY KEY (MOLECULE_ID, BOND_ID),
                                      FOREIGN KEY (MOLECULE_ID) REFERENCES Molecules,
                                      FOREIGN KEY (BOND_ID) REFERENCES Bonds );""")

    def __setitem__(self, table, values):
    # method to set tables based on tuple values
        if table == "Elements": # set Elements table
            self.conn.execute(f"""INSERT
                                  INTO   Elements
                                  VALUES ('{values[0]}', '{values[1]}', '{values[2]}', '{values[3]}', '{values[4]}','{values[5]}', '{values[6]}');""")

        if table == "Atoms": # set Atoms table
            self.conn.execute(f"""INSERT
                                  INTO   Atoms
                                  VALUES ('{values[0]}', '{values[1]}', '{values[2]}', '{values[3]}', '{values[4]}');""")

        if table == "Bonds": # set Bonds table
            self.conn.execute(f"""INSERT
                                  INTO   Bond
                                  VALUES ('{values[0]}', '{values[1]}', '{values[2]}', '{values[3]}');""")

        if table == "Molecules": # set Molecules table
            self.conn.execute(f"""INSERT
                                  INTO   Molecules
                                  VALUES ('{values[0]}', '{values[1]}');""")

        if table == "MoleculeAtom": # set MoleculeAtom table
            self.conn.execute(f"""INSERT
                                  INTO   MoleculeAtom
                                  VALUES ('{values[0]}', '{values[1]}');""")

        if table == "MoleculeBond": # set MoleculeBond table
            self.conn.execute(f"""INSERT
                                   INTO   MoleculeBond
                                   VALUES ('{values[0]}', '{values[1]}');""")

    def add_atom(self, molname, atom):
    # method to add atom attributes to atom table
        # insert atom attributes to table
        self.conn.execute(f"""INSERT
                              INTO   Atoms
                              VALUES (null, '{atom.atom.element}', '{atom.atom.x}', '{atom.atom.y}', '{atom.atom.z}');""")

        self.conn.commit()

        # set moleculeID to molecule ID where molecule name is molname
        moleculeID = self.conn.execute(f"""SELECT Molecules.MOLECULE_ID 
                                           FROM Molecules 
                                           WHERE Molecules.NAME = '{molname}'""")

        # set atomID to atom ID that is the max from Atoms table
        atomID = self.conn.execute("""SELECT * 
                                      FROM Atoms 
                                      WHERE ATOM_ID = (SELECT MAX(ATOM_ID) FROM Atoms)""")

        row = atomID # set row to atomID
        atomID = row.fetchone()[0] # fetch from row

        molIndex = moleculeID # set molIndex  to moleculeID
        moleculeID = molIndex.fetchone()[0] # fetch from molIndex
        
        # insert moleculeID and atomID into MoleculeAtom table
        self.conn.execute(f"""INSERT 
                              INTO MoleculeAtom 
                              VALUES ( '{moleculeID}', '{atomID}' )""")
        
        self.conn.commit()

    def remove_element(self, element):

        cursor = self.conn.cursor() # create cursor

        cursor.execute(f"""SELECT Elements.ELEMENT_NAME
                            FROM ELEMENTS
                            WHERE Elements.ELEMENT_NAME = '{element}'""")
        
        elementName = cursor.fetchall()

        if(elementName):
            self.conn.execute(f"""DELETE
                                FROM Elements
                                WHERE ELEMENT_NAME = '{element}'""")
            
            self.conn.commit()
            return 0

        else:
            return 1
        
    
    def get_molecule(self):
        cursor = self.conn.cursor()

        # Select Molecule IDs, Names, Bond Counts, and Atom Counts
        cursor.execute("""SELECT Molecules.MOLECULE_ID, Molecules.NAME, COUNT(DISTINCT Bonds.BOND_ID), COUNT(DISTINCT Atoms.ATOM_ID)
                    FROM Molecules
                    JOIN MoleculeBond ON Molecules.MOLECULE_ID = MoleculeBond.MOLECULE_ID
                    JOIN Bonds ON MoleculeBond.BOND_ID = Bonds.BOND_ID
                    JOIN MoleculeAtom ON Molecules.MOLECULE_ID = MoleculeAtom.MOLECULE_ID
                    JOIN Atoms ON MoleculeAtom.ATOM_ID = Atoms.ATOM_ID
                    GROUP BY Molecules.MOLECULE_ID""")

        result = cursor.fetchall()

        molecules = []

        # Loop Through Molecules
        for data in result:
            name = data[1]
            bond_count = data[2]
            atom_count = data[3]

            # Create Molecule Dictionary
            molecule = {
                "name": name,
                "bond_count": bond_count,
                "atom_count": atom_count
            }

            # Append Molecule to List
            molecules.append(molecule)

        return molecules
    
    def molecule_exists(self, name):
        cursor = self.conn.cursor()
        cursor.execute(f"""SELECT * FROM Molecules WHERE NAME = '{name}'""")
        row = cursor.fetchone()

        if row is None:
            return False
        else:
            return True
       

    def add_bond(self, molname, bond):
     # method to add bond attributes to bond table
        # insert bond attributes to table
        self.conn.execute(f"""INSERT
                              INTO   Bonds
                              VALUES (null, '{bond.bond.a1}', '{bond.bond.a2}', '{bond.bond.epairs}');""")

        self.conn.commit()

        # set moleculeID to molecule ID where molecule name is molname
        moleculeID = self.conn.execute(f"""SELECT Molecules.MOLECULE_ID 
                                           FROM Molecules 
                                           WHERE Molecules.NAME = '{molname}'""")

        # set bondID to bond ID that is the max from Bonds table
        bondID = self.conn.execute("""SELECT * 
                                      FROM Bonds 
                                      WHERE BOND_ID = (SELECT MAX(BOND_ID) FROM Bonds)""")

        row = bondID # set row to bondID
        bondID = row.fetchone()[0] # fetch from row

        molIndex = moleculeID # set molIndex to moleculeID
        moleculeID = molIndex.fetchone()[0] # fetch from molIndex

         # insert moleculeID and bondID into MoleculeBond table
        self.conn.execute(f"""INSERT 
                              INTO MoleculeBond 
                              VALUES ('{moleculeID}', '{bondID}')""")
        
        self.conn.commit()

    def add_molecule(self, name, fp):
     # method to add molecule to molecule table
        mol = MolDisplay.Molecule() # create molecule object
        mol.parse(fp)   # parse file

        # insert molecule with name into Molecules table
        self.conn.execute(f"""INSERT
                              INTO   Molecules
                              VALUES (null, '{name}');""")

        self.conn.commit()

        cursor = self.conn.cursor()
        # loop through atoms
        for i in range(mol.atom_no):
            atom = MolDisplay.Atom(mol.get_atom(i)) 
            self.add_atom(name, atom) # add atom to table
            if (self.find_element(atom.atom.element) == 1):
                # add default values into elements table
                self.conn.execute(f"""INSERT
                                      INTO   Elements
                                      VALUES ('{1}', '{atom.atom.element}', '{atom.atom.element}', 'FFFFFF', '050505', '020202', '{45}');""")
        # loop through bonds
        for i in range(mol.bond_no):
            bond = MolDisplay.Bond(mol.get_bond(i))
            self.add_bond(name, bond) # add bond to table
    
    def find_element(self, elemname):
        cursor = self.conn.cursor()

        cursor.execute(f"""SELECT Elements.ELEMENT_NAME
                          FROM ELEMENTS
                          WHERE Elements.ELEMENT_NAME = '{elemname}'""")

        element_name = cursor.fetchall()

        if(element_name):
            return 0
        else:
            return 1


    def load_mol(self, name):
    # method to load molecule data into molecule object
        mol = MolDisplay.Molecule()

        cursor = self.conn.cursor() # create cursor

        # select all columns from Atoms, MoleculeAtom, and Molecules where atomID, molecule name, and moleculeID match the conditions
        cursor.execute(f"""SELECT *
                           FROM Atoms, MoleculeAtom, Molecules
                           WHERE Atoms.ATOM_ID = MoleculeAtom.ATOM_ID AND Molecules.NAME = '{name}' AND
                           Molecules.MOLECULE_ID = MoleculeAtom.MOLECULE_ID
                           ORDER BY ATOM_ID ASC
                        """)

        atoms = cursor.fetchall() # set data to atoms array

        # loop through each atom in atoms
        for atom in atoms:
            # append atom to molecule
            mol.append_atom(atom[1], atom[2], atom[3], atom[4])
        
        # select all columns from Bonds, MoleculeBond, and Molecules where bondID, molecule name, and moleculeID match the conditions
        cursor.execute(f"""SELECT *
                           FROM Bonds, MoleculeBond, Molecules
                           WHERE Bonds.BOND_ID = MoleculeBond.BOND_ID AND Molecules.NAME = '{name}' AND
                           Molecules.MOLECULE_ID = MoleculeBond.MOLECULE_ID
                           ORDER BY BOND_ID ASC
                        """)
        
        bonds = cursor.fetchall() # set data to bonds array

        # loop through each bond in bonds
        for bond in bonds:
            # append bond to molecule
            mol.append_bond(bond[1], bond[2], bond[3])

        return mol # return molecule›

    def radius(self):
    # method to return a dictionary with ELEMENT_CODE values mapped to RADIUS
        cursor = self.conn.cursor() # create cursor

        # select ELEMENT_CODE and RADIUS from Elements table
        cursor.execute("""SELECT ELEMENT_CODE, RADIUS
                          FROM Elements""")
        
        data = cursor.fetchall() # get data

        dictionary = dict(data) # create dictionary based on data

        return dictionary # return dictionary
    
    def element_name(self):
    # method to return a dictionary with ELEMENT_CODE values mapped to ELEMENT_NAME
        cursor = self.conn.cursor()

        # select ELEMENT_CODE and ELEMENT_NAME from Elements table
        cursor.execute("""SELECT ELEMENT_CODE, ELEMENT_NAME
                          FROM Elements""")
        
        data = cursor.fetchall() # get data

        dictionary = dict(data) # create dictionary based on data

        return dictionary # return dictionary
    
    def radial_gradients(self):
    # method to return string comprised of gradients of colours and element names found in Elements table
        string = ""

        cursor = self.conn.cursor() # set cursor

        # select data from elements
        cursor.execute("""SELECT ELEMENT_NAME, COLOUR1, COLOUR2, COLOUR3 
                          FROM Elements""")

        elements = cursor.fetchall() # set elements to data

        for element in elements: # loop through data
            # concatenate for each iteration
            string = string + """ 
<radialGradient id="%s" cx="-50%%" cy="-50%%" r="220%%" fx="20%%" fy="20%%">
  <stop offset="0%%" stop-color="#%s"/>
  <stop offset="50%%" stop-color="#%s"/>
  <stop offset="100%%" stop-color="#%s"/>
</radialGradient>""" % (element[0], element[1], element[2], element[3]) # add data
                    
        return string # return string

# if __name__ == "__main__":
#         db = Database(reset=True);
#         db.create_tables();
#         db['Elements'] = ( 1, 'H', 'Hydrogen', 'FFFFFF', '050505', '020202', 25 );
#         db['Elements'] = ( 6, 'C', 'Carbon', '808080', '010101', '000000', 40 );
#         db['Elements'] = ( 7, 'N', 'Nitrogen', '0000FF', '000005', '000002', 40 );
#         db['Elements'] = ( 8, 'O', 'Oxygen', 'FF0000', '050000', '020000', 40 );
#         fp = open( 'benzene.sdf' );
#         db.add_molecule( 'Benzene', fp );
#         fp = open( 'cocaine.sdf' );
#         db.add_molecule( 'Cocaine', fp );
#         fp = open( 'mdma.sdf' );
#         db.add_molecule( 'MDMA', fp );
#         # display tables
#         print( db.conn.execute( "SELECT * FROM Elements;" ).fetchall() );
#         print( db.conn.execute( "SELECT * FROM Molecules;" ).fetchall() );
#         print( db.conn.execute( "SELECT * FROM Atoms;" ).fetchall() );
#         print( db.conn.execute( "SELECT * FROM Bonds;" ).fetchall() );
#         print( db.conn.execute( "SELECT * FROM MoleculeAtom;" ).fetchall() );
#         print( db.conn.execute( "SELECT * FROM MoleculeBond;" ).fetchall() );

# if __name__ == "__main__":
#         db = Database(reset=False); # or use default

#         MolDisplay.radius = db.radius();
#         MolDisplay.element_name = db.element_name();
#         MolDisplay.header += db.radial_gradients();

#         for molecule in [ 'Benzene', 'Cocaine', 'MDMA' ]:
#             mol = db.load_mol( molecule );
#             mol.sort();
#             fp = open( molecule + ".svg", "w" );
#             fp.write( mol.svg() );
#             fp.close();