#include "mol.h"

#include <stdio.h>

/*
Method: Copies values of element, x, y, and z into an atom
Params: atom to set, atom element, and atom's xyz positions
Return: None
*/
void atomset(atom *atom, char element[3], double *x, double *y, double *z)
{
    strcpy(atom->element, element); // strcpy element to atom element

    atom->x = *x; // set xyz positions of atom
    atom->y = *y;
    atom->z = *z;
}

/*
Method: Copies values from an atom and sets them to an element name, and xyz positions
Params: atom to get, element, and xyz positions
Return: None
*/
void atomget(atom *atom, char element[3], double *x, double *y, double *z)
{
    strcpy(element, atom->element); // copy atom element into element

    *x = atom->x; // set xyz positions to atom xyz positions
    *y = atom->y;
    *z = atom->z;
}

/*
Method: Copies values from two atoms and epairs, and sets them to a bond
Params: bond to set, atom a1, atom a2, and epairs
Return: None
*/
void bondset(bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs)
{
    bond->a1 = *a1; // set bond atoms indices to a1 and a2
    bond->a2 = *a2;
    bond->atoms = *atoms; // set bond atoms to atoms array
    bond->epairs = *epairs; // set bond epairs to epairs

    compute_coords(bond);
}

/*
Method: Copies values from a bond and sets them to atoms a1, a2, atoms, and epairs
Params: bond to get, atom a1, atom a2, epairs
Return: None
*/
void bondget(bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs)
{
    *a1 = bond->a1; // get atoms indices 
    *a2 = bond->a2;
    *atoms = bond->atoms; // get atoms 
    *epairs = bond->epairs; // get epairs from bond epairs
}

/*
Method: Computes x1,x2,y1,y2,x,len,dy and dx values for a bond
Params: bond
Return: None
*/
void compute_coords(bond *bond)
{
    bond->x1 = bond->atoms[bond->a1].x; // set x1 and x2 values
    bond->x2 = bond->atoms[bond->a2].x;
    bond->y1 = bond->atoms[bond->a1].y; // set y1 and y2 values
    bond->y2 = bond->atoms[bond->a2].y; 
    bond->z = (bond->atoms[bond->a1].z + bond->atoms[bond->a2].z) / 2; // set z value to average z value of two atoms
    bond->len = sqrt((bond->atoms[bond->a2].x - bond->atoms[bond->a1].x) * ((bond->atoms[bond->a2].x - bond->atoms[bond->a1].x)) + // set len to distance between two points
                    ((bond->atoms[bond->a2].y - bond->atoms[bond->a1].y)) * ((bond->atoms[bond->a2].y - bond->atoms[bond->a1].y)));
    bond->dy = (bond->atoms[bond->a2].y - bond->atoms[bond->a1].y) / bond->len; // set dy and dx to difference in y or x divided by len
    bond->dx = (bond->atoms[bond->a2].x - bond->atoms[bond->a1].x) / bond->len;
}

/*
Method: Mallocs a molecule and sets various fields in a molecule
Params: atom max, bond max
Return: tempMol
*/
molecule *molmalloc(unsigned short atom_max, unsigned short bond_max)
{
    molecule *tempMol = (molecule *)malloc(sizeof(molecule)); // malloc tempMol
    if (tempMol == NULL)
    {
        return NULL;
    }

    tempMol->atom_no = 0;                             // set tempMol atom number to 0
    tempMol->atom_max = atom_max;                     // set tempMol atom max to atom_max
    tempMol->atoms = malloc(sizeof(atom) * atom_max); // malloc atoms array
    if (tempMol->atoms == NULL)
    {
        return NULL;
    }

    tempMol->atom_ptrs = malloc(sizeof(atom) * atom_max); // malloc atom_ptrs array
    if (tempMol->atom_ptrs == NULL)
    {
        return NULL;
    }

    tempMol->bond_no = 0;                             // set tempMol bond number to 0
    tempMol->bond_max = bond_max;                     // set tempMol bond max to bond_max
    tempMol->bonds = malloc(sizeof(atom) * bond_max); // malloc bonds array
    if (tempMol->bonds == NULL)
    {
        return NULL;
    }

    tempMol->bond_ptrs = malloc(sizeof(atom) * bond_max); // maloc bond_ptrs
    if (tempMol->bond_ptrs == NULL)
    {
        return NULL;
    }

    return tempMol; // return malloced tempMol
}

