import ccdc.search
import os
from mercury_interface import MercuryInterface
from subprocess import Popen

helper = MercuryInterface()
html_file = helper.output_html_file
dir_path = os.path.dirname(os.path.realpath(__file__))

entry = helper.current_entry
id = helper.identifier
crystal = entry.crystal
molecule = crystal.molecule

f = open(html_file, "w")
f.write('Atomic Distances for Structure: ' + (id))
f.write('<br>')
f.write('A .txt file including all atomic distances for this structure has been produced in ' + (dir_path) + ' \Output Folder')
f.write('<br>')
Output = []
Distances = []

for atomone in molecule.atoms:
        atom2 = atomone
        if atom2.atomic_symbol == "H":
            break
        atomtwos = []
        for atomtwo in atomone.neighbours:
            atomtwos.append(atomtwo)
            atom1 = atomtwo
            if atom1.atomic_symbol == "H":
                break
            Distance = (ccdc.descriptors.MolecularDescriptors.atom_distance(atom1, atom2))
            if Distance not in Distances and Distance != 0:
                Distances.append(Distance)
                Output.append("DFIX   " + str(round((Distance),3)) + "   0.01   " +atom1.label +'   '+ atom2.label+'\n')
            else:
                continue
            for atomthree in atomtwos:
                atom3 = atomthree
                if atom3.atomic_symbol == "H":
                    break
                Distance2 = (ccdc.descriptors.MolecularDescriptors.atom_distance(atom1, atom3))
                if Distance2 not in Distances and Distance2 != 0:
                    Distances.append(Distance2)
                    Output.append("DFIX   " + str(round((Distance2),3)) + "   0.03   " +atom1.label +'   '+ atom3.label+'\n' )
                else:
                    continue

with open ((dir_path) +'\Output Folder' + '\ ' + (id)+' SHELX_No_H.txt','w') as g:
    for item in Output:
        g.write(item)

p = Popen((dir_path) +'\Output Folder' + '\ ' + (id)+' SHELX_No_H.txt', shell=True)
