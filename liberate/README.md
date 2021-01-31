
# Liberate Library Characterization

## Summary

Liberate takes in tcl scripts and netlist files and generates ldb libraries containing the performance of the netlists

##  How to Use
1. Run Characterization and generate Liberty files
2. Review output files

##  Steps
1. Run Characterization
     1. Run characterization using Liberate.  cmd:
         liberate tcl/char.tcl |& tee char.log
     2. Check log file char.log for "ERROR" messages.
        Look for "Characterization statistics." Check the number of cells passed match the size of the run
        set. See notes for the number of cells to be run.
        Check the number of cells failed is zero.
        Look for "Finished writing." Again check that no cells failed during the lib writing process.
     3. Note the ldb/ directory (characterization database) has been created
        In the ldb/ directory, individual cell ldb files are present. Also, there will be client_<#>.log files.
        Check each log file for "ERROR" messages.
     4. Check liberty file lib/example_nldm.lib
2. Note that tcl/char.tcl has been setup to enable command line input.  User can use the command line input feature to set PVT.
     1. Run characterization for PVT PROCESS=ff VDD=1.1 TEMP=0  cmd:
          liberate tcl/char.tcl PROCESS=ff VDD=1.1 TEMP=0 |& tee char.log
        The following ldb and lib files were created:
          ldb/tst_ff_1.1_0.ldb.gz, lib/tst_ff_1.1_0_nldm.lib
        User can use this command line input feature to enable programability to the run script.
     2. See Makefile for example of commands for the rest of the PVT corners.

##  Notes
1. RAK is setup to allow user to run 9 cells (all different cell types).
   In the interest of fast turn around time, only AND2X1 and INVX1 is setup to be characterize initially.
   User can update setup to run all the cells by modifying file cells.tcl:
       comment out last line "set cells { AND2X1 INVX1 }", and run characterization
2. File tcl/char.tcl is setup with some user programmability in mind.
   1. Change library name by setting variable LIBNAME
   2. Change Process,Voltage,Temp (PVT)
   3. By default, liberate is setup to only characterize formats NLDM, NLPM, ECSM. 
      To generate data for other formats, such as ECSMN, CCS, CCSN, CCSP, 
      user will need to add options such as -ecsmn, -ccs, -ccsn, -ccsp 
      to commands "char_library" (for characterization),
      and write_library (for writing data to Liberty file)
   4. User can run characterization using Distributed Resource Management (DRM) tool like LSF
      Edit tcl/char.tcl and change the following:
          CLIENTS=<# of jobs to submit to LSF>
          THREAD=<# of cpu's per job to submit to LSF>
          RSH_CMD=<LSF command>