/*
Method: Copies a molecule into another malloced molecule
Params: molecule src
Return: tempMol
*/
molecule *molcopy(molecule *src)
{
    molecule *tempMol = molmalloc(src->atom_max, src->bond_max); // molmalloc tempMol by src atom max and bond max
    if (tempMol == NULL)
    {
        return NULL;
    }

    for (int i = 0; i < src->atom_no; i++) // loop through src atom number
    {
        // atomset tempMol's atom array at [i] to src atoms at [i]
        atomset(&tempMol->atoms[i], src->atoms[i].element, &src->atoms[i].x, &src->atoms[i].y, &src->atoms[i].z);
        molappend_atom(tempMol, &src->atoms[i]); // molappend src atoms at [i] to tempMol
    }

    for (int i = 0; i < src->bond_no; i++) // loop through src bond number
    {
        // bondset tempMol's bond array at [i] to src bonds at [i]
        bondset(&tempMol->bonds[i], &src->bonds[i].a1, &src->bonds[i].a2, &src->bonds[i].atoms, &src->bonds[i].epairs);
        molappend_bond(tempMol, &src->bonds[i]); // molappend src bonds at [i] to tempMol
    }

    tempMol->atom_no = src->atom_no; // set tempMol atom_no and bond_no to src atom number & bond number
    tempMol->bond_no = src->bond_no;

    return tempMol; // return tempMol
}

/*
Method: Frees contents of a molecule
Params: molecule ptr
Return: None
*/
void molfree(molecule *ptr)
{
    free(ptr->atoms); // free molecule contents first
    free(ptr->bonds);
    free(ptr->atom_ptrs);
    free(ptr->bond_ptrs);
    free(ptr); // free molecule
}

/*
Method: Appends an atom to a molecule
Params: molecule, atom
Return: None
*/
void molappend_atom(molecule *molecule, atom *atom)
{
    if (molecule->atom_no == molecule->atom_max) // if molecule atom number is equal to atom max
    {
        if (molecule->atom_max == 0) // if atom max is 0
        {
            molecule->atom_max++; // increment atom max
        }
        else
        {
            molecule->atom_max = molecule->atom_max * 2; // in any other case, double atom max
        }

        molecule->atoms = realloc(molecule->atoms, sizeof(struct atom) * molecule->atom_max);           // reallocate atoms array for new atom max
        molecule->atom_ptrs = realloc(molecule->atom_ptrs, sizeof(struct atom *) * molecule->atom_max); // reallocate atom_ptrs for new atom max

        if (molecule->atoms == NULL)
        {
            printf("Error!\n");
            exit(0);
        }

        if (molecule->atom_ptrs == NULL)
        {
            printf("Error!\n");
            exit(0);
        }

        for (int i = 0; i < molecule->atom_max; i++) // loop until atom max
        {
            molecule->atom_ptrs[i] = &(molecule->atoms[i]); // reset atom_ptrs to address of atoms in atoms array
        }
    }

    molecule->atoms[molecule->atom_no] = *atom;                                     // set first empty element of atoms array to atom to append
    molecule->atom_ptrs[molecule->atom_no] = &(molecule->atoms[molecule->atom_no]); // set first empty atom_ptr to address of appended atom
    molecule->atom_no++;                                                            // increment atom number
}

/*
Method: Appends a bond to a molecule
Params: molecule, bond
Return: None
*/
void molappend_bond(molecule *molecule, bond *bond)
{
    if (molecule->bond_no == molecule->bond_max) // if molecule bond number is equal to bond max
    {
        if (molecule->bond_max == 0) // if bond max is 0
        {
            molecule->bond_max++; // increment bond max
        }
        else
        {
            molecule->bond_max = molecule->bond_max * 2; // in any other case, double bond max
        }

        molecule->bonds = realloc(molecule->bonds, sizeof(struct bond) * molecule->bond_max);           // reallocate bonds array for new bond max
        molecule->bond_ptrs = realloc(molecule->bond_ptrs, sizeof(struct bond *) * molecule->bond_max); // reallocate bond_ptrs for new bond max

        if (molecule->bonds == NULL) // if either realloc fails
        {
            printf("Error!\n");
            exit(0); // exit program
        }

        if (molecule->bond_ptrs == NULL)
        {
            printf("Error!\n");
            exit(0);
        }

        for (int i = 0; i < molecule->bond_max; i++) // loop until bond max
        {
            molecule->bond_ptrs[i] = &(molecule->bonds[i]); // reset bond_ptrs to address of bonds in bonds array
        }
    }

    molecule->bonds[molecule->bond_no] = *bond;                                     // set first empty element of bonds array to bond to append
    molecule->bond_ptrs[molecule->bond_no] = &(molecule->bonds[molecule->bond_no]); // set first empty bond_ptr to address of appended bond
    molecule->bond_no++;                                                            // increment bond number
}

