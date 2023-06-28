import numpy as np 
import cosmology as cosmo 
import healpy as hp 
import liblightcone as llc
import backend as bk
import os
import sys
import argparse

# for full res websky 1LPT at nside=1024:
#   export LPT_DISPLACEMENTS_PATH=/pscratch/sd/m/malvarez/websky-displacements/
#   srun -n $nproc --gpus-per-task=1 python lightcone.py --grid-nside 6144 --map-nside 1024

# ------ commandline parameters
parser = argparse.ArgumentParser(description='Commandline interface to lptmap')
parser.add_argument('--grid-nside', type=int, help=' input displacement grid [default = 768]', default=768)
parser.add_argument('--map-nside',  type=int, help='output map healpix Nside [default = 512]', default=512)
args = parser.parse_args()

grid_nside            = args.grid_nside # cube shape is parameterized by grid_nside; full resolution for websky is 6144
map_nside             = args.map_nside

# ------ hardcoded parameters
L_box                 = 7700. # periodic box size in comoving Mpc; lattice spacing is L_box / grid_nside
comov_lastscatter_Gpc = 13.8  # conformal distance to last scattering surface in Gpc
zmin                  = 0.05  # minimum redshift for projection (=0.05 for websky products)
zmax                  = 4.5   # maximum redshift for projection (=4.50 for websky products)

force_no_mpi          = False 
force_no_gpu          = False

kappa_map_filebase = f'./output/kappa_map_grid-{ grid_nside }_nside-{ map_nside }'

print(f"LIGHTCONE: Setting backend...")
backend = bk.backend(force_no_mpi=force_no_mpi, force_no_gpu=force_no_gpu)
print(f"LIGHTCONE: Backend configuration complete.")

# Paths to displacement fields
try:
    path2disp = os.environ['LPT_DISPLACEMENTS_PATH']
except:
    path2disp = '/Users/shamik/Documents/Work/websky_datacube/'

print(f"LIGHTCONE: Path to displacement files set to {path2disp}")

if grid_nside == 768:
    sxfile = path2disp+'sx1_7700Mpc_n6144_nb30_nt16_no768'
    syfile = path2disp+'sy1_7700Mpc_n6144_nb30_nt16_no768'
    szfile = path2disp+'sz1_7700Mpc_n6144_nb30_nt16_no768'
else:
    sxfile = path2disp+'sx1_7700Mpc_n6144_nb30_nt16_v2'
    syfile = path2disp+'sy1_7700Mpc_n6144_nb30_nt16_v2'
    szfile = path2disp+'sz1_7700Mpc_n6144_nb30_nt16_v2'

print(f"LIGHTCONE: Computing cosmology...")
cosmo_wsp = cosmo.cosmology(Omega_m=0.31, h=0.68) # for background expansion consistent with websky
print(f"LIGHTCONE: Cosmology computed")

print(f"LIGHTCONE: Setting up lightcone workspace...")
lpt_wsp = llc.lightcone_workspace(cosmo_wsp, grid_nside, map_nside, L_box, zmin, zmax)

print(f"LIGHTCONE: Computing LPT to kappa map...")
kappa_map = lpt_wsp.lpt2map([sxfile, syfile, szfile], backend, bytes_per_cell=4)
print(f"LIGHTCONE: Kappa map computed. Saving to file.")


backend.mpi_backend.writemap2file(kappa_map, kappa_map_filebase+".fits")
print(f"LIGHTCONE: Kappa map saved. Exiting...")




