#########################################
#   Help
#########################################
help :
	@ echo '--------------------------------------------------'
	@ echo '  Characterization'
	@ echo '      make char_tt - run characterization on typical corner (using default settings)'
	@ echo '      make char_all - run characterization on all non-typical corner using command line variable setting'
	@ echo '--------------------------------------------------'

char_tt :
	liberate tcl/char.tcl 2>&1 | tee char.log
char_all :
	liberate tcl/char.tcl PROCESS=ss VDD=0.9 TEMP=85 2>&1 | tee char_ss_0.9_85.log
	liberate tcl/char.tcl PROCESS=ss VDD=0.9 TEMP=0  2>&1 | tee char_ss_0.9_0.log
	liberate tcl/char.tcl PROCESS=ff VDD=1.1 TEMP=85 2>&1 | tee char_ff_1.1_85.log
	liberate tcl/char.tcl PROCESS=ff VDD=1.1 TEMP=0  2>&1 | tee char_ff_1.1_0.log

.PHONY : reset
reset :
	rm -rf .*[~%] *[~%]
	rm -rf ldb lib *.log