/*
Method: Comparative helper function for qsort, compares atoms z values
Params: void *a, void *b
Return: 1 if left compared atom is greater, -1 if right compared atom is greater, 0 any other case
*/
int comparatorAtom(const void *a, const void *b)
{
    struct atom *const *atom1 = a; // set atom1 to a, atom2 to b
    struct atom *const *atom2 = b;

    if ((*atom1)->z > (*atom2)->z)
    {             // if atom1 is greater
        return 1; // return 1
    }
    else if ((*atom1)->z < (*atom2)->z)
    {              // if atom2 is greater
        return -1; // return -1
    }
    else
    {
        return 0; // else, return 0
    }
}

/*
Method: Comparative helper function for qsort, compares bonds z value
Params: void *a, void *b
Return: 1 if left compared bond average is greater, -1 if right compared bond average is greater, 0 any other case
*/
int bond_comp(const void *a, const void *b)
{
    struct bond *const *bond1 = a; // set bond1 to a, bond2 to b
    struct bond *const *bond2 = b;

    if (((*bond1)->z) > ((*bond2)->z))
    {             // if bond1 z is higher
        return 1; // return 1
    }
    else if (((*bond1)->z) < ((*bond2)->z))
    {              // if bond2 z is higher
        return -1; // return -1
    }
    else
    {
        return 0; // else, return 0
    }
}

/*
Method: Sorts atom pointers and bond pointers by ascending z values
Params: molecule
Return: None
*/
void molsort(molecule *molecule)
{
    qsort(molecule->atom_ptrs, molecule->atom_no, sizeof(struct atom *), comparatorAtom); // call qsort functions to sort atomptrs and bondptrs
    qsort(molecule->bond_ptrs, molecule->bond_no, sizeof(struct bond *), bond_comp);
}

/*
Method: Rotates a matrix on its X axis using various values for each index
Params: matrix to pass in, degree to use
Return: None
*/
void xrotation(xform_matrix xform_matrix, unsigned short deg)
{

    double rad = deg * M_PI / 180; 

	xform_matrix[0][0] = 1.00;
	xform_matrix[0][1] = 0.00;
	xform_matrix[0][2] = 0.00;
	xform_matrix[1][0] = 0.00;
	xform_matrix[1][1] = cos(rad);
	xform_matrix[1][2] = sin(rad) * -1.00;
	xform_matrix[2][0] = 0.00;
	xform_matrix[2][1] = sin(rad);
	xform_matrix[2][2] = cos(rad);
}

/*
Method: Rotates a matrix on its Y axis using various values for each index
Params: matrix to pass in, degree to use
Return: None
*/
void yrotation(xform_matrix xform_matrix, unsigned short deg)
{

    double rad = deg * M_PI / 180; 

	xform_matrix[0][0] = cos(rad);
	xform_matrix[0][1] = 0.00;
	xform_matrix[0][2] = sin(rad);
	xform_matrix[1][0] = 0.00;
	xform_matrix[1][1] = 1.00;
	xform_matrix[1][2] = 0.00;
	xform_matrix[2][0] = sin(rad) * -1.00;
	xform_matrix[2][1] = 0.00;
	xform_matrix[2][2] = cos(rad);
}

/*
Method: Rotates a matrix on its Z axis using various values for each index
Params: matrix to pass in, degree to use
Return: None
*/
void zrotation(xform_matrix xform_matrix, unsigned short deg)
{

    double rad = deg * M_PI / 180; 
    // create matrix
	xform_matrix[0][0] = cos(rad);
	xform_matrix[0][1] = sin(rad) * -1.00;
	xform_matrix[0][2] = 0.00;
	xform_matrix[1][0] = sin(rad);
	xform_matrix[1][1] = cos(rad);
	xform_matrix[1][2] = 0.00;
	xform_matrix[2][0] = 0.00;
	xform_matrix[2][1] = 0.00;
	xform_matrix[2][2] = 1.00;
}

/*
Method: Performs matrix multiplication on the xform matrix with each atoms x,y, and z values
Params: molecule, matrix to pass in
Return: None
*/
void mol_xform(molecule *molecule, xform_matrix matrix)
{
   for (int i = 0; i < molecule->atom_no; i++) {
		double x = molecule->atoms[i].x; 
		double y = molecule->atoms[i].y; 
		double z = molecule->atoms[i].z; 
        
		for (int j = 0; j < 3; j++) {
			switch (j) {
			case 0:
				molecule->atoms[i].x = matrix[0][0] * x + matrix[0][1] * y + matrix[0][2] * z; //Calculate new x value
				break;
			case 1:
				molecule->atoms[i].y = matrix[1][0] * x + matrix[1][1] * y + matrix[1][2] * z; //Calculate new y value
				break;
			case 2:
				molecule->atoms[i].z = matrix[2][0] * x + matrix[2][1] * y + matrix[2][2] * z; //Calculate new z value
				break;
			}
		}
	}

	for (int i = 0; i < molecule->bond_no; i++) {
		compute_coords(&molecule->bonds[i]);
	}
    
}



