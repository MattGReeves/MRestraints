import ccdc.search
import os
from mercury_interface import MercuryInterface
from subprocess import Popen
import re

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
        atom2label = atom2.label
        if atom2.atomic_symbol == "H":
            break
        m1 = re.search("\d", atom2label)
        n1 = m1.start()
        newatom2label = atom2label[:n1] + "(" + atom2label[n1:] + ")"
        atomtwos = []
        for atomtwo in atomone.neighbours:
            atomtwos.append(atomtwo)
            atom1 = atomtwo
            atom1label = atom1.label
            if atom1.atomic_symbol == "H":
                break
            m2 = re.search("\d", atom1label)
            n2 = m2.start()
            newatom1label = atom1label[:n2] + "(" + atom1label[n2:] + ")"
            Distance = (ccdc.descriptors.MolecularDescriptors.atom_distance(atom1, atom2))
            if Distance not in Distances and Distance != 0:
                Distances.append(Distance)
                Output.append("DIST   " + str(round((Distance),3)) + ", 0.01   =   " +newatom1label +'   To   '+ newatom2label+'\n')
            else:
                continue
            for atomthree in atomtwos:
                atom3 = atomthree
                atom3label = atom3.label
                if atom3.atomic_symbol == "H":
                    break
                m3 = re.search("\d", atom3label)
                n3 = m3.start()
                newatom3label = atom3label[:n3] + "(" + atom3label[n3:] + ")"
                Distance2 = (ccdc.descriptors.MolecularDescriptors.atom_distance(atom1, atom3))
                if Distance2 not in Distances and Distance2 != 0:
                    Distances.append(Distance2)
                    Output.append("DIST   " + str(round((Distance2),3)) + ", 0.03   =   " +newatom1label +'   To   '+ newatom3label+'\n')
                else:
                    continue

with open ((dir_path) +'\Output Folder' + '\ ' + (id)+' Crystals_No_H.txt','w') as g:
    for item in Output:
        g.write(item)

p = Popen((dir_path) +'\Output Folder' + '\ ' + (id)+' Crystals_No_H.txt', shell=True)
